import cv2 
import numpy as np  
import time

# Webcamera no 0 is used to capture the frames 
cap = cv2.VideoCapture(0)  
print(cap)  
# This drives the program into an infinite loop. 
#frame=cap.get(cv2.CAP_PROP_FRAME_COUNT)
#f=int(frame)
#print(f)
#curr=0

while(cap.isOpened()): 
    #curr+=1
    start=time.time()       
    # Captures the live stream frame-by-frame 
    ret, frame = cap.read()  
    
    # Converts images from BGR to HSV 
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    #frame = frame[:,:,0]
    lower = np.array([0, 140, 140])  #YELLOW  #0, 0, 130 RED
    upper = np.array([120, 255, 255]) #YELLOW  #40, 40, 255 RED
    #lower = np.array([150]) 
    #upper = np.array([255])  
  
# Here we are defining range of bluecolor in HSV 
# This creates a mask of blue coloured  
# objects found in the frame. 
    mask = cv2.inRange(frame, lower, upper)
    #mask = cv2.inRange(mask, 0, 30)

    #lower_green = np.array([170, 0, 0]) 
    #upper_green = np.array([180, 255, 255]) 

    #mask2 = cv2.inRange(hsv, lower_green, upper_green)

    #mask=cv2.bitwise_or(mask1,mask2)

    kernelOpen=np.ones((2,2))
    kernelClose=np.ones((80,80))

    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    maskFinal=maskClose
    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(frame,conts,-1,(255,0,0),3)
    #print("conts:::",type(conts))
    if len(conts)!=0:
        c = max(conts, key=cv2.contourArea)
        #print("c:::",type(c))
        x,y,w,h=cv2.boundingRect(c)
        cv2.rectangle(frame,(x-2,y-2),(x+w+2,y+h+2),(0,255,0), 2)
    #for i in range(len(conts)):
        #x,y,w,h=cv2.boundingRect(conts[i])
        #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 2)
        #cv2.putText(cv2.fromarray(frame), str(i+1),(x,y+h),font,(0,255,255))
# The bitwise and of the frame and mask is done so  
# that only the blue coloured objects are highlighted  
# and stored in res 
    res = cv2.bitwise_and(frame,frame, mask= mask) 
    cv2.imshow('frame',frame) 
    cv2.imshow('mask',mask) 
    cv2.imshow('res',res) 
    cv2.imshow('Opend',maskOpen)
    cv2.imshow('Close',maskClose)
    
# This displays the frame, mask  
# and res which we created in 3 separate windows. 
    k = cv2.waitKey(5) & 0xFF
    if k == 27: 
        break
    #print(time.time()-start)

    #if(curr==f):
    #    break
print("EOF")  
# Destroys all of the HighGUI windows. 
cv2.destroyAllWindows() 
  
# release the captured frame 
cap.release() 