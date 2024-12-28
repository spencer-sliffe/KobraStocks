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

auth = Blueprint('auth', __name__) # makes blueprint object


@auth.route('/api/signup', methods=['POST']) # route to signup
def signup():
    data = request.get_json() # gets request
    email = data.get('email', '').lower() # gets email box
    password = data.get('password', '') # gets password
    first_name = data.get('first_name', '')# gets first name
    last_name = data.get('last_name', '')# gets last name
    phone_number = data.get('phone_number', '')# gets phone number

    try:
        valid = validate_email(email) # validates email
        email = valid.normalized # normalizes email 
    except EmailNotValidError as e: # if email not valid 
        return jsonify({'error': str(e)}), 400 # error message

    if not first_name or not last_name or not password:
        return jsonify({'error': 'First name, last name, and password are required'}), 400 # missing info error message

    if User.query.filter_by(email=email).first(): 
        return jsonify({'error': 'Email already registered'}), 400 # email already registered error message 

    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
    ) # user schema 
    user.set_password(password) # sets password
    db.session.add(user) # makes db session
    db.session.commit() # commits session

    return jsonify({'message': 'User created successfully'}), 201 # success message


@auth.route('/api/login', methods=['POST']) # login route
def login():
    data = request.get_json() # receives data
    email = data.get('email', '').lower() # gets email
    password = data.get('password', '') # gets password

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id) 
        return jsonify({'access_token': access_token}), 200 # success console message
    else:
        return jsonify({'error': 'Invalid credentials'}), 401 # invalid credentials error message


@auth.route('/api/user', methods=['GET']) # User route
@jwt_required()
def get_user():
    user_id = get_jwt_identity() # gets user
    user = User.query.get(user_id) # query user if 
    if user:
        return jsonify({
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'budget': user.budget,
            'favorite_stocks': [fs.ticker for fs in user.favorite_stocks],
            'watched_stocks': [ws.ticker for ws in user.watched_stocks],
        }), 200 # returns user data
    else:
        return jsonify({'error': 'User not found'}), 404 # non existant user message