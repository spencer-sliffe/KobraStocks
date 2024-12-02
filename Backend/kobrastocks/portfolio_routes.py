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

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import Portfolio
from .portfolio_services import portfolio_analysis
from .services import (
    add_stock_to_portfolio,
    remove_stock_from_portfolio,
    get_portfolio,
    get_portfolio_recommendations
)
from .serializers import (
    portfolio_schema,
    portfolio_recommendations_schema
)

portfolio = Blueprint('portfolio', __name__, url_prefix='/api/portfolio')


@portfolio.route('', methods=['GET'])
@jwt_required()
def get_user_portfolio():
    user_id = get_jwt_identity()
    portfolio_data = get_portfolio(user_id)
    return jsonify(portfolio_schema.dump({'stocks': portfolio_data})), 200


@portfolio.route('', methods=['POST'])
@jwt_required()
def add_stock():
    user_id = get_jwt_identity()
    data = request.get_json()
    ticker = data.get('ticker')
    amount_invested = data.get('amount_invested')

    if not ticker or amount_invested is None:
        return jsonify({'message': 'Ticker and amount_invested are required.'}), 400

    success = add_stock_to_portfolio(user_id, ticker, amount_invested)
    if success:
        return jsonify({'message': f'{ticker} added to portfolio.'}), 200
    else:
        return jsonify({'message': 'Failed to add stock to portfolio.'}), 500


@portfolio.route('/<string:ticker>', methods=['DELETE'])
@jwt_required()
def remove_stock(ticker):
    user_id = get_jwt_identity()
    success = remove_stock_from_portfolio(user_id, ticker)
    if success:
        return jsonify({'message': f'{ticker} removed from portfolio.'}), 200
    else:
        return jsonify({'message': 'Failed to remove stock from portfolio.'}), 500


@portfolio.route('/analysis', methods=['GET'])
@jwt_required()
def get_portfolio_analysis():
    user_id = get_jwt_identity()
    # Fetch user's portfolio from the database
    user_portfolio = Portfolio.query.filter_by(user_id=user_id).first()
    if not user_portfolio or not user_portfolio.stocks:
        return jsonify({'message': 'Portfolio not found or is empty.'}), 404

    # Prepare portfolio data
    portfolio_data = {stock.ticker: stock.amount_invested for stock in user_portfolio.stocks}

    # Perform portfolio analysis
    analysis_result = portfolio_analysis(portfolio_data)
    if not analysis_result:
        return jsonify({'message': 'Error analyzing portfolio.'}), 500

    return jsonify(analysis_result), 200