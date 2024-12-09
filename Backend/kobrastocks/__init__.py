"""
------------------Prologue--------------------
File Name: __init__.py
Path: Backend/kobrastocks/__init__.py

Description:
Initializes the Flask application and configures key components, including database, encryption, JWT, CORS, and environment variables. Registers main, authentication, user, and portfolio blueprints for route handling.

Input:
Environment variables (SECRET_KEY, SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY)

Output:
Flask app instance with configured routes and extensions

Collaborators: Spencer Sliffe
---------------------------------------------
"""

from flask import Flask
import os

from .extensions import db, bcrypt, jwt
from .routes import main as main_blueprint
from .auth_routes import auth as auth_blueprint
from .user_routes import user as user_blueprint
from .portfolio_routes import portfolio as portfolio_blueprint
from .suggestions_routes import suggestions as suggestions_blueprint
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from .stock_routes import stocks as stocks_blueprint


migrate = Migrate()
load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {
    "origins": "http://localhost:8080",
    "methods": ["GET", "POST", "DELETE", "PUT", "OPTIONS"],
    "allow_headers": ["Authorization", "Content-Type", "X-Requested-With"],
    "supports_credentials": True
}})


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'your_database_uri')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your_jwt_secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
migrate.init_app(app, db)

# Register blueprints here
app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(portfolio_blueprint)
app.register_blueprint(suggestions_blueprint)
app.register_blueprint(stocks_blueprint)

