import Queue
import threading
import time

from joyce_byers import alphabet

exit_message = object()

class MessageProcessor(object):
    def __init__(self, max_size, flicker_timeout):
        self.thread = threading.Thread(target=self.run, name='MessageProcessor')
        self.queue = Queue.Queue(maxsize=max_size)
        self.flicker_timeout = flicker_timeout

        self.thread.start()

    def add_message(self, msg):
        try:
        	self.queue.put_nowait(msg)
        	return True
        except Queue.Full:
        	return False

    def stop(self):
        self.queue.put(exit_message, block=True)
        self.thread.join()

    def run(self):
        print 'TODO: Turn on LEDs'
        abc = alphabet.Alphabet()

        while True:
            try:
                msg = self.queue.get(True, self.flicker_timeout)
            except Queue.Empty:
                msg = None

            if msg == exit_message:
                break
            elif msg is not None:
                print 'TODO: Blink out {}'.format(msg)
                abc.message(msg)
                time.sleep(60)
            else:
                print 'TODO: Flicker'
                abc.flicker()
                time.sleep(60)

        print 'TODO: Turn off LEDs'
        abc.off()
