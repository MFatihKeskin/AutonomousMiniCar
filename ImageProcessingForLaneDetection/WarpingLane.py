# Write your code here :-)
import cv2
import numpy as np

def getLaneCurve(img):
    imgThres = thresholding(img)
    cv2.imshow('ThresholdingVideo',imgThres)

    imgGauss = GaussianBlur(imgThres)
    cv2.imshow('GaussianBlurVideo',imgGauss)

    imgCanny = CannyEdgeDetection(imgGauss)
    cv2.imshow('CannyEdgeDetectionVideo',imgCanny)

    return None

def thresholding(img):
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lowerWhite = np.array([85, 0, 0]
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

def getLaneCurve(img):
    imgCopy = img.copy() #orjinal görüntü saklanıyor

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
    h,w,c = img.shape
    points = valTrackbars()
    imgWarp = warpingLane(imgCanny, points, w, h)
    cv2.imshow('WarpingLaneVideo',imgWarp)
    imgWarpPoints = drawPoints(imgCopy,points) 
    cv2.imshow('WarpingLanePointsVideo',imgWarpPoints)
    return None


frameCounter = 0
if __name__ == '__main__':
    cap = cv2.VideoCapture('vid1.mp4')
    initializeTrackbarValue = [93,208,121,96]
    initializeTrackbars(initializeTrackbarValue)
    while True:

        #videonun sonsuz döngüde çalışması için
        frameCounter +=1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            frameCounter=0

        success, img = cap.read()
        img = cv2.resize(img,(480,240))
        getLaneCurve(img)
        cv2.imshow('Vid',img)
        cv2.waitKey(1)
