from RPi import GPIO
import time

class Ventilator():
    def __init__(self,switch_front_end=0, toestand=1, pin=18, temperatuur=21, set_temp=10):
        self.pin = pin
        self.temperatuur = temperatuur
        self.set_temp = set_temp
        self.ActuatorPower = ''
        self.toestand = toestand
        self.switch_front_end = switch_front_end

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin,GPIO.OUT)
        self.pwm_motor = GPIO.PWM(pin,1000)


    def set_active(self, switch_front_end, toestand, temperatuur, set_temp=20):
        self.temperatuur = temperatuur
        self.set_temp = set_temp
        self.toestand = toestand
        self.switch_front_end = switch_front_end
        if self.toestand == 1 and switch_front_end == 1:
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

        else:
            self.pwm_motor.stop()
            self.ActuatorPower = 'OFF'


        return self.ActuatorPower


