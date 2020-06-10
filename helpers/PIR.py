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
        self.buffer = 0 #PIR Sensor blijft voor een bepaalde tijd op 1 staan (2 tellen) => Buffer nodig zodat ventilator niet constant uitgaat na x-aantal seconden.
        self.triggered = False

    def registratie(self):
        waarde =GPIO.input(self.pin)
        if waarde==1 and self.triggered == False: 
            self.buffer +=1
            if self.buffer == 4:
                self.counter = 0
                self.buffer = 0
            else:
                self.counter = 1 

            self.triggered == True                      
            
        elif waarde==0:  
            self.triggered = False          

        return self.counter
            

