import pika
import sys
import functools
print(sys.version_info.major)
if sys.version_info.major == 3:
    import queue
else:
    import Queue as queue
import time
import threading

class none_publisher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.messages = queue.Queue()

    def schedule_next_message(self):
        try:
            msg = self.messages.get(True, 0.01)
            print(msg)
        except queue.Empty:
            pass

        finally:
            pass 

        threading.Timer(0.1, self.schedule_next_message).start()
        # self.schedule_next_message()


    def stop(self):
        self._stopping = True

    def run(self):
        # while True:
        try:
            self.schedule_next_message()
        except KeyboardInterrupt:
            print('control c seen')
            self.stop()


