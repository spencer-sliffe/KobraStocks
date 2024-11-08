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
