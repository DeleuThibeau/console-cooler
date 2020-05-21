from RPi import GPIO
import spidev


class Mcp:
    def __init__(self, bus=0, device=0):
        spidev.SpiDev() 
        spi.open(bus,device)
        self.spi.max_speed_hz= 10 ** 5  

    def read_channel(self, channel):
        spi = spidev.SpiDev() 
        spi.open(0,0)
        spi.max_speed_hz= 10 ** 5  
        # 128 want je potentio is aangesloten op H1 (1000 0000)    
        message =[1,channel,0]

        bytes_in= spi.xfer(message)
        # print(f"De bytes zijn {bytes_in}")
        
        byte_1 = bytes_in[1]
        byte_2 = bytes_in[2]
        shift_byte1 = byte_1 << 8
        totale_byte = shift_byte1 | byte_2
        # print(f"De 10 bits hebben een waarde van {totale_byte} \n\n")

        return totale_byte
 

    def close(self):
        self.spi.close()

