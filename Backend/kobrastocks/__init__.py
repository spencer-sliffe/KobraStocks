from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../client', static_url_path='')
CORS(app)

# Set configuration variables
app.config['ADMIN_EMAIL'] = 'admin@example.com'

from kobrastocks.routes import main as main_blueprint

app.register_blueprint(main_blueprint)
