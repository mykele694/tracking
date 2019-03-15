import pyzbar
import numpy as np 
import cv2
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt

def posizione(cam,box,distanza):
    assecentrale=cam[1]/2
    #propW=(box[2]/cam[1])
    #propH=(box[3]/cam[0])
    centro=[(box[0]+box[2]/2),(box[1]+box[3]/2)]
    #cv2.putText(gray,"P W: "+ str(float(distanza)), (400,100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2)
    #cv2.putText(gray,"P H: "+ str(float(propH)), (400,120), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2)
    if (distanza>500.0):  #propW<1/2 and propH<1/2                    
        if(centro[0]<assecentrale):
             sfasamento=(assecentrale-centro[0])
             cv2.putText(gray,"Target sx di:"+ str(int(sfasamento)), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2) #print("il target si trova a sx di :",sfasamento)
             
             return centro
        elif(centro[0]>assecentrale):
             sfasamento=(centro[0]-assecentrale)
             cv2.putText(gray,"Target dx di:"+ str(int(sfasamento)) , (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2) #print("il target si trova a dx di :",sfasamento)
             
             return centro
        elif(centro[0]==assecentrale):
             cv2.putText(gray,"Target centrato", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2) #print("il target si trova di fronte al robot")
             return centro
    else:
        cv2.putText(gray,"Target vicino", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2) #print("il target è vicino")
        return centro    

def get_size_cam (frame):                              #Individuo le dimensioni del frame
    height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    info_dim=[height,width]
    return info_dim

def calc_distanza(focal,pxmm,objpix):
    objreal=150
    objmm=objpix/pxmm
    dist=(objreal*focal)/objmm
    return dist


firstcapture=True #variabile che indica se il target è da inizializzare
tracking=False    #tracking  
#loc = None        #variabile per stampare a video stato track
inizializza=True  #variabile per inizializzare il target
nframe=0      #contatore di solo track senza riconoscimento oggetto
statotrack=0  #variabile che indica lo stato del tracking (nullo,qr,track)
foc=3.67      #lunghezza focale della nostra cam
t=0           #contatore di cili(frame)
assex=[0]     #lista che salva la x del centro per ogni frame
assey=[0]     #lista che tiene conto della y del centro per ogni frame
stato=[0]     #array dello stato di track nel tempo
distance=[0]
distanza=0.0

cap=cv2.VideoCapture(0)
#cap.set(3,1920)
#cap.set(4,1080)
ret,gray=cap.read()
lista=get_size_cam(cap)
print ("DIMENSIONE FRAME altezza= ",lista[0]," larghezza= ",lista[1])

pxmm=lista[1]/foc

while (cap.isOpened()):
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    barcode=decode(gray)
    
    if (len(barcode)==1):
        for obj in barcode:
            bbox=(obj.rect[0],obj.rect[1],obj.rect[2],obj.rect[3])

        if not inizializza:
            ret,bbox=tracker.update(gray)
            #print(ret)
            
            statotrack=1 
            cv2.putText(gray,"Tracking QR", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2)
            #print("target ok")

        if inizializza:  
            tracker = None
            tracker=cv2.TrackerMedianFlow_create()
            cv2.putText(gray,"NEW", (30,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2)
            firstcapture=False
            tracking=True
            inizializza=False
            nframe=0
            ret = tracker.init(gray, bbox)

        if ret:
            inizializza=False
            distanza=calc_distanza(foc,pxmm,bbox[2])
            statotrack=1

        else:
            print("Target Letto e Perso") 
            tracking=False               
            firstcapture=True
            inizializza=True
            statotrack=0        
        #print(ret)
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(gray, p1, p2, (255,0,0), 2, 1)             

    else:
        if (firstcapture==False):
            if tracking:
                ret, bbox = tracker.update(gray)
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(gray, p1, p2, (0,255,0), 2, 1)
                cv2.putText(gray,"Tracking Target", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2)
                nframe=nframe+1
                if(nframe==1000):
                    firstcapture=True
                    tracking=False
                    nframe=0
                    print("Target originale mancante da troppo tempo")
                if ret:                    
                    statotrack=2
                    distanza=calc_distanza(foc,pxmm,bbox[2])                    

                else: 
                    tracking=False
            else:
                cv2.putText(gray, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,0,0),2)
                print("Target Perso")
                firstcapture=True
                
            inizializza=True
        else:
            cv2.putText(gray, "Nessun Target", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    if tracking:        
        assex[t:t]=[posizione(lista,bbox,distanza)[0]]        
        assey[t:t]=[posizione(lista,bbox,distanza)[1]]
        distance[t:t]=[distanza]
        cv2.putText(gray,"Distanza mm:"+str(float(round(distance[t],1))), (50,400), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2) 
        
    if not tracking:
        statotrack=0
        assex[t:t]=[0]
        assey[t:t]=[0]
        distance[t:t]=[0]
    stato[t:t]=[statotrack]
    t=t+1
        

    cv2.imshow('frame',gray)
    if (cv2.waitKey(1) & 0xFF==ord('q')):
        break   

temp=np.arange(0,(t+1),1)                               #grafici matplot
x=np.array(assex)
y=np.array(assey)
z=np.array(stato)
d=np.array(distance)
fig, axs = plt.subplots(3,1)
axs[0].plot(temp, x, temp, y)    
axs[0].set_ylabel('(X,Y) centro px')
axs[0].grid(True)
axs[0].set_xlabel('X_blue Y_yellow')
axs[1].plot(temp,d)
axs[1].set_ylabel('distanza mm')
axs[2].plot(temp,z)
axs[2].set_ylabel('stato tracking')
axs[2].set_xlabel('TIME')
fig.tight_layout()
plt.show()

cap.release()
cv2.destroyAllWindows()        
