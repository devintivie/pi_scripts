import board
import adafruit_ahtx0
from datetime import datetime 
import time
sensor = adafruit_ahtx0.AHTx0(board.I2C())


while(True):
    temp = sensor.temperature * 9 / 5 + 32
    humid = sensor.relative_humidity

    print(f'{datetime.now()}')
    print(f'current temp = {temp:.2f}')
    print(f'humidity = {humid:.2f}')
    print()
    time.sleep(5)
