import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from datetime import datetime
from urllib.parse import quote
import json
import os


class DemandRequest:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def make_request(self):
        api_key = os.getenv('API_KEY')
        url = f"https://api.esios.ree.es/indicators/1293?start_date={self.start_date}T00%3A00%3A00Z&end_date={self.end_date}T23%3A50%3A00Z&geo_ids[]=8741"
        headers = {
            'x-api-key': api_key,
            'Cookie': 'incap_ses_267_1885724=oZbDAuWrlHwM8qqzL5O0A8XfcGQAAAAAEdi5ZX7RIaLSklaqpbL4zg==; nlbi_1885724=jnBrON6IpV3Q3qeUlFRiyAAAAABLfW+66IEH3e1Rw/O/w4TP; visid_incap_1885724=Rw73m3OjRPGdpM+zRAfco6XkbGQAAAAAQUIPAAAAAAC74qJiUYc/nFyR3I/+SDKr'
        }
        response = requests.get(url, headers=headers)
        return response.json()


class FFTCalculator:
    def __init__(self, signal):
        self.signal = signal

    def fft(self):
        """Calculate the FFT of a list of numbers."""
        return np.fft.fft(self.signal)

    def format_fft_to_json(self, fft_result):
        """Format the result of the FFT to JSON."""
        return json.dumps({
            "real": fft_result.real.tolist(),
            "imag": fft_result.imag.tolist(),
        })


class FFTPlot:
    def __init__(self, signal, fft_result):
        self.signal = signal
        self.fft_result = fft_result

    def plot_frequency_domain(self, fft_result):
        N = len(self.signal)
        T = 10 * 60
        frequencies = np.fft.fftfreq(N, T)
        fig, ax = plt.subplots()
        ax.plot(frequencies, np.abs(fft_result))
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.title('Signal in the Frequency Domain')
        xmin = -1e-4
        xmax = 1e-4
        num_ticks = 5
        xticks = np.linspace(xmin, xmax, num_ticks)
        ax.set_xlim(xmin, xmax)
        ax.set_xticks(xticks)
        ax.set_xticklabels(['{:.1e}'.format(xtick) for xtick in xticks])
        return fig

    def plot_time_domain(self):
        time = np.arange(len(self.signal)) * (10 * 60)
        fig, ax = plt.subplots()
        ax.plot(time, self.signal)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Signal in the Time Domain')
        return fig

    def save_plot(self, fig, plot_filename):
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(plot_filename)


def convert_to_utc(date):
    original_format = '%Y-%m-%d'
    target_format = '%Y-%m-%d'
    date_obj = datetime.strptime(date, original_format)
    target_date_string = date_obj.strftime(target_format)
    encoded_date_string = quote(target_date_string)
    return encoded_date_string
