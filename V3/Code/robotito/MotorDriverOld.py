#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import threading
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from Encoder import Encoder

##Motor       Number
##Front Left  0
##Front Right 1
##Back Left   2
##Back Right  3

##Controls the motor function with encoders
class MotorDriver(threading.Thread):

    
    def __init__(self):
        #THREAD
        
        ##MOTOR DRIVER
        self.mh = Adafruit_MotorHAT(addr=0x60)
        
        ##MOTORS
        self.motors=[]
        for i in range(1,5):
            self.motors.append(self.mh.getMotor(i))   
        
        #ENCODERS
        GPIO.setmode(GPIO.BCM)
        ##Sensor pins for each of the hall effect sensors for each encoder
        ##Encoder      0        1        2        3    
        self.pins = [[4,17], [18,27], [22,23], [24,25]]
        self.pinDict = {4:0, 18:1, 22:2, 24:3} 
        ##Create encoders and interrupt callbacks
        self.encoders=[]
        for i in range(0,4):
            e = Encoder(self.pins[i][0], self.pins[i][1], i) 
            self.encoders.append(e)         
            GPIO.setup(self.pins[i][0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            #Initialize the interrupt - triggers on the rising edge
            GPIO.add_event_detect(self.pins[i][0], GPIO.RISING, callback = self.update)
        
        #MEMBERS
        self.speedTar = 0   #in RPS
        self.speeds = [0]*4 #0-255
        self.time = time.time
        #Testing
        self.count = 0
        
    ##FUNCTIONS
    def release(self):
        for i in range(4):
            self.motors[i].run(Adafruit_MotorHAT.RELEASE)
    
    def setSpeed(self, num):
        self.motors[num].setSpeed(self.speeds[num]) 

    def setRPS(self):
        speed = int(-5.6*(self.speedTar**2)+76*self.speedTar)
        for i in range(4):
            self.speeds[i] = speed
            self.setSpeed(i)
            self.maintainRPS(i)
    
    def maintainRPS(self, num):
        self.count = self.count + 1
        if self.count % 60 == 0:
            print('%.2f, %.2f, %.2f, %.2f'%(self.encoders[0].rps, self.encoders[1].rps, self.encoders[2].rps, self.encoders[3].rps))
            self.count = 0
        if self.encoders[num].rps < self.speedTar + .25:
            self.speeds[num] = self.speeds[num] + 1 
            self.setSpeed(num) 
        elif self.encoders[num].rps > self.speedTar - .25:
            self.speeds[num] = self.speeds[num] - 1 
            self.setSpeed(num)    
         
    def stop(self, num):
        self.encoders[num].count=0
        self.encoders[num].elapsed=0
        self.encoders[num].rps=0
        self.speedTar = 0
        self.speed = 0
        self.motors[num].setSpeed(0)
             
    def update(self, event):
        num = self.pinDict[event]
        currentTime = time.time()        
        self.encoders[num].count = self.encoders[num].count + .5
        self.encoders[num].elapsed = currentTime - self.encoders[num].lastReadTime
        self.encoders[num].lastReadTime = currentTime
        self.encoders[num].rps = float(1/(self.encoders[num].elapsed*60))
        self.maintainRPS(num)

    def cleanup(self):
        print('\n\nExiting...\n\n')
        for i in range(4):
            self.m.stop(i)
        self.release()
        GPIO.cleanup()