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

    def registratie(self):

        waarde =GPIO.input(self.pin)
        if waarde==1:                 
            # print(self.counter)
            self.counter = 1
            
        elif waarde==0:               
            self.counter = 0
            # print(self.counter)

        print(self.counter)
        
        # time.sleep(5)
        return self.counter
            

