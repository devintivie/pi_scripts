import pika
import sys
import functools
import queue
import time

class mq_publisher(object):
    def __init__(self, name, parameters):
        self.connection_parameters = parameters
        self.name = name
        self.exchange_name = "rtsh_topics"
        self.routing_key='master.control.response'
        self.messages = queue.Queue()
        self._stopping = False
        self.QUEUE = ''

    def connect(self):
        conn = pika.SelectConnection(
            parameters= self.connection_parameters,
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed
        )

        self._connection = conn



    def on_connection_open(self, _unused_connection):
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_connection_open_error(self):
        self.stop()

    def on_connection_closed(self, connection, reason):
        self._channel = None
        print(reason)
        self._connection.ioloop.stop()

    def on_channel_open(self, channel):
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange()

    def add_on_channel_close_callback(self):
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        self._channel = None
        if not self._stopping:
            self._connection.close()

    def setup_exchange(self):
        cb = functools.partial(
            self.on_exchange_declareok, userdata=self.exchange_name)
        self._channel.exchange_declare(exchange=self.exchange_name, exchange_type='topic', callback = cb)
        

    def on_exchange_declareok(self, _unused_frame, userdata):
        # self.setup_queue()
        self.start_publishing()
    
    def setup_queue(self):
        try:
            self._channel.queue_declare('', auto_delete = True, callback=self.on_queue_declareok)#, exclusive=True)
        finally:
            print('wtf')

    def on_queue_declareok(self, frame):
        self._channel.queue_bind(exchange=self.exchange_name, queue=self.QUEUE, routing_key=self.routing_key, callback=self.on_bindok)
   
    def on_bindok(self, frame):
        self.start_publishing()

    def start_publishing(self):
        self.schedule_next_message()

    def schedule_next_message(self):
        try:
            msg = self.messages.get(True, 0.01)
            self._channel.basic_publish(exchange=self.exchange_name, routing_key='master.control.response', body=str(msg))
        except queue.Empty:
            pass
        except pika.exceptions.ChannelWrongStateError as ex:
            print(f'wrong state error ={ex}')

        finally:
            pass 

        self.messages.put("hello")
        if not self._stopping :
            self._connection.ioloop.call_later(0.000, self.schedule_next_message)

        
        # time.sleep(0.001)
        # self.schedule_next_message()
        # self._connection.add_timeout(0.001, self.schedule_next_message)



    def stop(self):
        self._stopping = True
        self.close_channel()
        self.close_connection()

    def close_channel(self):
        """Invoke this command to close the channel with RabbitMQ by sending
        the Channel.Close RPC command.
        """
        if self._channel is not None:
            self._channel.close()

    def close_connection(self):
        """This method closes the connection to RabbitMQ."""
        if self._connection is not None:
            self._connection.close()

    def run(self):
        # while True:
        try:
            self.connect()
            self._connection.ioloop.start()
        except KeyboardInterrupt:
            print('control c seen')
            self.stop()
            if (self._connection is not None and
                    not self._connection.is_closed):
                # Finish closing
                self._connection.ioloop.start()



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

    pub = mq_publisher(name, parameters)
    pub.run()



# channel = connection.channel()