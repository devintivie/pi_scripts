from flask import Flask, render_template, redirect, url_for, request
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
    temp = sensor.temperature * 9 / 5 + 32
    temperature_string = f'{temp:.2f}'
    humid = sensor.relative_humidity    
    humid_string = f'{humid:.2f}'
    timeString = now.strftime("%Y-%m-%d %H:%M:%S:%f")
    templateData = {
        'title' : 'Wine Fridge',
        'time': timeString,
        'temperature' : temperature_string,
        'humidity' : humid_string
    }
    return render_template('index.html', **templateData)

 
   
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
