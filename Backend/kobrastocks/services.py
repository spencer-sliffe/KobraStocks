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
from .indicators import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


 #Add Indicators 
        #SMA and EMA are lists of the MA windows that will be added to the Training set
        #all other indicators are set windows so the param tell if they are added or not 0 or 1
        
def add_indicators(dataframe,SMA,EMA,RSI,MACD,ATR,BBands,VWAP):
    if SMA:  #ADDS SMA
        dataframe=add_SMA(dataframe,50)
        dataframe=add_SMA(dataframe,100)
        dataframe=add_SMA(dataframe,200)
    if SMA:   #ADDS EMA
        dataframe=add_EMA(dataframe,12)
        dataframe=add_EMA(dataframe,26)
        dataframe=add_EMA(dataframe,200)
    if RSI:  #ADDS RSI
        dataframe=add_RSI(dataframe) 
    if MACD:  #ADDS MACD
        dataframe=add_MACD(dataframe) 
    if ATR:  #ADDS ATR
        dataframe=add_ATR(dataframe) 
    if BBands:  #ADDS BBANDS
        dataframe=add_BollingerBands(dataframe) 
    if VWAP:  #ADDS VWAP
        dataframe=add_VWAP(dataframe) 
    dataframe.dropna(inplace=True)
    return dataframe

def make_chart(dataframe):
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


def get_predictions(ticker):
    dataframe = retrieve_data(ticker)
    if dataframe is None:
        return None
    dataframe = add_indicators(dataframe,0,0,0,0,0,0,0)
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


def get_stock_chart(ticker):
    dataframe = retrieve_data(ticker)
    if dataframe is None:
        return None
    dataframe = add_indicators(dataframe,0,0,0,0,0,0,)
    fig = make_chart(dataframe)
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
