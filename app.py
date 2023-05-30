from flask import Flask
from flask_migrate import Migrate
from modules.models import db
from modules.routes import api
import os

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(api)
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)
