arduino_info = {
    "port": "",                # arduino-computer connection port
    "pin": "",                 # pin on arduino that reads voltage across thermistor
    "resistor_resistence": 0,  # resistence of resistor in thermistor-resistor circuit
    "coeff_1": 0,              # Steinhart-Hart coefficients for thermistor
    "coeff_2": 0,
    "coeff_3": 0,
}

MySQL_credentials = {
    "host": "",
    "user": "",
    "password": "",
    "database": "",
    "table": ""
}

temp_site_info = {
    "url": "",                # site address to get outside temperature from
    "HTML element type": "",   # div, span, p, etc. that temperature is
    "HTML class name": "",     # HTML class name of element containing current temperature
}