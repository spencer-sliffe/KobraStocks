
import yfinance as yf
import pandas as pd
import matplotlib as plt
import datetime as datetime, timedelta



def makeChart(dataframe):
    pass





def MA50(dataframe):
   dataframe['MA5']=dataframe['Close'].rolling(window=50).mean()
def MA9(dataframe):
   dataframe['MA5']=dataframe['Close'].rolling(window=50).mean()
   
def MACD(dataframe):
    dataframe['EMA12'] = dataframe['Close'].ewm(span=12, adjust=False).mean()
    dataframe['EMA26'] = dataframe['Close'].ewm(span=26, adjust=False).mean()

    dataframe['MACD'] = dataframe['EMA12'] - dataframe['EMA26']
    dataframe['Signal_Line'] = dataframe['MACD'].ewm(span=9, adjust=False).mean()
   
def main(ticker,period):

   time =datetime.now()
    year=int(time.year)
    yesterday = time - timedelta(days=1)
    startyear=year-5
    startStr=(str(startyear)+'-1-1')
    print(startStr)
    print(yesterday.strftime("%Y-%m-%d"))
    priceData= yf.Ticker(ticker)
    