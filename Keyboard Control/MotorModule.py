import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM) #BCM mode enable for gpio
GPIO.setwarnings(False)

class Motor():
    #motor= Motor(2,7,11,17,13,15) #motor driver connection pins to RPi
    def __init__(self,EnaA,In1A,In2A,EnaB,In1B,In2B):#L298N motor driver pins
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B
        #set output all l298n pins
        GPIO.setup(self.EnaA,GPIO.OUT)
        GPIO.setup(self.In1A,GPIO.OUT)
        GPIO.setup(self.In2A,GPIO.OUT)
        GPIO.setup(self.EnaB,GPIO.OUT)
        GPIO.setup(self.In1B,GPIO.OUT)
        GPIO.setup(self.In2B,GPIO.OUT)
        
        #set pwm control with %20 duty cycle for right and left motors
        self.pwmA = GPIO.PWM(self.EnaA, 20);
        self.pwmA.start(0);
        self.pwmB = GPIO.PWM(self.EnaB, 20);
        self.pwmB.start(0);

    def move(self,speed=0.5,turn=0,t=0):
        speed *=100
        turn *=100
        leftSpeed = speed - turn
        rightSpeed = speed + turn
        if leftSpeed>100: leftSpeed=15 #speed border
        elif leftSpeed<-100: leftSpeed= -15 #speed border
        if rightSpeed>100: rightSpeed=15 #speed border
        elif rightSpeed<-100: rightSpeed= -15 #speed border

        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))

        if leftSpeed>0:
            GPIO.output(self.In1A,GPIO.HIGH)
            GPIO.output(self.In2A,GPIO.LOW)
        else:
            GPIO.output(self.In1A,GPIO.LOW)
            GPIO.output(self.In2A,GPIO.HIGH)

        if rightSpeed>0:
            GPIO.output(self.In1B,GPIO.HIGH)
            GPIO.output(self.In2B,GPIO.LOW)
        else:
            GPIO.output(self.In1B,GPIO.LOW)
            GPIO.output(self.In2B,GPIO.HIGH)
        sleep(t)
    #stop function for a brake
    def stop(self,t=0):
        self.pwmA.ChangeDutyCycle(0);
        self.pwmB.ChangeDutyCycle(0);
        sleep(t)

#main function as a test
def main():
    motor.move(0.2,0,2)
    motor.stop(2)
    motor.move(-0.2,0.2,2)
    motor.stop(2)

if __name__ == '__main__':
    motor= Motor(2,7,11,17,13,15) #L298N motor driver connection pins to RPi
    main()
