"""
------------------Prologue--------------------
File Name: manage.py
Path: KobraStocks/Backend/manage.py

Description:
Provides command-line management tools for the Flask application, integrating Flask-Script and Flask-Migrate. Enables database migrations via the `db` command for easy database schema changes.

Input:
Command-line arguments to execute management commands, primarily for database migrations.

Output:
Executes specified commands, such as `db` for migration operations.

Collaborators: Spencer Sliffe
---------------------------------------------
"""

from flask_migrate import Migrate
from kobrastocks import app
from kobrastocks.extensions import db

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()