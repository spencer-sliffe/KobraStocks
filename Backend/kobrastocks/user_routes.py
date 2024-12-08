"""
------------------Prologue--------------------
File Name: user_routes.py
Path: Backend/kobrastocks/user_routes.py

Description:
Defines routes for managing user-specific data, including favorites, watchlist, and budget:
- `GET /api/favorites`: Retrieves the user's list of favorite stocks.
- `POST /api/favorites`: Adds a stock to the user's favorites.
- `DELETE /api/favorites/<ticker>`: Removes a stock from the user's favorites.
- `GET /api/watchlist`: Retrieves the user's watchlist.
- `POST /api/watchlist`: Adds a stock to the user's watchlist.
- `DELETE /api/watchlist/<ticker>`: Removes a stock from the user's watchlist.
- `PUT /api/user/budget`: Updates the user's budget.

Input:
JWT tokens for authenticated routes, JSON payloads with stock tickers and budget.

Output:
JSON responses indicating success, failure, or requested data.

Collaborators: Spencer Sliffe
---------------------------------------------
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from kobrastocks.models import User, FavoriteStock, WatchedStock, WatchedCrypto, FavoriteCrypto
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


@user.route('/api/watchlist', methods=['GET'])
@jwt_required()
def get_watchlist():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    watchlist = [ws.ticker for ws in user.watched_stocks]
    return jsonify({'watchlist': watchlist}), 200


@user.route('/api/watchlist', methods=['POST'])
@jwt_required()
def add_watchlist():
    user_id = get_jwt_identity()
    data = request.get_json()
    ticker = data.get('ticker')
    if not ticker:
        return jsonify({'error': 'Ticker is required'}), 400
    existing = WatchedStock.query.filter_by(user_id=user_id, ticker=ticker).first()
    if existing:
        return jsonify({'message': 'Stock already in watchlist'}), 200
    watch_stock = WatchedStock(user_id=user_id, ticker=ticker)
    db.session.add(watch_stock)
    db.session.commit()
    return jsonify({'message': 'Stock added to watchlist'}), 201


@user.route('/api/watchlist/<string:ticker>', methods=['DELETE'])
@jwt_required()
def remove_watchlist(ticker):
    user_id = get_jwt_identity()
    watch_stock = WatchedStock.query.filter_by(user_id=user_id, ticker=ticker).first()
    if watch_stock:
        db.session.delete(watch_stock)
        db.session.commit()
        return jsonify({'message': 'Stock removed from watchlist'}), 200
    else:
        return jsonify({'error': 'Stock not found in watchlist'}), 404


@user.route('/api/user/budget', methods=['PUT'])
@jwt_required()
def update_budget():
    user_id = get_jwt_identity()
    data = request.get_json()
    budget = data.get('budget')

    if budget is None:
        return jsonify({'error': 'Budget is required'}), 400

    try:
        budget = float(budget)
    except ValueError:
        return jsonify({'error': 'Budget must be a number'}), 400

    user = User.query.get(user_id)
    if user:
        user.budget = budget
        db.session.commit()
        return jsonify({'message': 'Budget updated successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@user.route('/api/crypto_favorites', methods=['GET'])
@jwt_required()
def get_crypto_favorites():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    favorites = [fc.ticker for fc in user.favorite_crypto]
    return jsonify({'favorites': favorites}), 200


@user.route('/api/crypto_favorites', methods=['POST'])
@jwt_required()
def add_crypto_favorite():
    user_id = get_jwt_identity()
    data = request.get_json()
    crypto_id = data.get('crypto_id')
    ticker = data.get('ticker')
    if not crypto_id:
        return jsonify({'error': 'id is required'}), 400

    existing = FavoriteCrypto.query.filter_by(user_id=user_id, crypto_id=crypto_id, ticker=ticker).first()
    if existing:
        return jsonify({'message': 'Crypto already in favorites'}), 200

    favorite = FavoriteCrypto(user_id=user_id, crypto_id=crypto_id, ticker=ticker)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Crypto added to favorites'}), 201


@user.route('/api/crypto_favorites/<string:crypto_id>', methods=['DELETE'])
@jwt_required()
def remove_crypto_favorite(crypto_id):
    user_id = get_jwt_identity()
    favorite = FavoriteCrypto.query.filter_by(user_id=user_id, crypto_id=crypto_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message': 'Crypto removed from favorites'}), 200
    else:
        return jsonify({'error': 'Crypto not found in favorites'}), 404


@user.route('/api/crypto_watchlist', methods=['GET'])
@jwt_required()
def get_crypto_watchlist():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    watchlist = [wc.ticker for wc in user.watched_crypto]
    return jsonify({'watchlist': watchlist}), 200


@user.route('/api/crypto_watchlist', methods=['POST'])
@jwt_required()
def add_crypto_to_watchlist():
    user_id = get_jwt_identity()
    data = request.get_json()
    crypto_id = data.get('crypto_id')
    ticker = data.get('ticker')
    if not crypto_id:
        return jsonify({'error': 'crypto_id is required'}), 400

    existing = WatchedCrypto.query.filter_by(user_id=user_id, crypto_id=crypto_id, ticker=ticker).first()
    if existing:
        return jsonify({'message': 'Crypto already in watchlist'}), 200

    watch_crypto = WatchedCrypto(user_id=user_id, crypto_id=crypto_id, ticker=ticker)
    db.session.add(watch_crypto)
    db.session.commit()
    return jsonify({'message': 'Crypto added to watchlist'}), 201


@user.route('/api/crypto_watchlist/<string:crypto_id>', methods=['DELETE'])
@jwt_required()
def remove_crypto_from_watchlist(crypto_id):
    user_id = get_jwt_identity()
    watch_crypto = WatchedCrypto.query.filter_by(user_id=user_id, crypto_id=crypto_id).first()
    if watch_crypto:
        db.session.delete(watch_crypto)
        db.session.commit()
        return jsonify({'message': 'Crypto removed from watchlist'}), 200
    else:
        return jsonify({'error': 'Crypto not found in watchlist'}), 404