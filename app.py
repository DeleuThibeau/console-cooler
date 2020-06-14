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

#PIR variabele
pir = Pir()

#UltraSonic Variabalen
ultra = UltraSonic(27,17)

#LCD variabale
lcd = LCD()

#Ventilator
vent = Ventilator(1, 18)

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
        
@app.route(endpoint + '/meting/<DeviceID>', methods=['GET'])
def get_meting_device(DeviceID):
    if request.method == 'GET':
        s = DataRepository.read_meting_device(DeviceID)
        return jsonify(Meting_Device=s), 200

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






@app.route(endpoint + '/treinen/<trein_id>/vertraging', methods=['PUT'])
def update_comment(metingID):
    if request.method == 'PUT':
        gegevens = DataRepository.json_or_formdata(request)
        return jsonify(trein_id=trein_id), 200




#Globale variabele
toggle_switch_front_end = 1
goal_temp = 20


@socketio.on('F2B_switch_toggle')
def switch_toggle(data):
    global toggle_switch_front_end
    print('ventilator gaat aan/uit')
    new_status = data['toggle_status']
    
    toggle_switch_front_end = new_status

    print('De nieuwe status is', new_status)



@socketio.on('F2B_update_goal_temp')
def set_goal_temp(data):
    global goal_temp
    print('goal temp wordt ingesteld')
    new_goal_temp = data['goal_temp']
    
    goal_temp = new_goal_temp
    print('De nieuwe goal temp is', new_goal_temp)
    time.sleep(1)









#--------------------------------------------------CREATIE METINGEN / LCD DISPLAY / WEGSCHRIJVEN NAAR DATABASE-------------------------------------------------------

#--------------------------------LDR--------------------------------
def read_ldr_metingen():
    byte = Ldr.spi_lichtsensor()
    Mcp.closepi()
    ldr = Ldr.omzetting_lichtsensor(byte)
    return ldr

def create_ldr_metingen(date, ldr, ActuatorPower, ID=6, commentaar='Geen commentaar', ingestelde_temp=20):
    DataRepository.create_meting(ID,date,ldr,ActuatorPower,commentaar,ingestelde_temp)

#------------------------------One Wire-----------------------------
def read_onewire_metingen():
    temp = OneWire.read_one_wire()
    return temp

def create_oneWire_metingen(date,temp, ActuatorPower, ID=7, commentaar='Geen commentaar', ingestelde_temp=20):
    DataRepository.create_meting(ID,date,temp,ActuatorPower,commentaar,ingestelde_temp)
    
#----------------------------Ultra Sonic----------------------------
def read_ultrasonic_metingen():
    afstand = ultra.meting()
    return afstand

def create_ultraSonic_metingen(date,ultrasonic, ActuatorPower, ID=9, commentaar='Geen commentaar', ingestelde_temp=20):
    DataRepository.create_meting(ID,date,ultrasonic, ActuatorPower, commentaar, ingestelde_temp)

#--------------------------------PIR--------------------------------
def read_pir():
    toestand = pir.registratie()
    return toestand

# Counter nodig om PIR te laten werken als knop.
counter = 0

#--------------------------------LCD--------------------------------
def lcd_display():
    lcd.ipAdres()


switch_front_end = 0
#----------------------------------------------------Cumulatie (total) van bovenstaande metingen-------------------------------------------------------------
def total():
    while True:
        global counter
        global toggle_switch_front_end
        global goal_temp
        goal_temp = int(goal_temp)

        us_sensor = read_ultrasonic_metingen()
        # print(us_sensor)
        ldr_sensor = read_ldr_metingen()
        # print(ldr_sensor)
        ow_sensor = read_onewire_metingen()
        # print(ow_sensor)
        pir_sensor = read_pir()
        # print(pir_sensor)

        #VentilatorToestand
        actuatorPower = vent.set_active(toggle_switch_front_end, pir_sensor,ow_sensor, goal_temp)

        date = datetime.now()
        json_date = json.dumps(date, indent=4, sort_keys=True, default=str)
        create_ultraSonic_metingen(date,us_sensor, actuatorPower)

        counter +=1
        # print(counter)

        if counter == 15:
            lcd_display()
            date = datetime.now()
            json_date = json.dumps(date, indent=4, sort_keys=True, default=str)

            create_ldr_metingen(date,ldr_sensor, actuatorPower,6,'Geen commentaar',goal_temp)
            create_oneWire_metingen(date,ow_sensor, actuatorPower,7,'Geen commentaar',goal_temp)
            create_ultraSonic_metingen(date,us_sensor, actuatorPower,9,'Geen commentaar',goal_temp)

            counter =0
        # print(counter)

        time.sleep(1)


#------------------------------------------------------------------Threads--------------------------------------------------------------------------------

#Total
threading.Timer(3,total).start()


#------------------------------------------------------------if__name__='__main__'------------------------------------------------------------------------

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')  

# The end