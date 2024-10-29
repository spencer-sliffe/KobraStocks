# Backend/kobrastocks/routes.py
import requests
from flask import Blueprint, jsonify, request, current_app

from .serializers import stock_data_schema, contact_form_schema
from .services import (
    get_stock_data,
    send_contact_form,
    get_predictions,
    get_stock_chart,
)
from .utils import convert_to_builtin_types

main = Blueprint('main', __name__)


@main.route('/api/stock_data', methods=['GET'])
def stock_data():
    ticker = request.args.get('ticker', default='AAPL', type=str)
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
    predictions = get_predictions(ticker)
    predictions = convert_to_builtin_types(predictions)
    return jsonify(predictions)


@main.route('/api/stock_chart', methods=['GET'])
def stock_chart():
    ticker = request.args.get('ticker', default='AAPL', type=str)
    MA9 = request.args.get('MA9', default='false') == 'true'
    MA50 = request.args.get('MA50', default='false') == 'true'
    MACD = request.args.get('MACD', default='false') == 'true'
    RSI = request.args.get('RSI', default='false') == 'true'
    fig = get_stock_chart(ticker, MA9=MA9, MA50=MA50, MACD=MACD, RSI=RSI)

    if fig is None:
        return jsonify({'error': f"Could not generate chart for ticker {ticker}"}), 404

    fig_dict = fig.to_dict()
    fig_dict = convert_to_builtin_types(fig_dict)
    return jsonify(fig_dict)


@main.route('/api/hot_stocks', methods=['GET'])
def hot_stocks():
    """
    Fetch the top 10 hot stocks.
    """
    try:
        # Replace 'YOUR_ALPHA_VANTAGE_API_KEY' with your actual API key
        api_key = 'H7YI95UIHH8ATZ8H'
        # API endpoint for top gainers
        url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={api_key}'

        response = requests.get(url)
        data = response.json()

        # Parse the response to get top gainers
        # Note: Alpha Vantage does not provide a direct 'top gainers' endpoint.
        # Alternatively, we can fetch a list of symbols and compute the gainers ourselves.
        # For simplicity, let's use a predefined list for now.

        hot_stocks_list = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'FB', 'JNJ', 'V', 'JPM']

        # Fetch stock data for each ticker
        hot_stocks_data = []
        for ticker in hot_stocks_list:
            stock_data = get_stock_data(ticker)
            if stock_data:
                hot_stocks_data.append(stock_data)

        return jsonify(hot_stocks_data), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching hot stocks: {e}")
        return jsonify({'error': 'Failed to fetch hot stocks'}), 500