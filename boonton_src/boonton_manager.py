

import os
import sys
import json
import time
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
        # self.startup()startup


    def startup(self):
        sensors = self.get_sensors()
        print('create_sensors')
        self.create_sensors(sensors)
        print('init sensors')
        self.init_all_sensors()
        # print('reset sensors')
        # self.reset_all_sensors()

    def get_sensors(self):
        string_val = create_string_buffer(128)
        result = self.lib.Btn55xxx_FindResources(";", 128, string_val)
        val = get_ctype_string(string_val)
        print(result)
        parts = val.split(';')
        return parts

    def create_sensors(self, device_list):
        for a in device_list:
            serial = a[21:26]
            if not serial in self.sensors:
                print(f'adding <{serial}>')
                if serial != '':
                    self.sensors[serial] = boonton_55318(self.lib, serial, self.config, self.publisher)
            else:
                print(f'<{serial}> is already active')
            
    def init_all_sensors(self):
        print('inside init sensors')
        print(f'sensor count = {len(self.sensors)}')
        for k ,sensor in self.sensors.items():
            print(f'init {k}')
            if not sensor._handle:
                print(f'{k} : start init')
                sensor.initialize()

    def close_all_sensors(self):
        remove_list = list()
        for serial, sensor in self.sensors.items():
            sensor.close()
            remove_list.append(serial)
        for s in remove_list:
            sensor = self.sensors.pop(s, None)
            del sensor
            
    def reset_all_sensors(self):
        print('inside reset sensors')
        for serial,sensor in self.sensors.items():
            print(f'reset sensor {serial}')
            sensor.reset()

    def trace_read(self, serial):
        self.sensors[serial].trace_read()
        data = self.sensors[serial].trace

        print(f'data datatype = {type(data)}')
        jo = {
            "header" : {
                "type" : "trace",
                "serial" : serial 
            },
            "payload" :{
                "data" : data
            }
        }
        response = json.dumps(jo, indent=2)
        self.publisher.messages.put(response)
        time.sleep(1.5)




    

if __name__ == "__main__":
    import sys
    sys.path.append('../rabbitmq_dev')
    from none_publisher import *
    
    config = None
    publisher = none_publisher()
    publisher.start()
    boonton_control = boonton_manager(config, publisher)
    boonton_control.startup()

    boonton_control.trace_read('10208')