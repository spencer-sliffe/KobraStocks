"""
------------------Prologue--------------------
File Name: utils.py
Path: Backend/kobrastocks/utils.py

Description:
Contains utility functions for data formatting, stock data parsing, and financial indicator calculations. Functions include:
- `format_date`: Converts date strings to readable formats.
- `parse_stock_data`: Cleans raw stock data into a structured format.
- `calculate_percentage_change`: Computes the percentage change between two values.
- `convert_to_builtin_types`: Converts complex types (e.g., NumPy and pandas objects) to Python built-ins for JSON serialization.
- Indicator functions (`add_sma`, `add_ema`, `add_rsi`, etc.): Compute financial indicators like SMA, EMA, RSI, MACD, ATR, Bollinger Bands, and VWAP for stock analysis.

Input:
Dataframes containing stock data, raw API responses, and individual numerical values.

Output:
Formatted data, calculated indicator columns, and cleaned JSON-serializable structures.

Collaborators: Spencer Sliffe, Saje Cowell, Charlie Gillund
---------------------------------------------
"""
import logging
import os
from datetime import datetime
import numpy as np
import pandas as pd
import openai
import yfinance as yf


def format_date(date_str):
    """
    Converts a date string into a more readable format.
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except ValueError:
        return date_str


def parse_stock_data(raw_data):
    """
    Parse raw stock data from an external API into a clean format.
    """
    return {
        'ticker': raw_data.get('ticker'),
        'open': raw_data.get('open_price'),
        'close': raw_data.get('close_price'),
        'high': raw_data.get('high_price'),
        'low': raw_data.get('low_price'),
        'volume': raw_data.get('volume'),
    }


def calculate_percentage_change(old_value, new_value):
    """
    Utility function to calculate the percentage change between two values.
    """
    if old_value == 0:
        return None
    try:
        return ((new_value - old_value) / old_value) * 100
    except TypeError:
        return None


def convert_to_builtin_types(obj):
    """Converts Objects to a """
    if isinstance(obj, dict):
        return {k: convert_to_builtin_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_builtin_types(v) for v in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif isinstance(obj, pd.Timedelta):
        return obj.total_seconds()
    else:
        return obj


def add_sma(dataframe, time=14):
    """calculates Simple Moving Average given a df"""
    dataframe[f'SMA_{time}'] = dataframe['Close'].rolling(window=time).mean()
    return dataframe


def add_ema(dataframe, time=14):
    """calculates Exponential Moving Average given a df"""
    dataframe[f'EMA_{time}'] = dataframe['Close'].ewm(span=time, adjust=False).mean()
    return dataframe


def add_rsi(dataframe, time=14):
    """Relative Strength Index"""
    delta = dataframe['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=time).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=time).mean()
    rs = gain / loss
    dataframe[f'RSI_{time}'] = 100 - (100 / (1 + rs))
    return dataframe


def add_macd(dataframe, fast=12, slow=26, signal=9):
    """Moving Average Convergence Divergence"""
    dataframe['MACD_Line'] = dataframe['Close'].ewm(span=fast, adjust=False).mean() - dataframe['Close'].ewm(span=slow, adjust=False).mean()
    dataframe['MACD_Signal'] = dataframe['MACD_Line'].ewm(span=signal, adjust=False).mean()
    dataframe['MACD_Hist'] = dataframe['MACD_Line'] - dataframe['MACD_Signal']
    return dataframe


def add_atr(dataframe, time=5):
    """Average True Range"""
    high_low = dataframe['High'] - dataframe['Low']
    high_close = np.abs(dataframe['High'] - dataframe['Close'].shift())
    low_close = np.abs(dataframe['Low'] - dataframe['Close'].shift())
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    dataframe[f'ATR_{time}'] = true_range.rolling(window=time).mean()
    return dataframe


def add_bollinger_bands(dataframe, time=20):
    """Bollinger Bands"""
    dataframe['BB_Middle'] = dataframe['Close'].rolling(window=time).mean()
    dataframe['BB_Upper'] = dataframe['BB_Middle'] + 2 * dataframe['Close'].rolling(window=time).std()
    dataframe['BB_Lower'] = dataframe['BB_Middle'] - 2 * dataframe['Close'].rolling(window=time).std()
    return dataframe


def add_vwap(dataframe):
    """Volume Weighted Average Price"""
    dataframe['VWAP'] = (dataframe['Volume'] * (dataframe['High'] + dataframe['Low'] + dataframe['Close']) / 3).cumsum() / dataframe['Volume'].cumsum()
    return dataframe


def mean_variance_optimization(data, weights):
    """
    Calculate expected return, risk, and covariance matrix of the portfolio.
    """
    returns = data.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    # Annualize returns and covariance
    annual_factor = 252  # Trading days in a year
    mean_returns *= annual_factor
    cov_matrix *= annual_factor

    expected_return = np.dot(weights, mean_returns)
    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
    risk = np.sqrt(portfolio_variance)
    return expected_return, risk, cov_matrix


def calculate_diversification_ratio(data, weights, trading_days=252):
    """
    Calculate the diversification ratio of the portfolio.
    """
    weights = np.array(weights)
    returns = data.pct_change().dropna()

    # Handle the single-stock case
    if returns.shape[1] == 1:
        return 1.0

    # Calculate daily volatilities and annualize them
    volatilities_daily = returns.std()
    volatilities_annual = volatilities_daily * np.sqrt(trading_days)

    # Weighted sum of individual annualized volatilities
    weighted_volatility = np.dot(weights, volatilities_annual)

    # Calculate annualized portfolio volatility
    cov_matrix_daily = returns.cov()
    cov_matrix_annual = cov_matrix_daily * trading_days
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix_annual, weights)))

    # Compute diversification ratio
    if portfolio_volatility != 0:
        diversification_ratio = weighted_volatility / portfolio_volatility
    else:
        diversification_ratio = 0.0

    return diversification_ratio


def calculate_sharpe_ratio(expected_return, risk, risk_free_rate=0.02):
    """
    Calculate the Sharpe Ratio of the portfolio.
    """
    excess_return = expected_return - risk_free_rate
    sharpe_ratio = excess_return / risk if risk != 0 else 0
    return sharpe_ratio


def generate_chat_prompts(portfolio_details, sharpe_ratio, diversification_ratio, expected_return, risk, alpha, beta, sortino_ratio, max_drawdown):
    """
    Generate prompts for OpenAI API based on portfolio metrics and detailed holdings.
    """
    portfolio_description = ', '.join([
        f"{item['ticker']} ({item['shares']} shares at ${item['current_price']:.2f}, {item['weight_percentage']}% weight)"
        for item in portfolio_details
    ])

    # Incorporate new metrics into the prompt
    # We'll mention alpha, beta, sortino_ratio, and max_drawdown along with the existing metrics
    prompt1 = (
        f"Analyze a portfolio consisting of the following stocks: {portfolio_description}. "
        f"The portfolio has:\n"
        f"- Expected annual return: {expected_return:.2%}\n"
        f"- Annualized risk: {risk:.2%}\n"
        f"- Sharpe ratio: {sharpe_ratio:.2f}\n"
        f"- Diversification ratio: {diversification_ratio:.2f}\n"
        f"- Alpha: {alpha:.2f}\n"
        f"- Beta: {beta:.2f}\n"
        f"- Sortino ratio: {sortino_ratio:.2f}\n"
        f"- Max drawdown: {max_drawdown:.2%}\n\n"
        f"What are your thoughts on this portfolio given these metrics?"
    )

    prompt2 = (
        "Based on the analysis, rate this portfolio from A to F, considering factors like diversification, "
        "risk, expected return, alpha, beta, Sortino ratio, and max drawdown."
    )

    prompt3 = (
        f"Given the current portfolio of {portfolio_description}, please suggest specific stocks to add or remove "
        f"to improve diversification, risk-adjusted returns, and potentially improve metrics like Sharpe ratio, Sortino ratio, and reduce max drawdown. "
        f"Exclude the stocks already included in the portfolio."
    )

    return [prompt1, prompt2, prompt3]


def get_chat_analysis(prompts):
    """
    Get analysis from OpenAI's ChatCompletion API using the generated prompts.
    """
    openai.api_key = os.getenv('OPENAI_API_KEY')
    if not openai.api_key:
        raise ValueError("OpenAI API key not found in environment variables.")

    responses = []
    for i, prompt in enumerate(prompts):
        try:
            # Check if prompt length exceeds model's context window
            if len(prompt) > 2048:
                logging.warning(f"Prompt {i+1} is too long. Truncating the prompt.")
                prompt = prompt[:2048]

            # Create a chat completion
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a financial advisor providing insights on a stock portfolio."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                n=1,
                temperature=0.5,
            )
            # Extract the assistant's reply
            message = response['choices'][0]['message']['content'].strip()
            responses.append(message)
        except Exception as e:
            logging.error(f"OpenAI API error on prompt {i+1}: {e}")
            responses.append("Could not generate response due to an error.")
    return responses


def check_stock_validity(ticker):
    """
    Checks if the given ticker is a valid and actively traded stock.
    Returns True if valid, False otherwise.
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        print(ticker_obj)
        # Attempt to fetch basic stock information
        info = ticker_obj.info
        # Check if the stock has a current market price
        if 'regularMarketOpen' in info and info['regularMarketOpen'] is not None:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error checking stock validity for {ticker}: {e}")
        return False


def get_stock_chat_analysis(prompts):
    """
    Get analysis from OpenAI's ChatCompletion API using the generated prompts.
    """
    openai.api_key = os.getenv('OPENAI_API_KEY')
    if not openai.api_key:
        raise ValueError("OpenAI API key not found in environment variables.")

    responses = []
    for i, prompt in enumerate(prompts):
        try:
            # Check if prompt length exceeds model's context window
            if len(prompt) > 2048:
                logging.warning(f"Prompt {i+1} is too long. Truncating the prompt.")
                prompt = prompt[:2048]

            # Create a chat completion
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a financial analyst providing insights on stocks."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                n=1,
                temperature=0.5,
            )
            # Extract the assistant's reply
            message = response['choices'][0]['message']['content'].strip()
            responses.append(message)
        except Exception as e:
            logging.error(f"OpenAI API error on prompt {i+1}: {e}")
            responses.append("Could not generate response due to an error.")
    return responses


def generate_stock_analysis_prompt(stock_data):
    """
    Generate a prompt for OpenAI API based on stock data.
    Incorporates user-specific investment details if available.
    """
    prompt = (
        f"Provide a detailed analysis for the stock {stock_data['ticker']} ({stock_data['name']}). "
        f"The current price is ${stock_data['close_price']:.2f}. "
        f"The stock has changed {stock_data['percentage_change']:.2f}% since yesterday. "
        f"The day's range was from ${stock_data['low_price']:.2f} to ${stock_data['high_price']:.2f}. "
        f"Volume traded was {stock_data['volume']}. "
    )
    if 'user_shares' in stock_data:
        prompt += (
            f"\nThis user holds {stock_data['user_shares']} shares purchased at "
            f"${stock_data['user_pps_at_purchase']:.2f} each. The total invested is "
            f"${stock_data['user_total_invested']:.2f}, currently valued at ${stock_data['user_current_value']:.2f}, "
            f"resulting in a profit/loss of ${stock_data['user_profit_loss']:.2f} "
            f"({stock_data['user_profit_loss_percentage']:.2f}% change)."
        )

    prompt += "\nPlease provide an insightful analysis of the stock's current performance and future prospects in the context of the user's personal holdings."

    return prompt
