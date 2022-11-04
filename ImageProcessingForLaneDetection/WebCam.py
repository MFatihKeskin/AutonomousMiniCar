import cv2
import time
import numpy as np

cap = cv2.VideoCapture('vid1.mp4')

def getImg(display = False):
    _, img = cap.read()
    img = cv2.resize(img,(480,240))

    if display:
        cv2.imshow('IMG',img)
        cv2.waitKey(1)
    return img

if __name__ == '__main__':
    while True:
        img = getImg(True)
