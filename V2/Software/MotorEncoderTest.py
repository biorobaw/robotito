#!/usr/bin/python
import time
import atexit
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from MotorDriver import MotorDriver
##Constants
##Full signal(255) to motors
##Theoretical 530rpm / 60s = 8.3rps = .11321s/rot
##Actual (with wheel attached), makes roughly 1 rotation at full speed, no load = 8.5RPS
##148-160encoder signals per revolution
 
##MotorDriver and motors
m=MotorDriver()

#Left Motor
speed=50
while(True):
    input('Press any key to continue')
    for i in range(4):
        m.motors[i].run(Adafruit_MotorHAT.FORWARD)
        m.setSpeed(i,speed)
    while(m.encoders[0].count<10):
        pass
    for i in range(4):
        m.stop(i)    
atexit.register(m.release())        
GPIO.cleanup()   


