from machine import Pin, ADC, I2C
import time
from imu import MPU6050
from easy_comms import Easy_comms
import utime
import math

GMRPin = Pin(28, Pin.IN)
LEDPin = Pin(25, Pin.OUT)

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

i2c = I2C(0, sda=Pin(12), scl=Pin(13), freq=200000)
imu = MPU6050(i2c)

currX = 0
currY = 0
currZ = 0
fast = 10
hast = -10
altx = 0
alty = 0
altz = 0

prev = 1
curr = 0

count = 0

# sensor id depends on sensor
# sensor 1 or 2
# change accordingly
sensor_id = 1
error_id = 0
com1 = Easy_comms(0, 9600)

start_time = utime.ticks_us()

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
    #print("accelX:", ax,"\t accelY:",ay,"\t accelZ:",az,"\t gyroX:",gx,"\t gyroY:",gy,"\t gyroZ:",gz,"\t temp:",tem,"        ",end="\r")
    
    if currX + currY + currZ == 0:
        currX = ax
        currY = ay
        currZ = az
        
    if abs(currX - ax) > fast or abs(currY - ay) > fast or abs(currY - ay) > fast:
        error_id = 1
        print(ax, ay, az, fast)
        com1.send(f'Sensor {sensor_id} has error {error_id}')

    end_time = utime.ticks_us()
    elapsed_time = utime.ticks_diff(end_time, start_time)
    altx = altx + 0.5 * gx * math.pow(elapsed_time / 1000000, 2)
    alty = alty + 0.5 * gy * math.pow(elapsed_time / 1000000, 2)
    altz = altz + 0.5 * gz * math.pow(elapsed_time / 1000000, 2)

    if altx <= hast or alty <= hast or altz <= hast:
        error_id = 2
        print(altx, alty, altz, hast)
        com1.send(f'Sensor {sensor_id} has error {error_id}')

    if abs(gx) >= 60 or abs(gy) >= 60 or abs(gz) >= 60:
        error_id = 3
        print(gx, gy, gz)
        com1.send(f'Sensor {sensor_id} has error {error_id}')
    
    while error_id != 0:
        message = ""
        message = com1.read()

        if message == "Button Pressed":
            error_id = 0
            count = 0
            message = ""
    
    while not(GMRPin.value()):
        LEDPin.value(1)
        if prev != curr:
            curr = 1
            count += 1
            time.sleep(sensor_id * 0.1)
            com1.send(f'Sensor {sensor_id} has wheel {count}')
    LEDPin.value(0)
    curr = 0
    start_time = utime.ticks_us()
