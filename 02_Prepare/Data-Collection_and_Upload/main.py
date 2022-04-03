from datetime import date, datetime

from data_object import Data
from user_info import MySQL_credentials


Log = "02_Prepare/Data-Collection_and_Upload/log.txt"

with open(Log, 'a') as log:
    log.write("\n" + "----------------------------------------------------"
              + "\n\n")
    log.write(str(date.today()) + " | " + str(datetime.now().strftime("%H:%M"))
              + " | " + "Operation ran ")

    try: 
        observation = Data()

        observation.insert_into_MySQL(MySQL_credentials)

        log.write("successfully" + "\n")

    except Exception as Argument:
        log.write("unsuccessfully" + "\n")
        log.write(str(Argument) + "\n")
