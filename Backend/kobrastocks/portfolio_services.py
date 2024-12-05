"""
------------------Prologue--------------------
File Name: portfolio_services.py
Path: Backend/kobrastocks/portfolio_services.py

Description:
Implements core services for data retrievel and portfolio analysis


Input:
Portfolio Object

Output:
Serialized stock data, predictions, charts, and contact form confirmation.

Collaborators: Charlie Gillund, Chatgpt(For Debugging and ChatGPT api assistance )
Date 11/18/24
---------------------------------------------
"""
import pytz
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime
import logging

from .models import Portfolio
from . import db
from .models import PortfolioStock
from .services import get_current_stock_price, get_predictions, get_stock_data, get_stock_price_at_date
from .utils import (
    mean_variance_optimization,
    calculate_sharpe_ratio,
    calculate_diversification_ratio,
    generate_chat_prompts,
    get_chat_analysis
)
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def portfolio_analysis(portfolio):
    try:
        end_date = datetime.now()
        start_date = end_date.replace(year=end_date.year - 5)
        tickers = list(portfolio.keys())
        number_of_shares = np.array(list(portfolio.values()), dtype=float)

        # Fetch current prices for the tickers
        current_prices = {}
        for ticker in tickers:
            price = get_current_stock_price(ticker)
            if price is None:
                logging.error(f"Could not fetch current price for {ticker}")
                return None
            current_prices[ticker] = price

        # Calculate total value of the portfolio
        total_value = 0.0
        stock_values = []
        for ticker, shares in portfolio.items():
            stock_value = shares * current_prices[ticker]
            stock_values.append(stock_value)
            total_value += stock_value

        if total_value == 0:
            logging.error("Total value of portfolio is zero.")
            return None

        # Calculate weights based on current value of each stock
        weights = np.array(stock_values) / total_value

        # Prepare detailed portfolio information
        portfolio_details = []
        weight_percentages = (weights * 100).round(2).tolist()
        for ticker, shares, price, weight in zip(tickers, number_of_shares, current_prices.values(), weight_percentages):
            portfolio_details.append({
                'ticker': ticker,
                'shares': shares,
                'current_price': price,
                'weight_percentage': weight
            })

        # Fetch historical data for analysis
        data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
        if data.empty:
            logging.error("No data fetched for the given tickers.")
            return None

        # Handle the case where data is a Series (single stock)
        if isinstance(data, pd.Series):
            data = data.to_frame()
            data.columns = [tickers[0]]

        # Drop rows with missing values
        data = data.dropna()

        # Calculate portfolio metrics
        expected_return, risk, cov_matrix = mean_variance_optimization(data, weights)
        sharpe_ratio = calculate_sharpe_ratio(expected_return, risk)
        diversification_ratio = calculate_diversification_ratio(data, weights)

        # Generate prompts and get analysis from OpenAI
        prompts = generate_chat_prompts(
            portfolio_details, sharpe_ratio, diversification_ratio, expected_return, risk
        )
        chat_responses = get_chat_analysis(prompts)

        return {
            'analysis': {
                'chat_responses': chat_responses
            },
            'metrics': {
                'expected_return': expected_return,
                'risk': risk,
                'sharpe_ratio': sharpe_ratio,
                'diversification_ratio': diversification_ratio
            }
        }
    except Exception as e:
        logging.error(f"Error in portfolio_analysis: {e}")
        return None


def get_or_create_portfolio(user_id):
    portfolio = Portfolio.query.filter_by(user_id=user_id).first()
    if not portfolio:
        portfolio = Portfolio(user_id=user_id)
        db.session.add(portfolio)
        db.session.commit()
    return portfolio


def add_stock_to_portfolio(user_id, ticker, num_shares, purchase_date=None):
    try:
        portfolio = get_or_create_portfolio(user_id)

        # Ensure purchase_date is a timezone-aware datetime
        if purchase_date:
            if isinstance(purchase_date, str):
                # Parse string into a datetime object
                purchase_date = datetime.fromisoformat(purchase_date)
            if purchase_date.tzinfo is None:  # If it's timezone-naive
                # Convert to timezone-aware using UTC (or your desired timezone)
                purchase_date = pytz.utc.localize(purchase_date)

        price = get_stock_price_at_date(ticker, purchase_date)
        if price is None:
            logger.error(f"Could not fetch price for {ticker} at date {purchase_date}")
            return False

        existing_stock = PortfolioStock.query.filter_by(portfolio_id=portfolio.id, ticker=ticker).first()
        if existing_stock:
            # Update the number of shares and recalculate the average price per share
            total_shares = existing_stock.number_of_shares + num_shares
            total_cost = (existing_stock.number_of_shares * existing_stock.pps_at_purchase) + (num_shares * price)
            average_price = total_cost / total_shares
            existing_stock.number_of_shares = total_shares
            existing_stock.pps_at_purchase = average_price
        else:
            new_stock = PortfolioStock(
                ticker=ticker.upper(),
                number_of_shares=num_shares,
                pps_at_purchase=price,
                portfolio=portfolio
            )
            db.session.add(new_stock)

        db.session.commit()
        return True
    except Exception as e:
        logger.error(f"Error adding stock to portfolio: {e}")
        return False


def remove_stock_from_portfolio(user_id, ticker):
    try:
        portfolio = get_or_create_portfolio(user_id)
        stock = PortfolioStock.query.filter_by(portfolio_id=portfolio.id, ticker=ticker).first()
        if stock:
            db.session.delete(stock)
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error removing stock from portfolio: {e}")
        return False


def get_portfolio(user_id):
    portfolio = get_or_create_portfolio(user_id)
    stocks = PortfolioStock.query.filter_by(portfolio_id=portfolio.id).all()
    portfolio_data = []
    for stock in stocks:
        stock_data = get_stock_data(stock.ticker)
        if stock_data:
            stock_data['number_of_shares'] = stock.number_of_shares
            stock_data['pps_at_purchase'] = stock.pps_at_purchase
            stock_data['total_invested'] = stock.number_of_shares * stock.pps_at_purchase
            stock_data['current_value'] = stock.number_of_shares * stock_data['close_price']
            stock_data['profit_loss'] = stock_data['current_value'] - stock_data['total_invested']
            stock_data['profit_loss_percentage'] = (
                (stock_data['profit_loss'] / stock_data['total_invested']) * 100
                if stock_data['total_invested'] != 0 else 0
            )
            portfolio_data.append(stock_data)
    return portfolio_data


def get_portfolio_recommendations(user_id, indicators={}):
    portfolio = get_or_create_portfolio(user_id)
    stocks = PortfolioStock.query.filter_by(portfolio_id=portfolio.id).all()
    recommendations = {}
    for stock in stocks:
        predictions = get_predictions(
            stock.ticker,
            MACD=indicators.get('MACD', False),
            RSI=indicators.get('RSI', False),
            SMA=indicators.get('SMA', False),
            EMA=indicators.get('EMA', False),
            ATR=indicators.get('ATR', False),
            BBands=indicators.get('BBands', False),
            VWAP=indicators.get('VWAP', False)
        )
        if predictions:
            recommendations[stock.ticker] = predictions
    return recommendations