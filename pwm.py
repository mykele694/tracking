import Adafruit_PCA9685
import time

class PwmClass:
    #definisco gli argomenti della classe pwm: a=frequenza del pwm,
    #b=canale su cui vedo il segnale, c=transizione del segnale low-high
    #d= transizione del segnale high-low.
    def __init__(self, freq=60, channel=5, on=0, off=0, cam=0): 
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.set_freq(freq)
        self.ch = channel
        self.start = 375
        if cam == 1:
            self.setting_pwm(self.ch, 0, 375)

    
    def set_freq(self, freq): #setto la frequenza del pwm.
        self.pwm.set_pwm_freq(freq)
    
    #setto su un canale l'inizio e la fine del segnale alto del pwm.
    def setting_pwm(self, ch, on, off): 
        self.pwm.set_pwm(self.ch, on, off)

    def rotate(self, angle):
        if angle > 180:
            angle = 180
        elif angle < 0:
            angle = 0
        dest = int(self.map2(angle))
        #print("DEST",dest)
        self.pwm.set_pwm(self.ch,0,dest)
        #self.slope(self.start,dest)
        self.start = dest
        
    
    def slope(self,start,dest):
        for i in range(start,dest,10):
            self.pwm.set_pwm(self.ch,0,i)
            time.sleep(0.01)

    def map2(self,x,in_min=0,in_max=180,out_min=150,out_max=600):
        return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min

if __name__ == '__main__':
    test = PwmClass(60,15,0,0,1)
    while True:
        for i in range(180):
            test.rotate(i)
            time.sleep(0.01)
        time.sleep(1)
        for i in range(180,0,-1):
            test.rotate(i)
            time.sleep(0.01)
        time.sleep(1)
    
    


