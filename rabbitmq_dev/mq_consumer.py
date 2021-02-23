import functools
import time
import pika
import sys
import json

import threading
# from pi_response_base import *
from payload import payload
# from pc_command_processor import pc_command_processor
from pi_command_processor import pi_command_processor
# from pi_control_commands import *

class mq_consumer(threading.Thread):

    def __init__(self, name, parameters, routing_keys, publisher):
        threading.Thread.__init__(self)
        self.connection_parameters = parameters
        self.name = name
        self.exchange_name = "rtsh_topics"
        self.routing_keys = routing_keys#["rasp.control.pi1", "rasp.control.*"]
        self._stopping = False
        self.queue_name = ''
        self.publisher = publisher
        self.command_processor = pi_command_processor()

        self.should_reconnect = False
        self.was_consuming = False

        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        # self._url = amqp_url
        self._is_consuming = False
        # In production, experiment with higher prefetch values
        # for higher consumer throughput
        self._prefetch_count = 1
        

    def connect(self):
        try:
            # print('connect start')
            conn = pika.SelectConnection(
                parameters=self.connection_parameters,
                on_open_callback=self.on_connection_open,
                on_open_error_callback=self.on_connection_open_error,
                on_close_callback=self.on_connection_closed)

            self._connection = conn
        except Exception:
            print('connect exception')
    
    def on_connection_open(self, _unused_connection):
        # print(f'on connection open')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_connection_open_error(self, _unused_connection, err):
        print(f'on connection error = {err}')
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason):
        self._channel = None
        print(f' connection_closed_reason = {reason}')
        if self._closing:
            self._connection.ioloop.stop()
        else:
            self.reconnect()

    def on_channel_open(self, channel):
        # print('on channel open')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange()

    def add_on_channel_close_callback(self):
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        print(f'channel closed, reason = {reason}')
        self.close_connection()

    def setup_exchange(self):#, exchange_name):
        cb = functools.partial(
            self.on_exchange_declareok, userdata=self.exchange_name)
        self._channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type= 'topic',
            callback=cb)

    def on_exchange_declareok(self, _unused_frame, userdata):
        self.setup_queue()

    def setup_queue(self):
        cb = functools.partial(self.on_queue_declareok, userdata=self.queue_name)
        self._channel.queue_declare(queue=self.queue_name, exclusive=True, auto_delete=True, callback=cb)

    def on_queue_declareok(self, _unused_frame, userdata):
        queue_name = userdata
        cb = functools.partial(self.on_bindok, userdata=queue_name)
        for key in self.routing_keys:
            self._channel.queue_bind(
                queue_name,
                self.exchange_name,
                routing_key= key,
                callback=cb)

    def on_bindok(self, _unused_frame, userdata):
        self.set_qos()

    def set_qos(self):
        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame):
        self.start_consuming()

    def start_consuming(self):
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(
            self.queue_name, self.on_message)
        self.was_consuming = True
        self._is_consuming = True

    def add_on_cancel_callback(self):
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        if self._channel:
            self._channel.close()

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.
        :param pika.channel.Channel _unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param bytes body: The message body
        """

        data = payload(body)
        response = self.process_rpc_command(data)
        # print('processed response')
        # print(response)
        # print()
        self.publisher.messages.put(response)
        self.acknowledge_message(basic_deliver.delivery_tag)

    def process_rpc_command(self, data):
        command = data.command
        # payload = data.payload

        response = self.command_processor.process(data)#    commands[command](payload)

        o = {
            "header" : {
                "command" : f"{command}_response",
                "hostname" : self.name,
            },
            "payload" : response 
        }

        response_json = json.dumps(o, indent=2)
        
        return response_json

    def acknowledge_message(self, delivery_tag):
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
            cb = functools.partial(
                self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelok(self, _unused_frame, userdata):
        self.close_channel()

    def close_channel(self):
        self._channel.close()

    def close_connection(self):
        self._is_consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            print('Connection is closing or already closed')
        else:
            self._connection.close()
            self.stop()

    def reconnect(self):
        """Will be invoked if the connection can't be opened or is
        closed. Indicates that a reconnect is necessary then stops the
        ioloop.
        """
        self.should_reconnect = True
        self.stop()

    def run(self):
        """Run the example consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the SelectConnection to operate.
        """
        self.connect()
        self._connection.ioloop.start()

    def stop(self):
        """Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection. The IOLoop is started again because this method is invoked
        when CTRL-C is pressed raising a KeyboardInterrupt exception. This
        exception stops the IOLoop which needs to be running for pika to
        communicate with RabbitMQ. All of the commands issued prior to starting
        the IOLoop will be buffered but not processed.
        """
        if not self._closing:
            self._closing = True
            if self._is_consuming:
                self.stop_consuming()
                # self._connection.ioloop.start()
            else:
                self._connection.ioloop.stop()




if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = 'pc'
    credentials = pika.PlainCredentials('devin', 'Ikorgil19')
    parameters = pika.ConnectionParameters(
        host='192.168.68.109', 
        port=5672, 
        virtual_host='/', 
        credentials=credentials,
        heartbeat=0)

    con = mq_consumer(name, parameters, None)
    print('consumer start run()')
    con.start()
    while True:
        try:
            time.sleep(0.5)
            con.run()
        except KeyboardInterrupt:
            con.stop()
            break
            # pub.stop()

    print('consumer post run()')


