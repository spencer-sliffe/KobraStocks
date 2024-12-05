"""
------------------Prologue--------------------
File Name: services.py
Path: Backend/kobrastocks/services.py

Description:
Implements core services for data retrieval, technical indicator computation, model training, chart creation, and email handling. Key functions include:
- `retrieve_data`: Fetches and prepares historical stock data.
- `add_indicators`: Adds technical indicators (e.g., MACD, RSI) to stock data.
- `make_chart`: Generates candlestick and volume charts for a given stock.
- `train_models` and `train_regression_models`: Trains classification and regression models for stock price forecasting.
- `get_stock_data` and `get_predictions`: Fetches processed stock data and predictions for specified indicators.
- `send_contact_form` and `send_email`: Handles contact form submissions and email notifications.

Input:
Ticker symbols, technical indicators, contact form data, and user configurations.

Output:
Serialized stock data, predictions, charts, and contact form confirmation.

Collaborators: Spencer Sliffe, Saje Cowell, Charlie Gillund
---------------------------------------------
"""

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from flask import current_app
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.utils import class_weight
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from .utils import *

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

        # Classification targets
        dataframe['Tomorrow'] = (dataframe['Close'].shift(-1) > dataframe['Close']).astype(int)
        dataframe['Week'] = (dataframe['Close'].shift(-5) > dataframe['Close']).astype(int)
        dataframe['Month'] = (dataframe['Close'].shift(-21) > dataframe['Close']).astype(int)

        # Regression targets
        dataframe['Close_Tomorrow'] = dataframe['Close'].shift(-1)
        dataframe['Close_NextWeek'] = dataframe['Close'].shift(-5)
        dataframe['Close_NextMonth'] = dataframe['Close'].shift(-21)  # Approximate number of trading days in a month

        # Drop rows with NaN in target columns
        dataframe.dropna(subset=[
            'Close_Tomorrow', 'Close_NextWeek', 'Close_NextMonth',
            'Tomorrow', 'Week', 'Month'
        ], inplace=True)

        return dataframe
    except Exception as e:
        print(f"Error retrieving data for ticker {ticker}: {e}")
        return None


from concurrent.futures import ThreadPoolExecutor, as_completed


def add_indicators(dataframe, MACD=False, RSI=False, SMA=False, EMA=False, ATR=False, BBands=False, VWAP=False):
    indicators = []

    if MACD:
        indicators.append(('MACD', add_macd))
    if RSI:
        indicators.append(('RSI', add_rsi))
    if SMA:
        indicators.append(('SMA', add_sma))
    if EMA:
        indicators.append(('EMA', add_ema))
    if ATR:
        indicators.append(('ATR', add_atr))
    if BBands:
        indicators.append(('BBands', add_bollinger_bands))
    if VWAP:
        indicators.append(('VWAP', add_vwap))

    def apply_indicator(indicator_func):
        try:
            return indicator_func(dataframe.copy())
        except Exception as e:
            logger.error(f"Error applying indicator {indicator_func.__name__}: {e}")
            return None

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(apply_indicator, func) for name, func in indicators]
        for future in futures:
            result = future.result()
            if result is not None:
                dataframe = result

    dataframe.dropna(inplace=True)
    return dataframe



def make_chart(ticker,interval='1d',zoom=60):
    
    try:
        if interval not in ['1d', '1wk', '1mo']:
            raise ValueError("Interval must be one of ['1d', '1wk', '1mo']")
        # Set the start date to 5 years ago from today
        time = datetime.now()
        startyear = time.year - 5
        startStr = f"{startyear}-01-01"
        yesterday = (time - timedelta(days=1))
        
        # Fetch historical data for the specified interval
        ticker_obj = yf.Ticker(ticker)
        dataframe = ticker_obj.history(start=startStr, end=yesterday, interval=interval)
        chartData = dataframe.copy()
        if dataframe.empty:
            raise ValueError(f"No data found for ticker {ticker}")
        
        chartData = chartData.reset_index()
        chartData['Date'] = pd.to_datetime(chartData['Date']).dt.date
        length=len(chartData)

        chartData.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True, errors='ignore')
       
         # Determine initial zoom range
        zoom_data=chartData[-zoom:]

        price_min=zoom_data['Low'].min()
        price_max=zoom_data['High'].max()
        volume_max=chartData['Volume'].max()
        # Create the figure with subplots
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.01,
            row_heights=[0.7, 0.3]
        )

        # Add candlestick trace
        fig.add_trace(
            go.Candlestick(
                x=chartData['Date'].astype(str),
                open=chartData['Open'],
                high=chartData['High'],
                low=chartData['Low'],
                close=chartData['Close'],
                name='Price',
                increasing_line_color='green',
                decreasing_line_color='red',
                
            ),
            row=1, col=1
        )
        
        # Add volume bar trace
        fig.add_trace(
            go.Bar(
                x=chartData['Date'].astype(str),
                y=chartData['Volume'],
                name='Volume',
                marker_color='blue',
                opacity=0.5,
            ),
            row=2, col=1
        )
    

        # Update layout
        fig.update_layout(
        
            xaxis=dict(
                type='category',
                showgrid=False,
                showticklabels=False,  # Hide x-axis labels on top chart
                range=[length-zoom,length],
              
            ),
            xaxis2=dict(
                type='category',
                showgrid=False,
                showticklabels=False,
                tickformat='%b %d, %Y',
                ticks='outside',
                range=[length-zoom,length]
            ),
            yaxis=dict(
                title='Price',
                showgrid=True,
                gridcolor='rgba(200,200,200,0.2)',
                range=[price_min * 0.95, price_max * 1.05]  # Add padding
            ),
            yaxis2=dict(
                title='Volume',
                showgrid=False,
                range=[0, volume_max*1.1],
                side='right',
                fixedrange=True 
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
            margin=dict(
                l=60, r=20, t=50, b=50
            ),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )

        # Add hover templates for better interactivity

        # Update x-axes properties
        fig.update_xaxes(
            rangeslider_visible=False,
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True
        )
#
        ## Update y-axes properties
        fig.update_yaxes(
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True
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


def train_regression_models(dataframe, target_column):
    if dataframe.shape[0] < 50:
        logger.error("Not enough data to train the regression model.")
        return None

    # Ensure the dataframe is sorted by date
    dataframe = dataframe.sort_index()

    # Define feature columns
    target_vars = ['Close_Tomorrow', 'Close_NextWeek', 'Close_NextMonth']
    feature_columns = [col for col in dataframe.columns if col not in target_vars]

    X = dataframe[feature_columns]
    Y = dataframe[target_column]

    # Split data into training and testing sets
    split_index = int(len(X) * 0.8)
    if split_index == 0 or split_index == len(X):
        logger.error("Not enough data to split into training and testing sets.")
        return None

    X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
    Y_train, Y_test = Y.iloc[:split_index], Y.iloc[split_index:]

    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Time Series Cross-Validation
    tscv = TimeSeriesSplit(n_splits=5)

    # Hyperparameter Grid
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [None, 10],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
    }

    rf = RandomForestRegressor(random_state=42)

    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=tscv,
        n_jobs=-1,
        verbose=0,
        scoring='neg_mean_squared_error'
    )

    # Fit the Model
    grid_search.fit(X_train_scaled, Y_train)

    # Evaluate the Model
    Y_pred = grid_search.predict(X_test_scaled)
    mse = mean_squared_error(Y_test, Y_pred)
    mae = mean_absolute_error(Y_test, Y_pred)
    r2 = r2_score(Y_test, Y_pred)
    logger.info(f"Regression metrics for {target_column} - MSE: {mse}, MAE: {mae}, R2: {r2}")

    # Predict Next Period
    latest_data = X.iloc[-1].values.reshape(1, -1)
    latest_data_df = pd.DataFrame(latest_data, columns=X.columns)
    latest_data_scaled = scaler.transform(latest_data_df)
    next_prediction = grid_search.predict(latest_data_scaled)[0]

    return {
        'mse': mse,
        'mae': mae,
        'r2': r2,
        'prediction': next_prediction,
    }


def get_stock_data(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)
        dataframe = ticker_obj.history(period='5y')
        if dataframe.empty or len(dataframe) < 2:
            return None  # Not enough data to calculate percentage change

        # Get stock name
        stock_info = ticker_obj.info
        stock_name = stock_info.get('shortName', '') or stock_info.get('longName', '')

        previous_close = dataframe['Close'].iloc[-2]
        current_close = dataframe['Close'].iloc[-1]

        # Check if previous_close is not zero and not NaN
        if previous_close and not np.isnan(previous_close):
            percentage_change = ((current_close - previous_close) / previous_close) * 100
        else:
            percentage_change = 0.0

        stock_data = {
            "ticker": ticker,
            "name": stock_name,
            "open_price": dataframe['Open'].iloc[-1],
            "close_price": current_close,
            "high_price": dataframe['High'].iloc[-1],
            "low_price": dataframe['Low'].iloc[-1],
            "volume": int(dataframe['Volume'].iloc[-1]),
            "percentage_change": percentage_change
        }
        return stock_data
    except Exception as e:
        current_app.logger.error(f"Error getting stock data for {ticker}: {e}")
        return None


def get_predictions(ticker, MACD=False, RSI=False, SMA=False, EMA=False, ATR=False, BBands=False, VWAP=False):
    try:
        dataframe = retrieve_data(ticker)
        if dataframe is None:
            return None

        # Add indicators in parallel
        dataframe = add_indicators(
            dataframe,
            MACD=MACD,
            RSI=RSI,
            SMA=SMA,
            EMA=EMA,
            ATR=ATR,
            BBands=BBands,
            VWAP=VWAP
        )

        predictions = {}

        def train_for_horizon(dwm):
            try:
                classification_result = train_models(dataframe, dwm)
                regression_target_map = {1: 'Close_Tomorrow', 2: 'Close_NextWeek', 3: 'Close_NextMonth'}
                regression_target = regression_target_map.get(dwm)
                regression_result = train_regression_models(dataframe, regression_target)
                return (dwm, classification_result, regression_result)
            except Exception as e:
                logger.error(f"Error training model for dwm={dwm}: {e}")
                return (dwm, None, None)

        # Use ThreadPoolExecutor to train models in parallel
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(train_for_horizon, dwm) for dwm in [1, 2, 3]]
            for future in as_completed(futures):
                dwm, classification_result, regression_result = future.result()
                if classification_result and regression_result:
                    time_horizon_map = {1: 'Tomorrow', 2: 'Week', 3: 'Month'}
                    horizon = time_horizon_map.get(dwm)
                    predictions[horizon] = {
                        'classification': classification_result,
                        'regression': regression_result
                    }

        return predictions if predictions else None

    except Exception as e:
        logger.error(f"Error in get_predictions: {e}")
        return None


def get_stock_chart(ticker,interval='1d'):
    dataframe = retrieve_data(ticker)
    if dataframe is None:
        return None
    fig = make_chart(ticker,interval=interval)
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


def get_current_stock_price(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)
        data = ticker_obj.history(period='1d')
        if data.empty:
            raise ValueError(f"No data found for ticker {ticker}")
        current_price = data['Close'].iloc[-1]
        return current_price
    except Exception as e:
        logger.error(f"Error getting current stock price for {ticker}: {e}")
        return None
