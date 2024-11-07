# Backend/kobrastocks/services.py

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from flask import current_app
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.utils import class_weight
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_sma(dataframe, time):
    """Simple Moving Average"""
    dataframe[f'SMA_{time}'] = dataframe['Close'].rolling(window=time).mean()
    return dataframe


def add_ema(dataframe, time):
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


def retrieve_data(ticker):
    try:
        time = datetime.now()
        startyear = time.year - 5
        startStr = f"{startyear}-01-01"
        ticker_obj = yf.Ticker(ticker)
        yesterday = (time - timedelta(days=1)).strftime('%Y-%m-%d')
        dataframe = ticker_obj.history(period='5y', start=startStr, end=yesterday)
        if dataframe.empty:
            raise ValueError(f"No data found for ticker {ticker}")
        dataframe.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True, errors='ignore')
        dataframe['Tomorrow'] = dataframe['Close'] < dataframe['Close'].shift(-1)
        dataframe['Week'] = dataframe['Close'] < dataframe['Close'].shift(-5)
        dataframe['Month'] = dataframe['Close'] < dataframe['Close'].shift(-30)
        return dataframe
    except Exception as e:
        print(f"Error retrieving data for ticker {ticker}: {e}")
        return None


def add_indicators(dataframe,MACD=False, RSI=False, SMA=False, EMA=False, ATR=False, BBands=False, VWAP=False):
    if MACD:
        dataframe = add_macd(dataframe)
    if RSI:
        dataframe = add_rsi(dataframe)
    if SMA:
        dataframe = add_sma(dataframe)
    if EMA:
        dataframe = add_ema(dataframe)
    if ATR:
        dataframe = add_atr(dataframe)
    if BBands:
        dataframe = add_bollinger_bands(dataframe)
    if VWAP:
        dataframe = add_vwap(dataframe)
    dataframe.dropna(inplace=True)
    return dataframe


def make_chart(dataframe, MA9, MA50, MACD, RSI):
    try:
        chartData = dataframe.copy()
        chartData['Date'] = chartData.index
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03)
        fig.add_trace(go.Candlestick(
            x=chartData['Date'],
            open=chartData['Open'],
            high=chartData['High'],
            low=chartData['Low'],
            close=chartData['Close'],
            increasing_line_color='green',
            decreasing_line_color='red',
            name="Candlestick"
        ), row=1, col=1)
        if MA9:
            fig.add_trace(go.Scatter(
                x=chartData['Date'],
                y=chartData['MA9'],
                mode='lines',
                line=dict(color='blue', width=1.5),
                name='MA9'
            ), row=1, col=1)
        if MA50:
            fig.add_trace(go.Scatter(
                x=chartData['Date'],
                y=chartData['MA50'],
                mode='lines',
                line=dict(color='purple', width=1.5),
                name='MA50'
            ), row=1, col=1)
        if MACD:
            fig.add_trace(go.Scatter(
                x=chartData['Date'],
                y=chartData['MACD'],
                mode='lines',
                line=dict(color='green', width=1.5),
                name='MACD'
            ), row=1, col=1)
        if RSI:
            fig.add_trace(go.Scatter(
                x=chartData['Date'],
                y=chartData['RSI'],
                mode='lines',
                line=dict(color='orange', width=1.5),
                name='RSI'
            ), row=1, col=1)
        fig.add_trace(go.Bar(
            x=chartData['Date'],
            y=chartData['Volume'],
            name='Volume',
            marker_color='blue'
        ), row=2, col=1)
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            paper_bgcolor='black',
            yaxis=dict(title='Price'),
            yaxis2=dict(title='Volume', side='right', showticklabels=False)
        )
        return fig
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def train_models(dataframe, dwm):

    if dataframe.shape[0] < 10:
        logger.error("Not enough data to train the model.")
        raise ValueError("Not enough data to train the model.")

    # Ensure the dataframe is sorted by date or time index
    dataframe = dataframe.sort_index()

    # Retain potentially useful features
    target_vars = ['Month', 'Week', 'Tomorrow']
    feature_columns = [col for col in dataframe.columns if col not in target_vars]
    X = dataframe[feature_columns]

    # Extract the target variable
    target_map = {1: 'Tomorrow', 2: 'Week', 3: 'Month'}
    target_col = target_map.get(dwm, 'Month')
    if target_col not in dataframe.columns:
        logger.error(f"Target column '{target_col}' not found in dataframe.")
        raise ValueError(f"Target column '{target_col}' not found in dataframe.")
    Y = dataframe[target_col].astype(int)

    # Split data into training and test sets based on time
    split_index = int(len(X) * 0.8)
    if split_index == 0 or split_index == len(X):
        logger.error("Not enough data to split into training and testing sets.")
        raise ValueError("Insufficient data for splitting.")
    X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
    Y_train, Y_test = Y.iloc[:split_index], Y.iloc[split_index:]

    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Handle class imbalance
    classes = np.unique(Y_train)
    class_weights = class_weight.compute_class_weight('balanced', classes=classes, y=Y_train)
    class_weights_dict = dict(zip(classes, class_weights))

    # Use TimeSeriesSplit for cross-validation
    tscv = TimeSeriesSplit(n_splits=5)

    # Expand hyperparameter grid
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [None, 10],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
    }

    rf = RandomForestClassifier(random_state=42, class_weight=class_weights_dict)

    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=tscv,
        n_jobs=-1,
        verbose=0,
        scoring='balanced_accuracy'
    )

    # Fit the model
    grid_search.fit(X_train_scaled, Y_train)

    # Evaluate the model on the test set
    Y_pred = grid_search.predict(X_test_scaled)
    accuracy = grid_search.score(X_test_scaled, Y_test)
    report = classification_report(Y_test, Y_pred, output_dict=True)
    logger.info("Classification Report:")
    logger.info(classification_report(Y_test, Y_pred))

    # Predict the next time point
    latest_data = X.iloc[-1].values.reshape(1, -1)
    # Convert latest_data to DataFrame to maintain feature names
    latest_data_df = pd.DataFrame(latest_data, columns=X.columns)
    latest_data_scaled = scaler.transform(latest_data_df)
    today_prediction = grid_search.predict(latest_data_scaled)[0]

    return {
        'accuracy': accuracy,
        'classification_report': report,
        'today_prediction': int(today_prediction),
    }


def get_stock_data(ticker):
    dataframe = retrieve_data(ticker)
    if dataframe is None or dataframe.empty:
        return None

    if len(dataframe) < 2:
        return None

    previous_close = dataframe['Close'].iloc[-2]
    current_close = dataframe['Close'].iloc[-1]
    percentage_change = ((current_close - previous_close) / previous_close) * 100 if previous_close != 0 else 0

    stock_data = {
        "ticker": ticker,
        "open_price": dataframe['Open'].iloc[-1],
        "close_price": current_close,
        "high_price": dataframe['High'].iloc[-1],
        "low_price": dataframe['Low'].iloc[-1],
        "volume": int(dataframe['Volume'].iloc[-1]),
        "percentage_change": percentage_change
    }
    return stock_data


def get_predictions(ticker, MACD, RSI, SMA, EMA, ATR, BBands, VWAP):
    dataframe = retrieve_data(ticker)
    if dataframe is None:
        return None
    dataframe = add_indicators(dataframe, MACD=MACD, RSI=RSI, SMA=SMA, EMA=EMA, ATR=ATR, BBands=BBands, VWAP=VWAP)
    d_result = train_models(dataframe, dwm=1)
    w_result = train_models(dataframe, dwm=2)
    m_result = train_models(dataframe, dwm=3)

    # Check if the results are None and proceed accordingly
    if d_result is None or w_result is None or m_result is None:
        return None

    # Retrieve accuracy and prediction from the dictionary
    return {
        'daily': {
            'prediction': int(d_result['today_prediction']),
            'accuracy': float(d_result['accuracy'])
        },
        'weekly': {
            'prediction': int(w_result['today_prediction']),
            'accuracy': float(w_result['accuracy'])
        },
        'monthly': {
            'prediction': int(m_result['today_prediction']),
            'accuracy': float(m_result['accuracy'])
        }
    }


def get_stock_chart(ticker, MA9=False, MA50=False, MACD=False, RSI=False):
    dataframe = retrieve_data(ticker)
    if dataframe is None:
        return None
    dataframe = add_indicators(dataframe, MA9=MA9, MA50=MA50, MACD=MACD, RSI=RSI)
    fig = make_chart(dataframe, MA9=MA9, MA50=MA50, MACD=MACD, RSI=RSI)
    if fig is None:
        return None
    return fig


def send_contact_form(contact_data):
    """
    Handle contact form submission.
    """
    name = contact_data.get('name')
    email = contact_data.get('email')
    message = contact_data.get('message')
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


def send_email(subject, recipient, body):
    """
    Implement email sending logic here.
    """
    print(f"Sending email to {recipient}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
