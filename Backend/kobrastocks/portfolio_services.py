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
import numpy as np
import pandas as pd
from datetime import datetime
import logging
from .utils import (
    mean_variance_optimization,
    calculate_sharpe_ratio,
    calculate_diversification_ratio,
    generate_chat_prompts,
    get_chat_analysis
)


def portfolio_analysis(portfolio):
    try:
        end_date = datetime.now()
        start_date = end_date.replace(year=end_date.year - 5)
        tickers = list(portfolio.keys())
        weights = np.array(list(portfolio.values()), dtype=float)

        # Normalize weights
        total_weight = np.sum(weights)
        if total_weight == 0:
            logging.error("Total weight of portfolio is zero.")
            return None
        weights = weights / total_weight

        # Fetch adjusted closing prices for the tickers
        data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
        if data.empty:
            logging.error("No data fetched for the given tickers.")
            return None

        # Handle the case where data is a Series (single stock)
        if isinstance(data, pd.Series):
            data = data.to_frame()
            data.columns = [tickers[0]]

        # Drop rows with missing values
        data = data.dropna()

        # Calculate portfolio metrics
        expected_return, risk, cov_matrix = mean_variance_optimization(data, weights)
        sharpe_ratio = calculate_sharpe_ratio(expected_return, risk)
        diversification_ratio = calculate_diversification_ratio(data, weights)

        # Generate prompts and get analysis from OpenAI
        prompts = generate_chat_prompts(
            tickers, weights, sharpe_ratio, diversification_ratio, expected_return, risk
        )
        chat_responses = get_chat_analysis(prompts)

        return {
            'analysis': {
                'chat_responses': chat_responses
            },
            'metrics': {
                'expected_return': expected_return,
                'risk': risk,
                'sharpe_ratio': sharpe_ratio,
                'diversification_ratio': diversification_ratio
            }
        }
    except Exception as e:
        logging.error(f"Error in portfolio_analysis: {e}")
        return None
