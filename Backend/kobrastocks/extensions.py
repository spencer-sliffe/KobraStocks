"""
------------------Prologue--------------------
File Name: extensions.py
Path: Backend/kobrastocks/extensions.py

Description:
Initializes and provides instances of core Flask extensions used across the application, including SQLAlchemy for database management, Bcrypt for password hashing, and JWTManager for handling JWT-based authentication.

Input:
N/A

Output:
Instances of SQLAlchemy, Bcrypt, and JWTManager for application-wide use

Collaborators: Spencer Sliffe
---------------------------------------------
"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
