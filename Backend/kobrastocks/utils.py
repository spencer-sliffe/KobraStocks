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

from datetime import datetime
import numpy as np
import pandas as pd


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
    """Simple Moving Average"""
    dataframe[f'SMA_{time}'] = dataframe['Close'].rolling(window=time).mean()
    return dataframe


def add_ema(dataframe, time=14):
    """Exponential Moving Average"""
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