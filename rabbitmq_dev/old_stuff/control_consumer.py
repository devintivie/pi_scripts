import pika
import json
from payload import payload

credentials = pika.PlainCredentials('devin', 'Ikorgil19')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.68.109', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

exchange_name = "topic_logs"
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

routing_key = "control.light"

channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")

    jo = payload(body)
    print(f"[x] Received message brightness = {jo.brightness}")


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
# connection.close()