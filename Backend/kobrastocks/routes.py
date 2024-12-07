"""
------------------Prologue--------------------
File Name: routes.py
Path: Backend/kobrastocks/routes.py

Description:
Defines primary application routes for stock data retrieval, contact form submission, stock predictions, chart generation, and hot stock filtering based on user budget. Integrates with external APIs and handles data serialization, validation, and error logging.

Input:
Query parameters (ticker, technical indicators), JSON data for contact forms, and JWT tokens for authenticated routes

Output:
JSON responses with stock data, prediction results, chart data, and hot stock listings

Collaborators: Spencer Sliffe, Saje Cowell, Charlie Gillund
---------------------------------------------
"""

import requests
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User

from .serializers import stock_data_schema, contact_form_schema, crypto_data_schema
from .services import (
    get_stock_data,
    send_contact_form,
    get_predictions,
    get_stock_chart, get_crypto_data,
)
from .utils import convert_to_builtin_types

main = Blueprint('main', __name__)


@main.route('/api/stock_data', methods=['GET'])
def stock_data():
    ticker = request.args.get('ticker', type=str)
    stock_data = get_stock_data(ticker)
    if stock_data is None:
        return jsonify({'error': f"No data found for ticker {ticker}"}), 404
    return jsonify(stock_data_schema.dump(stock_data))


@main.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()
    errors = contact_form_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    success = send_contact_form(data)
    if success:
        return jsonify({"message": "Contact form submitted successfully"}), 200
    else:
        return jsonify({"error": "Failed to submit contact form"}), 500


@main.route('/api/predictions', methods=['GET'])
def predictions():
    ticker = request.args.get('ticker', default='AAPL', type=str)
    MACD = request.args.get('MACD', default='false') == 'true'
    RSI = request.args.get('RSI', default='false') == 'true'
    SMA = request.args.get('SMA', default='false') == 'true'
    EMA = request.args.get('EMA', default='false') == 'true'
    ATR = request.args.get('ATR', default='false') == 'true'
    BBands = request.args.get('BBands', default='false') == 'true'
    VWAP = request.args.get('VWAP', default='false') == 'true'

    predictions_result = get_predictions(
        ticker,
        MACD=MACD,
        RSI=RSI,
        SMA=SMA,
        EMA=EMA,
        ATR=ATR,
        BBands=BBands,
        VWAP=VWAP
    )

    if predictions_result is None:
        return jsonify({'error': 'Predictions could not be generated'}), 400

    return jsonify(predictions_result)


@main.route('/api/stock_chart', methods=['GET'])
def stock_chart():
    ticker = request.args.get('ticker', default='AAPL', type=str)

    fig = get_stock_chart(ticker)

    if fig is None:
        return jsonify({'error': f"Could not generate chart for ticker {ticker}"}), 404

    fig_dict = fig.to_dict()
    fig_dict = convert_to_builtin_types(fig_dict)
    return jsonify(fig_dict)


@main.route('/api/hot_stocks', methods=['GET'])
@jwt_required()
def hot_stocks():
    try:
        import os
        api_key = os.environ.get('RAPIDAPI_KEY')
        if not api_key:
            return jsonify({'error': 'API key not found'}), 500

        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user_budget = user.budget

        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-movers"

        querystring = {"region": "US", "lang": "en-US", "count": "50", "start": "0"}

        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        # Extract top gainers
        gainers = data.get('finance', {}).get('result', [])
        hot_stocks_list = []
        for mover in gainers:
            if mover.get('title') == 'Day Gainers':
                for quote in mover.get('quotes', []):
                    ticker = quote.get('symbol')
                    if ticker:
                        hot_stocks_list.append(ticker)

        hot_stocks_data = []
        for ticker in hot_stocks_list:
            stock_data = get_stock_data(ticker)
            if stock_data and stock_data.get('close_price') is not None:
                if user_budget is None or stock_data['close_price'] <= user_budget:
                    hot_stocks_data.append(stock_data)

        hot_stocks_data = hot_stocks_data[:10]

        if not hot_stocks_data:
            return jsonify({'message': 'No hot stocks found within your budget. Showing all hot stocks.'}), 200

        return jsonify(hot_stocks_data), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching hot stocks: {e}")
        return jsonify({'error': 'Failed to fetch hot stocks'}), 500


@main.route('/api/news', methods=['GET'])
def get_stock_news_articles():
    """
    Fetch the latest stock market news using the News API.
    """
    try:
        from newsapi import NewsApiClient
        import os

        # Retrieve API key from environment variables
        api_key = os.environ.get('NEWS_API_KEY')
        if not api_key:
            return jsonify({'error': 'API key not found'}), 500

        # Initialize the News API client
        newsapi = NewsApiClient(api_key=api_key)

        # Get query parameters
        query = request.args.get('query', default='stock market', type=str)
        page = request.args.get('page', default=1, type=int)

        # Fetch news articles
        all_articles = newsapi.get_everything(
            q=query,
            sort_by='publishedAt',
            page_size=10,  # Limit articles per page
            page=page,
            language='en'
        )

        # Return the articles
        return jsonify(all_articles)

    except Exception as e:
        current_app.logger.error(f"Error fetching news articles: {e}")
        return jsonify({'error': 'Failed to fetch news articles'}), 500


@main.route('/api/hot_crypto', methods=['GET'])
@jwt_required()
def get_hot_crypto_currencies():
    try:
        # Get the user's budget
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user_budget = user.budget

        # Fetch cryptocurrency data from CoinGecko
        url = "https://api.coingecko.com/api/v3/coins/markets"
        query_params = {
            "vs_currency": "usd",  # Prices in USD
            "order": "market_cap_desc",  # Top cryptocurrencies by market cap
            "per_page": 50,  # Fetch top 50
            "page": 1,  # Page number
            "sparkline": False  # No sparkline data
        }
        response = requests.get(url, params=query_params)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch cryptocurrency data'}), 500

        cryptos = response.json()
        hot_crypto_data = []

        # Filter cryptocurrencies within the user's budget
        for crypto in cryptos:
            price = crypto.get('current_price')
            if price and (user_budget is None or price <= user_budget):
                hot_crypto_data.append({
                    "ticker": crypto.get('symbol'),
                    "name": crypto.get('name'),
                    "price": price,
                    "market_cap": crypto.get('market_cap'),
                    "24h_change": crypto.get('price_change_percentage_24h')
                })

        # Limit to top 10
        hot_crypto_data = hot_crypto_data[:10]

        if not hot_crypto_data:
            return jsonify({'message': 'No hot cryptocurrencies found within your budget. Showing top cryptocurrencies.'}), 200

        return jsonify(hot_crypto_data), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching hot cryptocurrencies: {e}")
        return jsonify({'error': 'Failed to fetch hot cryptocurrencies'}), 500


@main.route('/api/crypto_data', methods=['GET'])
def crypto_data():
    ticker = request.args.get('ticker', type=str)
    crypto_data = get_crypto_data(ticker)
    if crypto_data is None:
        return jsonify({'error': f"No data found for ticker {ticker}"}), 404
    return jsonify(crypto_data_schema.dump(crypto_data))