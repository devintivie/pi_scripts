import pika

# Step #3
def on_open(connection):

    connection.channel(on_open_callback=on_channel_open)

# Step #4
def on_channel_open(channel):

    # channel.basic_publish('test_exchange',
    #                         'test_routing_key',
    #                         'message body value',
    #                         pika.BasicProperties(content_type='text/plain',
    #                                              delivery_mode=1))

    data = 'hello'
    exchange_name = "rtsh_topics"
    while True:
        channel.basic_publish(exchange=exchange_name, routing_key='master.control.response', body=str(data))

        # connection.close()

# Step #1: Connect to RabbitMQ
# parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
credentials = pika.PlainCredentials('devin', 'Ikorgil19')
parameters = pika.ConnectionParameters(
    host='192.168.68.109', 
    port=5672, 
    virtual_host='/', 
    credentials=credentials,
    heartbeat=0)

connection = pika.SelectConnection(parameters=parameters,
                                   on_open_callback=on_open)

try:

    # Step #2 - Block on the IOLoop
    connection.ioloop.start()

# Catch a Keyboard Interrupt to make sure that the connection is closed cleanly
except KeyboardInterrupt:

    # Gracefully close the connection
    connection.close()

    # Start the IOLoop again so Pika can communicate, it will stop on its own when the connection is closed
    connection.ioloop.start()