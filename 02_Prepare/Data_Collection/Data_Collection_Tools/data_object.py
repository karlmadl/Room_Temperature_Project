from datetime import datetime, date   
from mysql.connector import connect, Error

import data_collection_functions as dcf


class Data:
    """Collects data as attributes to insert into MySQL database.  

    Data point attributes (stored as class attributes) are gathered upon
    instatiation.  Use insert_into_MySQL method with dict containing
    MySQL database.  Class attribute names will be used as column names
    for INSERT INTO SQL statement.

    Parameters
    ----------
    Arduino_Info : dict
        Dict containing all necessary information to allow a connection
        to an Arduino via pyfirmata and other information about the
        thermistor-resistor circuit connected to the Arduino.
    ```
    Arduino_Info = {
        "port": "",
        "pin": "",
        "resistence": 0,
        "coefficients": [0, 0, 0]
        }
    ```
    Temp_Site_Info : dict
        Dict containing neccessary information about the website to
        retrieve current reported outdoor temperature from.
    ```
    Temp_Site_Info = {
        "url": "",
        "HTML element type": "",
        "HTML class name": ""
        }
    ```
    """
    def __init__(self, Arduino_Info: dict, Temp_Site_Info: dict):
        self.time = datetime.now().strftime("%H:%M")
        self.date = date.today()
        self.season = dcf.get_season()
        self.inside_temperature = dcf.record_inside_temperature(arduino_info=Arduino_Info)
        self.outside_temperature = int(dcf.get_outside_temperature(site_info=Temp_Site_Info))

    @property
    def data(self) -> dict:
        """Return dict of instance attribute names (as keys) and their
        values"""
        return vars(self)


    def insert_into_MySQL(self, db_info: dict):
        """Insert attributes into MySQL table described by db_info.

        Parameters
        ----------
        db_info : dict
            Dict must have "host", "user", "password", "database", and
            "table" keys with proper values as strings.
        
        Example
        ----------
        ```
        example_dict = {
            "host": "localhost",
            "user": "admin",
            "password": "securepassword",
            "database": "MyDatabase",
            "table": "Table_1"
        }

        observation = Data()

        observation.insert_into_MySQL(db_info=example_dict)
        ```
        """
        statement = f"""INSERT INTO {db_info['table']} ({', '.join(self.data)}) 
                     VALUES ({('%s, '*len(self.data)).rstrip(', ')})"""  
        values = [*self.data.values()]

        try:
            with connect(
                host = db_info['host'],
                user = db_info['user'],
                password = db_info['password'],
                database = db_info['database']
            ) as connection:

                cursor = connection.cursor()
                cursor.execute(statement, values)
                
                connection.commit()

        except Error as e:
            return e

