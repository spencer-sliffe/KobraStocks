"""
------------------Prologue--------------------
File Name: auth_routes.py
Path: Backend/kobrastocks/auth_routes.py

Description:
Defines authentication routes for user signup, login, and user information retrieval. Includes email validation, password hashing, and JWT-based access token generation for secure user management.

Input:
JSON data for user credentials and profile details (email, password, first name, last name, phone number)

Output:
JSON responses for signup, login success with access token, and user profile data

Collaborators: Spencer Sliffe
---------------------------------------------
"""

from flask import Blueprint, request, jsonify
from .models import User
from .extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from email_validator import validate_email, EmailNotValidError

auth = Blueprint('auth', __name__)


@auth.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email', '').lower()
    password = data.get('password', '')
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    phone_number = data.get('phone_number', '')

    try:
        valid = validate_email(email)
        email = valid.normalized
    except EmailNotValidError as e:
        return jsonify({'error': str(e)}), 400

    if not first_name or not last_name or not password:
        return jsonify({'error': 'First name, last name, and password are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').lower()
    password = data.get('password', '')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@auth.route('/api/user', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'budget': user.budget,
            'favorite_stocks': [fs.ticker for fs in user.favorite_stocks],
            'watched_stocks': [ws.ticker for ws in user.watched_stocks],
        }), 200
    else:
        return jsonify({'error': 'User not found'}), 404