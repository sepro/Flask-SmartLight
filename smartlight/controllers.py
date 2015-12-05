from flask import Blueprint
from smartlight import led

import json

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return 'Hello World!'


@main.route('/color/set/<name>')
def set_color(name):
    try:
        led.set_color(name=name)
    except Exception as e:
        return json.dumps({'status': 'error', 'message': e})
    else:
        return json.dumps({'status': 'succes', 'message': 'Set color to ' + name})


