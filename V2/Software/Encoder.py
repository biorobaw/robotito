#!/usr/bin/python
import RPi.GPIO as GPIO

class Encoder:
    ##Constructor
    def __init__(self, pins):
        #Setup GPIO pin for encoder
        GPIO.setmode(GPIO.BCM)
        #pin numbers
        self.pins=[pins[0], pins[1]]
        #setup pins
        GPIO.setup(pins[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #GPIO.setup(pins[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.states=[(GPIO.input(pins[0]))] #(GPIO.input(pins[1]))]
        self.states_O=[0, 0]
        self.count=0
        self.error=0     
        # Initialize the interrupts - these trigger on both the rising and falling edge
        GPIO.add_event_detect(self.pins[0], GPIO.BOTH, callback = self.update)  
        #GPIO.add_event_detect(self.pins[1], GPIO.BOTH, callback = self.update)
        #GPIO.add_event_callback(pins[0], self.update)
        #GPIO.add_event_callback(pins[1], self.update)
        
    def update(self, event):
        self.states_O[0]=self.states[0]
        #self.states_O[1]=self.states[1]
        self.states[0]=GPIO.input(self.pins[0])
        #self.states[1]=GPIO.input(self.pins[1])
       
        if ((self.states[0], self.states_O[0])==(0, 0) or(self.states[0], self.states_O[0])==(1, 1)):
            return
        else:
            self.count+=1

       

        
