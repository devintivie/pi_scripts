

import os
import sys
from ctypes import *
from boonton_55318 import *
from boonton_helpers import *

class boonton_manager:
    def __init__(self, config, mq_publisher):
        curr_dir = os.path.dirname(__file__)
        print(curr_dir)
        self.lib = cdll.LoadLibrary('../boonton_src/libBoonton55.so.1.0.4')
        # self.lib = None
        print(self.lib)
        self.sensors = dict()
        self.config = config
        self.publisher = mq_publisher
        self.startup()

    def startup(self):
        sensors = self.get_sensors()
        print('create_sensors')
        self.create_sensors(sensors)
        print('init sensors')
        self.init_all_sensors()
        print('reset sensors')
        self.reset_all_sensors()

    def get_sensors(self):
        string_val = create_string_buffer(128)
        result = self.lib.Btn55xxx_FindResources(";", 128, string_val)
        val = get_ctype_string(string_val)
        
        parts = val.split(';')
        return parts

    def create_sensors(self, device_list):
        for a in device_list:
            serial = a[21:26]
            print(f'<{serial}>')
            if serial != '':
                self.sensors[serial] = boonton_55318(self.lib, serial, self.config, self.publisher)
            
    def init_all_sensors(self):
        print('inside init sensors')
        print(f'sensor count = {len(self.sensors)}')
        for sensor in self.sensors.values():
            sensor.initialize()

    def close_all_sensors(self):
        for sensor in self.sensors.values():
            sensor.close()
            
    def reset_all_sensors(self):
        print('inside reset sensors')
        for sensor in self.sensors.values():
            sensor.reset()

    