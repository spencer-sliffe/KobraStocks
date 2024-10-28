# Backend/kobrastocks/user_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from kstocks.models import User, FavoriteStock, WatchedStock
from .extensions import db

user = Blueprint('user', __name__)


@user.route('/api/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    favorites = [fs.ticker for fs in user.favorite_stocks]
    return jsonify({'favorites': favorites}), 200


@user.route('/api/favorites', methods=['POST'])
@jwt_required()
def add_favorite():
    user_id = get_jwt_identity()
    data = request.get_json()
    ticker = data.get('ticker')
    if not ticker:
        return jsonify({'error': 'Ticker is required'}), 400
    existing = FavoriteStock.query.filter_by(user_id=user_id, ticker=ticker).first()
    if existing:
        return jsonify({'message': 'Stock already in favorites'}), 200
    favorite = FavoriteStock(user_id=user_id, ticker=ticker)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Stock added to favorites'}), 201


@user.route('/api/favorites/<string:ticker>', methods=['DELETE'])
@jwt_required()
def remove_favorite(ticker):
    user_id = get_jwt_identity()
    favorite = FavoriteStock.query.filter_by(user_id=user_id, ticker=ticker).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message': 'Stock removed from favorites'}), 200
    else:
        return jsonify({'error': 'Stock not found in favorites'}), 404