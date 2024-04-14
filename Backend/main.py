
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from  sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
import numpy as np
import plotly.graph_objects as go 
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.subplots import make_subplots




def addRSI(dataframe):

   dataframe['Price Diff'] = dataframe['Close'].diff()
   #shows gain and loss of prices 
   dataframe['Gain'] = np.where(dataframe['Price Diff'] > 0, dataframe['Price Diff'], 0)
   dataframe['Loss'] = np.where(dataframe['Price Diff'] < 0, -dataframe['Price Diff'], 0)

   window_length = 14
   
   #calculates moving average upon the gains and losses seperately
   dataframe['Avg Gain'] = dataframe['Gain'].ewm(alpha=1/window_length, min_periods=window_length).mean()
   dataframe['Avg Loss'] = dataframe['Loss'].ewm(alpha=1/window_length, min_periods=window_length).mean()
   #calculates strength
   dataframe['RS'] = dataframe['Avg Gain'] / dataframe['Avg Loss']
   dataframe['RSI'] = 100 - (100 / (1 + dataframe['RS']))
   dataframe.drop(['Price Diff', 'Gain', 'Loss', 'Avg Gain', 'Avg Loss', 'RS'], axis=1, inplace=True)
   return dataframe




def addMA50(dataframe):
   dataframe['MA50']=dataframe['Close'].rolling(window=50).mean()
   return dataframe

def addMA9(dataframe):
   dataframe['MA9']=dataframe['Close'].rolling(window=9).mean()
   return dataframe
   
def addMACD(dataframe):
    dataframe['EMA12'] = dataframe['Close'].ewm(span=12, adjust=False).mean()
    dataframe['EMA26'] = dataframe['Close'].ewm(span=26, adjust=False).mean()

    dataframe['MACD'] = dataframe['EMA12'] - dataframe['EMA26']
    dataframe['Signal_Line'] = dataframe['MACD'].ewm(span=9, adjust=False).mean()
    dataframe=dataframe.drop(['EMA12','EMA26'],axis=1)
    return dataframe
    


def retrieveData(ticker,period):
   time =datetime.now()
   year=int(time.year)
   yesterday = time - timedelta(days=1)
   startyear=year-5
   startStr=(str(startyear)+'-1-1')
   ticker= yf.Ticker(ticker)
   dataframe=ticker.history(period='1d',start=startStr,end=yesterday)
   dataframe=dataframe.drop(['Dividends','Stock Splits'],axis=1)
   dataframe['Tomorrow'] =dataframe['Close']<dataframe['Close'].shift(-1)
   dataframe['Week'] =dataframe['Close']<dataframe['Close'].shift(-5)
   dataframe['Month'] =dataframe['Close']<dataframe['Close'].shift(-30)
   return dataframe
   

def addIndicators(dataframe,MA9,MA50,MACD,RSI):
   if(MACD):
      dataframe=addMACD(dataframe)
   if(MA9):
      dataframe=addMA9(dataframe)
   if(RSI):
      dataframe=addRSI(dataframe)
   if(MA50):
      dataframe=addMA50(dataframe)
   return dataframe


def makeChart(dataframe,MA9,MA50):
   try:
      # Ensure 'Date' is a datetime type and set as index if not already
      chartData=dataframe
      chartData['Date'] = chartData.index
      chartData['Date'] = pd.to_datetime(chartData['Date'])
      

      # Create moving averages
      if MA9:
        chartData['MA9'] = chartData['Close'].rolling(window=9).mean()
      if MA50 :
        chartData['MA50'] = chartData['Close'].rolling(window=50).mean()
      # Create a candlestick chart
      fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, subplot_titles=('', ''), 
                        row_width=[0.2, 0.7])
      
      fig.add_trace(
            go.Candlestick(x=dataframe.index,
                           open=dataframe['Open'],
                           high=dataframe['High'],
                           low=dataframe['Low'],
                           close=dataframe['Close'],
                           increasing_line_color='green',
                           decreasing_line_color='red',
                           name="Candlestick"),
            row=1, col=1)
      # Add MA9 and MA50 to the chart
      if MA9:
         fig.add_trace(go.Scatter(x=chartData['Date'], y =chartData['MA9'], mode='lines', line=dict(color='blue', width=1.5), name='MA9'), row=1, col=1)
      if MA50:
         fig.add_trace(go.Scatter(x=chartData['Date'], y=chartData['MA50'], mode='lines', line=dict(color='purple', width=1.5), name='MA50'), row=1, col=1)
      # Add volume as a bar chart
      fig.add_trace(go.Bar(x=chartData.index, y=chartData['Volume'], name='Volume', marker_color='blue'), row=2, col=1)
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
          ),
          yaxis2=dict(
              title='Volume',
              domain=[0, 0.2],  # Volume bars space
              side='right',
              showticklabels=False
          )
      )
      # Update axis 
      fig.update_xaxes(title_font=dict(color='#00FF00'),tickfont=dict(color='#00FF00'))
      fig.update_yaxes(title_font=dict(color='#00FF00'),tickfont=dict(color='#00FF00'))
      return fig
   except Exception as e:
      print(f"An error occurred: {e}")
      return None 

def trainModels(dataframe,dwm):
   #dwm 1=day 2=week 3=week   
   X = dataframe.drop(['Month', 'Week', 'Tomorrow', 'High', 'Low', 'Open'], axis=1)
   if dwm==1:
      Y = dataframe['Tomorrow'].astype(int)
   elif dwm==2:
      Y = dataframe['Week'].astype(int)
   else:
      Y = dataframe['Month'].astype(int)


   X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

   param_grid = {
          'n_estimators': [100, 200, 300],
          'min_samples_split': [2, 5],
          'bootstrap': [True, False],
          'max_depth': [None, 10, 20],
          'min_samples_leaf': [1, 2],
      }
   rf = RandomForestClassifier(random_state=42)
   grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2, scoring='accuracy')
   grid_search.fit(X_train, Y_train)
   best_grid = grid_search.best_estimator_
   predictions = best_grid.predict(X_test)
   rfAcc = accuracy_score(Y_test, predictions)

   todayData = dataframe.tail(1).drop(['Month', 'Week', 'Tomorrow', 'High', 'Low', 'Open'], axis=1)
   todayPrediction = best_grid.predict(todayData)[0]
   
   return rfAcc,todayPrediction
     
     
     
     
     
      #ADD LATER
      #param_grid = {
      #    'C': [0.1, 1, 10],
      ##
      #    'kernel': ['rbf', 'poly', 'sigmoid']
      ##
      ##svm = SVC()
      #    'gamma': [1, 0.1, 0.01],
      ##grid_search.fit(X_train, Y_train)
      #}
      ##print("SVM MONTH Improved Accuracy:", accuracy_score(Y_test, predictions))
      #grid_search = GridSearchCV(svm, param_grid, cv=3, verbose=2, n_jobs=-1)
      ##
      #predictions = best_grid.predict(X_test)
      ##print(classification_report(Y_test, predictions))#


   

      







