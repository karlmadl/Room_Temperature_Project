import time
import math
import requests
from typing import Union
from datetime import date, datetime

from bs4 import BeautifulSoup
import pyfirmata

from user_info import arduino_info as AI



Y = 2000  # Dummy leap year to allow input X-02-29 (leap day)
seasons = [('winter', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('spring', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('summer', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('autumn', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('winter', (date(Y, 12, 21),  date(Y, 12, 31)))]

# Returns the season based on current date, based on northern hemisphere
def get_season():
    now = date.today()
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)


def record_inside_temperature(data_points: int = 10, 
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
    def connect_to_arduino(port, pin):
        """Connect to Arduino board at specified port and watches
        specified pin.  

        Parameters
        ----------
        port : str
            The connection port between Arduino and computer.  The name
            of this port can be found in the Arduino IDE when connected
            to a board.
        pin : str

        """
    # Connects to Arduino and initializes pyfirmata
    ARDUINO_BOARD = pyfirmata.Arduino( AI['port'] )
    PYFIRMATA_ITERATOR = pyfirmata.util.Iterator(ARDUINO_BOARD)
    PYFIRMATA_ITERATOR.start()  
    analog_input = ARDUINO_BOARD.get_pin( AI['pin'] )   # Points to which analog pin voltages should be read from
    

    # Necessary constants for calculation; resistor resistence and Steinhart-Hart coefficients
    RESISTOR = AI['resistor_resistence']
    C1, C2, C3 = AI['coeff_1'], AI['coeff_2'], AI['coeff_3']
    readings = []
    
    while len(readings) < data_points:
        voltage_reading = analog_input.read()
        
        # If statement to account for first few values read as NoneType
        if type(voltage_reading) == float:

            voltage_reading *= 1023   # Converts pyfirmata analog reading back to arduino analog (0-1 to 0-1023)
            
            # Solves for thermistor resistence then takes then log which is needed for Steinhart-Hart
            thermistor_resistence = RESISTOR * (1023.0 / voltage_reading - 1.0)
            log_thermistor_resistence = math.log(thermistor_resistence)
            
            # Steinhart-Hart and conversion from Kelvin to Fahrenheit
            T_kelvin = (1.0 / (C1 + C2*log_thermistor_resistence + C3*(log_thermistor_resistence ** 3)))
            T_celsius = T_kelvin - 273.15
            T_fahrenheit = (T_celsius * 9.0)/ 5.0 + 32.0
            
            readings.append(T_fahrenheit)
        
        time.sleep(seconds / data_points)
    
    average_temperature = int(sum(readings) / len(readings))
    
    return average_temperature


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