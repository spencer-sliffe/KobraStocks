# Backend/kobrastocks/routes.py
import requests
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User

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
    MACD = request.args.get('MACD', default='false') == 'true'
    RSI = request.args.get('RSI', default='false') == 'true'
    SMA = request.args.get('SMA', default='false') == 'true'
    EMA = request.args.get('EMA', default='false') == 'true'
    ATR = request.args.get('ATR', default='false') == 'true'
    BBands = request.args.get('BBands', default='false') == 'true'
    VWAP = request.args.get('VWAP', default='false') == 'true'
    predictions = get_predictions(ticker, MACD=MACD, RSI=RSI, SMA=SMA, EMA=EMA, ATR=ATR, BBands=BBands, VWAP=VWAP)
    predictions = convert_to_builtin_types(predictions)
    return jsonify(predictions)


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