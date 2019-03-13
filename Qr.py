import pyzbar.pyzbar as pyzbar
import numpy as np 
import cv2
from pyzbar.pyzbar import decode

def decode(im) : 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)
 
  # Print results
  for obj in decodedObjects:
    print('Type : ', obj.type)
    print('Data : ', obj.data,'\n')
    print('rect:',obj.rect,'\n')
    print('polygon:',obj.polygon,'\n') 
  return decodedObjects

cap=cv2.VideoCapture(0)

if(cap.isOpened()==True):
    while(cap.isOpened()==True):
        ret,frame=cap.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',gray)
        barcode=decode(gray)
        if (cv2.waitKey(1) & 0xFF=='q') : 
         break


else:
    print("Streaming fallito")


