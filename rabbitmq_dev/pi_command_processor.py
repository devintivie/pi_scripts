
import sys
import os
sys.path.append('../boonton_src')
sys.path.append('../rabbitmq_dev')

from pi_response_base import *
from boonton_manager import *
from pi_interface_helpers import *
import boonton_helpers

# dispatch = {
#     'status_check' : status_check_response
# }

class pi_command_processor(object):
    def __init__(self, config, publisher, boonton_control):
        self.publisher = publisher
        self.name = config['name']
        # self.config = config['boonton_parameters']

        self.boonton_control = boonton_control

        self.status = 'idle'
        self.sensors = list()

    # def get_processing_method(self, command, payload):
    #     if command == 'status_check':
    #         response_command = f'{command}_response'
    #         response_object = self.status_check_response(payload)
    #     elif command == 'boonton_startup':
    #         response_command = f'{command}_response'
    #         response_object = self.boonton_startup_response(payload)
    #     elif command == 'start_poll':
    #         response_command = f'{command}_response'
    #         response_object = self.start_poll_response(payload)
    #     elif command == 'stop_poll':
    #         response_command = f'{command}_response'
    #         response_object = self.stop_poll_response(payload)
    #     else:
    #         response_command = f'unknown_response'
    #         response_object = self.unknown_response()

    #     o = {
    #         "header" : {
    #             "command" : response_command,
    #             "hostname" : self.name,
    #         },
    #         "payload" : response_object 
    #     }
    #     self.publish(o)

    def get_processing_method(self, command, payload):
        response_command = f'{command}_response'
        try:
            user_func = getattr(self, response_command, None)#  dispatch.get(command)
            response_object = user_func(payload)
        except Exception as ex:
            print(f'processing exception -> {ex}, type = {type(ex)}')
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
        msg = publish_message('master.control.response', response_json)
        self.publisher.messages.put(msg)

    def process_command(self, data):
        command = data.command
        payload = data.payload
        print(f'processing command {command}')
        self.get_processing_method(command, payload)

    def status_check_response(self, payload):
        # print('enter status_check response')
        wlan = if_info('wlan0', getMAC('wlan0'), get_if_ip('wlan0'))
        eth = if_info('eth0', getMAC('eth0'), get_if_ip('eth0'))
        if_list = list()
        if_list.append(wlan)
        if_list.append(eth)
        response = status_check(if_list=if_list)
        self.update_sensor_list()
        response.status = self.status
        response.sensors = self.sensors
        return response.__dict__

    def boonton_startup_response(self, payload):
        print('received boonton startup command')
        response = self.startup_power_meters()
        return response.__dict__

    def boonton_close_sensors_response(self, payload):
        print('received boonton startup command')
        response = self.close_power_meters()
        return response.__dict__

    def boonton_reset_sensors_response(self, payload):
        print('received boonton reset command')
        response = self.reset_power_meters()
        return response.__dict__

    def boonton_load_from_config_response(self, payload):
        print('received boonton load config command')
        # response = self.()
        # return response.__dict__
        print(payload)
        # serial = payload.serial
        # print(f'boonton load config serial = {serial}')
        # print(f'filename = {payload.filename}')
        response = self.sensor_load_from_config_file(payload['serial'], payload['filename'])
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
        self.update_sensor_list()

        status = "startup complete"
        self.status = status

        response.status = self.status
        response.sensors = self.sensors
        print(status)
        return response

    def close_power_meters(self):
        response = command_response()
        self.boonton_control.close_all_sensors()
        self.update_sensor_list()

        status = "sensors closed"
        self.status = status

        response.status = status
        response.sensors = self.sensors
        print(status)
        return response

    def reset_power_meters(self):
        response = command_response()
        self.boonton_control.reset_all_sensors()
        self.update_sensor_list()

        status = "sensors reset"
        self.status = status

        response.status = status
        response.sensors = self.sensors
        print(status)
        return response

    def sensor_load_from_config_file(self, serial, filename):
        print(f'sensor load serial = {serial}')
        print(f'sensor load filename = {filename}')
        try:
            with open(filename) as f:
                config = json.load(f)['config']
        except FileNotFoundError:
            curr_dir = os.path.dirname(__file__)
            with open(curr_dir + '/' +filename) as f:
                config = json.load(f)['config']


        response = self.boonton_control.sensors[serial].load_settings_from_dict(config)

        # freq = self.config['rf_frequency']
        # ans = self.boonton_control.sensors[serial].set_frequency(freq)
        # response.status = status
        # response.sensors = self.sensors
        # print(status)
        return response

    def update_sensor_list(self):
        sensors = list()
        for sensor in self.boonton_control.sensors.values():
            sensor.get_frequency()
            print(sensor.trig_settings['frequency'])
            sensors.append(sensor_info(sensor).__dict__)
        else:
            self.sensors = sensors

    def start_poll_power_meters(self):
        response = command_response()
        self.boonton_control.start_polling_power_meters()
        status = "started"
        response.status = status
        self.status = status
        print(response.status)
        return response

    def stop_poll_power_meters(self):
        response = command_response()
        self.boonton_control.stop_polling_power_meters()
        status = "stopped"
        response.status = status
        self.status = status
        print(status)
        return response
