from flask import Blueprint
from smartlight import led

import json

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return 'Hello World!'


@main.route('/color/name/<name>')
def set_color_name(name):
    try:
        led.set_color(name=name)
    except Exception as e:
        return json.dumps({'status': 'error', 'message': e})
    else:
        return json.dumps({'status': 'succes', 'message': 'Set color to ' + name})


@main.route('/color/rgb/<int:r>/<int:g>/<int:b>')
def set_color_rgb(r, g, b):
    try:
        led.set_color(red=r, green=g, blue=b)
    except Exception as e:
        return json.dumps({'status': 'error', 'message': e})
    else:
        message = 'Set color to rgb %d, %d, %d' % (r, g, b)
        return json.dumps({'status': 'succes', 'message': message})


@main.route('/color/')
@main.route('/color')
def get_color_rgb():
    try:
        color = led.get_color()
    except Exception as e:
        return json.dumps({'status': 'error', 'message': e})
    else:
        message = 'Current color ' + str(color)
        return json.dumps({'status': 'succes', 'message': message, 'color': color})
