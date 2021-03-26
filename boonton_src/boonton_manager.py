

import os
import sys
from ctypes import *
from boonton_55318 import *
from boonton_helpers import *

class boonton_manager:
    def __init__(self):
        self.lib = cdll.LoadLibrary('./libBoonton55.so.1.0.4')
        # self.lib = None
        print(self.lib)
        self.sensors = dict()

        self.startup()

    def startup(self):
        sensors = self.get_sensors()
        self.create_sensors(sensors)

    def get_sensors(self):
        string_val = create_string_buffer(128)
        ans = self.lib.Btn55xxx_FindResources(";", 128, string_val)
        val = get_ctype_string(string_val)
        
        parts = val.split(';')
        return parts

    def create_sensors(self, device_list):
        for a in device_list:
            serial = a[21:26]
            self.sensors[serial] = boonton_55318(self.lib, serial)
            
    def init_sensors(self):
        for sensor in self.sensors.values():
            sensor.initialize()

    def close_sensors(self):
        for sensor in self.sensors.values():
            sensor.close()
            

    def reset_sensors(self):
        for serial, sensor in self.sensors:
            sensor.reset()

    def get_temps(self):
        for sensor in self.sensors.values():
            print(sensor.get_current_temp)

            