from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from modules.routes import api

app = Flask(__name__)
# After creating the Flask app, you can make all APIs allow cross-origin access.
CORS(app)
app.register_blueprint(api)


if __name__ == "__main__":
    app.run(debug=True)
