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

if __name__ == '__main__':
    cap = cv2.VideoCapture('vid1.mp4')
    while True:
        success, img = cap.read()
        img = cv2.resize(img,(480,240))
        getLaneCurve(img)
        cv2.imshow('Vid',img)
        cv2.waitKey(1)
