from machine import Pin, ADC
import time

GMRPin = Pin(0, Pin.IN)
LEDPin = Pin(25, Pin.OUT)

#adc = ADC(Pin(26, mode=Pin.IN))

while True:
    while GMRPin.value():
        LEDPin.value(0)
    LEDPin.value(1)