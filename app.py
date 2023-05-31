from flask import Flask
from flask_cors import CORS
from modules.routes import api

app = Flask(__name__)  # Create an instance of the Flask application
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for the app
app.register_blueprint(api)  # Register the blueprint for the API routes

if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask app in debug mode
