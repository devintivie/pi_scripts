from mq_consumer import *
from mq_publisher import *
import os
import json
import time

if len(sys.argv) > 1:
    config_file = sys.argv[1]
else:
    config_file = 'pc_rabbitmq.json'

try:
    with open(f'{config_file}') as f:
        config = json.load(f)['config']
except FileNotFoundError as error:
    curr_dir = os.path.dirname(__file__)
    with open(f'{curr_dir}/{config_file}') as f:
        config = json.load(f)['config']

file_credentials = config['credentials']
file_parameters = config['rabbit_parameters']
credentials = pika.PlainCredentials(file_credentials['user'], file_credentials['password'])
parameters = pika.ConnectionParameters(
    host=file_parameters['host'], 
    port=file_parameters['port'], 
    virtual_host=file_parameters['vhost'], 
    credentials=credentials,
    heartbeat=file_parameters['heartbeat'])

pub = mq_publisher(parameters)
file_routing = list(config['routing_keys'])
con = mq_consumer(config['name'], parameters, file_routing, pub)
print('publisher start run()')
pub.start()
print('consumer start run()')
con.start()
print('publisher post run()')

while True:
    try:
        time.sleep(0.5)
    except KeyboardInterrupt:
        con.stop()
        pub.stop()
        break