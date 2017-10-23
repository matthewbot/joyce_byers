#!/usr/bin/env python

from joyce_byers.flask_api import app
from joyce_byers.messages import MessageProcessor
import atexit

if __name__ == '__main__':
    message_proc = MessageProcessor(max_size=3,
                                    flicker_timeout=120)

    try:
        app.message_callback = message_proc.add_message
        app.run(host='0.0.0.0')
    finally:
        message_proc.stop()
