import json

class status_check(object):
    def __init__(self, if_list): # name, 
        # self.name = name
        self.interfaces = list()
        # self.sensors = list()
        for iface in if_list:
            self.interfaces.append(iface.__dict__)
        # for sensor in sensor_list:
        #     self.sensors.append(sensor)

class command_response(object):
    pass

class publish_message(object):
    def __init__(self, routing_key, message):
        self.routing_key = routing_key
        self.message = message
    

class data_message(object):
    def __init__(self, serial, data):
        self.serial = serial
        

# class rabbitmq_response(object):
#     def __init__(self): # name, 
#         self.status = 'idle'
#         self.interfaces = list()
#         self.sensors = list()
    
#     def set_interfaces(self, if_list):
#         self.interfaces.clear()
#         for iface in if_list:
#             self.interfaces.append(iface.__dict__)

class if_info(object):
    def __init__(self, if_name, mac, ip):
        self.name = if_name
        self.mac = mac
        self.ip_address = ip

class sensor_info(object):
    def __init__(self, sensor):
        # print(f'sensor info -> {sensor._handle}')
        self.serial_number = sensor.serial
        self.status = str(sensor.status)