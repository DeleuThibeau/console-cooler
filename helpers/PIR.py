from RPi import GPIO
import time


class Pir():
    def __init__(self,pin=20):
        self.pin = pin
        self.counter = 0
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN) 
        self.counter = 0
        self.triggered = False

    def registratie(self):
        waarde =GPIO.input(self.pin)
        if waarde==1 and self.triggered == False: 
            if self.counter == 1:
                self.counter = 0
            else:
                self.counter = 1 

            self.triggered == True          
            # print(self.counter)
            
            
        elif waarde==0:  
            self.triggered = False          
            # print(self.counter)

        # print(self.counter)
        
        # time.sleep(5)
        return self.counter
            

