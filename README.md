# API Routes Documentation

## FFT Demand Calculation and Plots Generation
- **Route:** /demand/fft/<start_date>/<end_date>
- **Methods:** GET, POST
- **Description:** This route calculates the Fast Fourier Transform (FFT) of the demand signal within the specified date range and generates frequency and time domain plots.

### Request Parameters
- **<start_date>** (string): The start date of the demand signal in the format "YYYY-MM-DD".
- **<end_date>** (string): The end date of the demand signal in the format "YYYY-MM-DD".

### GET Request
- **Method:** GET
- **Description:** Retrieves the frequency and time domain plots for the real demand signal within the specified date range.

Example request
```
GET /demand/fft/2018-09-02/2018-10-06
```

Response
The response will be a JSON object containing the URLs of the generated plots.

Example response:
```
{
  "freq_fig": "https://cloudinary.com/your-freq-fig-url",
  "time_fig": "https://cloudinary.com/your-time-fig-url"
}
```

## FFT Demand Calculation (JSON Response)
- **Route:** /demand/fft/<start_date>/<end_date>/json
- **Method:** GET
- **Description:** This route calculates the Fast Fourier Transform (FFT) of the real demand signal within the specified date range and returns the result in JSON format.

### Request Parameters
- **<start_date>** (string): The start date of the demand signal in the format "YYYY-MM-DD".
- **<end_date>** (string): The end date of the demand signal in the format "YYYY-MM-DD".

### GET Request
- **Method:** GET
- **Description:** Retrieves the FFT calculation of the real demand signal within the specified date range.

Example request
```
GET /demand/fft/2018-09-02/2018-10-06/json
```

Response
The response will be a JSON object containing the FFT calculation result.

Example response:
```
{
    "real": [204113960.0, -2854331.1955984314, ..., 887552.4259813137, -2854331.195598432],
    "imag": [1.5188561519607902e-09, 4678001.51987003, ..., -1361281.5264175774, -4678001.519870028]
}
```
