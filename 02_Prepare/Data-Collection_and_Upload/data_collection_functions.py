from datetime import date, datetime

Y = 2000 # dummy leap year to allow input X-02-29 (leap day)
seasons = [('winter', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('spring', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('summer', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('autumn', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('winter', (date(Y, 12, 21),  date(Y, 12, 31)))]


# returns the season based on current date, based on northern hemisphere
def get_season():
    now = date.today()
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)





import time
from typing import Iterator
import pyfirmata
import math
from user_info import arduino_info as AI


def temperature_reader(data_points=10, seconds=10):                 # params refer to number of desired data points and how long of a duration they're to be taken over

    ARDUINO_BOARD = pyfirmata.Arduino( AI['port'] )                 # points to the port arduino is connected to
    PYFIRMATA_ITERATOR = pyfirmata.util.Iterator(ARDUINO_BOARD)     # initializes pyfirmata
    PYFIRMATA_ITERATOR.start()
    analog_input = ARDUINO_BOARD.get_pin( AI['pin'] )               # points to which analog pin voltages should be read from

    R1 = AI['resistor_resistence']                                  # resistence of resistor in series with thermistor
    C1, C2, C3 = AI['coeff_1'], AI['coeff_2'], AI['coeff_3']        # manufacturer LUT constants / Steinhart-Hart constants for particular thermistor
    readings = []
    
    while len(readings) < data_points:
        voltage_reading = analog_input.read()
        
        if type(voltage_reading) == float:                              # if statement required since first few readings will be reported as NoneType
            voltage_reading *= 1023                                     # converts pyfirmata analog reading back to arduino analog (0-1 to 0-1023)
            
            R2 = R1 * (1023.0 / voltage_reading - 1.0)                  # solves for thermistor resistence
            logR2 = math.log(R2)
            
            T_kelvin = (1.0 / (C1 + C2*logR2 + C3*logR2*logR2*logR2))   #solves steinhart-hart eqn and converts kelvin to celsius then to fahrenheit
            T_celsius = T_kelvin - 273.15
            T_fahrenheit = (T_celsius * 9.0)/ 5.0 + 32.0
            
            readings.append(T_fahrenheit)
        
        time.sleep(seconds / data_points)
    
    average_temperature = int(sum(readings) / len(readings))
    
    return average_temperature





from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from user_info import driver_info


# webscrapes to retrieve specified weather station current temperature measurement
def weather_temperature():
    driver: WebDriver = webdriver.Chrome(driver_info['driver_path'])

    
    # silences almost all of the console logging done by selenium
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    
    
    driver.get(driver_info['site'])
    temperature_html = driver.find_element_by_xpath(driver_info['temp_xpath'])
    temperature = int(temperature_html.text)

    driver.quit()

    return temperature  





from user_info import My_SQL_credentials as CREDS   # imports dictionary of MySQL credentials and info (database, table)
from mysql.connector import connect, Error

# creates the query and connects to the mysql database before inserting data dictionary as data into the table  
def insert_into_MySQL(data: dict):
    
    query = f"INSERT INTO {CREDS['table']} ({', '.join(data)}) VALUES ({('%s, '*len(data)).rstrip(', ')})"
    args = [*data.values()]
    
    try:
        with connect(
            host = CREDS['host'],
            user = CREDS['user'],
            password = CREDS['password'],
            database = CREDS['database']
        ) as connection:

            cursor = connection.cursor()
            cursor.execute(query, args)
            
            connection.commit()

    except Error as e:
        print(e)
