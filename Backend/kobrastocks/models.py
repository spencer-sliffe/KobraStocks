"""
------------------Prologue--------------------
File Name: models.py
Path: Backend/kobrastocks/models.py

Description:
Defines the data models for the application, including User, FavoriteStock, and WatchedStock. User model includes attributes for user details and password management, while FavoriteStock and WatchedStock models relate stocks to individual users.

Input:
None directly; models are populated and queried by other application components

Output:
Database table representations for User, FavoriteStock, and WatchedStock, with methods for password hashing and checking

Collaborators: Spencer Sliffe
---------------------------------------------
"""

from .extensions import db, bcrypt
from datetime import datetime

#DATABASE SCHEMA FOR USERS
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    budget = db.Column(db.Float, nullable=True)
    reset_code = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    favorite_stocks = db.relationship('FavoriteStock', backref='user', lazy=True)
    watched_stocks = db.relationship('WatchedStock', backref='user', lazy=True)
    portfolio = db.relationship('Portfolio', back_populates='user', uselist=False)
    favorite_cryptos = db.relationship('FavoriteCrypto', backref='user', lazy=True)
    watched_cryptos = db.relationship('WatchedCrypto', backref='user', lazy=True)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

#DATABASE SCHEMA FOR STOCK FAVORITES
class FavoriteStock(db.Model):
    __tablename__ = 'favorite_stocks'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

#DATABASE SCHEMA FOR STOCK WATCHLIST
class WatchedStock(db.Model):
    __tablename__ = 'watched_stocks'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

#DATABASE SCHEMA FOR PORTFOLIO
class Portfolio(db.Model):
    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)

    # Relationships
    user = db.relationship('User', back_populates='portfolio')
    stocks = db.relationship('PortfolioStock', back_populates='portfolio', cascade='all, delete-orphan')

#DATABASE SCHEMA FOR PORTFOLIO ASSET
class PortfolioStock(db.Model):
    __tablename__ = 'portfolio_stocks'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False, unique=False)
    number_of_shares = db.Column(db.Integer, nullable=False)
    pps_at_purchase = db.Column(db.Float, nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'))

    # Relationships
    portfolio = db.relationship('Portfolio', back_populates='stocks')

#DATABASE SCHEMA FOR CRYPTO FAVORITES
class FavoriteCrypto(db.Model):
    __tablename__ = 'favorite_crypto'

    id = db.Column(db.Integer, primary_key=True)
    crypto_id = db.Column(db.String(20), nullable=False)
    ticker = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

#DATABASE SCHEMA FOR CRYPTO WATCHLIST
class WatchedCrypto(db.Model):
    __tablename__ = 'watched_crypto'

    id = db.Column(db.Integer, primary_key=True)
    crypto_id = db.Column(db.String(20), nullable=False)
    ticker = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)