from datetime import date, datetime
from user_info import log
import data_collection_functions as dcf


with open(log, 'a') as log:
    log.write("\n" + "----------------------------------------------------" + "\n\n")
    log.write(str(date.today()) + " | " + str(datetime.now().strftime("%H:%M")) + " | " + "Operation ran ")



    try: 
        data = {
            "time": datetime.now().strftime("%H:%M"),
            "date": date.today(),
            "season": dcf.get_season(),
            "inside_temperature": dcf.temperature_reader(data_points=10, seconds=10),
            "outside_temperature": dcf.weather_temperature()
        }

        dcf.insert_into_MySQL(data)



        log.write("successfully" + "\n")

    except Exception as Argument:
        log.write("unsuccessfully" + "\n")
        log.write(str(Argument) + "\n")
