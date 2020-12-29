import pika
import json

credentials = pika.PlainCredentials('devin', 'Ikorgil19')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.68.109', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

exchange_name = "topic_logs"
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
routing_key = "voice.command"

o = {
    "command": "turn on",
    "arguments" : [
        "all",
        "lights"
    ]
}

message = json.dumps(o, indent=2)
channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)

connection.close()