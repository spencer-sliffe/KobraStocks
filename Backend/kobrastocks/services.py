import yfinance as yf
from flask import current_app
from some_email_library import send_email  # Example for sending emails
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots

# Indicator functions
def addRSI(dataframe):
    dataframe['Price Diff'] = dataframe['Close'].diff()
    dataframe['Gain'] = np.where(dataframe['Price Diff'] > 0, dataframe['Price Diff'], 0)
    dataframe['Loss'] = np.where(dataframe['Price Diff'] < 0, -dataframe['Price Diff'], 0)
    window_length = 14
    dataframe['Avg Gain'] = dataframe['Gain'].ewm(alpha=1/window_length, min_periods=window_length).mean()
    dataframe['Avg Loss'] = dataframe['Loss'].ewm(alpha=1/window_length, min_periods=window_length).mean()
    dataframe['RS'] = dataframe['Avg Gain'] / dataframe['Avg Loss']
    dataframe['RSI'] = 100 - (100 / (1 + dataframe['RS']))
    dataframe.drop(['Price Diff', 'Gain', 'Loss', 'Avg Gain', 'Avg Loss', 'RS'], axis=1, inplace=True)
    return dataframe

def addMA50(dataframe):
    dataframe['MA50'] = dataframe['Close'].rolling(window=50).mean()
    return dataframe

def addMA9(dataframe):
    dataframe['MA9'] = dataframe['Close'].rolling(window=9).mean()
    return dataframe

def addMACD(dataframe):
    dataframe['EMA12'] = dataframe['Close'].ewm(span=12, adjust=False).mean()
    dataframe['EMA26'] = dataframe['Close'].ewm(span=26, adjust=False).mean()
    dataframe['MACD'] = dataframe['EMA12'] - dataframe['EMA26']
    dataframe['Signal_Line'] = dataframe['MACD'].ewm(span=9, adjust=False).mean()
    dataframe.drop(['EMA12', 'EMA26'], axis=1, inplace=True)
    return dataframe

# Data retrieval and indicator adding
def retrieveData(ticker, period):
    time = datetime.now()
    startyear = time.year - 5
    startStr = f"{startyear}-01-01"
    ticker = yf.Ticker(ticker)
    dataframe = ticker.history(period='1d', start=startStr, end=(time - timedelta(days=1)).strftime('%Y-%m-%d'))
    dataframe.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True)
    dataframe['Tomorrow'] = dataframe['Close'] < dataframe['Close'].shift(-1)
    dataframe['Week'] = dataframe['Close'] < dataframe['Close'].shift(-5)
    dataframe['Month'] = dataframe['Close'] < dataframe['Close'].shift(-30)
    return dataframe

def addIndicators(dataframe, MA9, MA50, MACD, RSI):
    if MACD:
        dataframe = addMACD(dataframe)
    if MA9:
        dataframe = addMA9(dataframe)
    if RSI:
        dataframe = addRSI(dataframe)
    if MA50:
        dataframe = addMA50(dataframe)
    return dataframe

# Chart generation
def makeChart(dataframe, MA9, MA50):
    try:
        chartData = dataframe
        chartData['Date'] = chartData.index
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03)
        fig.add_trace(go.Candlestick(x=dataframe.index, open=dataframe['Open'], high=dataframe['High'], 
                                     low=dataframe['Low'], close=dataframe['Close'], increasing_line_color='green', 
                                     decreasing_line_color='red', name="Candlestick"), row=1, col=1)
        if MA9:
            fig.add_trace(go.Scatter(x=chartData['Date'], y=chartData['MA9'], mode='lines', line=dict(color='blue', width=1.5), name='MA9'), row=1, col=1)
        if MA50:
            fig.add_trace(go.Scatter(x=chartData['Date'], y=chartData['MA50'], mode='lines', line=dict(color='purple', width=1.5), name='MA50'), row=1, col=1)
        fig.add_trace(go.Bar(x=chartData.index, y=chartData['Volume'], name='Volume', marker_color='blue'), row=2, col=1)
        fig.update_layout(xaxis_rangeslider_visible=False, paper_bgcolor='black')
        return fig
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Model training
def trainModels(dataframe, dwm):
    X = dataframe.drop(['Month', 'Week', 'Tomorrow', 'High', 'Low', 'Open'], axis=1)
    Y = dataframe[dwm].astype(int)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    param_grid = {'n_estimators': [100, 200, 300], 'max_depth': [None, 10, 20]}
    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2, scoring='accuracy')
    grid_search.fit(X_train, Y_train)
    
    rfAcc = accuracy_score(Y_test, grid_search.predict(X_test))
    todayPrediction = grid_search.best_estimator_.predict(dataframe.tail(1).drop(['Month', 'Week', 'Tomorrow'], axis=1))[0]
    
    return rfAcc, todayPrediction

def get_stock_data(ticker, period):
    """
    Fetch stock data for a specific ticker and period from Yahoo Finance.
    This logic is separated from the route and can be reused in different places.
    """
    stock = yf.Ticker(ticker)
    dataframe = stock.history(period=f"{period}d")
    
    # Simplify the dataframe to return JSON-friendly data
    stock_data = {
        "ticker": ticker,
        "open_price": dataframe['Open'][0],
        "close_price": dataframe['Close'][0],
        "high_price": dataframe['High'][0],
        "low_price": dataframe['Low'][0],
        "volume": dataframe['Volume'][0]
    }
    return stock_data

def send_contact_form(contact_data):
    """
    Handle contact form submission. This can send an email or store data in a database.
    """
    name = contact_data.get('name')
    email = contact_data.get('email')
    message = contact_data.get('message')
    
    # Example: Sending an email notification
    try:
        send_email(
            subject="New Contact Form Submission",
            recipient=current_app.config['ADMIN_EMAIL'],
            body=f"Message from {name} ({email}): {message}"
        )
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send contact form: {e}")
        return False
