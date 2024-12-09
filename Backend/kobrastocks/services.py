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
import pytz
import requests
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
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score,accuracy_score
from sklearn.utils import class_weight
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from concurrent.futures import ThreadPoolExecutor, as_completed
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense,Dropout

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

        
        
        return dataframe
    except Exception as e:
        print(f"Error retrieving data for ticker {ticker}: {e}")
        return None


def add_indicators(dataframe, MACD=False, RSI=False, SMA=False, EMA=False, ATR=False, BBands=False, VWAP=False):
    indicators = []
    indicator_names=[]
    if MACD:
        indicators.append(('MACD', add_macd))
        indicator_names.append('MACD')
    if RSI:
        indicators.append(('RSI', add_rsi))
        indicator_names.append('RSI')
    if SMA:
        indicators.append(('SMA', add_sma))
        indicator_names.append('SMA')
    if EMA:
        indicators.append(('EMA', add_ema))
        indicator_names.append('EMA')
    if ATR:
        indicators.append(('ATR', add_atr))
        indicator_names.append('ATR')
    if BBands:
        indicators.append(('BBands', add_bollinger_bands))
        indicator_names.append('BBands')
    if VWAP:
        indicators.append(('VWAP', add_vwap))
        indicator_names.append('VWAP')

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
    if len(indicator_names)>0:
        dataframe.dropna(subsets=indicator_names,inplace=True)
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
    
    target_vars = ['Month', 'Week', 'Tomorrow','Close_Tomorrow',  'Close_NextWeek',  'Close_NextMonth','Date']
    feature_columns = [col for col in dataframe.columns if col not in target_vars]
  
 
    X = dataframe[feature_columns]
    
    # Extract the target variable
    target_map = {1: 'Tomorrow', 2: 'Week', 3: 'Month'}
    target_col = target_map.get(dwm)
    if target_col not in dataframe.columns:
        #ogger.error(f"Target column '{target_col}' not found in dataframe.")
        raise ValueError(f"Target column '{target_col}' not found in dataframe.")
    dataframe = dataframe.dropna(subset=[target_col])
    if dataframe[target_col].isna().any():
        raise ValueError(f"Target column '{target_col}' contains NaN values.")
    Y = dataframe[target_col].astype(int)

    # Split data into training and test sets based on time
    split_index = int(len(X) * 0.8)
    if split_index == 0 or split_index == len(X):
        logger.error("Not enough data to split into training and testing sets.")
        raise ValueError("Insufficient data for splitting.")

    X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
    Y_train, Y_test = Y.iloc[:split_index], Y.iloc[split_index:]

    # Handle class imbalance
    classes = np.unique(Y_train)
    class_weights = class_weight.compute_class_weight('balanced', classes=classes, y=Y_train)
    class_weights_dict = dict(zip(classes, class_weights))

   
    #rf = RandomForestClassifier(random_state=42, class_weight=class_weights_dict)
    rf = LinearDiscriminantAnalysis()
   
    # Fit the model
    rf.fit(X_train, Y_train)

    # Evaluate the model on the test set
    Y_pred = rf.predict(X_test)
    accuracy = accuracy_score(Y_test, Y_pred)
    report = classification_report(Y_test, Y_pred)
    logger.info("Classification Report:")
    logger.info(classification_report(Y_test, Y_pred))

    # Predict the next time point
    latest_data = X.iloc[-1].values.reshape(1, -1)
    # Convert latest_data to DataFrame to maintain feature names
    latest_data_df = pd.DataFrame(latest_data, columns=X.columns)
    today_prediction = rf.predict(latest_data_df)[0]

    return {
        'accuracy': accuracy,
        'classification_report': report,
        'today_prediction': int(today_prediction),
    }

def train_regression_models(dataframe,dwm):
    if dataframe.shape[0] < 50:
        logger.error("Not enough data to train the regression model.")
        return None

    # Ensure the dataframe is sorted by date
    dataframe = dataframe.sort_index()

    target_map = {1: 'Close_Tomorrow', 2:'Close_NextWeek', 3:  'Close_NextMonth'}
    target_col = target_map.get(dwm)
    print("target",target_col)
    if not target_col:
        return None
    sequence_len = {1: 5, 2: 7 , 3: 10}.get(dwm, 1)

    # Define feature columns
    target_vars = ['Close_Tomorrow', 'Close_NextWeek', 'Close_NextMonth','Tomorrow','Month','Week']
    feature_columns = [col for col in dataframe.columns if col not in target_vars]
    
    X = dataframe[feature_columns].values

    dataframe = dataframe.dropna(subset=[target_col])
    Y = dataframe[target_col].values


    scaler_X = MinMaxScaler(feature_range=(0, 1))
    scaler_Y = MinMaxScaler(feature_range=(0, 1))
    features_scaled = scaler_X.fit_transform(X)
    target_scaled = scaler_Y.fit_transform(Y.reshape(-1, 1))

    X_Sequence=[]
    Y_Sequence=[]
    for i in range(len(target_scaled)-sequence_len):
        X_Sequence.append(features_scaled[i:i +sequence_len])
        Y_Sequence.append(target_scaled[i + sequence_len-3])
    X_Sequence=np.array(X_Sequence)
    Y_Sequence=np.array(Y_Sequence)

    # Split data into training and testing sets
    split_index = int(len(X_Sequence) * 0.8)
    if split_index == 0 or split_index == len(X_Sequence):
        logger.error("Not enough data to split into training and testing sets.")
        return None

    X_train, X_test = X_Sequence[:split_index], X_Sequence[split_index:]
    Y_train, Y_test = Y_Sequence[:split_index], Y_Sequence[split_index:]

    
    model = Sequential([
        LSTM(64, activation='relu',  input_shape=(X_train.shape[1], X_train.shape[2])),
    # Output layer with 1 unit for regression
    Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')


    model.fit(X_train, Y_train, epochs=25, batch_size=32, verbose=1)
 



    # Evaluate the Model
    Y_pred = model.predict(X_test)
    predictions_rescaled = scaler_Y.inverse_transform(Y_pred)
    y_test_rescaled = scaler_Y.inverse_transform(Y_test.reshape(-1, 1))
    mse = mean_squared_error(y_test_rescaled, predictions_rescaled)
    mae=mean_absolute_error(y_test_rescaled, predictions_rescaled)
    r2=r2_score(y_test_rescaled, predictions_rescaled)

    # Predict Next Period
    latest_data = features_scaled[-sequence_len:]
    latest_data_df = np.expand_dims(latest_data,axis=0)
    next_prediction_scaled = model.predict(latest_data_df)
    next_prediction = scaler_Y.inverse_transform(next_prediction_scaled)[0][0]
    logger.info(f"Regression metrics for {next_prediction} - MSE: {mse}, MAE: {mae}, R2: {r2}")
    next_prediction=int(next_prediction*100)
    next_prediction=next_prediction/100
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
                
                regression_result = train_regression_models(dataframe, dwm)
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
                else:
                    print("if statment missed")

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


def get_stock_price_at_date(ticker, purchase_date=None):
    try:
        ticker_obj = yf.Ticker(ticker)

        if purchase_date:
            # Parse the purchase_date string to a timezone-aware datetime object
            if isinstance(purchase_date, str):
                purchase_datetime = datetime.fromisoformat(purchase_date)
            else:
                purchase_datetime = purchase_date

            if purchase_datetime.tzinfo is None:  # Ensure it is timezone-aware
                purchase_datetime = pytz.utc.localize(purchase_datetime)

            # Define the date range around the purchase date
            start_date = (purchase_datetime - timedelta(days=1)).strftime('%Y-%m-%d')
            end_date = (purchase_datetime + timedelta(days=1)).strftime('%Y-%m-%d')

            # Fetch historical data for the specific date range
            data = ticker_obj.history(start=start_date, end=end_date)
            if data.empty:
                logger.error(f"No data found for {ticker} around {purchase_date}")
                return None

            # Find the closest date to the purchase_date
            data['Datetime'] = data.index
            data['Datetime'] = data['Datetime'].apply(lambda x: x.tz_localize('UTC') if x.tzinfo is None else x)
            data['Time_Diff'] = abs(data['Datetime'] - purchase_datetime)
            closest_row = data.loc[data['Time_Diff'].idxmin()]
            price = closest_row['Close']
            return price
        else:
            # If no purchase_date is provided, get the current stock price
            return get_current_stock_price(ticker)
    except Exception as e:
        logger.error(f"Error getting stock price for {ticker} at date {purchase_date}: {e}")
        return None


def get_stock_results_data(ticker):
    try:
        # Create the ticker object
        ticker_obj = yf.Ticker(ticker)
        # Get stock information
        stock_info = ticker_obj.info
        print(stock_info)

        # Extract at least 30 relevant data points
        stock_results_data = {
            "close": stock_info.get("close"),
            "ticker": stock_info.get("symbol"),
            "name": stock_info.get("shortName"),
            "long_name": stock_info.get("longName"),
            "sector": stock_info.get("sector"),
            "industry": stock_info.get("industry"),
            "market_cap": stock_info.get("marketCap"),
            "enterprise_value": stock_info.get("enterpriseValue"),
            "price": stock_info.get("currentPrice"),
            "previous_close": stock_info.get("previousClose"),
            "open": stock_info.get("open"),
            "day_low": stock_info.get("dayLow"),
            "day_high": stock_info.get("dayHigh"),
            "fifty_two_week_low": stock_info.get("fiftyTwoWeekLow"),
            "fifty_two_week_high": stock_info.get("fiftyTwoWeekHigh"),
            "fifty_day_average": stock_info.get("fiftyDayAverage"),
            "two_hundred_day_average": stock_info.get("twoHundredDayAverage"),
            "volume": stock_info.get("volume"),
            "average_volume": stock_info.get("averageVolume"),
            "regular_market_volume": stock_info.get("regularMarketVolume"),
            "regular_market_price": stock_info.get("regularMarketPrice"),
            "dividend_yield": stock_info.get("dividendYield"),
            "trailing_pe": stock_info.get("trailingPE"),
            "forward_pe": stock_info.get("forwardPE"),
            "beta": stock_info.get("beta"),
            "total_cash": stock_info.get("totalCash"),
            "total_debt": stock_info.get("totalDebt"),
            "revenue": stock_info.get("totalRevenue"),
            "revenue_per_share": stock_info.get("revenuePerShare"),
            "gross_profit": stock_info.get("grossProfits"),
            "ebitda": stock_info.get("ebitda"),
            "operating_cashflow": stock_info.get("operatingCashflow"),
            "free_cashflow": stock_info.get("freeCashflow"),
            "profit_margins": stock_info.get("profitMargins"),
            "return_on_assets": stock_info.get("returnOnAssets"),
            "return_on_equity": stock_info.get("returnOnEquity"),
            "earnings_quarterly_growth": stock_info.get("earningsQuarterlyGrowth"),
            "earnings_growth": stock_info.get("earningsGrowth"),
            "revenue_growth": stock_info.get("revenueGrowth"),
            "operating_margins": stock_info.get("operatingMargins"),
            "ebitda_margins": stock_info.get("ebitdaMargins"),
            "gross_margins": stock_info.get("grossMargins"),
            "book_value": stock_info.get("bookValue"),
            "price_to_book": stock_info.get("priceToBook"),
            "cash_per_share": stock_info.get("totalCashPerShare"),
            "debt_to_equity": stock_info.get("debtToEquity"),
            "held_percent_institutions": stock_info.get("heldPercentInstitutions"),
            "held_percent_insiders": stock_info.get("heldPercentInsiders"),
            "short_ratio": stock_info.get("shortRatio"),
            "shares_outstanding": stock_info.get("sharesOutstanding"),
            "float_shares": stock_info.get("floatShares"),
            "implied_shares_outstanding": stock_info.get("impliedSharesOutstanding"),
            "shares_short": stock_info.get("sharesShort"),
            "shares_short_prior_month": stock_info.get("sharesShortPriorMonth"),
            "short_percent_of_float": stock_info.get("shortPercentOfFloat"),
            "date_short_interest": stock_info.get("dateShortInterest"),
            "last_split_date": stock_info.get("lastSplitDate"),
            "last_split_factor": stock_info.get("lastSplitFactor"),
            "address": f"{stock_info.get('address1')}, {stock_info.get('city')}, {stock_info.get('state')} {stock_info.get('zip')}, {stock_info.get('country')}",
            "website": stock_info.get("website"),
            "full_time_employees": stock_info.get("fullTimeEmployees"),
            "company_officers": stock_info.get("companyOfficers"),
            "recommendation_key": stock_info.get("recommendationKey"),
            "recommendation_mean": stock_info.get("recommendationMean"),
            "number_of_analyst_opinions": stock_info.get("numberOfAnalystOpinions"),
            "target_high_price": stock_info.get("targetHighPrice"),
            "target_low_price": stock_info.get("targetLowPrice"),
            "target_mean_price": stock_info.get("targetMeanPrice"),
            "target_median_price": stock_info.get("targetMedianPrice"),
            "exchange": stock_info.get("exchange"),
            "quote_type": stock_info.get("quoteType"),
            "currency": stock_info.get("currency"),
            "financial_currency": stock_info.get("financialCurrency"),
            "earnings_date": stock_info.get("earningsDate"),
            "most_recent_quarter": stock_info.get("mostRecentQuarter"),
            "last_fiscal_year_end": stock_info.get("lastFiscalYearEnd"),
            "next_fiscal_year_end": stock_info.get("nextFiscalYearEnd"),
            "long_business_summary": stock_info.get("longBusinessSummary"),
        }

        return stock_results_data
    except Exception as e:
        current_app.logger.error(f"Error getting stock data for {ticker}: {e}")
        return None


def get_crypto_data(crypto_id):
    """
    Fetches data for a specific cryptocurrency using the CoinGecko API.
    """
    try:
        # CoinGecko API base URL
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"

        # Make the API request
        response = requests.get(url)
        if response.status_code != 200:
            current_app.logger.error(f"Failed to fetch data for crypto id: {crypto_id}")
            return None

        data = response.json()
        print(data)
        # Extract relevant fields
        crypto_data = {
            "id": crypto_id,
            "ticker": data.get("symbol", "").upper() if data.get("symbol") else "N/A",
            "name": data.get("name", "N/A"),
            "price": data.get("market_data", {}).get("current_price", {}).get("usd"),
            "market_cap": data.get("market_data", {}).get("market_cap", {}).get("usd"),
            "percentage_change_24h": data.get("market_data", {}).get("price_change_percentage_24h"),
            "volume": data.get("market_data", {}).get("total_volume", {}).get("usd"),
            "rank": data.get("market_cap_rank"),
            "symbol": data.get("symbol")
        }

        # Ensure all required fields are present
        if crypto_data["price"] is None:
            raise ValueError("Missing required cryptocurrency data.")

        return crypto_data

    except Exception as e:
        current_app.logger.error(f"Error fetching crypto data for {crypto_id}: {e}")
        return None