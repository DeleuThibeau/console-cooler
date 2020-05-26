from RPi import GPIO
import time
from PIR import PIR

Pir = PIR(20)
Vent = Ventilator()

try: 
    while True:
        Pir.registratie()
        time.sleep(1)


except KeyboardInterrupt as e:
    print(e)
    # GPIO.output(motor,GPIO.LOW)

finally:
    GPIO.cleanup()
    print("Script has stopped")        
        