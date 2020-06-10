from RPi import GPIO
import time

class Ventilator():
    def __init__(self,toestand=1, pin=18, temperatuur=21, set_temp=10):
        self.pin = pin
        self.temperatuur = temperatuur
        self.set_temp = set_temp
        self.ActuatorPower = ''
        self.toestand = toestand

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin,GPIO.OUT)
        self.pwm_motor = GPIO.PWM(pin,1000)


    def set_active(self, toestand, temperatuur, set_temp=20):
        self.temperatuur = temperatuur
        self.set_temp = set_temp
        self.toestand = toestand
        if self.toestand == 1:
            if self.temperatuur >= self.set_temp + 0.5 or self.temperatuur <= self.set_temp + 4:
                self.pwm_motor.start(100)
                self.pwm_motor.ChangeDutyCycle(50)
                self.ActuatorPower = 'LOW'

            if self.temperatuur > self.set_temp + 4 or self.temperatuur <= self.set_temp + 6:
                self.pwm_motor.ChangeDutyCycle(70) 
                self.ActuatorPower = 'MEDIUM'

            if self.temperatuur > self.set_temp + 6:
                self.pwm_motor.ChangeDutyCycle(100)
                self.ActuatorPower = 'HIGH'

            if self.temperatuur < self.set_temp + 1.5:
                self.pwm_motor.stop()
                self.ActuatorPower = 'OFF'

            # print(self.pin)
            # print(self.toestand)
            # print(self.temperatuur)
            # print(self.set_temp)
            # print(self.ActuatorPower)

        else:
            self.pwm_motor.stop()
            self.ActuatorPower = 'OFF'
            # print(self.pin)
            # print(self.toestand)
            # print(self.temperatuur)
            # print(self.set_temp)
            # print(self.ActuatorPower)


        return self.ActuatorPower


