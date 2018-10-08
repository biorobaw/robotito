#!/usr/bin/python
import RPi.GPIO as GPIO
from multiprocessing import Value
GPIO.setmode(GPIO.BCM)
class Encoder:


##CONSTRUCTOR
    #def __init__(self, _pinA, _pinB, _motor):
    ##self.pins = [_pinA, _pinB]
    def __init__(self, _pin):
        self.pin = _pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #Initialize the interrupt-triggers on the rising edge
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback = self.updateCounts)
        self.count = 0 

##FUNCTIONS
    def updateCounts(self, event):
        self.count = self.count + 1
    
    def countReset(self):
        self.count=0
        
    def cleanup(self):
        GPIO.cleanup()