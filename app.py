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

# Code voor componenten via helper klasses
from helpers.Mcp import Mcp
from helpers.Pir import Pir
from helpers.Ventilator import Ventilator
from helpers.OneWire import OneWire
from helpers.Ldr import Ldr
# from helpers.UltraSonic import UltraSonic

from RPi import GPIO
import spidev


#Globale variabelen
Mcp = Mcp()

OneWire = OneWire()
temp = OneWire.read_one_wire()

Pir = Pir(20)
Ldr = Ldr(0)

Ventilator = Ventilator(18,temp,20)

date = datetime.now()
json_date = json.dumps(date, indent=4, sort_keys=True, default=str)


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


    #-------------------------Ventilator----------------------------
    ActuatorPower = Ventilator.PWM()
    
    #----------------------------LDR--------------------------------

    byte = Ldr.spi_lichtsensor()
    Mcp.closepi
    ldr = Ldr.omzetting_lichtsensor(byte)

    DataRepository.create_meting(2,date,ldr,ActuatorPower,'Geen commentaar')
    data_ldr = DataRepository.read_meting(2)
    data_ldr.update({'Datum': json_date})
    print(f"json van LDR = \n {data_ldr}\n\n")

    socketio.emit('B2F_LDR_weergeven', {'ldr': data_ldr})

    #--------------------------One Wire-----------------------------

    temp = OneWire.read_one_wire()
    DataRepository.create_meting(1,date,temp,ActuatorPower,'Geen commentaar')
    data_temp = DataRepository.read_meting(1)
    data_temp.update({'Datum': json_date})
    print(f"json van temp = \n {data_temp}")

    socketio.emit('B2F_OneWire_weergeven', {'Onewire': data_temp})



if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')  

    


# knop1.on_press(lees_knop)

# DataRepository.create_sensor('One wire','Een warmte sensor',4,'temperatuur','graden celcius')

# DataRepository.create_sensor('PIR Motion sensor','Een bewegingsensor',9,'motione','m/s')

# DataRepository.create_sensor('Ultra sonic sensor','een afstand sensor die wordt gebruikt om de luchtsnelheid te berekenen',5,'afstand','meter')

# DataRepository.create_actuator('Ventilator','Guncaizhu','Een koelingsapparaat dat werkt op 5V',14.99,'Rotatie','Lucht')

# DataRepository.update_Device('Sensor','PIR Motion sensor','m/s', 'Onbekend', 9,'Een bewegingsensor',2)

# DataRepository.update_Device('Sensor','One Wire temperatuur sensor','Graden celcius', 'Dallas', 2,'Een temperatuursensor dat werkt via een MCP3008',1)



# date = datetime.now()

# DataRepository.create_meting(4,1,date,0,0,'Geen commentaar')