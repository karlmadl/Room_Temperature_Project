---
title: Data Collection and Storage Outline
author: Karl Madl
date: 01 September 2021
---


# Data Collection
* Data will be collected and uploaded automatically by a recurring scheduled Python script **main&#46;py** found in **02_Prepare/Data-Collection_and_Upload**.

* Windows Task Scheduler is used to run a batch file pointing to the path of **python.exe** and **main&#46;py** to execute **main&#46;py** every four hours at 00:00, 04:00, 08:00, 12:00, 16:00, and 20:00.

    ## **main&#46;py**
    * The first three lines of **main&#46;py** are the relevant imports: date and dateime, an import containing a **log.txt** file path, and an import of a local Python file containing the functions necessary to collect the desired data (as well as a function to format this data and upload it to storage).

    * I decided to forego the Python's logging and create a very simple custom log, therefore the main logic of **main&#46;py** is wrapped in a *with open()* and a nested *try-except* structure.

    * Inside the *try* section, the script builds a dictionary **data** with keys that match the column names of our database - we'll use this to upload the data to the database. Each value is assigned by either *date*/*datetime* functions or by a function that was imported from the local Python file, **data_collection_functions&#46;py**.

    * The **data** dictionary is then passed to the *insert_into_MySQL* function to upload to the MySQL database. If all of these steps are executed then the *try* clause reaches a line that will write to the **log** that the operation was run to completion. Otherwise, the script will write the error message thrown to the same **log**. 

    ## **data_collection_functions&#46;py**

    ### *get_season()*
    * Credit for this function goes to user *jfs* on Stack Overflow for this [reply](https://stackoverflow.com/a/28688724). 
    A list containing 5 (winter is broken down to beginning of year and end of year) tuples of pairs (season, date range). The function then matches the month and day of the current time to the corresponding range and returns the associated season.

    ### *temperature_reader()*
    * This function's purpose is to connect to an Arduino that drives a thermistor circuit, convert this reading, and use it to complete a calculation to give a very good approximation of the temperature of the thermistor (which is, ideally, at equlibrium with the air around it, giving the temperature of the air inside the room).

        > The circuit is a simple thermistor-resisitor series cicuit.
        >   #### ![alt text](circuit.png "Thermistor-Resistor Circuit")

    * To keep all the main logic of the function in Python, Pyfirmata was used to connect to the Arduino with the Pyfirmata script uploaded to it. However, the code was originally developed in the Arduino language which reads voltages from 0 to 1023 whereas Pyfirmata normalizes these readings from 0.0 to 1.0. This is why **voltage_reading** gets scaled by 1023.

    * The rest of the function is simply the execution of the [Steinhart-Hart equation](https://en.wikipedia.org/wiki/Steinhart%E2%80%93Hart_equation) and then a conversion from Kelvin to Fahrenheit. This is all first wrapped in an *if* statement to account for the first few readings always returning null values as things are being initialized. 

    * This is then wrapped in a *while* statement, which is what the parameters of **data_points** and **seconds** are for. By default, both of these values are 10 and they tell the function how many data points should be taken and then averaged for a final result and the total time length (in seconds, obviously) over which those data points should be taken. Therefore, by default the function will take 10 data points, 1 every second.

    ### *weather_temperature()*
    * This function is a very simple webscraper that goes to a specified weather website, uses a specified XPATH found in the HTML of the website that points to the current outdoor temperature posted and returns the text value of that HTML element.

    * In this case, [wunderground.com](wundergound.com) was used as the website and the closest weather station to the location of the building where the indoor temperatures were being measured was the one chosen for outdoor temperatures. This station is less than a half-mile away so we can be confident that the general temperature reportings were representative of the temperature outside the working building.

    ### *insert_into_MySQL()*
    * This function has nothing to do with data collection, but rather takes the **data** dictionary that was created and builds an "INSERT INTO, VALUES" SQL statement before connecting to the MySQL database using *mysql.connector* package.

    * When the query is being constructed, it first specifies the columns that will be inserted into by joining the keys of the **data** dictionary. Then it joins as many **%s**'s as there are columns, as these will be the placeholders for the values to be inserted which will be stored in the variable **args**. 

    * The function then uses the login information (which has been redacted from the repository for safety measures) from **user_info** to connect to the database.

    * Finally, the cursor executes the the query using *execute()* with arguments **query** and **args**. Any exceptions that are thrown are printed to the console and logged in **log**, though this is handled by **main&#46;py**.   

# Data Storage
The data will be stored in a MySQL database. There's particular advantage to using MySQL in this case over a lighter weight option such as SQLite, it was simply chosen because I wanted to work with it.