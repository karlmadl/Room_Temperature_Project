from Season.season_getter import get_season
from datetime import date, datetime
from Arduino_Reading.arduino_reading import temperature_reader
from Weather_Data.weather_data import weather_temperature
from MySQL.mysql_part import data_entry_to_MySQL


parameters = {
    "time": datetime.now().strftime("%H:%M"),
    "date": date.today(),
    "season": get_season(),
    "inside_temperature": temperature_reader(),
    "outside_temperature": weather_temperature()
}

data_entry_to_MySQL(parameters)
