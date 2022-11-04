import cv2
import numpy as np
import time

def thresholding(img):
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lowerWhite = np.array([85, 0, 0]) 
    upperWhite = np.array([179, 160, 255]) 
    maskedWhite= cv2.inRange(hsv,lowerWhite,upperWhite) 
    return maskedWhite

def GaussianBlur(img):
    Gaussian = cv2.GaussianBlur(img,(7,7),0) 
    return Gaussian

def CannyEdgeDetection(img):
    CannyImg = cv2.Canny(img,85,179)
    return CannyImg

def nothing(a):
    pass

def initializeTrackbars(intialTracbarVals,wT=480, hT=240):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", intialTracbarVals[0],wT//2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", intialTracbarVals[1], hT, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", intialTracbarVals[2],wT//2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", intialTracbarVals[3], hT, nothing)

def valTrackbars(wT=480, hT=240):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (wT-widthTop, heightTop), (widthBottom , heightBottom ), (wT-widthBottom, heightBottom)])
    return points

def warpingLane (img,points,w,h,inv=False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    if inv:
        matrix = cv2.getPerspectiveTransform(pts2,pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgWarp = cv2.warpPerspective(img,matrix,(w,h))
    return imgWarp

def drawPoints(img,points):
    for x in range( 0,4):
        cv2.circle(img,(int(points[x][0]),int(points[x][1])),15,(0,0,255),cv2.FILLED)
    return img

def getHistogram(img, display=False, minVal = 0.1, region = 4):
    if region ==1:
        histValues = np.sum(img, axis=0)
    else :
        histValues = np.sum(img[img.shape[0]//region:,:], axis=0)

    maxValue = np.max(histValues)  # FIND THE MAX VALUE
    minValue = minVal*maxValue
    indexArray =np.where(histValues >= minValue) # ALL INDICES WITH MIN VALUE OR ABOVE
    basePoint =  int(np.average(indexArray)) # AVERAGE ALL MAX INDICES VALUES

    if display:
        imgHist = np.zeros((img.shape[0],img.shape[1],3),np.uint8)
        #imgHist = imgHist-img
        for x,intensity in enumerate(histValues):
            if intensity > minValue:
                color= (255,100,100)
            else:
                color= (0,0,255)
            cv2.line(imgHist,(x,img.shape[0]),(x,img.shape[0]-(intensity//255//region)),color,1)
            cv2.circle(imgHist,(basePoint,img.shape[0]),20,(0,255,255),cv2.FILLED)
            cv2.circle(img,(basePoint,img.shape[0]),20,(100,50,255),cv2.FILLED)
        return basePoint,imgHist
    return basePoint

curveList = []
avgVal = 10

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        #hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
  
def getLaneCurve(img,display = 2):
    imgCopy = img.copy() 
    imgResult = img.copy() 

    #STEP1
    imgThres = thresholding(imgCopy)
    #cv2.imshow('ThresholdingVideo',imgThres)

    #STEP2
    imgGauss = GaussianBlur(imgThres)
    #cv2.imshow('GaussianBlurVideo',imgGauss)

    #STEP3
    imgCanny = CannyEdgeDetection(imgGauss)
    #cv2.imshow('CannyEdgeDetectionVideo',imgCanny)

    #STEP4
    hT,wT,c = img.shape
    points = valTrackbars()
    imgWarp = warpingLane(imgThres, points, wT, hT)
    #cv2.imshow('WarpingLaneVideo',imgWarp)
    imgWarpPoints = drawPoints(imgCopy,points) 
    #cv2.imshow('WarpingLanePointsVideo',imgWarpPoints)

    #STEP5
    #curveAveragePoint bizdeki basePoint
    basePoint, imgHistt = getHistogram(imgCanny,display=True,minVal=0.9, region=4)
    #cv2.imshow('HistogramFindingCurve',imgHistt)

    #STEP6
    midPoint, imgHist = getHistogram(imgWarp,display=True,minVal=0.5, region=1)
    #cv2.imshow('OptimizingCurve',imgHist)
    curveRaw = (basePoint-midPoint)
    curveDegree = round(curveRaw*0.01*21,2)
    intCurveDegree = int(curveRaw*0.01*21)
    print("Slope / Eğim =", curveDegree,"Degree") 

    curveList.append(curveRaw)
    if len(curveList) > avgVal:
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))

    if display != 0:
        imgInvWarp = warpingLane(imgWarp, points, wT, hT,inv = True)
        imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT//3,0:wT] = 0,0,0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0,50,50
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
        midY = 450
        cv2.putText(imgResult,'Degree:'+str(curveDegree),(intCurveDegree+40,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),3)
        cv2.putText(imgHist,'Degree:'+str(curveDegree),(intCurveDegree+40,70),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
        cv2.line(imgResult,(wT//2,midY),(wT//2+(curve*3),midY),(153,76,0),5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY-25), (wT // 2 + (curve * 3), midY+25), (153,76,0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve//50 ), midY-10), (w * x + int(curve//50 ), midY+10), (128,0,0), 2)
        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - time.time());
        #fps=round(11*fps*100000,2)
        #print(fps)
        cv2.putText(imgResult, 'FPS:'+str(30), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230,50,50), 3)
        if display == 2:
            imgStacked = stackImages(1,([img,imgThres,imgCanny],[imgHist,imgWarpPoints,imgResult]))
            cv2.imshow('ImageStack',imgStacked)
        elif display == 1:
            cv2.imshow('Resutlt',imgResult)

    #STEP 7
        #Normalisation for my motor module
        '''curve = curve/100
        if curve>1:
            curve=1
        if curve<-1:
            curve=-1
        print('curve:',curve)'''
    return curve, basePoint, midPoint





frameCounter = 0
if __name__ == '__main__':
    cap = cv2.VideoCapture('vid1.mp4')
    initializeTrackbarValue = [93,208,121,96] 
    initializeTrackbars(initializeTrackbarValue)
    while True:
        frameCounter +=1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            frameCounter=0

        success, img = cap.read()
        img = cv2.resize(img,(480,240))
        #getLaneCurve(img)
        result = getLaneCurve(img,display=2)
        #cv2.imshow('Vid',img)
        cv2.waitKey(1)
