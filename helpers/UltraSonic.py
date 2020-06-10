import RPi.GPIO as GPIO
import time
from datetime import datetime

class UltraSonic:
    def __init__(self,echo, trig): 
        self.echo = echo
        self.trig = trig
        self.__setup()
        self.distance = 0

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def meting(self):
        GPIO.output(self.trig, False)
        time.sleep(2)

        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()

        while GPIO.input(self.echo) == 1:
            puls_end = time.time()

        pulse_duration = puls_end - pulse_start

        self.distance = pulse_duration*17150
        # adj_distance = self.distance*0.98

        self.distance = round(self.distance, 2)

        #Distance sensor geeft waarde van rond de 1000 als er geen verandering is in afstand => Delen zodat hij 0 geeft (=> Geen verandering)

        if self.distance > 80:
            self.distance = self.distance /101900000
        
        # print(f'Distance: {self.distance:.2f} cm')

        return self.distance
        