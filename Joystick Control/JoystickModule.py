'''
-sudo apt-get -y install jd
Install Ds4:
-sudo pip3 install ds4drv
-sudo wget https://raw.githubusercontent.com/chrippa/ds4drv/master/udev/50-ds4drv.rules -O /etc/udev/rules.d/50-ds4drv.rules
-sudo udevadm control --reload-rules
-sudo udevadm trigger
-sudo nano /etc/rc.local
(add after # By default this script does nothing. line, add a new line:
/usr/local/bin/ds4drv &)
'''
import pygame
from time import sleep
pygame.init()
# http://man.hubwiz.com/docset/PyGame.docset/Contents/Resources/Documents/ref/joystick.html#pygame.joystick.Joystick
controller = pygame.joystick.Joystick(0) # create joystick object for 1 joystick
controller.init()
buttons = {'x':0,'o':0,'t':0,'s':0,
           'L1':0,'R1':0,'L2':0,'R2':0,
           'share':0,'options':0,
           'axis1':0.,'axis2':0.,'axis3':0.,'axis4':0.}
axiss=[0.,0.,0.,0.,0.,0.] #float value between of +-1 for axis

def getJS(name=''): #catch joystick adc value
    global buttons
    for event in pygame.event.get(): #catch queue events
        if event.type == pygame.JOYAXISMOTION: #catch analog joystick value
            axiss[event.axis] = round(event.value,2)

        elif event.type == pygame.JOYBUTTONDOWN: # catch the button at falling adge
            #print(event.dict, event.joy, event.button, 'PRESSED')
            for x,(key,val) in enumerate(buttons.items()):
                if x<10: #10 degeri buton sayisina gore verildi
                    if controller.get_button(x): #read button is pressed
                        buttons[key]=1 #set button

        elif event.type == pygame.JOYBUTTONUP:  # catch the button at rising adge
            #print(event.dict, event.joy, event.button, 'RELEASED')
            for x,(key,val) in enumerate(buttons.items()):
                if x<10: #10 is max button number
                    if event.button ==x:   #read button is pressed
                        buttons[key]=0 #reset button

    # set for dualshock joystick
    buttons['axis1'],buttons['axis2'] ,buttons['axis3'] ,buttons['axis4']  = [axiss[0],axiss[1],axiss[3],axiss[4]]

    if name == '':#for personal button
        return buttons
    else:
        return buttons[name]

def main():
    print(getJS()) #print all joystick button and axis value
    sleep(0.05)


if __name__ == '__main__':
  while True:
    main()
