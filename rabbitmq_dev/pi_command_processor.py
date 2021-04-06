
import sys
sys.path.append('../boonton_src')
sys.path.append('../rabbitmq_dev')

from pi_response_base import *
from boonton_manager import *
from pi_interface_helpers import *

# commands = {
#     "status_check" : lambda x : status_check_response(x),
#     "start_poll" : lambda x : start_poll_response(x),
#     "stop_poll" : lambda x : stop_poll_response(x)
#     # "identity" : response_identity
# }

class pi_command_processor(object):
    def __init__(self, config, publisher):
        self.publisher = publisher
        self.name = config['name']
        self.config = config['boonton_parameters']
        # self.commands = commands
        self.boonton_manager = boonton_manager(self.config, self.publisher)


        # self.processing_commands = callable_dict({
        #     "status_check" : lambda x : self.status_check_response(x),
        #     # "identity" : response_identity
        # })
        # self.processing_commands = {
        #     {'status_check': lambda x: self.status_check_response(x)}
        # }

    # def process(self, data):
    #     command = data.command
    #     payload = data.payload

    #     response_object = self.commands[command](payload)
    #     return response_object

    def get_processing_method(self, command, payload):
        if command == 'status_check':
            response_command = f'{command}_response'
            response_object = self.status_check_response(payload)
        elif command == 'start_poll':
            response_command = f'{command}_response'
            response_object = self.start_poll_response(payload)
        elif command == 'stop_poll':
            response_command = f'{command}_response'
            response_object = self.stop_poll_response(payload)
        else:
            response_command = f'unknown_response'
            response_object = self.unknown_response()
        # response_object = self.processing_commands[command](payload)

        o = {
            "header" : {
                "command" : response_command,
                "hostname" : self.name,
            },
            "payload" : response_object 
        }
        return o

    def process_command(self, data):
        command = data.command
        payload = data.payload
        print(f'processing command {command}')
        o = self.get_processing_method(command, payload)

        response_json = json.dumps(o, indent=2)
        self.publisher.messages.put(response_json)

    def status_check_response(self, payload):
        wlan = if_info('wlan0', getMAC('wlan0'), get_if_ip('wlan0'))
        eth = if_info('eth0', getMAC('eth0'), get_if_ip('eth0'))
        if_list = list()
        if_list.append(wlan)
        if_list.append(eth)
        response = status_check(if_list=if_list)
        response.status = "ok"
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
