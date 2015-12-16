from flask import Flask
from blinkstick import blinkstick

from queue import Queue
from smartlight.animations import Animations

import os

app = Flask(__name__)

app.config.from_object('config')

led = blinkstick.find_first()

queue = Queue()
queue.put("Timer")

animation_thread = Animations(queue)

# Check this to make sure the Werkzeug reloader doesn't spawn an extra thread !
if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    print("Starting animations thread...")
    animation_thread.start()

if led is not None:
    led.set_mode(3)
else:
    # raise "BlinkStick not found!"
    pass

from smartlight.controllers import main
app.register_blueprint(main)

