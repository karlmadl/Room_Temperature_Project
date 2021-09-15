from datetime import date, datetime
import data_collection_functions as dcf
log = "02_Prepare/Data-Collection_and_Upload/log.txt"


with open(log, 'a') as log:
    log.write("\n" + "----------------------------------------------------" + "\n\n")
    log.write(str(date.today()) + " | " + str(datetime.now().strftime("%H:%M")) + " | " + "Operation ran ")



    try: 
        data = {
            "time": datetime.now().strftime("%H:%M"),
            "date": date.today(),
            "season": dcf.get_season(),
            "inside_temperature": dcf.temperature_reader(),
            "outside_temperature": dcf.weather_temperature()
        }

        dcf.insert_into_MySQL(data)



        log.write("successfully" + "\n")

    except Exception as Argument:
        log.write("unsuccessfully" + "\n")
        log.write(str(Argument) + "\n")
