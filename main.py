from datetime import date, datetime
from Season.season_getter import get_season
from Arduino_Reading.arduino_reading import temperature_reader
from Weather_Data.weather_data import weather_temperature
from MySQL.mysql_part import insert_into_MySQL


data = {
    "time": datetime.now().strftime("%H:%M"),
    "date": date.today(),
    "season": get_season(),
    "inside_temperature": temperature_reader(data_points=10, seconds=10),
    "outside_temperature": weather_temperature()
}

insert_into_MySQL(data)
