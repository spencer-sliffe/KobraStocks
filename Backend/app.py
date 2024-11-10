"""
------------------Prologue--------------------
File Name: app.py
Path: Backend/kobrastocks/main.py

Description:
Configures the main entry point for the Flask application, setting up routing to serve static files for both API and non-API requests. Routes to index.html for paths that don't match existing static files, supporting single-page application routing.

Input:
URL paths, with `api/` paths reserved for API calls.

Output:
Serves index.html or requested static files from the configured static folder.

Collaborators: Spencer Sliffe
---------------------------------------------
"""

from kobrastocks import app
import os
from flask import send_from_directory

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path.startswith('api/'):
        return app.send_static_file('index.html')  # Or return a 404 if you prefer
    elif path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
