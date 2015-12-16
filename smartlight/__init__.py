from flask import Flask
from blinkstick import blinkstick

from config import DEBUG
from queue import Queue
from smartlight.animations import Animations

import os


# Find blinckstick and set mode
led = blinkstick.find_first()

if led is not None:
    led.set_mode(3)
else:
    # raise "BlinkStick not found!"
    pass

# Create queue and threads for background workers
queue = Queue()
animation_thread = Animations(queue)

# Check this to make sure the Werkzeug reloader doesn't spawn an extra thread !
if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not DEBUG:
    print("Starting animations thread...")
    animation_thread.start()

# Set up Flask App
app = Flask(__name__)

app.config.from_object('config')

from smartlight.controllers import main
app.register_blueprint(main)

