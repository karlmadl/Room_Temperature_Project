arduino_info = {
    "port": "",                     # arduino-computer connection port
    "pin": "",                      # pin on arduino that reads voltage across thermistor
    "resistor_resistence": 0,       # resistence of resistor in thermistor-resistor circuit
    "coeff_1": 0,                   # Steinhart-Hart coefficients for thermistor
    "coeff_2": 0,
    "coeff_3": 0,
}

My_SQL_credentials = {
    "host": "",
    "user": "",
    "password": "",
    "database": "",
    "table": ""
}

driver_info = {
    "driver_path": "",              # path to local webdriver to do the webscraping
    "site": "",                     # site address to get outside temperature from
    "temp_xpath": ""                # HTML xpath of element containing current temperature
}