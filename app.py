from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from modules.models import db
from modules.routes import api

app = Flask(__name__)
# After creating the Flask app, you can make all APIs allow cross-origin access.
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://power_demand_user:1PQcApeqs1j2XpPWig3AseSG3xd9Atn1@dpg-chr6nc9mbg5e1f0blurg-a.frankfurt-postgres.render.com/power_demand"
db.init_app(app)
app.register_blueprint(api)
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)
