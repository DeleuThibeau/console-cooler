# pylint: skip-file
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS

import time
from datetime import datetime
import threading
import json
import subprocess
from RPi import GPIO
import spidev

#---------------------------------------------------Code voor componenten via helper klasses------------------------------------------------------------

from helpers.Mcp import Mcp
from helpers.PIR import Pir
from helpers.Ventilator import Ventilator
from helpers.OneWire import OneWire
from helpers.Ldr import Ldr
from helpers.UltraSonic import UltraSonic
from helpers.Lcd import LCD

#-------------------------------------------------------------Klasse variabelen------------------------------------------------------------------------

#LDR weerstand variabelen
Mcp = Mcp()
Ldr = Ldr(0)

#OneWire variabelen
OneWire = OneWire()
temp = OneWire.read_one_wire()

#PIR variabele
pir = Pir()

#Ventilator
Ventilator = Ventilator(1, 18, temp, 10)


#UltraSonic Variabalen
ultra = UltraSonic(27,17)

#LCD variabale
lcd = LCD()

#------------------------------------------------------------flask/routes/sockets-----------------------------------------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
# socketio = SocketIO(app)
CORS(app)


endpoint = '/api/v1'


# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


@app.route(endpoint + '/metingen', methods=['GET'])
def get_metingen():
    if request.method == 'GET':
        s = DataRepository.read_metingen()
        return jsonify(Metingen=s), 200

@app.route(endpoint + '/metingen/<DeviceID>', methods=['GET'])
def get_metingen_device(DeviceID):
    if request.method == 'GET':
        s = DataRepository.read_metingen_device(DeviceID)
        return jsonify(Metingen_Device=s), 200

@app.route(endpoint + '/devices', methods=['GET'])
def get_all_devices():
    if request.method == 'GET':
        s = DataRepository.read_devices()
        return jsonify(Devices=s), 200

@app.route(endpoint + '/<device>', methods=['GET'])
def get_device(DeviceID):
    if request.method == 'GET':
        s = DataRepository.read_device(DeviceID)
        return jsonify(Device=s), 200

# SOCKET IO
# @socketio.on('connect')
# def initial_connection():
#     print('A new client connect')

#-------------------------------------------------------CREATIE METINGEN / LCD DISPLAY----------------------------------------------------------------------

#--------------------------------LDR--------------------------------

def create_ldr_metingen():
    while True:
        ActuatorPower = Ventilator.set_active()
        print(ActuatorPower)
        date = datetime.now()
        json_date = json.dumps(date, indent=4, sort_keys=True, default=str)

        byte = Ldr.spi_lichtsensor()
        Mcp.closepi()
        ldr = Ldr.omzetting_lichtsensor(byte)
        DataRepository.create_meting(6,date,ldr,ActuatorPower,'Geen commentaar',20)
        time.sleep(60)

#------------------------------One Wire-----------------------------

def create_oneWire_metingen():
    while True:
        ActuatorPower = Ventilator.set_active()
        print(ActuatorPower)
        date = datetime.now()
        json_date = json.dumps(date, indent=4, sort_keys=True, default=str)
        temp = OneWire.read_one_wire()


        DataRepository.create_meting(7,date,temp,ActuatorPower,'Geen commentaar',25)
        time.sleep(60)

#----------------------------Ultra Sonic----------------------------

def create_ultraSonic_metingen():
    while True:
        ActuatorPower = Ventilator.set_active()
        print(ActuatorPower)
        date = datetime.now()
        json_date = json.dumps(date, indent=4, sort_keys=True, default=str)

        afstand = ultra.meting()
        DataRepository.create_meting(9,date,afstand,ActuatorPower,'Geen commentaar',25)
        time.sleep(60)

#------------------------------LCD----------------------------------

def lcd_display():
    # print('test')
    while True:
        lcd.ipAdres()
        time.sleep(60)
    


#----------------------------PIR-----------------------------------


#---------------------------Threads---------------------------------

#LDR
threading.Timer(10, create_ldr_metingen).start()

#TEMPERATUUR
threading.Timer(10, create_oneWire_metingen).start()

#ULTRA SONIC
threading.Timer(10, create_ultraSonic_metingen).start()

#LCD
threading.Timer(60, lcd_display).start()

#Ventilator
# threading.Timer(1,thread_ventilator).start()


#------------------------------------------------------------if__name__='__main__'------------------------------------------------------------------------

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')  