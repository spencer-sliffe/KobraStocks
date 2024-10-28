# Backend/kobrastocks/__init__.py
from flask import Flask
import os

# Import extensions
from .extensions import db, bcrypt, jwt

# Import blueprints
from .routes import main as main_blueprint
from .auth_routes import auth as auth_blueprint

app = Flask(__name__)

# Load configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'your_database_uri')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your_jwt_secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions with the app
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

# Register blueprints
app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)
