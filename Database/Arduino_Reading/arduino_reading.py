import time
from typing import Iterator
import pyfirmata
import math
from user_info.arduino_location import arduino_info as AI


def temperature_reader(data_points, seconds):                       # params refer to number of desired data points and how long of a duration they're to be taken over

    ARDUINO_BOARD = pyfirmata.Arduino( AI['port'] )                 # points to the port arduino is connected to
    PYFIRMATA_ITERATOR = pyfirmata.util.Iterator(ARDUINO_BOARD)     # initializes pyfirmata
    PYFIRMATA_ITERATOR.start()
    analog_input = ARDUINO_BOARD.get_pin( AI['pin'] )               # points to which analog pin voltages should be read from

    R1 = AI['resistor_resistence']                                  # resistence of resistor in series with thermistor
    C1, C2, C3 = AI['coeff_1'], AI['coeff_2'], AI['coeff_3']        # manufacturer LUT constants / Steinhart-Hart constants for particular thermistor
    readings = []
    
    while len(readings) < data_points:
        voltage_reading = analog_input.read()
        
        if type(voltage_reading) == float:                              # if statement required since first few readings will be reported as NoneType
            voltage_reading *= 1023                                     # converts pyfirmata analog reading back to arduino analog (0-1 to 0-1023)
            
            R2 = R1 * (1023.0 / voltage_reading - 1.0)                  # solves for thermistor resistence
            logR2 = math.log(R2)
            
            T_kelvin = (1.0 / (C1 + C2*logR2 + C3*logR2*logR2*logR2))   #solves steinhart-hart eqn and converts kelvin to celsius then to fahrenheit
            T_celsius = T_kelvin - 273.15
            T_fahrenheit = (T_celsius * 9.0)/ 5.0 + 32.0
            
            readings.append(T_fahrenheit)
        
        time.sleep(seconds / data_points)
    
    average_temperature = int(sum(readings) / 10)
    
    return average_temperature
