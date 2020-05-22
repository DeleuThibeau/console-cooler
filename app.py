# pylint: skip-file
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

import time
import threading

# -----------------------------------------------------------------------------------------------------------------------------------

# Code voor componenten
from helpers.klasseknop import Button
from helpers.Mcp import Mcp
from RPi import GPIO
import spidev


led1 = 20
knop1 = Button(21)


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led1, GPIO.OUT)


def spi_lichtsensor(waarde):
    Mcp.read_channel(waarde)
    return Mcp.read_channel(waarde)


def omzetting_lichtsensor(byte):
    global percentage_lichtsensor
    percentage_lichtsensor = (byte/1023) * 100
    percentage_lichtsensor = 100-percentage_lichtsensor
    print(
        f"De lichtsensor heeft een percentage van: {percentage_lichtsensor:.2f}%")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)


# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    # vraag de status op van de lampen uit de DB
    status = DataRepository.read_status_lampen()
    socketio.emit('B2F_status_lampen', {'lampen': status})


@socketio.on('F2B_switch_light')
def switch_light(data):
    print('licht gaat aan/uit')
    lamp_id = data['lamp_id']
    new_status = data['new_status']
    # spreek de hardware aan
    # stel de status in op de DB
    res = DataRepository.update_status_lamp(lamp_id, new_status)
    print(lamp_id)
    if lamp_id == "2":
        lees_knop(20)
    # vraag de (nieuwe) status op van de lamp
    data = DataRepository.read_status_lamp_by_id(lamp_id)
    socketio.emit('B2F_verandering_lamp', {'lamp': data})


def lees_knop(pin):
    print("button pressed")
    if GPIO.input(led1) == 1:
        GPIO.output(led1, GPIO.LOW)
        res = DataRepository.update_status_lamp("2", "0")
    else:
        GPIO.output(led1, GPIO.HIGH)
        res = DataRepository.update_status_lamp("2", "1")
    data = DataRepository.read_status_lamp_by_id("2")
    socketio.emit('B2F_verandering_lamp', {'lamp': data})

try:
    setup()
    Mcp = Mcp()
    while True:
        lichtsensor = spi_lichtsensor(0)
        Mcp.closepi
        omzetting_lichtsensor(lichtsensor)
        time.sleep(1)

    knop1.on_press(lees_knop)

except Exception as ex:
    print(ex)

finally:
    print('\n Script is ten einde, cleanup is klaar')
    GPIO.cleanup()



if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
