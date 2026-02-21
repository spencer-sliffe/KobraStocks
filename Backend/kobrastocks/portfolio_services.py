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
logging.basicConfig(level=logging.INFO) # configs lgging 
logger = logging.getLogger(__name__)#
 

def portfolio_analysis(portfolio):
    try:
        end_date = datetime.now() # gets todays date
        start_date = end_date.replace(year=end_date.year - 5) # finds start date
        tickers = list(portfolio.keys()) # gets tickers from portfolio
        number_of_shares = np.array(list(portfolio.values()), dtype=float) # get number of shares of each stock

        # Fetch current prices and verify portfolio is non-empty
        current_prices = {} 
        for ticker in tickers:
            price = get_current_stock_price(ticker) # gets stock price
            if price is None:
                logging.error(f"Could not fetch current price for {ticker}") # logs  error message
                return None
            current_prices[ticker] = price # adds price to list

        total_value = sum(shares * current_prices[t] for t, shares in portfolio.items())
        if total_value == 0:
            logging.error("Total value of portfolio is zero.") # Logs error message
            return None

        weights = np.array([(portfolio[t] * current_prices[t]) / total_value for t in tickers]) # gets stock weight in portfolio

        # Fetch historical data
        data = yf.download(tickers, start=start_date, end=end_date)['Adj Close'] # gets stock prices 
        if isinstance(data, pd.Series): # if data in series
            data = data.to_frame() #convert to df
            data.columns = [tickers[0]] # Gets df column
        data = data.dropna() #drops invalid data
        if data.empty:
            logging.error("No data fetched for given tickers.") # logs error
            return None

        returns = data.pct_change().dropna() # gets pct change for stocks
        mean_returns = returns.mean() * 252 # gets mean returns
        cov_matrix = returns.cov() * 252 # gets cov matrix

        expected_return = np.dot(weights, mean_returns) # gets expected returns
        portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights)) # get port variance
        risk = np.sqrt(portfolio_variance) # calculates risk
        sharpe_ratio = calculate_sharpe_ratio(expected_return, risk) # calculates sharpe ratio
        diversification_ratio = calculate_diversification_ratio(data, weights) # calculates diverification ratio

        # Additional Metrics
        benchmark = yf.download('SPY', start=start_date, end=end_date)['Adj Close'].dropna() # get SPY data 
        benchmark_returns = benchmark.pct_change().dropna() # gets SPY returns 
        port_daily = (returns * weights).sum(axis=1) # gets daily retunrn via weight
        common_index = port_daily.index.intersection(benchmark_returns.index)#calculates
        port_daily = port_daily.reindex(common_index).dropna()# gets daily portfolio returns 
        bench_daily = benchmark_returns.reindex(common_index).dropna()#gets daily benchmark results

        # Alpha & Beta
        if len(port_daily) > 10:
            beta, alpha = np.polyfit(bench_daily, port_daily, 1) # gets beta and alpha
        else:
            alpha, beta = 0.0, 1.0 # else default beta and alpha

        # Sortino Ratio
        risk_free_rate = 0.02
        excess_returns = port_daily - risk_free_rate / 252
        downside = excess_returns[excess_returns < 0]
        if len(downside) > 0:
            downside_deviation = np.sqrt((downside**2).mean()) * np.sqrt(252) # gets variance of downside
        else:
            downside_deviation = 1e-6
        sortino_ratio = (expected_return - risk_free_rate) / downside_deviation # calulates sortino ratio

        # Max Drawdown
        cum_returns = (1 + port_daily).cumprod() # gets cumulative returns
        peak = cum_returns.cummax() # calculates max of return
        drawdown = (cum_returns - peak) / peak # calculates drawdowns
        max_drawdown = drawdown.min() if not drawdown.empty else 0.0 # calculates max drawdown

        metrics = {
            'expected_return': expected_return,
            'risk': risk,
            'sharpe_ratio': sharpe_ratio,
            'diversification_ratio': diversification_ratio,
            'alpha': alpha,
            'beta': beta,
            'sortino_ratio': sortino_ratio,
            'max_drawdown': max_drawdown
        } # metric dic

        portfolio_details = [
            {
                'ticker': t,
                'shares': portfolio[t],
                'current_price': current_prices[t],
                'weight_percentage': w
            } # portfolio dic
            for t, w in zip(tickers, (weights * 100))
        ]

        # Pass all metrics to generate_chat_prompts
        prompts = generate_chat_prompts(
            portfolio_details=portfolio_details,
            sharpe_ratio=sharpe_ratio,
            diversification_ratio=diversification_ratio,
            expected_return=expected_return,
            risk=risk,
            alpha=alpha,
            beta=beta,
            sortino_ratio=sortino_ratio,
            max_drawdown=max_drawdown
        ) # gets chat prompt 
        chat_responses = get_chat_analysis(prompts) # gets chat gpt responses

        return {
            'analysis': {
                'chat_responses': chat_responses
            },
            'metrics': metrics
        } # returns dic
    except Exception as e:
        logging.error(f"Error in portfolio_analysis: {e}")
        return None


def get_or_create_portfolio(user_id): 
    portfolio = Portfolio.query.filter_by(user_id=user_id).first() # gets portfolio
    if not portfolio:
        portfolio = Portfolio(user_id=user_id) # gets portfolio from db
        db.session.add(portfolio) # adds portfolio to seesion
        db.session.commit() # commits changes
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
            #Makes new stock obj 
            new_stock = PortfolioStock(
                ticker=ticker.upper(),
                number_of_shares=num_shares,
                pps_at_purchase=price,
                portfolio=portfolio
            )
            db.session.add(new_stock)

        db.session.commit() # commits changes
        return True
    except Exception as e:
        logger.error(f"Error adding stock to portfolio: {e}")
        return False

# this function gets the portfolio from the db and deletes the  inputted ticker from it 
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

# gets the saved portfolio given a user from the db and returns it 
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
    portfolio = get_or_create_portfolio(user_id) # gets portfolio
    stocks = PortfolioStock.query.filter_by(portfolio_id=portfolio.id).all() # gets stocks db object
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
        ) # gets prediction
        if predictions:
            recommendations[stock.ticker] = predictions #puts prediction in list
    return recommendations 