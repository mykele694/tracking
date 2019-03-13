import cv2
import numpy as np 
import sys

cap=cv2.VideoCapture(0)

while(cap.isOpened()==True):
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame',gray)
    key=cv2.waitKey(1) & 0xFF
    if (key == ord("s")):
     r=cv2.selectROI(gray,fromCenter=False,showCrosshair=True)
     r.init(gray,r)
    if (key==ord('q')):
       break

cap.release
cv2.destroyAllWindows