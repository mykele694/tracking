import numpy as np 
import cv2
import time

start_time = time.time()
x = 1 # displays the frame rate every 1 second
counter = 0
cap=cv2.VideoCapture(0)
ret,frame=cap.read()
print(cap.get(3))
print(cap.get(4))
cap.set(3,1920)
cap.set(4,1080)
while (cap.isOpened()):
    ret,frame=cap.read()
    cv2.imshow('frame',frame)
    counter+=1
    if (time.time() - start_time) > x :
        print("FPS: ", counter / (time.time() - start_time))
        counter = 0
        start_time = time.time()

    if (cv2.waitKey(1) & 0xFF==ord('q')):
        break
cap.release() 
cv2.destroyAllWindows()
