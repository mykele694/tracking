from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
import imutils
import time
import cv2
from pyzbar.pyzbar import decode


cap=PiVideoStream().start()
time.sleep(2.0)
fps=FPS().start()
firstime=True
tracking=False

while(True):
    frame=cap.read()
    barcode=decode(frame)
    if(len(barcode)==1):
    #    print(barcode)
        for obj in barcode:
            bbox=(obj.rect[0],obj.rect[1],obj.rect[2],obj.rect[3])
        if not firstime:
            ret,bbox=tracker.update(frame)
        else:
            tracker=None
            tracker=cv2.TrackerMedianFlow_create()
            ret=tracker.init(frame,bbox)
            firstime=False
        if ret:
            tracking=True
            print("tracker QR")
        else:
            tracking=False
    else:
        if tracking:
            ret,bbox=tracker.update(frame)
            if ret:
                tracking=True
                print("tracker")
            else:
                tracking=False
        firstime=True
    
    if tracking:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0,255,0), 2, 1)

    fps.update()
    cv2.imshow('frame',frame)
    if (cv2.waitKey(1) & 0xFF==ord('q')):
        break
    
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
cv2.destroyAllWindows()
cap.stop()
