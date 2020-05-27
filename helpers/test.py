from RPi import GPIO
import time
from LCD import LCD

GPIO.setmode(GPIO.BCM)
# Lcd = LCD(23,24,25,12,16,21,26,19,13,6)
lcd = LCD(23,24,6,13,19,26,21,16,12,25)
# lcd= LCD(False,24,23,6,13,19,26,21,16,12,25)

try:
    while True:
        lcd.tekst()
        time.sleep(1)
        

except Exception as ex:
    print(ex)


finally:
    print('\n Script is ten einde, cleanup is klaar')
    GPIO.cleanup()
        