from flask import Flask, render_template, redirect, url_for, request, jsonify
import flask
import datetime
# from simple_control import simple_controller
app = Flask(__name__)

import board
import adafruit_ahtx0
from datetime import datetime 
import time
sensor = adafruit_ahtx0.AHTx0(board.I2C())

# controller = simple_controller()
@app.route("/")
def hello():
    now = datetime.now()
    temperature_string = get_temperature()
    temperature_string = f'{temperature_string} {chr(176)}F'
    humid_string = get_humidity()
    humid_string = f'{humid_string} %'
    timeString = now.strftime("%Y-%m-%d %H:%M:%S:%f")
    templateData = {
        'title' : 'Wine Fridge',
        'time': timeString,
        'temperature' : temperature_string,
        'humidity' : humid_string
    }
    return render_template('index.html', **templateData)

@app.route('/api/v1/readings/temperature', methods=['GET'])
def api_get_temp():
    print
    temperature_string = get_temperature()
    temp_o = {'temperature' : temperature_string}
    return jsonify(temp_o)

@app.route('/api/v1/readings/humidity', methods=['GET'])
def api_get_humidity():
    humid = get_humidity()
    humid_o = {'humidity' : humid}
    return jsonify(humid_o)

@app.route('/api/v1/readings/all', methods=['GET'])
def api_get_all():
    # print('api get all data')
    temperature = get_temperature()
    humid = get_humidity()
    all_o = {
        'humidity' : humid,
        'temperature' : temperature
        }
    data_return = jsonify(all_o)
    # print(f'data_return = {data_return}')
    return data_return

def get_humidity():
    humid = sensor.relative_humidity  
    # print(type(humid))  
    # return f'{humid:.2f}'
    return humid

def get_temperature():
    temp = sensor.temperature# * 9 / 5 + 32
    # return f'{temp:.2f}'
    return temp
   
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
