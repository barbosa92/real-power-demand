from flask import Blueprint, render_template, request
from modules.models import db, Demand
from modules.utils import DemandRequest, FFTCalculator, FFTPlot, convert_to_utc
import json
from datetime import datetime

api = Blueprint("api", __name__)


@api.route("/")
def index():
    return render_template("index.html")


@api.route("/demand", methods=["GET"])
def demand():
    return render_template("demand.html")


@api.route("/demand/fft", methods=["POST"])
def fft_demand():
    if request.method == "POST":
        start_date = request.form.get("start_date")
        start_date = convert_to_utc(start_date)
        end_date = request.form.get("end_date")
        end_date = convert_to_utc(end_date)

        request_handler = DemandRequest(start_date, end_date)
        response = request_handler.make_request()
        signal = [item['value'] for item in response['indicator']['values']]

        fft_calculator = FFTCalculator(signal)
        fft_result = fft_calculator.fft()
        json_fft = fft_calculator.format_fft_to_json(fft_result)
        fft_plot = FFTPlot(signal, fft_result)
        freq_fig = fft_plot.plot_frequency_domain(fft_result)
        time_fig = fft_plot.plot_time_domain()

        freq_plot_filename = 'static/images/fig1.png'
        time_plot_filename = 'static/images/fig2.png'

        fft_plot.save_plot(freq_fig, freq_plot_filename)
        fft_plot.save_plot(time_fig, time_plot_filename)

        fft_string = json.dumps(json_fft)
        print(fft_string)

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        demand_data = Demand(start_date=start_date,
                             end_date=end_date, fft_string=fft_string)

        try:
            db.session.add(demand_data)
            db.session.commit()
        except Exception as e:
            print(f"There was a problem adding the real demand data: {str(e)}")
            return "Error: Failed to add demand data."

        freq_plot = '../static/images/fig1.png'
        time_plot = '../static/images/fig2.png'
        return render_template("fft_demand.html", freq_plot=freq_plot, time_plot=time_plot, id=demand_data.id)
    else:
        return render_template("404.html"), 404


@api.route("/demand/fft/json/<int:id>", methods=["GET"])
def fft_demand_json(id):
    demands = Demand.query.get(id)
    if demands:
        return json.loads(demands.fft_string)
    else:
        return "Error: Demand not found.", 404
