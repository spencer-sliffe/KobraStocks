# stock_routes.py

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from .services import get_stock_data
from .utils import generate_stock_analysis_prompt,get_stock_chat_analysis

stocks = Blueprint('stocks', __name__, url_prefix='/api/stocks')


@stocks.route('/<string:ticker>/analysis', methods=['GET'])
@jwt_required()
def get_stock_analysis(ticker):
    # Get stock data
    stock_data = get_stock_data(ticker)
    if not stock_data:
        return jsonify({'message': 'Stock data not found.'}), 404
    # Generate prompt
    prompt = generate_stock_analysis_prompt(stock_data)
    # Get analysis from OpenAI
    chat_response = get_stock_chat_analysis([prompt])
    if chat_response:
        analysis = chat_response[0]
        return jsonify({'analysis': analysis}), 200
    else:
        return jsonify({'message': 'Error generating stock analysis.'}), 500