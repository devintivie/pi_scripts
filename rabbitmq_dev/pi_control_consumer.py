import pika
import json
import sys
from payload import payload
import socket
import fcntl
import struct

from pi_response_base import *

name = sys.argv[1]

credentials = pika.PlainCredentials('devin', 'Ikorgil19')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.68.109', 
    port=5672, 
    virtual_host='/', 
    credentials=credentials,
    heartbeat=0))

channel = connection.channel()

exchange_name = "rtsh_topics"
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue
routing_key = f"rasp.control.{name}"
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)


routing_key_all = "rasp.control.all"
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key_all)

def getMAC(interface='eth0'):
    try:
        name = open(f'/sys/class/net/{interface}/address').read()
    except:
        name = "00:00:00:00:00:00"
    return name[:17]

def get_if_ip(interface='eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_address = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(interface[:15], 'utf-8')))[20:24])
    s = None
    return ip_address

def response_heartbeat(payload):
    # try:
    mac = getMAC('wlan0')
    ip = get_if_ip('wlan0')
    # except :
    #     return "Bloody Error In'it?" 
    response = pi_response_base(name=name, mac=mac, ip=ip)
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
    "heartbeat" : lambda x : response_heartbeat(x),
    # "identity" : response_identity
}

def process_rpc_command(data):
    command = data.command
    payload = data.payload

    response = commands[command](payload)

    o = {
        "response" : f"{command}_response",
        "payload" : response 
    }

    response_json = json.dumps(o, indent=2)
    
    return response_json

def callback(ch, method, props, body):
    print(f" [x] {method.routing_key}:{body}")

    # jo = payload(body)
    # print(f"[x] Received message command = {jo.command}")
    # print(f"[x] Received message payload = {jo.payload}")
    data = payload(body)
    response = process_rpc_command(data)

    print(f' [y] responded with {response}')

    
    ch.basic_publish(exchange=exchange_name, routing_key='master.control.response', properties=pika.BasicProperties(correlation_id=props.correlation_id), body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)





channel.basic_consume(queue=queue_name, on_message_callback=callback)
print(f'{name} consuming')
channel.start_consuming()

# connection.close()