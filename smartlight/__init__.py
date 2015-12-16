from flask import Flask
from blinkstick import blinkstick


app = Flask(__name__)

app.config.from_object('config')

led = blinkstick.find_first()

if led is not None:
    led.set_mode(3)
else:
    # raise "BlinkStick not found!"
    pass

from smartlight.controllers import main
app.register_blueprint(main)
