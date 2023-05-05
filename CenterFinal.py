from machine import Pin
from easy_comms import Easy_comms
import time
import json

led = Pin('LED', Pin.OUT)
#button1 = Pin(14, Pin.OUT)
#button2 = Pin(15, Pin.OUT)
n0 = Pin(18, Pin.OUT)
n1 = Pin(19, Pin.OUT)
n2 = Pin(20, Pin.OUT)
n3 = Pin(21, Pin.OUT)
m0 = Pin(13, Pin.OUT)
m1 = Pin(12, Pin.OUT)
m2 = Pin(11, Pin.OUT)
m3 = Pin(10, Pin.OUT)
green = Pin(26, Pin.OUT)
red = Pin(27, Pin.OUT)
yellow = Pin(15, Pin.OUT)
buttonE = Pin(14, Pin.IN, Pin.PULL_DOWN)

num1 = 0
num2 = 0

prev1 = 1
prev2 = 1
curr1 = 0
curr2 = 0

errDone = 0

sensor_id = 0
error_num = 0
wheel_count = 0

done1 = 0
done2 = 0

com1 = Easy_comms(0, 9600)

def inc(num):
    num = (num + 1) % 10
    return num

def setDisplay(num, side):
    d0 = num % 2
    d1 = num // 2 % 2
    d2 = num // 4 % 2
    d3 = num // 8 % 2

    if side == 0:
        n0.value(d0)
        n1.value(d1)
        n2.value(d2)
        n3.value(d3)
    else:
        m0.value(d0)
        m1.value(d1)
        m2.value(d2)
        m3.value(d3)

def getMes(errDone):
    global sensor_id, error_num, wheel_count
    
    if errDone == 0:
        message = ""
        message = com1.read()
        message_parts = message.split()

        sensor_id = message_parts[1]
        if message_parts[3] == "error":
            error_num = message_parts[4]
            print(f"Sensor {sensor_id} has error {error_num}")
            message = "errorfound"
            print(message)
            return 0
        else:
            wheel_count = message_parts[4]
            print(f"Sensor {sensor_id} has wheel {wheel_count}")
            return 2
    else:
        return 1

setDisplay(num1, 0)
setDisplay(num2, 1)

yellow.value(0)

while True:

    message = ""
    
    if num1 == num2:
        green.value(1)
        red.value(0)
        if num1 + num2 != 0:
            num1 = 0
            num2 = 0
            setDisplay(num1, 0)
            setDisplay(num2, 1)
        
    else:
        red.value(1)
        green.value(0)

    numred = getMes(errDone)
    
    if numred == 0:
        yellow.value(1)
        errDone = 1
    elif numred == 1:
        if buttonE.value():
            print("Button Pressed")
            com1.send("Button Pressed")
            yellow.value(0)
            errDone = 0
    else:
        if sensor_id == "1":
            num1 = inc(num1)
            setDisplay(num1, 0)
        if sensor_id == "2":
            num2 = inc(num2)
            setDisplay(num2, 1)

    time.sleep(0.1)
