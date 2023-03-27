from machine import Pin, I2C
import time
from imu import MPU6050

led = Pin('LED', Pin.OUT)
button1 = Pin(14, Pin.OUT)
button2 = Pin(15, Pin.OUT)
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

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

num1 = 0
num2 = 0
d0 = 0
d1 = 0
d2 = 0
d3 = 0
c0 = 0
c1 = 0
c2 = 0
c3 = 0

prev1 = 1
prev2 = 1
curr1 = 0
curr2 = 0

def print_gyro(ax, ay, az, gx, gy, gz, tem):
    print(ax,"\t",ay,"\t",az,"\t",gx,"\t",gy,"\t",gz,"\t",tem,"        ",end="\r")

while True:
    d0 = num1 % 2
    d1 = num1 // 2 % 2
    d2 = num1 // 4 % 2
    d3 = num1 // 8 % 2
    
    c0 = num2 % 2
    c1 = num2 // 2 % 2
    c2 = num2 // 4 % 2
    c3 = num2 // 8 % 2
    
    n0.value(d0)
    n1.value(d1)
    n2.value(d2)
    n3.value(d3)
    
    m0.value(c0)
    m1.value(c1)
    m2.value(c2)
    m3.value(c3)
    
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    
    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)
    gx=round(imu.gyro.x)
    gy=round(imu.gyro.y)
    gz=round(imu.gyro.z)
    tem=round(imu.temperature,2)
    print(ax,"\t",ay,"\t",az,"\t",gx,"\t",gy,"\t",gz,"\t",tem,"        ",end="\r")
    
    if num1 == num2:
        green.value(1)
        red.value(0)        
        if num1 + num2 != 0:
            num1 = 0
            num2 = 0
        
    else:
        red.value(1)
        green.value(0)
    
    if button1.value():
        if prev1 != curr1:
            led.value(1)
            curr1 = 1
            time.sleep(0.2)
            num1 = (num1 + 1) % 10
            print("press", num1)
            print("C", temperature)
            print_gyro(ax, ay, az, gx, gy, gz, tem)
            
        else:
            led.value(0)
            curr1 = 0
            time.sleep(0.2)
            num1 = (num1 + 1) % 10
            print("unpress", num1)
            print("C", temperature)
            print_gyro(ax, ay, az, gx, gy, gz, tem)
        
    if button2.value():
        if prev2 != curr2:
            led.value(1)
            curr2 = 1
            time.sleep(0.2)
            num2 = (num2 + 1) % 10
            print("press2", num2)
            print("C", temperature)
            print_gyro(ax, ay, az, gx, gy, gz, tem)
            
        else:
            led.value(0)
            curr2 = 0
            time.sleep(0.2)
            num2 = (num2 + 1) % 10
            print("unpress2", num2)
            print("C", temperature)
            print_gyro(ax, ay, az, gx, gy, gz, tem)
