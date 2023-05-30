from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


# Define the data model for a demand reuest between X and Y day and
#     store the result from the fft

class Demand(db.Model):
    """Model for storing real demand request and FFT result."""
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    fft_string = db.Column(db.Text, nullable=False)

    def __init__(self, start_date: date, end_date: date, fft_string: str) -> None:
        """Initialize a Demand object."""
        self.start_date = start_date
        self.end_date = end_date
        self.fft_string = fft_string
