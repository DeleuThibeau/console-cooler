from RPi import GPIO
import time


class Pir():
    def __init__(self,pin):
        self.pin = pin
        self.counter = 0
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)         #Read output from PIR motion sensor

    def registratie(self):
        pin =GPIO.input(self.pin)
        if pin==0:                 #When output from motion sensor is LOW
            print("No intruders",pin)
            
        elif pin==1:               #When output from motion sensor is HIGH
            print("Intruder detected",pin)
            print(pin)

        return pin
            

