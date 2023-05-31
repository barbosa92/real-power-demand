from flask import Blueprint, request
from flask_cors import cross_origin
from modules.utils import DemandRequest, FFTCalculator, FFTPlot, convert_to_utc
import cloudinary
import cloudinary.uploader
import cloudinary.api
import json
import os


# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Create a blueprint for API routes
api = Blueprint("api", __name__)


# Define route for the FFT demand calculation and plots generation
@api.route("/demand/fft/<start_date>/<end_date>", methods=["GET"])
@cross_origin()
def fft_demand(start_date, end_date):
    if request.method == "GET":
        start_date = convert_to_utc(start_date)
        end_date = convert_to_utc(end_date)

        # Create a DemandRequest object and make a request to the esios API
        request_handler = DemandRequest(start_date, end_date)
        response = request_handler.make_request()
        signal = [item['value'] for item in response['indicator']['values']]

        # Calculate FFT
        fft_calculator = FFTCalculator(signal)
        fft_result = fft_calculator.fft()

        # Create a FFTPlot object and plot the FFT
        fft_plot = FFTPlot(signal, fft_result)
        freq_fig = fft_plot.plot_frequency_domain(fft_result)
        time_fig = fft_plot.plot_time_domain()

        # Set filenames for saving the plots
        freq_plot_filename = 'static/images/fig1.png'
        time_plot_filename = 'static/images/fig2.png'

        # Upload plots to Cloudinary
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
        return 'Method not allowed'

# Define route for the FFT demand calculation (JSON response)


@api.route("/demand/fft/<start_date>/<end_date>/json", methods=["GET"])
def fft_demand_json(start_date, end_date):
    if request.method == "GET":
        start_date = convert_to_utc(start_date)  # Convert start_date to UTC
        end_date = convert_to_utc(end_date)  # Convert end_date to UTC
        request_handler = DemandRequest(start_date, end_date)
        response = request_handler.make_request()
        signal = [item['value'] for item in response['indicator']['values']]

        fft_calculator = FFTCalculator(signal)
        fft_result = fft_calculator.fft()
        json_fft = fft_calculator.format_fft_to_json(fft_result)
        return json_fft
    else:
        return 'Method not allowed'
