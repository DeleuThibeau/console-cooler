# pylint: skip-file
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

import time
from datetime import datetime
import threading
import json

# -----------------------------------------------------------------------------------------------------------------------------------

# Code voor componenten
from helpers.klasseknop import Button
from helpers.Mcp import Mcp
from helpers.PIR import PIR
from helpers.OneWire import OneWire

from RPi import GPIO
import spidev


#Globale variabelen
Mcp = Mcp()
OneWire = OneWire()
Pir = PIR()
date = datetime.now()
json_date = json.dumps(date, indent=4, sort_keys=True, default=str)



# Functies componenten
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    sensorid = ["28-011610c65dee"]
    temp = {}
    


def spi_lichtsensor(waarde):
    global Mcp
    Mcp.read_channel(waarde)
    return Mcp.read_channel(waarde)


def omzetting_lichtsensor(byte):
    global percentage_lichtsensor
    percentage_lichtsensor = (byte/1023) * 100
    percentage_lichtsensor = 100-percentage_lichtsensor
    # print(
    #     f"De lichtsensor heeft een percentage van: {percentage_lichtsensor:.2f}%")
    return percentage_lichtsensor


#--------------------------flask/routes/sockets----------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
# socketio = SocketIO(app)
CORS(app)


# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')


@socketio.on('connect')
def socket_ldr():
    global Mcp
    global date
    global json_date
    global OneWire
    setup()
    
    #----------------------------LDR--------------------------------

    lichtsensor = spi_lichtsensor(0)
    Mcp.closepi

    ldr = omzetting_lichtsensor(lichtsensor)
    DataRepository.create_meting(2,date,ldr,'OFF','Geen commentaar')
    data_ldr = DataRepository.read_meting(2)
    data_ldr.update({'Datum': json_date})
    print(f"json van LDR = \n {data_ldr}\n\n")

    socketio.emit('B2F_LDR_weergeven', {'ldr': data_ldr})

    #--------------------------One Wire-----------------------------

    temp = OneWire.read_one_wire()
    DataRepository.create_meting(1,date,temp,'OFF','Geen commentaar')
    data_temp = DataRepository.read_meting(1)
    data_temp.update({'Datum': json_date})
    print(f"json van temp = \n {data_temp}")

    socketio.emit('B2F_OneWire_weergeven', {'Onewire': data_temp})


# @socketio.on('connect')
# def socket_oneWire():
#     global OneWire
#     global date
#     global json_date
#     setup()

#     temp = OneWire.read_one_wire()
#     DataRepository.create_meting(1,date,temp,'OFF','Geen commentaar')
#     data_temp = DataRepository.read_meting(1)
#     data_temp.update({'Datum': json_date})
#     print(f"json van temp = \n {data_temp}")

#     socketio.emit('B2F_OneWire_weergeven', {'Onewire': data_temp})

    


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')  

# try:
#     setup()
#     Mcp = Mcp()
#     OneWire = OneWire()

#     while True:
#         #---Huidige tijd ophalen voor te schrijven naar databank---
#         date = datetime.now()

#         #-----------------LDR------------------------------
#         lichtsensor = spi_lichtsensor(0)
#         Mcp.closepi

#         ldr = omzetting_lichtsensor(lichtsensor)
        
#         DataRepository.create_meting(2,date,ldr,'OFF','Geen commentaar')
#         data_ldr = DataRepository.read_meting(2)
#         # print(f"json van LDR = \n {data_ldr}\n\n")

#         time.sleep(1)

#         #---------------One Wire----------------------------
#         # temp = OneWire.read_one_wire()
#         # DataRepository.create_meting(1,date,temp,'OFF','Geen commentaar')
#         # data_temp = DataRepository.read_metingen()
#         # print(f"json van temp = \n {data_temp}")

#         # DataRepository.create_metingen(1,date,temp,'OFF','Geen commentaar',2,date,ldr,'OFF','Geen commentaar')


#         socketio.emit('B2F_LDR_weergeven', {'ldr': data_ldr})
        

#         time.sleep(5)


#     # knop1.on_press(lees_knop)

# except Exception as ex:
#     print(ex)

# finally:
#     print('\n Script is ten einde, cleanup is klaar')
#     GPIO.cleanup()
    


# knop1.on_press(lees_knop)

# DataRepository.create_sensor('One wire','Een warmte sensor',4,'temperatuur','graden celcius')

# DataRepository.create_sensor('PIR Motion sensor','Een bewegingsensor',9,'motione','m/s')

# DataRepository.create_sensor('Ultra sonic sensor','een afstand sensor die wordt gebruikt om de luchtsnelheid te berekenen',5,'afstand','meter')

# DataRepository.create_actuator('Ventilator','Guncaizhu','Een koelingsapparaat dat werkt op 5V',14.99,'Rotatie','Lucht')

# DataRepository.update_Device('Sensor','PIR Motion sensor','m/s', 'Onbekend', 9,'Een bewegingsensor',2)

# DataRepository.update_Device('Sensor','One Wire temperatuur sensor','Graden celcius', 'Dallas', 2,'Een temperatuursensor dat werkt via een MCP3008',1)



# date = datetime.now()

# DataRepository.create_meting(4,1,date,0,0,'Geen commentaar')