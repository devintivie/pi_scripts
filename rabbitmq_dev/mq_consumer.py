
from mq_consumer_worker import *
from time import sleep


class mq_consumer(threading.Thread):
    def __init__(self, parameters, routing_keys, processor):
        threading.Thread.__init__(self)
        self.reconnect_delay = 0
        # self.name = name
        self.parameters = parameters
        self.routing_keys = routing_keys
        # self.publisher = publisher
        self.processor = processor
        self._worker = mq_consumer_worker(self.parameters, self.routing_keys, self.processor)

    def run(self):
        while True:
            try:
                print('run worker')
                self._worker.run()
            except KeyboardInterrupt:
                self._worker.stop()
                break
            print('maybe reconnect')
            self.maybe_reconnect()

    # def start(self):
    #     # self._worker.start()
    #     self.run()

    def interrupt(self):
        self._worker.interrupt()

    def maybe_reconnect(self):
        if self._worker.should_reconnect:
            self._worker.stop()
            reconnect_delay = self._get_reconnect_delay()
            time.sleep(reconnect_delay)
            self._worker = mq_consumer_worker(self.parameters, self.routing_keys, self.processor)
    
    def _get_reconnect_delay(self):
        if self._worker.was_consuming:
            self._reconnect_delay = 0
        else:
            self._reconnect_delay =5
        # if self._reconnect_delay > 30:
        #     self._reconnect_delay = 30
        return self._reconnect_delay

if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = 'pc'
    credentials = pika.PlainCredentials('devin', 'Ikorgil19')
    parameters = pika.ConnectionParameters(
        host='169.254.208.1', 
        port=5672, 
        virtual_host='/', 
        credentials=credentials,
        heartbeat=30)

    pub = none_publisher()
    con = mq_consumer(name, parameters, ["temp"], pub)
    print('consumer start run()')
    con.run()
    # # con.start()
    # while True:
    #     try:
    #         time.sleep(0.5)
    #         print('try run')
    #         con.run()
    #     except KeyboardInterrupt:
    #         con.stop()
    #         break
    #         # pub.stop()

    print('consumer post run()')


