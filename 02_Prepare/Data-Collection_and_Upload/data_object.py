from datetime import datetime, date   
from mysql.connector import connect, Error

import data_collection_functions as dcf


class Data:
    """Collects data as attributes to insert into MySQL database.  

    This class takes no parameters and data point attributes (stored as class
    attributes) are gathered upon instantiation.
    """
    def __init__(self):
        self.time = datetime.now().strftime("%H:%M")
        self.date = date.today()
        self.season = dcf.get_season()
        self.inside_temperature = dcf.record_inside_temperature()
        self.outside_temperature = int(dcf.get_outside_temperature())

    @property
    def data(self) -> dict:
        """Return dict of instance attribute names (as keys) and their values"""
        return vars(self)


    def insert_into_MySQL(self, db_info: dict):
        """Insert attributes into MySQL table described by db_info.

        Parameters
        ----------
        db_info : dict
            Dict must have "host", "user", "password", "database", and "table"
            keys with proper values as strings.
        
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

