import yfinance as yf 
import pandas as pd 
import numpy as np

import plotly.graph_objects as go 
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots


from  sklearn.ensemble import RandomForestClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,GRU, Dense, Dropout

from indicators import *


##This File contains a stock obj and performs functions such as collecting data graphing and training the models 

class Stock():
    # Defines Stock Object
    def __init__(self,ticker,interval="1d",start="2020-01-01"):
        data=yf.download(ticker,interval=interval,start=start) # Gets stock data+9+
        self.basic_data=data[["Open","High","Low","Close","Volume"]].copy() # Makes
        self.basic_data.index.name='Datetime' #Makes data index
        self.training_data=data[["Close","Volume"]].copy()
        
       


    #Add Indicators 
        #SMA and EMA are lists of the MA windows that will be added to the Training set
        #all other indicators are set windows so the param tell if they are added or not 0 or 1
        
    def add_Indicators(self,SMA,EMA,RSI,MACD,ATR,BBands,VWAP):
        for num in SMA:
            add_SMA(self.training_data,num)
        for num in EMA:
           add_EMA(self.training_data,num)
        if RSI:
            add_RSI(self.training_data) # ADDS INDICATOR
        if MACD:
            add_MACD(self.training_data) 
        if ATR:
            add_ATR(self.training_data) 
        if BBands:
            add_BollingerBands(self.training_data) 
        if VWAP:
            add_VWAP(self.training_data) 


    # Adds pct_change of the indices
    def add_indexes(self,indicies,interval="1d",start="2020-01-01"):
        indexes={
            "S&P":"^GSPC",
            "VIX":"^VIX",
            "DOW":"^DJI",
            "NASDAQ":"^IXIC",
            "RUSSELL":"^RUT"
        } # Dictionary full of indice names and their tickers
        for index in indicies: # goes through indices
            ticker=index[index] # gets indice
            data=yf.download(ticker,interval=interval,start=start) # retrives indices data
            self.training_data[index]=data["Close"].pct_chage() # Gets pct change of indices everyday


    def train_classification_model(self,model_type=0,prediction_date=1): # This is the First two AI models 
        self.training_data = self.training_data.dropna()
        result=self.training_data['Close']<self.training_data['Close'].shift(-prediction_date)# gets result
        fold1_x,fold2_x,fold1_y,fold2_y = train_test_split(self.training_data, result, test_size=0.5, random_state=42, shuffle=False) # splits Training data
       # Remove rows with NaN values from the training dataset
        
    
        if model_type:
            model=RandomForestClassifier(random_state=1) # gets Random Forest  
        else:
            model = LinearDiscriminantAnalysis() # model object LDA
        
        model.fit(fold1_x, fold1_y) # fold  1 training
        predictions1 = model.predict(fold2_x) #testing uing fold 2
        model.fit(fold2_x, fold2_y) #fold 2 training
        predictions2 = model.predict(fold1_x) #testing using fold 1
             


        actual = np.concatenate([fold2_y, fold1_y]) #merged actual results 
        predicted = np.concatenate([predictions1, predictions2]) #merged predicted results
        accuracy=accuracy_score(actual, predicted) #gets accuracy

        return model,accuracy
    
    #def train_regression_model(self,model_type=0,prediction_date=5): # These are teh other Two AI models 
    #    self.training_data = self.training_data.dropna()
    #    result=self.training_data['Close'].shift(-prediction_date)# gets result
    #    result = result.dropna()
    #    fold1_x,fold2_x,fold1_y,fold2_y = train_test_split(self.training_data, result, test_size=0.2, random_state=42, shuffle=False) # splits Training data for sequential testing .8 train .2 tests
    #    
    #    if model_type:
    #        model = Sequential() #Initializes Model Object
    #        model.add(LSTM(units=50, return_sequences=True, input_shape=(fold1_x.shape[1], 1))) # sets inital layer
    #        model.add(Dropout(0.2))# sets Dropout
    #        model.add(LSTM(units=50, return_sequences=False))# sets next Layer
    #        model.add(Dropout(0.2))# sets Dropout
    #        model.add(Dense(units=1)) # adds dense layer
    #        
    #         
    #    else:
    #        model = Sequential() # initializes Model Object 
    #        model.add(GRU(units=50, return_sequences=True, input_shape=(fold1_x.shape[1], 1))) # sets up inital layer
    #        model.add(Dropout(0.2))# sets Dropout
    #        model.add(GRU(units=50, return_sequences=False)) # Sets next Layer
    #        model.add(Dropout(0.2)) # sets Dropout
    #        model.add(Dense(units=1)) # adds dense layer
    #    
    #    model.compile(optimizer='adam', loss='mean_squared_error') # compiles 
    #    model.fit(fold1_x, fold1_y, epochs=20, batch_size=32, validation_data=(fold2_x,fold2_y))
    #    actual = fold2_y #actual results 
    #    predicted = model.predict(fold2_x) #predicted results
    #    accuracy=accuracy_score(actual, predicted) #gets accuracy

    #    return model,accuracy
     
    def get_Basic_Graph(self):
        try:
              # Ensure 'Date' is a datetime type and set as index if not already
            chartData=self.basic_data
            chartData['Date'] = chartData.index
            chartData['Date'] = pd.to_datetime(chartData['Date']) # Make the chart have datetime 

            # Create a candlestick chart
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                              vertical_spacing=0.03, subplot_titles=('', ''), 
                              row_width=[0.2, 0.7]) # Splits the chart so we can have both price and volume on the smae chart 

            fig.add_trace(
                  go.Candlestick(x=self.basic_data.index,
                                 open=self.basic_data['Open'],
                                 high=self.basic_data['High'],
                                 low=self.basic_data['Low'],
                                 close=self.basic_data['Close'],
                                 increasing_line_color='green',
                                 decreasing_line_color='red',
                                 name="Candlestick"),
                                  row=1, col=1)   #This makes candlestick chart 

            fig.add_trace(go.Bar(x=chartData.index, y=chartData['Volume'], name='Volume', marker_color='blue'), row=2, col=1)# Add volume as a bar chart
            # Update layout for aesthetics
            fig.update_layout(
                title='',
                xaxis_title='',
                yaxis_title='',
                xaxis_rangeslider_visible=False,
                paper_bgcolor='black',
                yaxis=dict(
                    title='Price',
                    domain=[0.2, 1]  # Adjust y-axis to make space for volume bars
                ), # sets up Price Appearence 
                yaxis2=dict(
                    title='Volume',
                    domain=[0, 0.2],  # Volume bars space
                    side='right',
                    showticklabels=False
                )  # Sets up Volume Appearance
              )
              # Update axis 
            fig.update_xaxes(title_font=dict(color='#00FF00'),tickfont=dict(color='#00FF00')) # Changes text appearence
            fig.update_yaxes(title_font=dict(color='#00FF00'),tickfont=dict(color='#00FF00'))# Changes text appearence
            return fig 
        except Exception as e:
            print(f"An error occurred: {e}")
            return None 



    
    

aapl=Stock("AAPL")
aapl.add_Indicators([5,20],[],0,0,0,0,0)
model,accuracy=aapl.train_classification_model()
print ("accuracy: ", accuracy)


    




