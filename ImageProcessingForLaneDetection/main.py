from MotorModule_11 import Motor
from LaneDetectionModule_8 import getLaneCurve
from LaneDetectionModule_8 import initializeTrackbars
import WebcamModule_10
#import cv2
import logging

motor = Motor(2,7,11,17,13,15)
#Motor(1,3,5,6,8,10)

def writeLog(curveRaw):
        logging.info(curveRaw)

def main():
    img = WebcamModule_10.getImg(True)
    return img

def curveVal(img):
    curve, basePoint, midPoint = getLaneCurve(img,1)
    curveRaw = (basePoint-midPoint)
    #logging.basicConfig(filename='9_curveRaw.txt', encoding='utf-8', level = logging.DEBUG)
    if basePoint>midPoint:
        initializeTrackbarValue = [curveRaw-basePoint,240,curveRaw-basePoint,0]
        initializeTrackbars(initializeTrackbarValue)
    elif basePoint<midPoint:
        initializeTrackbarValue = [curveRaw+basePoint,240,curveRaw+basePoint,0]
        initializeTrackbars(initializeTrackbarValue)
    return curveRaw
  
'''
    def writeLog(curveRaw):
        logging.info(curveRaw)

    logging.basicConfig(filename='curveRaw.txt', encoding='utf-8', level = logging.DEBUG)
    curveList.append(curveRaw)
    a=max(curveList)
    b=min(curveList)
    print("max:",a)
    print("min:",b)
'''

totalSum = 0
curveList = []
def listOfCurve(curveDif):
    curveList.append(curveDif)
    if len(curveList) == 30:
        totalSum = 0
        for i in curveList[0:30]:
            totalSum = totalSum + i
        totalSum = totalSum / 30
        del curveList[0:30]
        curveRaw=int(totalSum)
        print(curveRaw)
        #curveRaw is a sampled corner angle we can generate to motor.move function according to curveRaw
        #turn left
        if curveRaw < -170:
            motor.move (10,17)
            print("(10,17)")
        elif curveRaw >= -170 and curveRaw <= -150:
            motor.move (10,16)
            print("(10,16)")
        elif curveRaw > -150 and curveRaw <= -130:
            motor.move (10,15)
            print("(10,15)")
        elif curveRaw > -130 and curveRaw <= -110:
            motor.move (10,14)
            print("(10,14)")
        elif curveRaw > -110 and curveRaw <= -90:
            motor.move (10,13)
            print("(10,13)")
        elif curveRaw > -90 and curveRaw <= -70:
            motor.move (10,12)
            print("(10,12)")
        elif curveRaw > -70 and curveRaw <= -50:
            motor.move (10,11)
            print("(10,11)")
        #forward
        elif curveRaw >= -50 and curveRaw <= 50:
            motor.move (14,14)
            print("(13,13)")
        #turn right 
        elif curveRaw > 50 and curveRaw <= 70:
            motor.move (11,10)
            print("(11,10)")
        elif curveRaw > 70 and curveRaw <= 90:
            motor.move (12,10)
            print("(12,10)")
        elif curveRaw > 90 and curveRaw <= 110:
            motor.move (13,10)
            print("(13,10)")
        elif curveRaw > 110 and curveRaw <= 130:
            motor.move (14,10)
            print("(14,10)")
        elif curveRaw > 130 and curveRaw <= 150:
            motor.move (15,10)
            print("(15,10)")
        elif curveRaw > 150 and curveRaw <= 170:
            motor.move (16,10)
            print("(16,10)")
        elif curveRaw > 170:
            motor.move (17,10)
            print("(17,10)")
        else:
            print("Error")

if __name__ == '__main__':
    while True:
        #logCurve = main()
        #writeLog(logCurve)
        inputImg = main()
        curveDiff = curveVal(inputImg) 
        listOfCurve(curveDiff)
        sumOfList = 0
