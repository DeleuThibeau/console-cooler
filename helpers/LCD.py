from RPi import GPIO
import time
import subprocess

class LCD():

    def __init__(self, RS, E, pin7,pin6,pin5,pin4,pin3,pin2,pin1,pin0):
        self.RS = RS
        self.E = E
        self.pin0 = pin0
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4
        self.pin5 = pin5
        self.pin6 = pin6
        self.pin7 = pin7
        self.lijst_pinnen = [self.pin0,self.pin1, self.pin2, self.pin3, self.pin4, self.pin5, self.pin6, self.pin7]
        self.ip = ''
        self.__setup()

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.E, GPIO.OUT)
        GPIO.setup(self.RS, GPIO.OUT)
        # Lijst pinnen op output zetten

        for pin in self.lijst_pinnen:
            GPIO.setup(pin, GPIO.OUT)
        # Standaard E hoog zetten

        GPIO.output(self.E, GPIO.HIGH)
    
    def send_instruction(self,value):
        GPIO.output(self.RS, GPIO.LOW)
        self.set_data_bits(value)
        time.sleep(0.002)

        GPIO.output(self.E, GPIO.LOW)
        time.sleep(0.002)
        GPIO.output(self.E, GPIO.HIGH)
        time.sleep(0.01)


    def send_character(self,value):
        GPIO.output(self.RS, GPIO.HIGH)
        self.set_data_bits(value)
        time.sleep(0.002)

        GPIO.output(self.E, GPIO.LOW)
        time.sleep(0.002)
        GPIO.output(self.E, GPIO.HIGH)
        time.sleep(0.01)


    def set_data_bits(self,value):
        mask = 0b10000000
        for index in range(0, 7):
            pin = self.lijst_pinnen[index]
            # Als de waarde 1 is tussen mask en waarde (10000000/1xxxxxxx)
            if value & mask:
                GPIO.output(pin, GPIO.HIGH)
            # Als de waarde 0 is tussen mask en waarde (10000000/0xxxxxxx)
            else:
                GPIO.output(pin, GPIO.LOW)

            mask = mask >> 1

    def write_message(self,message):
        lengte_message = len(message)
        # print(lengte_message)
        for letter in range (0,lengte_message):
            letter = message[letter]
            ascii_letter = ord(letter)
            self.send_character(ascii_letter)
            time.sleep(0.1)


    def tekst(self):
        vraag = input("Geef een tekst die uw op het display wilt zien? >>\n")
        self.init_LCD()
        lijn_1 = vraag[0:16] # String afsnijden vanaf 16 tekens
        lijn_2 =''
        break_point = lijn_1.rfind(' ') # zoeken naar spatie om daar dan af te breken
        if break_point >= 0 and len(vraag) > 16:
            lijn_1 = lijn_1[0:break_point]
            lijn_2 = vraag[break_point+1:] # +1 of anders springt de 2é lijn 1 teken in naar rechts

        for letter in range(0,len(lijn_1)):
            self.write_message(lijn_1[letter])

        if len(lijn_2) > 0:
            self.send_instruction(0x80|0x40)
            for letter in range(0,len(lijn_2)):
                self.write_message(lijn_2[letter])  

        if len(vraag)>32: # Als de vraag langer is dan 32 karakters, schuift het display op naar links.
            for letter in vraag[32: (len(vraag))]:
                self.send_instruction(0x18) #Links scrollen  

    
    def Ip_adres(self):
        self.ip = subprocess.check_output(['hostname', '--all-ip-addresses']).decode('utf-8')
        self.ip = self.ip[:13]
        print(self.ip)
        # self.tektekstst(self.ip)



    def init_LCD(self):
        self.send_instruction(0b00111000)  # Function set
        self.send_instruction(0b00001111)  # Display on
        self.send_instruction(0b00000001)  # clear display/cursor home
