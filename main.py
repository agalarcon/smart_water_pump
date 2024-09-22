from machine import Pin
from machine import ADC
from time import sleep

led = Pin('LED', Pin.OUT)
water_pump = Pin(28, Pin.OUT)
water_sensor = ADC(Pin(27))
print('Water Pump Project Prototype')

while True:
    reading = water_sensor.read_u16()
    print(reading)
    if(reading > 1000):
        led.low()
        print('Detecting some DRY-ASS conditions')
    else:
        led.high()
        print('Some bitch poured water on me!')
    sleep(1)