from RPi import GPIO
import time
from PIR import PIR
from Ventilator import Ventilator

Pir = PIR(20)
Vent = Ventilator(18,25,20)

try: 
    while True:
        # Pir.registratie()
        x = Vent.PWM()
        print(x)

        time.sleep(1)


except KeyboardInterrupt as e:
    print(e)
    # GPIO.output(motor,GPIO.LOW)

finally:
    GPIO.cleanup()
    print("Script has stopped")        
        