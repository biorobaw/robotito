#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from Encoder import Encoder
pins=[[4, 17], [18, 27], [22, 23], [24, 25]]
##ENCODERS
encoders=[]
for i in range(4):
    e = Encoder(pins[i]) 
    encoders.append(e)

exit=False
while(not exit):
    exit=False
