from RPi import GPIO
import time

class OneWire:
    def __init__(self):
        self. sensorid = ["28-011610c65dee"]
        self.temp = {}
        # self.gewenste_temp = gewenste_temp

    def read_one_wire(self):
        for sensor in range(len(self.sensorid)):
            temperatuur_file = open("/sys/bus/w1/devices/" + self.sensorid[sensor] + "/w1_slave")
            text = temperatuur_file.read()
            temperatuur_file.close()
            secondline = text.split("\n")[1]
            temperatuur_data = secondline.split(" ")[9]
            temperatuur = float(temperatuur_data[2:])
            self.temp[sensor] = temperatuur / 1000
            temperatuur = self.temp[sensor]
            # print(f'De huidige temperatuur is {temperatuur} °C')
        return temperatuur
    
    # def ingestelde_temp(self, gewenste_temp):
         


    def test(self):
        x = print('Hallo')
        return x



        
