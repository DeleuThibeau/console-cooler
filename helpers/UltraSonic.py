import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

Trig = 17
Echo = 27

print('Afstand meten in progress')

GPIO.setup(Trig, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)

try:
    while True:

        GPIO.output(Trig, False)
        print('Wachten op sensor')
        time.sleep(2)

        GPIO.output(Trig, True)
        time.sleep(0.00001)
        GPIO.output(Trig, False)

        while GPIO.input(Echo) == 0:
            pulse_start = time.time()

        while GPIO.input(Echo) == 1:
            puls_end = time.time()

        pulse_duration = puls_end - pulse_start

        distance = pulse_duration*17150
        adj_distance = distance*0.98

        distance = round(distance, 2)
        print(f'Distance: {distance} cm')

        airflow = (5/2) * ((distance + adj_distance)/(distance*adj_distance))
        print(airflow)

except Exception as ex:
    print(ex)

finally:
    print('\n Script is ten einde, cleanup is klaar')
    GPIO.cleanup()
