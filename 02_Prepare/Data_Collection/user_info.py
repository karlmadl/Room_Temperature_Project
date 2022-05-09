Arduino_Circuit = {
    "port": "",          # arduino-computer connection port
    "pin": "",           # pin on arduino that reads voltage across thermistor
    "resistence": 0,     # resistence of resistor in thermistor-resistor circuit
    "coefficients": [    # Steinhart-Hart coefficients for thermistor
        0,
        0,
        0
    ]
}

MySQL_credentials = {
    "host": "",
    "user": "",
    "password": "",
    "database": "",
    "table": ""
}

Temperature_Site_Info = {
    "url": "",                # site address to get outside temperature from
    "HTML element type": "",  # div, span, p, etc. that temperature is
    "HTML class name": ""     # HTML class name of element containing current temperature
}