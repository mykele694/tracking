import pyzbar
from pyzbar.pyzbar import decode
import numpy as np 
import  cv2

cap=cv2.VideoCapture(0)
c=0
z=0
s=0
l=0
v=False
tracker = cv2.TrackerTLD_create()
while(cap.isOpened()==True):
    ret,gray= cap.read()
    #gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    barcode=decode(gray)
    if (len(barcode)==1):
        
            
        if(c==1):
            ret,bbox=tracker.update(gray)
            for obj in barcode:
                bbox=(obj.rect[0],obj.rect[1],obj.rect[2],obj.rect[3])
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(gray, p1, p2, (255,0,0), 2, 1)
            cv2.putText(gray,"Tracking QR", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2)
            z=1            
            
            ret,bbox=tracker.update(gray)

            if ret:
                lol="Target Located"               
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(gray, p1, p2, (0,255,0), 2, 1)
            else:
                lol="Located Failed"
                for obj in barcode:
                    bbox=(obj.rect[0],obj.rect[1],obj.rect[2],obj.rect[3])
                ret= tracker.init(gray,bbox)
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(gray, p1, p2, (0,255,0), 2, 1)
                
            cv2.putText(gray,lol, (400,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2)
            if(s==1):
                print("Target Ritrovato")
                s=0
                v=True
                l=1

        if(c==0):            
            for obj in barcode:
                bbox=(obj.rect[0],obj.rect[1],obj.rect[2],obj.rect[3])
            ret = tracker.init(gray, bbox)
            c=1
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(gray, p1, p2, (255,0,0), 2, 1)
            cv2.putText(gray,"Target Inizializzato", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2)
            print("Target Inizializzato")
            z=0
            
    else:
        if(z==1):
            if v:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(gray, p1, p2, (0,255,0), 2, 1)
                cv2.putText(gray,"Tracking Target", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2)
                l=1
                ret, bbox = tracker.update(gray)
                if ret:
                    lol="True"
                else: 
                    lol="False"
                cv2.putText(gray,lol, (400,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255),2)
                v=ret
                c=0


            else:
                cv2.putText(gray, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,0,0),2)
                if(l==1):
                    print("Tracking fallito")
                    l=0
                z=0
                s=1
        else:
            cv2.putText(gray, "Nessun Target", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    cv2.imshow('frame',gray)
    code = cv2.waitKey(1)
    if code == ord('q'):                                #Q per chiudere
      break




cap.release()
cv2.destroyAllWindows()
