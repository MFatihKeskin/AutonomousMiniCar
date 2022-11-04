from MotorModule import Motor
import pygame
import JoyStickModule as js
from time import sleep
import RPi.GPIO as GPIO

motor = Motor(2,21,11,17,13,15)
movement = 'Joystick' #we can select'Keyboard' or 'Joystick'

#pygame init func
def init():
    pygame.init()
    win = pygame.display.set_mode((100,100))

#read keyboard func
def getKey(keyName):
    ans = False
    for eve in pygame.event.get():pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame,'K_{}'.format(keyName))
    if keyInput [myKey]:
        ans = True
    pygame.display.update()

    return ans

def main():
    while True:
        #joystick control process
        if movement=='Joystick':
            jsValue = js.getJS() # To get all values
            jsValueAxis1=jsValue['axis1']
            jsValueAxis2=jsValue['axis2']
            jsValueStopButton = jsValue['x']
            #print("1---",jsValueAxis1)
            #print("2---",jsValueAxis2)

            GPIO.setup(27,GPIO.OUT,initial=GPIO.LOW)#brake lamp
            GPIO.setup(26,GPIO.OUT,initial=GPIO.LOW)#left signal
            GPIO.setup(19,GPIO.OUT,initial=GPIO.LOW)#right signal

            if(jsValueStopButton):#brake func
                jsValueAxis1=0
                jsValueAxis2=0
                GPIO.output(27,GPIO.HIGH) #brake lamp
            else:
                if(jsValueAxis1>0.25):
                    jsValueAxis1 = 1.5-(jsValueAxis1)
                    #left signal enable
                    GPIO.output(26,GPIO.HIGH) 
                    sleep(0.3)
                    GPIO.output(26,GPIO.LOW)
                if(jsValueAxis1<-0.25):
                    jsValueAxis1 = -1.5-(jsValueAxis1)
                    #right signal enable
                    GPIO.output(19,GPIO.HIGH)
                    sleep(0.3)
                    GPIO.output(19,GPIO.LOW)
                #i want to spin if maximum joystick value
                if(jsValueAxis2>0.15):
                    jsValueAxis2 = 1.5-(jsValueAxis2)
                if(jsValueAxis2<-0.15):
                    jsValueAxis2 = -1.5-(jsValueAxis2)

            motor.move((-jsValueAxis1),(-jsValueAxis2),0.1)
            #print("x axis:",jsValueAxis1)
            #print("y axis:",jsValueAxis2)
            
        #keyboard control process
        elif movement=='Keyboard':
            if getKey('LEFT'):
                print('Key Left was pressed')
                motor.move(0.2,0.2,0.5) #left wheels are backward, right wheels are forward

            if getKey('RIGHT'):
                print('Key Right was pressed')
                motor.move(-0.2,0.2,0.5) #right wheels are backward, left wheels are forward

            if getKey('UP'):
                print('Key Up was pressed')
                motor.move(-0.2,1.5,0.5) #all wheels are forward

            if getKey('DOWN'):
                print('Key Down was pressed')
                motor.move(-0.2,-1.5,0.5) #all wheels are backward

            if getKey('TAB'):
                print('Motor is Stopped')
                motor.stop(2) #stop all motors for 2 seconds

if __name__ == '__main__':
    init()
    while True:
        main()
