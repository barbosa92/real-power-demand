from flask import Blueprint
from flask import render_template
from modules.models import db, Task, Demand
from modules.utils import demand_request
import os

api = Blueprint("api", __name__)


@api.route("/")
def home():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)


@api.route("/demands")
def demands():
    demand_request()
    freq_plot = 'static/images/fig1.png'
    time_plot = 'static/images/fig2.png'

    return render_template("demands.html", freq_plot=freq_plot, time_plot=time_plot)


@api.after_request
def remove_temp_file(response):
    try:
        # Get the plot filename from the response
        freq_plot = response.headers.get(
            'freq_plot', '')
        time_plot = response.headers.get(
            'time_plot', '')

        # Delete the plot file
        if freq_plot & time_plot:
            os.remove(freq_plot, time_plot)
    except Exception as e:
        print(f"Error deleting plot file: {str(e)}")

    return response
