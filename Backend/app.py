from flask import Flask, send_from_directory
from flask_cors import CORS
from kobrastocks.routes import main as main_blueprint

def create_app():
    app = Flask(__name__, static_folder="../client/dist", template_folder="../client/dist")

    CORS(app)

    app.register_blueprint(main_blueprint)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        """
        Serve the Vue.js frontend build from the `dist` folder.
        This ensures that when you navigate to routes on the frontend, 
        the Vue.js router handles the page rendering.
        """
        if path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
