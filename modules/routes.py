from flask import Blueprint, render_template, request
from flask_cors import cross_origin
from modules.utils import DemandRequest, FFTCalculator, FFTPlot, convert_to_utc
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

api = Blueprint("api", __name__)


@api.route("/")
def index():
    return render_template("index.html")


@api.route("/demand", methods=["GET"])
def demand():
    return render_template("demand.html")


@api.route("/demand/fft/<start_date>/<end_date>", methods=["GET", "POST"])
@cross_origin()
def fft_demand(start_date, end_date):
    if request.method == "GET":
        start_date = convert_to_utc(start_date)
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

        freq_result = cloudinary.uploader.upload(freq_plot_filename)
        time_result = cloudinary.uploader.upload(time_plot_filename)

        # Get the public URLs of the uploaded images
        freq_fig_url = freq_result['secure_url']
        time_fig_url = time_result['secure_url']

        # Return the URLs as a dictionary
        figures = {
            'freq_fig': freq_fig_url,
            'time_fig': time_fig_url
        }

        # Convert the figures to JSON response
        response = json.dumps(figures)

        return (response)

    else:
        return render_template("404.html"), 404


@api.route("/demand/fft/<start_date>/<end_date>/json", methods=["GET"])
def fft_demand_json(start_date, end_date):
    start_date = convert_to_utc(start_date)
    end_date = convert_to_utc(end_date)
    request_handler = DemandRequest(start_date, end_date)
    response = request_handler.make_request()
    signal = [item['value'] for item in response['indicator']['values']]

    fft_calculator = FFTCalculator(signal)
    fft_result = fft_calculator.fft()
    json_fft = fft_calculator.format_fft_to_json(fft_result)
    return json_fft
