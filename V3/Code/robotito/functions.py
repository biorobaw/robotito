from Adafruit_MotorHAT import Adafruit_MotorHAT 
from MotorDriver import MotorDriver

UPDATEFREQ = .005 #In seconds
SPEEDRANGE = 1 #How wide of a range to balance maintainRPS delta

##ENCODERS
def updateRPS(encoders, speedsAct, elapsed):
    for i in range(4):
        if encoders[i].count>0:
            speedsAct[i] = float(encoders[i].count/(elapsed*60)) 
            #print('%s %s %s %s' %(i, encoders[i].count, elapsed.value, speedsAct[i]))
            encoders[i].count  =  0
        else:
            speedsAct[i] = 0   

##MOTORS 
def setSpeedsIn(m, speedTar):
    #Translate inches to input 0-255 and assign to speedsIn
    if not speedTar.full():
        st = speedTar.get()
    ms = int(-7*(st**2)+87*st)
    for i in range(4):
        m.speedsIn[i] = (ms)
    m.setSpeeds()

def maintainRPS(encoders, speedsAct, elapsed, speedTar, s):
    updateRPS(encoders, speedsAct, elapsed)
    for i in range(4):          
        print(speedsAct[0], speedTar, s[i])
        if speedsAct[i]<speedTar+SPEEDRANGE:
            s[i] = s[i]+1
        elif speedsAct[i]>speedTar-SPEEDRANGE:
            s[i] = s[i]-1    
    return s

def stop(encoders, speedsAct, speedTar, m):
    speedsTar = 0
    for i in range(4):
        m.speedsIn[i] = 0
        encoders[i].count = 0
        speedsAct[i] = 0
    m.setSpeeds()

##DIRECTIONAL FUNCTIONS
def forward(m, speedTar):
    for i in range(4):
        m.motors[i].run(Adafruit_MotorHAT.FORWARD)
    setSpeedsIn(m, speedTar)  
                  
def backward(m, speedTar):
    for i in range(4):
        m.motors[i].run(Adafruit_MotorHAT.BACKWARD)
    setSpeedsIn(m, speedTar)
            
def left(m, speedTar):
    m.motors[0].run(Adafruit_MotorHAT.BACKWARD)
    m.motors[1].run(Adafruit_MotorHAT.FORWARD)
    m.motors[2].run(Adafruit_MotorHAT.FORWARD)
    m.motors[3].run(Adafruit_MotorHAT.BACKWARD)
    setSpeedsIn(m, speedTar)
            
def right(m, speedTar):
    m.motors[0].run(Adafruit_MotorHAT.FORWARD)
    m.motors[1].run(Adafruit_MotorHAT.BACKWARD) 
    m.motors[2].run(Adafruit_MotorHAT.BACKWARD)
    m.motors[3].run(Adafruit_MotorHAT.FORWARD)
    setSpeedsIn(m, speedTar)
                        
def rotL(m, speedTar):
    m.motors[0].run(Adafruit_MotorHAT.FORWARD)
    m.motors[1].run(Adafruit_MotorHAT.FORWARD)
    m.motors[2].run(Adafruit_MotorHAT.BACKWARD)
    m.motors[3].run(Adafruit_MotorHAT.BACKWARD)
    setSpeedsIn(m, speedTar)

def rotR(m, speedTar):
    m.motors[0].run(Adafruit_MotorHAT.FORWARD)
    m.motors[1].run(Adafruit_MotorHAT.BACKWARD)
    m.motors[2].run(Adafruit_MotorHAT.FORWARD)
    m.motors[3].run(Adafruit_MotorHAT.BACKWARD)
    setSpeedsIn(m, speedTar)

def stopMotors(m, speedTar):
    m.speed  =  0
    m.direction  =  0
    m.stop()

##Function Dictionary
directions = {'w':forward,
              's':backward,
              'a':left,
              'd':right,
              'e':rotR,
              'q':rotL,
              'x':stopMotors
}
