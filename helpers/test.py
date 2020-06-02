from Ventilator import Ventilator
from RPi import GPIO
import time
from PIR import Pir


pir = Pir()
try:
    while True:
        pir.registratie()
        time.sleep(1)
        

except KeyboardInterrupt as e:
    print(e)
    # GPIO.output(motor,GPIO.LOW)

finally:
    GPIO.cleanup()
    print("Script has stopped")   





#------------------------------------------------------------------


# from RPi import GPIO
# import time

# set_temp = int(input("Geef de gewenste temperatuur in: "))
# sensorid = ["28-011610c65dee"]
# temp = {}

# motor=18


# GPIO.setmode(GPIO.BCM)


# GPIO.setup(motor,GPIO.OUT)
# pwm_motor = GPIO.PWM(motor,1000)


# print("Script is running")

# try:
#     while True:

#         for sensor in range(len(sensorid)):
#             temperatuur_file = open("/sys/bus/w1/devices/" + sensorid[sensor] + "/w1_slave")
#             text = temperatuur_file.read()
#             temperatuur_file.close()
#             secondline = text.split("\n")[1]
#             temperatuur_data = secondline.split(" ")[9]
#             temperatuur = float(temperatuur_data[2:])
#             temp[sensor] = temperatuur / 1000
#             temperatuur = temp[sensor]
#             print(f'De huidige temperatuur is {temperatuur} °C')
#             time.sleep(1)



#         if temperatuur >= set_temp + 2.5 or temperatuur <= set_temp + 4:
#             pwm_motor.start(100)
#             pwm_motor.ChangeDutyCycle(30)

#         if temperatuur > set_temp + 4 or temperatuur <= set_temp + 6:
#             pwm_motor.ChangeDutyCycle(50) 

#         if temperatuur > set_temp + 6:
#             pwm_motor.ChangeDutyCycle(100)

#         if temperatuur < set_temp + 1.5:
#             pwm_motor.stop()




# except KeyboardInterrupt as e:
#     print(e)
#     # GPIO.output(motor,GPIO.LOW)

# finally:
#     GPIO.cleanup()
#     print("Script has stopped")        
        
        








