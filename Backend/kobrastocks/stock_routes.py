# stock_routes.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from .services import get_stock_data
from .utils import generate_stock_analysis_prompt,get_stock_chat_analysis

stocks = Blueprint('stocks', __name__, url_prefix='/api/stocks')


@stocks.route('/<string:ticker>/analysis', methods=['GET'])
@jwt_required()
def get_stock_analysis(ticker):
    stock_data = get_stock_data(ticker)
    if not stock_data:
        return jsonify({'message': 'Stock data not found.'}), 404

    # Extract user-specific data from request.args
    user_shares = request.args.get('user_shares', type=float)
    user_pps = request.args.get('user_pps_at_purchase', type=float)
    user_invested = request.args.get('user_total_invested', type=float)
    user_value = request.args.get('user_current_value', type=float)
    user_pl = request.args.get('user_profit_loss', type=float)
    user_pl_percentage = request.args.get('user_profit_loss_percentage', type=float)

    if user_shares is not None:
        stock_data['user_shares'] = user_shares
        stock_data['user_pps_at_purchase'] = user_pps
        stock_data['user_total_invested'] = user_invested
        stock_data['user_current_value'] = user_value
        stock_data['user_profit_loss'] = user_pl
        stock_data['user_profit_loss_percentage'] = user_pl_percentage

    prompt = generate_stock_analysis_prompt(stock_data)
    chat_response = get_stock_chat_analysis([prompt])
    if chat_response:
        return jsonify({'analysis': chat_response[0]}), 200
    else:
        return jsonify({'message': 'Error generating stock analysis.'}), 500