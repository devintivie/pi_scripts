import pika
import json
from payload import payload

# from rpc_classes import *
from payload import *

credentials = pika.PlainCredentials('devin', 'Ikorgil19')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.68.109', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

queue_name = 'rpc_queue'
channel.queue_declare(queue=queue_name)
# def fib(n):
#     if n == 0:
#         return 0
#     elif n == 1:
#         return 1
#     else:
#         return fib(n - 1) + fib(n - 2)
def response_heartbeat(payload):

    status = "ok"
    response_dict = {
        "status" : status
    }
    return response_dict
class callable_dict(dict):
    def __getitem__(self, key):
        val = super().__getitem__(key)
        if callable(val):
            return val()
        return val

commands = callable_dict({
    "heartbeat" : response_heartbeat,
    # "identity" : response_identity
})



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


def on_request(ch, method, props, body):
    data = payload(body)
    response = process_rpc_command(data)

    # n = int(body)

    # print(f"[.] fib({n}, {props.reply_to}")
    # response = fib(n)
    ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id=props.correlation_id), body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=on_request)


channel.start_consuming()
# connection.close()