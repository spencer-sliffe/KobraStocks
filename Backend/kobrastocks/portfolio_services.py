import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from flask import current_app

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

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
    print("Correlation Matrix:")
    print(correlation_matrix)
    
    volatilities = returns.std()
    
    cov_matrix = returns.cov()
    
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    weighted_volatilities = np.dot(weights, volatilities)
    diversification_ratio = weighted_volatilities / portfolio_volatility
    
    print(f"\nDiversification Ratio: {diversification_ratio:.2f}")
    
    return correlation_matrix, diversification_ratio
