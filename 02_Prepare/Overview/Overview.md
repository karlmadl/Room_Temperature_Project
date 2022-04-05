---
Title: Data Collection and Storage Outline
Author: Karl Madl
Date: 01 September 2021
---


# Data Collection
* Data will be collected and uploaded automatically by a recurring scheduled Python script **main&#46;py** found in **02_Prepare/Data_Collection/**.

* Windows Task Scheduler is used to run a batch file pointing to the path of **python.exe** and **main&#46;py** to execute **main&#46;py** every four hours at 00:00, 04:00, 08:00, 12:00, 16:00, and 20:00.

    <br>

    ## **main&#46;py**
    * Instantiates an imported custom *Data* class to create an object with attributes of
        * time
        * date
        * season
        * inside temperature
        * outside temperature 
    
    * Dictionaries containing information about the Arduino circuit and website to be scraped for local weather temperature are imported from **user_info&#46;py** and passed as arguments to the *Data* class.

    * Finally, the *Data* class has an *insert_into_MySQL* method that takes a third dictionary from **user_info&#46;py** as an argument and uses **mysql.connector** to upload the class attribute values into the specified SQL table.

    * I wanted to keep a **log.txt** file to track any possible bugs and to be able to check that the script was executing properly, so I wrapped the main logic of **main&#46;py** in a *with open( )* and a nested *try-except* structure.

    <br>
    <br>

    ## **data_object&#46;py**
    * This file contains only the *Data* class definition; the object to gather the desired data and later upload it to the desired table in a MySQL server database.
    ### Attributes
    * Attributes are assigned to the output of their respective functions, some of which stem from the time and datetime modules, the rest of which are imported from **data_collection_functions&#46;py**.
    ### Properties
    * There exists only the *data* property which just returns the output of *vars( )* called on the instantiated object. This output is a dictionary of the attributes and their values that is use in the *insert_into_MySQL( )* method.
    ### Methods
    * The sole method is the *insert_into_MySQL( )* method. This function builds a standard "INSERT INTO" SQL statement based on the attributes of the class and uses **mysql.connector** to connect to and upload the data to a MySQL database.

    <br>
    <br>

    ## **data_collection_functions&#46;py**

    ### *get_season( )*
    * Credit for this function goes to user *jfs* on Stack Overflow for this [reply](https://stackoverflow.com/a/28688724). 
    A list containing 5 (winter is broken down to beginning of year and end of year) tuples of pairs (season, date range). The function then matches the month and day of the current time to the corresponding range and returns the associated season.

    ### *record_inside_temperature( )*
    * This function's purpose is to connect to an Arduino that drives a thermistor circuit, convert this reading, and use it to complete a calculation to give a very good approximation of the temperature of the thermistor (which is, ideally, at equlibrium with the air around it, giving the temperature of the air inside the room).

        > The circuit is a simple thermistor-resisitor series cicuit.
        >   #### ![alt text](circuit.png "Thermistor-Resistor Circuit")

    * To keep all the main logic of the function in Python, Pyfirmata was used to connect to the Arduino with the Pyfirmata script uploaded to it.

    * Two inner functions are created to establish a connection object to the pin that the voltage readings are to be taken from and to use the [Steinhart-Hart equation](https://en.wikipedia.org/wiki/Steinhart%E2%80%93Hart_equation) to convert these voltage readings to temperature. Only the first three terms of the Steinhart-Hart are considered. An *if* statement is used to account for the first few readings always returning null values as things are being initialized. 

    * This is then wrapped in a *while* statement, which is what the parameters of **data_points** and **seconds** are for. By default, both of these values are 10 and they tell the function how many data points should be taken and then averaged for a final result and the total time length (in seconds, obviously) over which those data points should be taken. Therefore, by default the function will take 10 data points, 1 every second.

    ### *get_outside_temperature( )*
    * This function is a very simple webscraper that goes to a specified weather website, uses a specified HTML type and class name found in the HTML of the website that points to the current outdoor temperature posted and returns the text value of that HTML element.

    * In this case, [wunderground.com](https://www.wunderground.com/) was used as the website and the closest weather station to the location of the building where the indoor temperatures were being measured was the one chosen for outdoor temperatures. This station is less than a half-mile away so we can be confident that the general temperature reportings were representative of the temperature outside the working building.
<br>
<br>

# Data Storage
* The data will be stored in a MySQL database. There's no particular advantage to using MySQL in this case over a lighter weight option such as SQLite, it was chosen because I wanted to work with it. The database will also assign an integer **id** to each observation entered into it, autoincremented. The other column data types are as follows:
    * **inside_temperature**: int
    * **outside_temperature**: int
    * **season**: VARCHAR(50)
    * **date**: date
    * **time**: time

* The information in **user_info.py** is stored as dictionaries with each dictionary being used for one at most one of the above functions, the skeleton of which is provided in the **02_Prepare/Data_Collection/** directory. *

* Every run of the script will be recorded into the **log.txt** file in the **02_Prepare/Data_Collection/** directory, as well as whether or not the script ran to completion or was terminated early due to some encountered error, including the thrown error message.

* The cleaned data will be stored in **cleaned_data.csv** in the **03_Process/** directory. Also in this directory will be a PDF version of the data cleaning process and a .txt file with a link to preview the HTML version of the same report (the HTML file is stored in the subdirectory **/Cleaning/**).

* Lastly of note, copies of all reports/presentations will be kept in a separate folder in the main directory of the project in **All_Reports/** for ease of acess for viewers.
