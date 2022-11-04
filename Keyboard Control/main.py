from MotorModule import Motor
import pygame

motor = Motor(2,7,11,17,13,15) #motor driver connection pins

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
