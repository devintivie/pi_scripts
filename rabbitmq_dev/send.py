import pika

credentials = pika.PlainCredentials('devin', 'Ikorgil19')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.68.109', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')

connection.close()