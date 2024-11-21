import yfinance as yf
import numpy as np
import pandas as pd 
from datetime import datetime, timedelta
import plotly.graph_objs as go




#def meanVariance(portfolio):
#    import numpy as np
#
def mean_variance_optimization(portfolioDF):

    weights = np.array(list(weights.values()))
    returns = portfolioDF['Weighted_Sum'].pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    print 



    expected_return = np.dot(weights, mean_returns)
    risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    return {"expected_return": expected_return, "risk": risk, "covariance_matrix": cov_matrix}

def sharpeRatio(portfolio):

    metrics = mean_variance_optimization(prices, weights)
    excess_return = metrics["expected_return"] - (.02/265)
    sharpe = excess_return / metrics["risk"]
    return sharpe



import matplotlib.pyplot as plt

def monte_carlo_simulation(prices, weights, num_simulations=1000):
   
    returns = prices.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    weights = np.array(list(weights.values()))
    
    simulated_returns = []
    for _ in range(num_simulations):
        random_weights = np.random.dirichlet(np.ones(len(weights)), size=1)
        sim_return = np.dot(random_weights, mean_returns)
        simulated_returns.append(sim_return)
    
    plt.hist(simulated_returns, bins=50, alpha=0.7)
    plt.title("Monte Carlo Simulation of Portfolio Returns")
    plt.xlabel("Portfolio Return")
    plt.ylabel("Frequency")
    plt.show()
    
    return simulated_returns









def portfolioAnalysis(portfolio):
    # Define time period (last 5 years)
    end_date = datetime.now()
    start_date = end_date.replace(year=end_date.year - 5)
    
    # Download price data
    tickers = list(portfolio.keys())
    weights = list(portfolio.values())
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close'] # gets all tickers adj close in the dataframe
    
    data['Weighted_Sum'] = data.dot(weights)

    print(data)




portfolioAnalysis({"AAPL": .2,"NIO":.8})

    
