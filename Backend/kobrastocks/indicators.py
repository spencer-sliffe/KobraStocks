####Indicator File has the functions to generate all of the Indicators used for analysis"
import pandas as pd 
import numpy as np

def add_SMA(dataframe, time):
    """Simple Moving Average"""
    dataframe[f'SMA_{time}'] = dataframe['Close'].rolling(window=time).mean()

def add_EMA(dataframe, time):
    """Exponential Moving Average"""
    dataframe[f'EMA_{time}'] = dataframe['Close'].ewm(span=time, adjust=False).mean()

def add_RSI(dataframe, time=14):
    """Relative Strength Index"""
    delta = dataframe['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=time).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=time).mean()
    rs = gain / loss 
    dataframe[f'RSI_{time}'] = 100 - (100 / (1 + rs))

def add_MACD(dataframe, fast=12, slow=26, signal=9):
    """Moving Average Convergence Divergence"""
    dataframe['MACD_Line'] = dataframe['Close'].ewm(span=fast, adjust=False).mean() - dataframe['Close'].ewm(span=slow, adjust=False).mean()
    dataframe['MACD_Signal'] = dataframe['MACD_Line'].ewm(span=signal, adjust=False).mean()
    dataframe['MACD_Hist'] = dataframe['MACD_Line'] - dataframe['MACD_Signal']

def add_ATR(dataframe, time=5):
    """Average True Range"""
    high_low = dataframe['High'] - dataframe['Low']
    high_close = np.abs(dataframe['High'] - dataframe['Close'].shift())
    low_close = np.abs(dataframe['Low'] - dataframe['Close'].shift())
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    dataframe[f'ATR_{time}'] = true_range.rolling(window=time).mean()

def add_BollingerBands(dataframe, time=20):
    """Bollinger Bands"""
    dataframe['BB_Middle'] = dataframe['Close'].rolling(window=time).mean()
    dataframe['BB_Upper'] = dataframe['BB_Middle'] + 2 * dataframe['Close'].rolling(window=time).std()
    dataframe['BB_Lower'] = dataframe['BB_Middle'] - 2 * dataframe['Close'].rolling(window=time).std()

def add_VWAP(dataframe):
    """Volume Weighted Average Price"""
    dataframe['VWAP'] = (dataframe['Volume'] * (dataframe['High'] + dataframe['Low'] + dataframe['Close']) / 3).cumsum() / dataframe['Volume'].cumsum()
