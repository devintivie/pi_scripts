
import sys
sys.path.append('../boonton_src')
sys.path.append('../rabbitmq_dev')

from pi_response_base import *
from boonton_manager import *
from pi_interface_helpers import *

class pi_command_processor(object):
    def __init__(self, config, publisher, boonton_control):
        self.publisher = publisher
        self.name = config['name']
        self.config = config['boonton_parameters']
        # self.commands = commands
        self.boonton_control = boonton_control

        self.status = 'idle'
        self.sensors = list()

    def get_processing_method(self, command, payload):
        if command == 'status_check':
            response_command = f'{command}_response'
            response_object = self.status_check_response(payload)
        elif command == 'boonton_startup':
            response_command = f'{command}_response'
            response_object = self.boonton_startup_response(payload)
        elif command == 'start_poll':
            response_command = f'{command}_response'
            response_object = self.start_poll_response(payload)
        elif command == 'stop_poll':
            response_command = f'{command}_response'
            response_object = self.stop_poll_response(payload)
        else:
            response_command = f'unknown_response'
            response_object = self.unknown_response()

        o = {
            "header" : {
                "command" : response_command,
                "hostname" : self.name,
            },
            "payload" : response_object 
        }
        self.publish(o)

    def publish(self, response_object):
        response_json = json.dumps(response_object, indent=2)
        self.publisher.messages.put(response_json)

    def process_command(self, data):
        command = data.command
        payload = data.payload
        print(f'processing command {command}')
        self.get_processing_method(command, payload)

    def status_check_response(self, payload):
        wlan = if_info('wlan0', getMAC('wlan0'), get_if_ip('wlan0'))
        eth = if_info('eth0', getMAC('eth0'), get_if_ip('eth0'))
        if_list = list()
        if_list.append(wlan)
        if_list.append(eth)
        response = status_check(if_list=if_list)
        response.status = self.status
        response.sensors = self.sensors
        return response.__dict__

    def boonton_startup_response(self, payload):
        print('received boonton startup command')
        response = self.startup_power_meters()
        return response.__dict__

    def start_poll_response(self, payload):
        print('received start poll command')
        response = self.start_poll_power_meters()
        return response.__dict__

    def stop_poll_response(self, payload):
        print('received stop poll command')
        response = self.stop_poll_power_meters()
        return response.__dict__

    def unknown_response(self):
        return dict()

    def startup_power_meters(self):
        response = command_response()
        self.boonton_control.startup()
        sensors = list()
        for sensor in self.boonton_control.sensors.keys():
            sensors.append(sensor_info(sensor).__dict__)
        else:
            response.sensors = sensors
            self.sensors = sensors

        response.status = "startup complete"
        print('startup complete')
        return response

    def start_poll_power_meters(self):
        response = command_response()
        response.status = "started"
        print('started')
        return response

    def stop_poll_power_meters(self):
        response = command_response()
        response.status = "stopped"
        print('stopped')
        return response
