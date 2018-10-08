#!/usr/bin/python
import sys
import ctypes as c
import time
import numpy as np
import pygame
from pygame.locals import *
from functions import *
from Sensors import Sensors
from Encoder import Encoder
from MotorDriver import MotorDriver
from multiprocessing import Process, Lock, Queue, Array
from Adafruit_MotorHAT import Adafruit_MotorHAT

## Signal int(0-255) to motors
## Theoretical 530rpm / 60s ~= 8.3rps ~= .11321s/rot
## Actual (with wheel attached), makes roughly 1 rotation at full speed, no load  =  8.5RPS
## ~255encoder signals per revolution

##MotorDriver and motors
#Front left motor  =  0
#Front right motor  =  1
#Back left motor  =  2
#Back right motor  =  3
 
##Runs as a seperate process to give an update signal to the sensors and to the encoders
def timer(elapsed, update):
    last = time.time()
    while True:
        elapsed = time.time()-last      
        if elapsed > UPDATEFREQ:
            update = 1
            last = time.time()

def mapWindow(update):
    s = Sensors()
    pygame.init()       
    pygame.display.set_mode((x, y), 0, 32) 
    gridMatrix[10][10] = 1
    screen  =  pygame.display.get_surface()
    print('Grid is engaged...\n')
    while (1):
        if update == 1:
            s.getDistances()
            forward = int(s.distances[0] / 100)
            gridMatrix[5][forward] = 0
            for i in range(10):
                for j in range(10):
                    if(gridMatrix[i][j] == 1):
                        pygame.draw.rect(screen, (255, 255, 255), ((10*i),(10*j),(10*i+10), (10*j+10)))
                    iTen=i*10
                    jTen=j*10
                    pygame.draw.line(screen, (255, 255, 255), (iTen, 0), (iTen, 500), 1)
                    pygame.draw.line(screen, (255, 255, 255), (0, jTen), (500, jTen), 1)

        #pygame.draw.rect(screen, (0, 200, 0), (0,0,int(x/2),int(y/2)))
        pygame.display.update()     
        pygame.time.wait(30)        
        screen.fill((0, 20, 0, 0))  

        for event in pygame.event.get():
            if event.type == QUIT:      
                for i in range(4):
                    encoders[i].cleanup()
                    s.shutdownSensors()
                pygame.quit()           
                sys.exit()

def motors(elapsed, update ,direction, speedTar):
    m = MotorDriver()
    #enocder derived speeds
    speedsAct = [0]*4
    ##Sensor pins for each of the hall effect sensors for each encoder
    ##Encoder  0        1        2        3    
    #pins  =  [[4,17], [18,27], [22,23], [24,25]]
    #Only using one pin interrupt because the encoders don't work properly
    pins = [4,18,22,24] 
    pinDict = {4:0, 18:1, 22:2, 24:3} 
    encoders = []
    for i in range(4):
        e  =  Encoder(pins[i])
        encoders.append(e)
    print('Motor and encoders are engaged...\n')
    while True:
        if update == 1:
            print('MaintainRPS %s %s %s...\n'%(update, elapsed, speedTar))
            m.speedsIn = maintainRPS(encoders, speedsAct, elapsed, speedTar, m.speedsIn)
            print(m.speedsIn[0])
            m.setSpeeds()
            update.put(0)
            directions[direction.get()](m, speedTar)

def menu(direction, speedTar):
    time.sleep(2)
    while True:
        try:
            speedTar = int(input('Enter speed 0-7: \n'))
            direction = input('Which direction?\nw for forward\ns for backward\nd for right\na for left\nspace for stop\nx to change the speed\n')
            return speedTar
        except ValueError:
            print("Ya done goofed, try one mo' 'gain.\n")
        except KeyError:
            print("Ya done goofed, try a valid direction.\n")
        except KeyboardInterrupt:
            print('\n\nExiting...\n\n')

if __name__ == '__main__':
    ##SHARED MEMORY
    elapsed = 0.0
    update = 0
    direction = 'x'
    speedTar = 0
    ##For Grid Menu
    (x,y) = (500, 500)
    gridMatrix = [Array('i', [0]*50)]*50
    
    timerP = Process(target = timer, args = (elapsed, update))
    timerP.start()
    #sensorsP = Process(target = sensors, args = (elapsed, update))
    #sensorsP.start()
    motorP = Process(target = motors, args = (elapsed, update ,direction, speedTar))
    motorP.start()
    mapP = Process(target = mapWindow, args = (update,))
    mapP.start()
    menu(direction, speedTar)
    mapP.terminate()
    motorP.terminate()
    timerP.terminate()
