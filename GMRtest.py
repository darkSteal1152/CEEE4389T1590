from machine import Pin, ADC, I2C
import time
from imu import MPU6050

GMRPin = Pin(2, Pin.IN)
LEDPin = Pin(25, Pin.OUT)
buttonR = Pin(21, Pin.OUT)

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

i2c = I2C(0, sda=Pin(12), scl=Pin(13), freq=400000)
imu = MPU6050(i2c)
err = Pin(22, Pin.OUT)
#adc = ADC(Pin(26, mode=Pin.IN))

currX = 0
currY = 0
currZ = 0
fast = 1

while True:
    
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    
    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,1)
    az=round(imu.accel.z,2)
    gx=round(imu.gyro.x, 2)
    gy=round(imu.gyro.y, 2)
    gz=round(imu.gyro.z, 2)
    tem=round(imu.temperature,2)
    print("accelX:", ax,"\t accelY:",ay,"\t accelZ:",az,"\t gyroX:",gx,"\t gyroY:",gy,"\t gyroZ:",gz,"\t temp:",tem,"        ",end="\r")
    
    if currX + currY + currZ == 0:
        currX = ax
        currY = ay
        currZ = az
        
    if abs(currX - ax) > fast or abs(currY - ay) > fast or abs(currY - ay) > fast:
        err.value(1)
    
    if buttonR.value():
        err.value(0)
        currX = ax
        currY = ay
        currZ = az
    
    while not(GMRPin.value()):
        LEDPin.value(1)
    LEDPin.value(0)

