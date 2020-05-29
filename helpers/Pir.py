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
        self.pin =GPIO.input(self.pin)
        if self.pin==0:                 #When output from motion sensor is LOW
            # print(self.counter)
            self.counter = 0
            
        elif self.pin==1:               #When output from motion sensor is HIGH
            self.counter += 1
            # print(self.counter)
            if self.counter > 1:
                self.counter -= 2

        return self.counter
            

