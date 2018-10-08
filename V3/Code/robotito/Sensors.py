#!/usr/bin/python

# MIT License
# 
# Copyright (c) 2017 John Bryan Moore
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import VL53L0X 
import RPi.GPIO as GPIO

class Sensors:
    def __init__(self):
        # Starting I2C address
        self.address = 0x2A
        # GPIO pin numbers for sensor shutdown 
        self.sensorShutdowns = [12, 13, 16, 19]
        self.sensors = []
        self.distances = [1000]*4
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        for i in range(4):
            # Setup GPIO for shutdown pins on each VL53L0X
            GPIO.setup(self.sensorShutdowns[i], GPIO.OUT)
            # Set all shutdown pins low to turn off each VL53L0X
            GPIO.output(self.sensorShutdowns[i], GPIO.LOW)
        # Keep all low for 500 ms or so to make sure they reset
        time.sleep(0.5)

        # Create one object per VL53L0X passing the address to give to
        # each.
        for i in range(4):
            GPIO.output(self.sensorShutdowns[i], GPIO.HIGH)
            s = VL53L0X.VL53L0X(self.address)
            self.address = self.address + 1
            self.sensors.append(s)
            GPIO.output(self.sensorShutdowns[i], GPIO.HIGH)
            self.sensors[i].start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)

    def getDistances(self):
        for i in range(4):
            self.distances[i] = self.sensors[i].get_distance()
            #print ("sensor %d - %d mm" % (self.sensors[i].my_object_number, self.distances[i]))

    def shutdownSensors(self):
        for i in range(4):
            self.sensors[i].stop_ranging()
            GPIO.output(self.sensorShutdowns[i], GPIO.LOW)
