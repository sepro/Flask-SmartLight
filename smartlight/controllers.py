from flask import Blueprint,render_template
from blinkstick import blinkstick

from time import sleep
import threading

import json

t = None
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('main.html')


@main.route('/color/name/<name>')
def set_color_name(name):
    try:
        led = blinkstick.find_first()
        led.set_color(name=name)
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})
    else:
        return json.dumps({'status': 'success', 'message': 'Set color to ' + name})


@main.route('/color/hex/<hex>')
def set_color_hex(hex):
    try:
        led = blinkstick.find_first()
        led.set_color(hex='#'+hex)
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})
    else:
        return json.dumps({'status': 'success', 'message': 'Set color to #' + hex})


@main.route('/color/rgb/<int:r>/<int:g>/<int:b>')
def set_color_rgb(r, g, b):
    try:
        led = blinkstick.find_first()
        led.set_color(red=r, green=g, blue=b)
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})
    else:
        message = 'Set color to rgb %d, %d, %d' % (r, g, b)
        return json.dumps({'status': 'success', 'message': message})


@main.route('/color/')
@main.route('/color')
def get_color_rgb():
    try:
        led = blinkstick.find_first()
        color = led.get_color()
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})
    else:
        message = 'Current color ' + str(color)
        return json.dumps({'status': 'success', 'message': message, 'color': color})


@main.route('/color/off/')
@main.route('/color/off')
def turn_off():
    try:
        led = blinkstick.find_first()
        led.turn_off()
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})
    else:
        message = 'Turned light off.'
        return json.dumps({'status': 'success', 'message': message})


@main.route('/color/pulse/<name>')
def pulse_color(name):
    try:
        led = blinkstick.find_first()
        led.morph(name=name)
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})
    else:
        message = 'Pulsing to ' + name
        return json.dumps({'status': 'success', 'message': message})


def thread():
    for i in range(20):
        sleep(1)
        print("Sleeping for %d seconds" % i)


@main.route('/thread/')
@main.route('/thread')
def create_thread():
    global t
    if t is not None:
        t.isAlive = False
    t = threading.Thread(target=thread)
    t.daemon = True
    t.start()
    return "Thread Started..."
