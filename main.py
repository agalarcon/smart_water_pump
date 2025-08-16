from machine import Pin
from machine import ADC
from time import sleep

led = Pin('LED', Pin.OUT)
water_pump = Pin(28, Pin.OUT)
water_sensor = ADC(Pin(27))
print('Water Pump Project Prototype')
counter = 0
threshold_time = 10
threshold_water_sensor = 7000

led.high()
sleep(1)
led.low()
sleep(1)
led.high()
sleep(1)
led.low()
sleep(1)
led.high()
sleep(1)
led.low()
sleep(1)

while True:
    reading = water_sensor.read_u16()
    print(reading)
    if(reading > threshold_water_sensor):
        led.low()
        counter = 0
        print('Detecting some DRY-ASS conditions')
        water_pump.low()
    elif counter < threshold_time and reading <= threshold_water_sensor:
        counter = counter + 1
        led.high()
        sleep(1)
        led.low()
        print(f'Something be suspicious... {counter}/{threshold_time}')
    elif counter >= threshold_time and reading <= threshold_water_sensor:
        led.high()
        print('Some bitch poured water on me!')
        water_pump.high()
        sleep(10)
    sleep(1)