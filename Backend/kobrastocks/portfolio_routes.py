"""
------------------Prologue--------------------
File Name: portfolio_routes.py
Path: Backend/kobrastocks/portfolio_routes.py

Description:
Defines routes for managing the user's portfolio. Includes endpoints for:
- Retrieving the user's portfolio.
- Adding a stock to the portfolio.
- Removing a stock from the portfolio.
- Getting recommendations for the portfolio based on owned stocks.

Input:
JSON data for stock tickers and amounts, JWT tokens for authentication.

Output:
JSON responses with portfolio data, status messages, and recommendations.

Collaborators: Spencer Sliffe
---------------------------------------------
"""
from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import Portfolio
from .portfolio_services import portfolio_analysis, get_portfolio, add_stock_to_portfolio, remove_stock_from_portfolio
from .serializers import (
    portfolio_schema,
    portfolio_recommendations_schema
)
from .utils import check_stock_validity

portfolio = Blueprint('portfolio', __name__, url_prefix='/api/portfolio')


@portfolio.route('', methods=['GET']) # Route to retrieve portfolio
@jwt_required()
def get_user_portfolio():
    user_id = get_jwt_identity() # Gets USER
    portfolio_data = get_portfolio(user_id) # gets user portfolio
    return jsonify(portfolio_schema.dump({'stocks': portfolio_data})), 200 # returns user Portfolio


@portfolio.route('', methods=['POST']) # portfolio post route
@jwt_required()
def add_stock():
    user_id = get_jwt_identity() # gets user
    data = request.get_json()
    ticker = data.get('ticker') # gets ticket
    num_shares = data.get('num_shares') # gets the number of shares
    purchase_date = data.get('purchase_date')  # ISO format expected (e.g., '2024-12-03T14:44')

    if not ticker or num_shares is None:
        return jsonify({'message': 'Ticker and num_shares are required.'}), 400 # error message

    valid = check_stock_validity(ticker)

    if not valid:
        return jsonify({'message': 'Invalid stock ticker'}), 400

    # Ensure purchase_date is in correct format
    if purchase_date:
        try:
            purchase_date = datetime.fromisoformat(purchase_date) # formats purchase date
        except ValueError:
            return jsonify({'message': 'Invalid purchase_date format. Use ISO 8601 format.'}), 400 # error message

    success = add_stock_to_portfolio(user_id, ticker, num_shares, purchase_date)
    if success:
        return jsonify({'message': f'{ticker} added to portfolio.'}), 200 # success message
    else:
        return jsonify({'message': 'Failed to add stock to portfolio.'}), 500 # error message


@portfolio.route('/<string:ticker>', methods=['DELETE']) # route to delete stok
@jwt_required()
def remove_stock(ticker):
    user_id = get_jwt_identity() # gets User
    success = remove_stock_from_portfolio(user_id, ticker) # removes stock from portfolio 
    if success:
        return jsonify({'message': f'{ticker} removed from portfolio.'}), 200 # success message
    else:
        return jsonify({'message': 'Failed to remove stock from portfolio.'}), 500 # removal Error message


@portfolio.route('/analysis', methods=['GET'])
@jwt_required()
def get_portfolio_analysis():
    user_id = get_jwt_identity()
    # Fetch user's portfolio from the database
    user_portfolio = Portfolio.query.filter_by(user_id=user_id).first() # gets user portfolio
    if not user_portfolio or not user_portfolio.stocks:
        return jsonify({'message': 'Portfolio not found or is empty.'}), 404 # error message

    # Prepare portfolio data (ticker: number_of_shares)
    portfolio_data = {stock.ticker: stock.number_of_shares for stock in user_portfolio.stocks} #makes portfolio data

    # Perform portfolio analysis
    analysis_result = portfolio_analysis(portfolio_data) #performs analysis result 
    if not analysis_result:
        return jsonify({'message': 'Error analyzing portfolio.'}), 500 #error message

    return jsonify(analysis_result), 200 # returns successful result
