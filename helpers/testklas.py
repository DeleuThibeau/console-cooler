import RPi.GPIO as GPIO
import time

RS = 23
E = 24
lijst_pinnen = [6, 13, 19, 26, 21, 16, 12,25] #D0


def setup():
    # Main program block
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(E, GPIO.OUT)
    GPIO.setup(RS, GPIO.OUT)
    # Lijst pinnen op output zetten
    for pin in lijst_pinnen:
        GPIO.setup(pin, GPIO.OUT)
    # Standaard E hoog zetten
    GPIO.output(E, GPIO.HIGH)


def send_instruction(value):
    GPIO.output(RS, GPIO.LOW)
    set_data_bits(value)
    time.sleep(0.002)

    GPIO.output(E, GPIO.LOW)
    time.sleep(0.002)
    GPIO.output(E, GPIO.HIGH)
    time.sleep(0.01)


def send_character(value):
    GPIO.output(RS, GPIO.HIGH)
    set_data_bits(value)
    time.sleep(0.002)

    GPIO.output(E, GPIO.LOW)
    time.sleep(0.002)
    GPIO.output(E, GPIO.HIGH)
    time.sleep(0.01)


def set_data_bits(value):
    mask = 0b10000000
    for index in range(0, 8):
        pin = lijst_pinnen[index]
        # Als de waarde 1 is tussen mask en waarde (10000000/1xxxxxxx)
        if value & mask:
            GPIO.output(pin, GPIO.HIGH)
        # Als de waarde 0 is tussen mask en waarde (10000000/0xxxxxxx)
        else:
            GPIO.output(pin, GPIO.LOW)

        mask = mask >> 1

def write_message(message):
    lengte_message = len(message)
    # print(lengte_message)
    for letter in range (0,lengte_message):
        letter = message[letter]
        ascii_letter = ord(letter)
        send_character(ascii_letter)
        time.sleep(0.1)

def cursor_on():
    send_instruction(0x0E)
    send_instruction(0x0F)

def cursor_off():
    send_instruction(0x0C)

def tekst():
    vraag = input("Geef een tekst die uw op het display wilt zien? >>\n")
    init_LCD()
    lijn_1 = vraag[0:16] # String afsnijden vanaf 16 tekens
    lijn_2 ='' # String die 16+ tekens moet opvangen
    break_point = lijn_1.rfind(' ') # zoeken naar spatie om daar dan af te breken
    if break_point >= 0 and len(vraag) > 16:
        lijn_1 = lijn_1[0:break_point]
        lijn_2 = vraag[break_point+1:] # +1 of anders springt de 2é lijn 1 teken in naar rechts

    for letter in range(0,len(lijn_1)):
        write_message(lijn_1[letter])

    if len(lijn_2) > 0:
        send_instruction(0x80|0x40)
        for letter in range(0,len(lijn_2)):
            write_message(lijn_2[letter])  

    if len(vraag)>32: # Als de vraag langer is dan 32 karakters, schuift het display op naar links.
        for letter in vraag[32: (len(vraag))]:
            send_instruction(0x18) #Links scrollen  
def cursor():
    vraag = input("Wilt u de cursor aan zetten? (antwoord met je of nee) >>\n")
    if vraag.lower() =='ja':
        cursor_on()
    else:
        cursor_off()

        

def init_LCD():
    send_instruction(0b00111000)  # Function set
    send_instruction(0b00001111)  # Display on
    send_instruction(0b00000001)  # clear display/cursor home



try:
    setup()
    init_LCD()
    while True:
        tekst()
        cursor()
        time.sleep(1)
    
        

except Exception as ex:
    print(ex)


finally:
    print('\n Script is ten einde, cleanup is klaar')
