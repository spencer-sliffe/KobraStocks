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






def portfolioAnalysis(portfolio):
    end_date = datetime.now()
    start_date = end_date.replace(year=end_date.year - 5)
    
   
    tickers = list(portfolio.keys())
    weights = list(portfolio.values())
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    sharpeRatio(data,weights)
   # monte_carlo_simulation(data,weights,100)
    correlateAndDiversification(data,weights)
    

def mean_variance_optimization(portfolioDF,weights):

    weights = np.array(weights)
    returns = portfolioDF.pct_change().dropna()
    print(returns)
    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    #cumulative_returns = (1 + returns).cumprod() - 1
#
    #print(cumulative_returns)
    expected_return = np.dot(weights, mean_returns)*252
    risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))*np.sqrt(252)
    print("expected_return: ", expected_return, " risk", risk, " covariance_matrix", cov_matrix)
    return {"expected_return": expected_return, "risk": risk, "covariance_matrix": cov_matrix}


def sharpeRatio(portfolioDF,weights):

    metrics = mean_variance_optimization(portfolioDF,weights)
    excess_return = metrics["expected_return"] - (.02/252)
    sharpe = excess_return / metrics["risk"]
    print("Sharpe: ",sharpe)
    return sharpe

def correlateAndDiversification(portfolioDF,weights):
    weights = np.array(weights)
    returns = portfolioDF.pct_change().dropna()
    
    correlation_matrix = returns.corr()
    
   
    
    volatilities = returns.std()
    
    cov_matrix = returns.cov()
    
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    weighted_volatilities = np.dot(weights, volatilities)
    diversification_ratio = weighted_volatilities / portfolio_volatility
    
    print(f"\nDiversification Ratio: {diversification_ratio:.2f}")
    
    return correlation_matrix, diversification_ratio


def makePrompt(tickers,weights,sharpe,diverse_ratio,expectedReturn,risk):
    prompt1=(f"The portfolio you are analyzing is all stock with the respective tickers {tickers} with the respective weights {weights} which is the percentage of the portfolio invested in each Ticker, This Portfolio has a sharpe ratio of {sharpe:.2}, the diversifaction ratio of {diverse_ratio:.2},the annual expected return is{expectedReturn:.2} and the annualized risk is {risk:.2}. What are your thoughts on this portfolio?")
    prompt2=(f"How would you Rate this all stocm portfolio out of (A-F) Based off of the average performance of all stock portfolios Please provide the rating as the first token")
    prompt3=(f"What Stocks would you suggest to add or Remove from this portfolio Make sure not to add stocks that are already in the portfolio")
    return prompt1,prompt2,prompt3


def ChatAnalysis(p1,p2,p3):
    openai.api_key="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"


    response1 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a financal advisor giving suggestions on a stock only portfolio Please make prompt 200 or less words "},
        {"role": "user", "content": p1}
    ],
    max_tokens=200,
    temperature=.5
    )
    response2 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": p1+ response1["choices"][0]["message"]["content"]},
        {"role": "user", "content": p2}
    ],
    max_tokens=1,
    temperature=.8
    )
    response3 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": p1 + response1["choices"][0]["message"]["content"]+"Please make prompt short and to the point "},
        {"role": "user", "content": p3}
    ],
    max_tokens=200,
    temperature=0.5
    )
    print(response1["choices"][0]["message"]["content"])
    print(response2["choices"][0]["message"]["content"])
    print(response3["choices"][0]["message"]["content"])


    return response1["choices"][0]["message"]["content"],response2["choices"][0]["message"]["content"],response3["choices"][0]["message"]["content"]
