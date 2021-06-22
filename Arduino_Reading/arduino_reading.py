import time
from typing import Iterator
import pyfirmata
import math


# pc coontrolled temperature reading with thermistor

def temperature_reader():

    ARDUINO_BOARD = pyfirmata.Arduino('COM3')
    PYFIRMATA_ITERATOR = pyfirmata.util.Iterator(ARDUINO_BOARD)
    PYFIRMATA_ITERATOR.start()
    analog_input = ARDUINO_BOARD.get_pin('a:0:i')

    R1 = 10000
    C1, C2, C3 = 1.009249522e-03, 2.378405444e-04, 2.019202697e-07
    readings = []
    
    while len(readings) < 10:
        voltage_reading = analog_input.read()
        
        if type(voltage_reading) == float:
            voltage_reading *= 1023
            R2 = R1 * (1023.0 / voltage_reading - 1.0)
            logR2 = math.log(R2)
            T_kelvin = (1.0 / (C1 + C2*logR2 + C3*logR2*logR2*logR2))
            T_celsius = T_kelvin - 273.15
            T_fahrenheit = (T_celsius * 9.0)/ 5.0 + 32.0
            readings.append(T_fahrenheit)
        
        time.sleep(2)
    
    average_temperature = int(sum(readings) / 10)
    
    return average_temperature
