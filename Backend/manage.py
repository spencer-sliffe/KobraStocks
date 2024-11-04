# KobraStocks/Backend/manage.py

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from kobrastocks import app
from kobrastocks.extensions import db
from flask.cli import FlaskGroup


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    app.run()

