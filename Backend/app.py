from kobrastocks import app  # This imports the app with blueprints already registered
import os
from flask import send_from_directory

# Define the catch-all route after all blueprints have been registered
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Do not serve static files for API routes
    if path.startswith('api/'):
        # Let Flask handle API routes
        return app.send_static_file('index.html')  # Or return a 404 if you prefer
    elif path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
