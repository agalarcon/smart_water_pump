"""
Filename: main.py
Author: Andrew Alarcon
Date: 2025-09-07
Version: 1.0.0
Description: This script is designed for a Raspberry Pi Pico W with RP2040 
connected to the following peripherals: a Level Sense LS2600 Surface Liquid 
Sensor, and a Tolako 5V Relay Module powering the Fielect 5-12V Self Priming 
Diaphragm Pump Motor. The purpose is to power the pump automatically on 
detection of a water leak through the water sensor. A 2K ohm resistor was used 
as a pull-down resistor for the water sensor circuit.
"""

## Imports ##
from machine import Pin
from machine import ADC
from time import sleep

## Definitions ##
# Pin Definitions
led     = Pin('LED', Pin.OUT)
"""LED Pin"""
wp      = Pin(28, Pin.OUT)
"""Water pump power enable PIN"""
ws_pwr  = Pin(22, Pin.OUT)
"""Water sensor power PIN"""
ws      = ADC(Pin(27))
"""Water sensor ADC (Analog to Digital Converter) Pin"""

# Globals
g_time_water_detected = 0
"""The time in seconds since the first detection of water"""
g_threshold_time = 5
"""The time to wait in seconds when the threshold value was initially reached
before turning on the pump"""
g_threshold_water_sensor = 9000
"""The ADC sensor value threshold for detecting water"""
g_debug = False
"""Boolean for enabling or disabling debug print statements"""

# Pin Definitions
led     = Pin('LED', Pin.OUT)
"""LED Pin"""
wp      = Pin(28, Pin.OUT)
"""Water pump power enable PIN"""
ws_pwr  = Pin(22, Pin.OUT)
"""Water sensor power PIN"""
ws      = ADC(Pin(27))
"""Water sensor ADC (Analog to Digital Converter) Pin"""

# Methods
def blink(blink_count, blink_period):
    """This function is a wrapper to blink the led for a consecutive amount of 
    times with a period of time wait in between.

    Args:
        blink_count (int): The number of times to blink the LED
        blink_period (double): The amount of time to wait between each blink of
         the LED
    """
    for iter in range(blink_count):
        led.high()
        sleep(blink_period)
        led.low()
        sleep(blink_period)
    return

def debug_print(debug_statement):
    """This function prints a debug statement if the g_debug bool is true

    Args:
        debug_statement (string): Statement to print
    """
    if(g_debug):
        print(debug_statement)
    return

# Toggle water sensor pwr pin high
ws_pwr.high()

debug_print('Water Pump Device v1.0.0')
blink(3,0.2)
debug_print('Entering Main Loop')
while True:
    ws_reading = ws.read_u16()
    debug_print(f'Water Sensor Reading: {ws_reading}')
    if(ws_reading < g_threshold_water_sensor):
        led.low()
        g_time_water_detected = 0
        debug_print('Detecting some DRY-ASS conditions')
        wp.low()
    elif g_time_water_detected < g_threshold_time and \
            ws_reading >= g_threshold_water_sensor:
        g_time_water_detected = g_time_water_detected + 1
        blink(1,0.5)
        debug_print(f'Something be suspicious... {g_time_water_detected}/{g_threshold_time}')
    elif g_time_water_detected >= g_threshold_time and \
            ws_reading >= g_threshold_water_sensor:
        led.high()
        g_time_water_detected = g_time_water_detected + 1
        debug_print('Some bitch poured water on me!')
        debug_print(f'{g_time_water_detected} sec since 1st detect')
        if(g_time_water_detected<10 or g_time_water_detected%10 != 0):
            debug_print('Pumping!')
            wp.high()
        else:
            debug_print('Letting motor rest!')
            wp.low()
    sleep(1)