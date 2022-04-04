arduino_info = {
    "port": "COM3",                # arduino-computer connection port
    "pin": "a:0:i",                 # pin on arduino that reads voltage across thermistor
    "resistence": 10000,  # resistence of resistor in thermistor-resistor circuit
    "coefficients": [1.009249522e-03,
                     2.378405444e-04,
                     2.019202697e-07], # Steinhart-Hart coefficients for thermistor
}

MySQL_credentials = {
    "host": "",
    "user": "",
    "password": "",
    "database": "",
    "table": ""
}

temp_site_info = {
    "url": "https://www.wunderground.com/weather/us/nj/howell-township/KNJHOWEL37",                # site address to get outside temperature from
    "HTML element type": "span",   # div, span, p, etc. that temperature is
    "HTML class name": "wu-value wu-value-to",     # HTML class name of element containing current temperature
}