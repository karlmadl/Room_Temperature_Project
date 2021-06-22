from Arduino_Reading.arduino_reading import temperature_reader
from Weather_Data.weather_data import weather_temperature
from Season.season_getter import get_season
from datetime import date, datetime
from MySQL.mysql_part import data_entry_to_MySQL


inside_temperature = temperature_reader()
outside_temperature = weather_temperature()
season = get_season()
current_date = date.today()
current_time = datetime.now().strftime("%H:%M")

data_entry_to_MySQL(inside_temperature, outside_temperature, season, current_date, current_time)
