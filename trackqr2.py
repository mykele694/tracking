import pyzbar
from pyzbar.pyzbar import decode
import numpy as np 
import  cv2

cap=cv2.VideoCapture(0)                             #leggo da videocamera
tracker=cv2.TrackerMedianFlow_create()              #inizializzo il tracker
c=0                                                 #variabile che indica se ho già inizializzato il tracking
z=0                                                 #variabile per controllare se posso seguire il target
s=0                                                 #variabile che indica se ho perso il target e se l'ho ritrovato
v=False                                             #variabile che indica se ho ret è true o false

while(cap.isOpened()):
    ret,gray= cap.read()
    #gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)    #valuto il frame in scala di grigi. se non commentato cambiare 'gray' alla riga precedente con 'frame'
    barcode=decode(gray)                            #decodifico l'immagine per trovare un qrcode
    if (len(barcode)==1):                           #qrcode riconosciuto
            
        if(c==1):
            
            for obj in barcode:
                qbox=(obj.rect[0],obj.rect[1],obj.rect[2],obj.rect[3])
            p1 = (int(qbox[0]), int(qbox[1]))
            p2 = (int(qbox[0] + qbox[2]), int(qbox[1] + qbox[3]))
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

        if(c==0):                                    #nel momento in cui riconosco un qrcode per la prima volta individuo le dimensioni e creo un boundingbox pari al qr
            for obj in barcode:
                bbox=(obj.rect[0],obj.rect[1],obj.rect[2],obj.rect[3])
            ret = tracker.init(gray, bbox)           #inizializzo il tracking con il boundingbox trovato
            c=1                                      #d'ora in avanti
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(gray, p1, p2, (255,0,0), 2, 1)
            cv2.putText(gray,"Target Inizializzato", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2)
            print("Target Inizializzato")
            z=0
            
    else:
        if(z==1):
            if v:
                ret, bbox = tracker.update(gray)
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(gray, p1, p2, (0,255,0), 2, 1)
                cv2.putText(gray,"Tracking Target", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2)
                l=1                
                if ret:
                    lol="True"
                else: 
                    lol="False"
                cv2.putText(gray,lol, (400,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2)
                v=ret
                c=0


            else:
                cv2.putText(gray, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,0,0),2)
                if(s==0):
                    print("Tracking fallito")
                    s=1
                z=0                
        else:
            cv2.putText(gray, "Nessun Target", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    cv2.imshow('frame',gray)
    code = cv2.waitKey(1)
    if code == ord('q'):                                #Q per chiudere
      break




cap.release()
cv2.destroyAllWindows()

