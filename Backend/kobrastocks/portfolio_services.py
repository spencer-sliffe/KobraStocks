"""
------------------Prologue--------------------
File Name: portfolio_services.py
Path: Backend/kobrastocks/portfolio_services.py

Description:
Implements core services for data retrievel and portfolio analysis


Input:
Portfolio Object

Output:
Serialized stock data, predictions, charts, and contact form confirmation.

Collaborators: Charlie Gillund, Chatgpt(For Debugging and ChatGPT api assistance )
Date 11/18/24
---------------------------------------------
"""

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from flask import current_app
import openai

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import logging

from . import db
from .models import PortfolioStock, Portfolio
from .utils import *





##Portfolio Analysis takes in a kek pair {stock: weight} portfolio and returns the desired portfolio prompts and metrics 
def portfolioAnalysis(portfolio):
    end_date = datetime.now() # gets date
    start_date = end_date.replace(year=end_date.year - 5) # sets how far back we going
    tickers = list(portfolio.keys()) # gets tickerrs
    weights = list(portfolio.values()) # gets weights 
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close'] # gets adj close stock returns over the desired periods 
    expR,risk,cov=mean_variance_optimization(data,weights) # calls first function to get expected value, risk and cov matrix
    sharpe=sharpeRatio(data,weights) # gets sharpe ratio
    corr,div=correlateAndDiversification(data,weights) # gets correlation matrix and diversification ratio 
    p1,p2,p3=makePrompt(tickers,weights,sharpe,div,expR,risk) # makes the prompts 
    r1,r2,r3=ChatAnalysis(p1,p2,p3) # returns the chat gpt prompts for the portfolio
    return r1,r2,r3,expR,risk # returns prompts and metrics




def mean_variance_optimization(portfolioDF,weights):

    weights = np.array(weights) # Turns weights into an array
    returns = portfolioDF.pct_change().dropna() # gets the pct change of the portfolio
    mean_returns = returns.mean() # gets average return over time period 
    cov_matrix = returns.cov() # gets covariance matrix

   
    expected_return = np.dot(weights, mean_returns)*252 #gets average annualized returns over the period 
    risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))*np.sqrt(252) # gets annualized risk over the desired period 
    return expected_return, risk, cov_matrix # returns metrics 


def sharpeRatio(portfolioDF,weights):

    expR,risk, = mean_variance_optimization(portfolioDF,weights) # gets risk and exp value 

    excess_return = expR - (.02) # gets return over RFR

    sharpe = excess_return / risk # calculates sharpe ratio
    
    return sharpe # returns Sharpe Ratio

def correlateAndDiversification(portfolioDF,weights):

    weights = np.array(weights) # turns weights into array

    returns = portfolioDF.pct_change().dropna() # gets pct change retruns 
    
    correlation_matrix = returns.corr() # gets correlation matrix
    
    volatilities = returns.std() # gets standard deviation/ volatility
    
    cov_matrix = returns.cov() # gets cov matrix
    
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) # calculates portfolio volatility
    
    weighted_volatilities = np.dot(weights, volatilities)#weights portfolio volatility

    diversification_ratio = weighted_volatilities / portfolio_volatility # gets diversification ratio
    
    return correlation_matrix, diversification_ratio # returns diversification ratio

#This Function Just takes in the metrics and forms strings usign the provided metrics 
def makePrompt(tickers,weights,sharpe,diverse_ratio,expectedReturn,risk):
    prompt1=(f"The portfolio you are analyzing is all stock with the respective tickers {tickers} with the respective weights {weights} which is the percentage of the portfolio invested in each Ticker, This Portfolio has a sharpe ratio of {sharpe:.2}, the diversifaction ratio of {diverse_ratio:.2},the annual expected return is{expectedReturn:.2} and the annualized risk is {risk:.2}. What are your thoughts on this portfolio?")
    prompt2=(f"How would you Rate this all stocm portfolio out of (A-F) Based off of the average performance of all stock portfolios Please provide the rating as the first token")
    prompt3=(f"What Stocks would you suggest to add or Remove from this portfolio Make sure not to add stocks that are already in the portfolio")
    return prompt1,prompt2,prompt3 # returns prompts 


def ChatAnalysis(p1,p2,p3):
    openai.api_key="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" # APIKEY

    response1 = openai.ChatCompletion.create(  # Creates Prompt Object
    model="gpt-3.5-turbo", # selects Model
    messages=[
        {"role": "system", "content": "You are a financal advisor giving suggestions on a stock only portfolio Please make prompt 200 or less words "}, # Context Promt
        {"role": "user", "content": p1} # Gives Actual Prompt 
    ],
    max_tokens=200, # Sets Max Amount of Tokens Returned 
    temperature=.5 # sets Randomness of chat generation
    )

    ##Same as Chat response 1
    response2 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": p1+ response1["choices"][0]["message"]["content"]},
        {"role": "user", "content": p2}
    ],
    max_tokens=1,
    temperature=.8
    )
    #Same as Chat Response 1 &2
    response3 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": p1 + response1["choices"][0]["message"]["content"]+"Please make prompt short and to the point "},
        {"role": "user", "content": p3}
    ],
    max_tokens=200,
    temperature=0.5
    )
    return response1["choices"][0]["message"]["content"],response2["choices"][0]["message"]["content"],response3["choices"][0]["message"]["content"] # returns prompt 
