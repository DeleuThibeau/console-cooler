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

#------------------Code voor componenten via helper klasses----------------

from helpers.Mcp import Mcp
from helpers.Pir import Pir
from helpers.Ventilator import Ventilator
from helpers.OneWire import OneWire
from helpers.Ldr import Ldr
from helpers.UltraSonic import UltraSonic
from helpers.Lcd import LCD

#-------------------------------Variabelen----------------------------

#LDR weerstand variabelen
Mcp = Mcp()
Ldr = Ldr(0)

#OneWire variabelen
OneWire = OneWire()
temp = OneWire.read_one_wire()

#PIR variabele
Pir = Pir()
toestand = Pir.registratie()
print(toestand)

#Ventilator variabele
Ventilator = Ventilator(toestand,18,temp,10)
print(temp)
print(Ventilator.PWM())

#UltraSonic Variabalen
ultra = UltraSonic(27,17)

#LCD variabale
lcd = LCD()

#--------------------------flask/routes/sockets----------------------

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
@socketio.on('connect')
def initial_connection():
    print('A new client connect')

    
#----------------------------------LDR-------------------------------

def create_ldr_metingen():
    while True:
        ActuatorPower = Ventilator.PWM()
        # print(ActuatorPower)
        date = datetime.now()
        json_date = json.dumps(date, indent=4, sort_keys=True, default=str)

        byte = Ldr.spi_lichtsensor()
        Mcp.closepi
        ldr = Ldr.omzetting_lichtsensor(byte)
        DataRepository.create_meting(6,date,ldr,ActuatorPower,'Geen commentaar',20)
        time.sleep(60)

#------------------------------One Wire-----------------------------

def create_oneWire_metingen():
    while True:
        ActuatorPower = Ventilator.PWM()
        # print(ActuatorPower)
        date = datetime.now()
        json_date = json.dumps(date, indent=4, sort_keys=True, default=str)

        temp = OneWire.read_one_wire()
        DataRepository.create_meting(7,date,temp,ActuatorPower,'Geen commentaar',25)
        time.sleep(60)

#----------------------------Ultra Sonic----------------------------

def create_ultraSonic_metingen():
    while True:
        ActuatorPower = Ventilator.PWM()
        # print(ActuatorPower)
        date = datetime.now()
        json_date = json.dumps(date, indent=4, sort_keys=True, default=str)

        afstand = ultra.meting()
        DataRepository.create_meting(9,date,afstand,ActuatorPower,'Geen commentaar',25)
        time.sleep(60)

#------------------------------LCD----------------------------------

def lcd_display():
    print('test')
    while True:
        lcd.ipAdres()
        time.sleep(60)

threading.Timer(60, create_ldr_metingen).start()
threading.Timer(60, create_oneWire_metingen).start()
threading.Timer(1, create_ultraSonic_metingen).start()
threading.Timer(60, lcd_display).start()

#----------------------if__name__='__main__'------------------------

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')  