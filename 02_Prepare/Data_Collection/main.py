from datetime import date, datetime

from Data_Collection_Tools.data_object import Data
import user_info as info


Log = "02_Prepare/Data-Collection_and_Upload/log.txt"

with open(Log, 'a') as log:
    log.write("\n"
              + "----------------------------------------------------"
              + "\n\n"
              + str(date.today())
              + " | "
              + str(datetime.now().strftime("%H:%M"))
              + " | "
              + "Operation ran ")

    try: 
        observation = Data(Arduino_Info=info.Arduino_Circuit,
                           Temp_Site_Info=info.Temperature_Site_Info)
        observation.insert_into_MySQL(info.MySQL_credentials)
        log.write("successfully" + "\n")

    except Exception as Argument:
        log.write("unsuccessfully" + "\n")
        log.write(str(Argument) + "\n")
