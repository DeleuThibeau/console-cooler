from helpers.Mcp import Mcp
from RPi import GPIO

class Ldr:
    def __init__(self, adres):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.Mcp = Mcp()
        self.adres = adres

    def spi_lichtsensor(self):
        self.Mcp.read_channel(self.adres)
        return self.Mcp.read_channel(self.adres)
    
    def omzetting_lichtsensor(self, byte):
        global percentage_lichtsensor
        percentage_lichtsensor = (byte/1023) * 100
        percentage_lichtsensor = 100-percentage_lichtsensor
        # print(
        #     f"De lichtsensor heeft een percentage van: {percentage_lichtsensor:.2f}%")
        return percentage_lichtsensor