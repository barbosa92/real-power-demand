from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)


class Demand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    power_demand = db.Column(db.String(255), nullable=False)
    geo_id = db.Column(db.Integer, nullable=False)
