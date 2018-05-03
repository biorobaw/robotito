#!/usr/bin/python
import RPi.GPIO as GPIO
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from Encoder import Encoder



class MotorDriver:
    pins=[[4, 17], [18, 27], [22, 23], [24, 25]]
    def __init__(self):
        ##Motor Driver
        self.mh = Adafruit_MotorHAT(addr=0x60)
        
        ##Motors
        self.motors=[]
        self.speeds=[0]*4
        for i in range(1,5):
            self.motors.append(self.mh.getMotor(i))
            
        ##Encoders
        self.encoders=[]
        for i in range(0,4):
            e = Encoder(self.pins[i]) 
            self.encoders.append(e)
        
    def release(self):
        for i in range(4):
            self.speeds[i]=0
            self.motors[i].run(Adafruit_MotorHAT.RELEASE)
    
    def setSpeed(self, num, speed):
        print('Set speed of motor: %s to %s' %(num, speed))
        self.speeds[num] = speed
        self.motors[num].setSpeed(speed)

    def stop(self, num):
        self.encoders[num].count=0
        print('Motor %s stopped.' %num)
        self.speeds[num] = 0
        self.motors[num].setSpeed(0)
        
