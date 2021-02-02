
import socket
import fcntl
import struct

from pi_response_base import *

def getMAC(interface='eth0'):
    try:
        name = open(f'/sys/class/net/{interface}/address').read()
    except:
        name = "00:00:00:00:00:00"
    return name[:17]

def get_if_ip(interface='eth0'):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_address = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(interface[:15], 'utf-8')))[20:24])
    except OSError:
        ip_address = 'if down'
    s = None
    return ip_address

def status_check_response(payload):
    wlan = if_info('wlan0', getMAC('wlan0'), get_if_ip('wlan0'))
    eth = if_info('eth0', getMAC('eth0'), get_if_ip('eth0'))
    # wlan_mac = getMAC('wlan0')
    # waln_ip = get_if_ip('wlan0')
    # eth_mac = getMAC('eth0')
    # eth_ip = get_if_ip('eth0')# except :
    #     return "Bloody Error In'it?" 
    if_list = list()
    if_list.append(wlan)
    if_list.append(eth)
    response = status_check(if_list=if_list)
    response.status = "ok"
    # status = "ok"
    # response_dict = {

    #     "status" : status
    # }
    return response.__dict__

class callable_dict(dict):
    def __getitem__(self, key):
        val = super().__getitem__(key)
        if callable(val):
            return val()
        return val

commands = {
    "status_check" : lambda x : status_check_response(x),
    # "identity" : response_identity
}



class pi_command_processor(object):
    def process(self, data):
        command = data.command
        payload = data.payload

        response_object = commands[command](payload)
        return response_object