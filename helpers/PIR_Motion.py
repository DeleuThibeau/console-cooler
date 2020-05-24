from gpiozero import MotionSensor
from datetime import datetime

pir = MotionSensor(17)

try: 
    while True:
        date = datetime.now()
        print(date)
        print('hallo')
        pir.wait_for_motion()
        print('Motion detected')
        pir.wait_for_no_motion()
        print('Motion stopped')

except Exception as ex:
    print(ex)

finally:
    print('\n Script is ten einde, cleanup is klaar')

