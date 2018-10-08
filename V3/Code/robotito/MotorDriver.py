#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
##Motor       Number
##Front Left  0
##Front Right 1
##Back Left   2
##Back Right  3

##Controls the motor function with encoders
class MotorDriver:
##CONSTRUCTOR
    def __init__(self):
        ##MOTOR DRIVER
        self.mh = Adafruit_MotorHAT(addr=0x60)
        
        ##MOTORS
        self.motors=[]
        for i in range(1,5):
            self.motors.append(self.mh.getMotor(i))   
        self.speedsIn=[0]*4
                                        
##HELPER FUNCTIONS                
    def release(self):
        for i in range(4):
            self.motors[i].run(Adafruit_MotorHAT.RELEASE)
                        
    def cleanup(self):
        GPIO.cleanup()        
    
    def stop(self):
        for i in range(4):    
            self.speedsIn[i] = 0
        self.setSpeeds()
            
    def setSpeeds(self):
        for i in range(4):            
            self.motors[i].setSpeed(self.speedsIn[i])