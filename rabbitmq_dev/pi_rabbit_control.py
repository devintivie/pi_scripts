from mq_consumer import *
from mq_publisher import *
from none_publisher import *
import os
import json
import time

print('pi rabbit control starting')
if len(sys.argv) > 1:
    config_file = sys.argv[1]
else:
    config_file = 'test_rabbitmq.json'
# print(f'rabbit config file = {config_file}')
try:
    with open(config_file) as f:
        config = json.load(f)['config']
except FileNotFoundError as error:
    curr_dir = os.path.dirname(__file__)
    with open(curr_dir + '/' +config_file) as f:
        config = json.load(f)['config']

print('pi json loaded')
file_credentials = config['credentials']
print('pi credentials')
file_parameters = config['rabbit_parameters']
print('pi parameters')
print('start wait for init')
time.sleep(5)
print('end wait for init')
credentials = pika.PlainCredentials(file_credentials['user'], file_credentials['password'])
pub_parameters = pika.ConnectionParameters(
    host=file_parameters['host'], 
    port=file_parameters['port'], 
    virtual_host=file_parameters['vhost'], 
    credentials=credentials,
    heartbeat=file_parameters['heartbeat'],
    client_properties={
        'connection_name' : file_parameters['publisher_name']
    })

con_parameters = pika.ConnectionParameters(
    host=file_parameters['host'], 
    port=file_parameters['port'], 
    virtual_host=file_parameters['vhost'], 
    credentials=credentials,
    heartbeat=file_parameters['heartbeat'],
    client_properties={
        'connection_name' : file_parameters['consumer_name']
    })

print('pi parameters set')
pub = mq_publisher(pub_parameters)
file_routing = list(config['routing_keys'])
con = mq_consumer(config['name'], con_parameters, file_routing, pub)
print('publisher start run()')
pub.start()
print('consumer start run()')
con.start()
print('publisher post run()')
print()
print('listening for routing keys as')
for fr in file_routing:
    print(fr)

while True:
    try:
        time.sleep(0.5)
        # if(con.should_reconnect):
        #     print('need to reconnect')
        #     con.connect()
        # else:
        #     print('running fine')
        # con.run()
    except KeyboardInterrupt:
        con.stop()
        pub.stop()
        break