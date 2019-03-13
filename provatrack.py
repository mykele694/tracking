import numpy as numpy
import pyzbar
import cv2
from pyzbar.pyzbar import decode

def get_barcode_info(frame):                              #passo l'immagine in una funzione che la converte in toni di grigio e analizza la presenza di un qr code

    barcodes = decode(gray_img)
    if (len(barcodes)==1):
        for obj in barcodes:
             puntosxu=obj.polygon[0]                        #individuo la posizione del punto in alto a sx del qrcode. polygon restituisce una lista con le coordinate dei quattro punti cardinali del qr code
             dimension=obj.rect                             #individuo le informazioni del qr code rect restituisce una lista con (posizione lato sinistro,posizione top,altezza,larghezza)
             xcentro=(puntosxu[0]+(dimension[2]/2))         #individuo la coordinata x del centro del qr code
             ycentro=(puntosxu[1]+(dimension[3]/2))         #individuo la coordinata y del centro del qr code
             print ("Coordinate Centro X: ",xcentro,"Y: ",ycentro)
             #print ("INFO QR: ",obj.data)
             posizionecentro=[xcentro,ycentro,obj.rect[2],obj.rect[3]]
             return posizionecentro                         #la funzione restituisce una lista con coordinata x e y del centro del qr code e la larghezza
    else: return False
 
def get_size_cam (frame):                              #Individuo le dimensioni del frame
    height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    info_dim=[height,width]
    return info_dim

def come_muoversi(frame,centro):
    assecentrale=frame[1]/2
    propW=(centro[2]/frame[1])
    propH=(centro[3]/frame[0])
    if (propW<1/3 and propH<1/3):                    #è settato in maniera che se il qr code supera 1/3 del frame visualizzato riconosce la vicinanza all'obbietivo
        if(centro[0]<assecentrale):
             sfasamento=(assecentrale-centro[0])
             return #print("il target si trova a sx di :",sfasamento)
        elif(centro[0]>assecentrale):
             sfasamento=(centro[0]-assecentrale)
             return #print("il target si trova a dx di :",sfasamento)
        else:
             return #print("il target si trova di fronte al robot")
    else:
         return print("il target è vicino")

def tracking_Qr(frame):                        #nel momento in cui riconosco un qr code inizio a tracciarlo
    barcode=decode(frame)
    if (len(barcode)==1):
        for obj in barcode:
            box=[obj.rect[0],obj.rect[1],obj.rect[2],obj.rect[3]] 
            return box                         #la funzione restituisce le dimensioni del box tracker



   


tracker = cv2.TrackerKCF_create()                #inizializzo un tracker(MedianFlow)
bbox=(20,30,50,60)
cap=cv2.VideoCapture(0)                                 #accedo allo stream della videocamera

if (cap.isOpened()==False):                             #controllo che il programma usi la videocamera
    print("Error opening video stream or file")         #cap.isOpened() riporta True se è attiva la videocamera

lista=get_size_cam(cap)                                 #creo una lista con altezza e larghezza del frame
print ("DIMENSIONE FRAME altezza= ",lista[0]," larghezza= ",lista[1])

while(cap.isOpened()):
    ret, frame = cap.read()                             #Ret riporta true se ho un frame in ingresso. Frame rappresenta la matrice dell'immagine
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    info = get_barcode_info(gray_img)                      #passo Frame come variabile della funzione (come return avrò la posizione del centro del qrcode)
    if(info!=False):
        come_muoversi(lista,info)
        bbox=tracking_Qr(gray_img)
    else:
        print("TAGET NON INDIVIDUATO!!")
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(gray_img, p1, p2, (255,0,0), 2, 1)
    cv2.imshow('Codice a Barre', gray_img)                 #finestra di stream
    code = cv2.waitKey(1)
    if code == ord('q'):                                #Q per chiudere
      break



cap.release()
cv2.destroyAllWindows()
