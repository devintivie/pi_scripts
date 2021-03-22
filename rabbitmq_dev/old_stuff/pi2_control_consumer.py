import pika
import json
from payload import payload

credentials = pika.PlainCredentials('devin', 'Ikorgil19')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.68.109', port=5672, virtual_host='/', credentials=credentials))

channel = connection.channel()

exchange_name = "rtsh_topics"
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue
routing_key = "rasp.control.pi2"
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)


routing_key_all = "rasp.control.*"
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key_all)


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

def callback(ch, method, props, body):
    print(f" [x] {method.routing_key}:{body}")

    # jo = payload(body)
    # print(f"[x] Received message command = {jo.command}")
    # print(f"[x] Received message payload = {jo.payload}")
    data = payload(body)
    response = process_rpc_command(data)

    ch.basic_publish(exchange='', routing_key='rasp.control.master', properties=pika.BasicProperties(correlation_id=props.correlation_id), body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue_name, on_message_callback=callback)

print('consuming....')
channel.start_consuming()
# connection.close()