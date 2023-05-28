import requests
import numpy as np
from scipy.fft import fft, ifft, fftfreq
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg


def demand_request():

    url = "https://api.esios.ree.es/indicators/1293?start_date=2018-09-02T00%3A00%3A00Z&end_date=2018-10-06T23%3A50%3A00Z&geo_ids[]=8741"

    payload = {}
    headers = {
        'x-api-key': '52eee0ecb656ca45bbdcff23167a537ca49e5dede1dcf5b05866c13db29e0a81',
        'Cookie': 'incap_ses_267_1885724=oZbDAuWrlHwM8qqzL5O0A8XfcGQAAAAAEdi5ZX7RIaLSklaqpbL4zg==; nlbi_1885724=jnBrON6IpV3Q3qeUlFRiyAAAAABLfW+66IEH3e1Rw/O/w4TP; visid_incap_1885724=Rw73m3OjRPGdpM+zRAfco6XkbGQAAAAAQUIPAAAAAAC74qJiUYc/nFyR3I/+SDKr'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    res = response.json()

    # Extract values from 'values' key
    signal = [item['value'] for item in res['indicator']['values']]

    # Step 2: Prepare the signal data
    # signal = [...]  # Replace [...] with your actual signal data

    # Step 3: Set the parameters
    N = len(signal)
    T = 10 * 60  # Set the sampling interval based on the time resolution of the signal

    # Step 3: Set the time values

    resolution_interval = 1 / T

    time = np.arange(len(signal)) * resolution_interval

    # Step 4: Perform the FFT
    fft_result = fft(signal)
    frequencies = fftfreq(N, T)

    # Step 5: Plot the frequency spectrum
    # plt.plot(frequencies, np.abs(fft_result))
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Amplitude')
    # plt.show()
    # freq_plot = 'static/images/freq_plot.png'
    # plt.savefig(freq_plot)

    fig1, ax1 = plt.subplots()
    ax1.plot(frequencies, np.abs(fft_result))
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')

    # Save the first plot with a unique filename
    plot_filename1 = f'static/images/fig1.png'
    canvas1 = FigureCanvasAgg(fig1)
    canvas1.print_png(plot_filename1)

    # Step 4: Plot the signal in the time domain
    # plt.plot(time, signal)
    # plt.xlabel('Time')
    # plt.ylabel('Amplitude')
    # plt.title('Signal in the Time Domain')
    # # plt.show()
    # time_plot = 'static/images/time_plot.png'
    # plt.savefig(time_plot)

    fig2, ax2 = plt.subplots()
    ax2.plot(time, signal)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Signal in the Time Domain')

    # Save the first plot with a unique filename
    plot_filename2 = f'static/images/fig2.png'
    canvas2 = FigureCanvasAgg(fig2)
    canvas2.print_png(plot_filename2)
