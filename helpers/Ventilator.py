from RPi import GPIO
import time

class Ventilator():
    def __init__(self, pin, temperatuur, set_temp):
        self.pin = pin
        self.temperatuur = temperatuur
        self.set_temp = set_temp
        self.ActuatorPower = ''

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(motor,GPIO.OUT)
        self.pwm_motor = GPIO.PWM(motor,1000)


    def PWM(self):
        if self.temperatuur >= self.set_temp + 2.5 or self.temperatuur <= self.set_temp + 4:
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

        return self.ActuatorPower


