import time
import requests
from typing import Iterable, Union
from datetime import date, datetime

import numpy as np
from bs4 import BeautifulSoup
import pyfirmata

# ----------------------------------------------------------------------
# GET SEASON
Y = 2000  # Dummy leap year to allow input X-02-29 (leap day)
seasons = [('winter', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('spring', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('summer', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('autumn', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('winter', (date(Y, 12, 21),  date(Y, 12, 31)))]


def get_season():
    """Return current nothern hemisphere season"""
    now = date.today()
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)


# ----------------------------------------------------------------------
# RECORD INSIDE TEMPERATURE

def record_inside_temperature(arduino_info: dict,
                              data_points: int = 10, 
                              seconds: Union[int, float] = 10) -> int:
    """Return temperature based on Arduino readings from thermistor
    circuit.
    
    Temperature reported is in Fahrenheit.  Connect to Arduino using
    pyfirmata and read voltages across thermistor in thermistor-resistor
    circuit.  Perform conversions and use Steinhart-Hart equation to
    determine the temperature at the head of the thermistor.

    Parameters
    ----------
    data_points : int
        Specify the number of readings to gather and average over;
        default 10
    seconds : int or float
        Across how many seconds the data points should be evenly spaced
        across; default 10

    Example
    ----------
    The following records 5 datapoints across 10 seconds (2 seconds
    between recordings) and then averages them, truncating all decimal
    places.
    >>> record_inside_temperature(data_points=5, seconds=10)
    70
    """

    def connect_to_arduino(port: str, pin: str):
        """Return pyfirmata connection object to a pin on Arduino board.
        
        Connect to Arduino board at specified port and watches specified
        pin.  The voltage value at this pin can be read using the .read
        method.

        Parameters
        ----------
        port : str
            The connection port between Arduino and computer.  The name
            of this port can be found in the Arduino IDE when connected
            to a board.
        pin : str
            Which pin on the Arduino board should voltage be read from.

        Example
        ----------
        >>> pin_connection = connect_to_arduino(port="COM3", pin="a:0:i")
        >>> pin_connection.read()
        0.3312
        """
        board = pyfirmata.Arduino(port)
        pyfirmata_iterator = pyfirmata.util.Iterator(board)
        pyfirmata_iterator.start()

        return board.get_pin(pin)    

    def Steinhart_Hart(voltage: Union[float, int],
                       resistence: Union[float, int],
                       coefficients: Iterable) -> float:
        """Return temperature given voltage.
        
        Use Steinhart-Hart to compute temperature based on thermistor 
        reading.  Uses only the first three terms to approximate,
        therefore requires the first three coefficients.  Returns
        temperature in Kelvin.
        
        Parameters
        ----------
        voltage : float, can be int
            Voltage drop measured across thermistor.
        resistence : float or int
            Resistence of the resistor in series with the thermistor.
        coefficients : Iterable (list, tuple) or ndarray
            Coefficients to be used in the Steinhart-Hart equation, 
            supplied by the manufacturer of the thermistor.  The first
            coefficient should be at index 0, followed by the subsequent
            coefficients at indices 1 and 2. 
        """
        C1 = coefficients[0]
        C2 = coefficients[1] 
        C3 = coefficients[2]
        
        thermistor_resistence = resistence*(1/voltage - 1)
        log_thermistor_resistence = np.log(thermistor_resistence)

        temperature = (1/(C1
                          + C2*log_thermistor_resistence
                          + C3*(log_thermistor_resistence**3)
                         )
                      )

        return temperature


    pin_connection = connect_to_arduino(port=arduino_info["port"],
                                        pin=arduino_info["pin"])
    
    readings = np.array([])
    while len(readings) < data_points:
        voltage_reading = pin_connection.read()
        if type(voltage_reading) == float:
            readings = np.append(readings, voltage_reading)
            time.sleep(seconds / data_points)
        else:
            time.sleep(1)
    
    temperatures_K = Steinhart_Hart(voltage=readings,
                                  resistence=arduino_info["resistence"],
                                  coefficients=arduino_info["coefficients"])

    average_temperature_K = np.mean(temperatures_K)

    average_temperature_F = (average_temperature_K - 273.15)*(9/5) + 32 
    
    return int(average_temperature_F)


# ----------------------------------------------------------------------
# GET OUTSIDE TEMPERATURE

def get_outside_temperature(site_info: dict) -> str:
    """Return current temperature as reported by specified weather
    station.
    
    Parameters
    ----------
    site_info : dict
        Dict containing information about what site to visit and which
        element contains temperature reading as text.
    ```
    example_nyc = {
        "url": "https://www.weather.gov/okx/"
        "HTML element type": "span"
        "HTML class name": "myfcst-tempf"
    }
    ```

    Example
    ----------
    >>> get_outside_temperature(site_info=example_nyc)
    "46°F"
    """
    try:
        page = requests.get(site_info["url"])
    except:
        raise Exception("Bad URL")

    soup = BeautifulSoup(page.text, "lxml")
    temperature_element = soup.find(site_info["HTML element type"],
                                    {"class": site_info['HTML class name']}
                                   )
    temperature = temperature_element.text
    if temperature is not None:
        return temperature
    else:
        raise Exception("Couldn't find element on page")