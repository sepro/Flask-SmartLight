from flask import Blueprint, render_template

from smartlight import animation_thread
from smartlight.utils import error_to_json

import json

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('main.html')


@main.route('/color/name/<name>')
@error_to_json
def set_color_name(name):
    animation_thread.stop()
    animation_thread.set_color(name=name)
    return json.dumps({'status': 'success', 'message': 'Set color to ' + name})


@main.route('/color/hex/<hex>')
@error_to_json
def set_color_hex(hex):
    animation_thread.stop()
    animation_thread.set_color(hex='#'+hex)
    return json.dumps({'status': 'success', 'message': 'Set color to #' + hex})


@main.route('/color/rgb/<int:r>/<int:g>/<int:b>')
@error_to_json
def set_color_rgb(r, g, b):
    animation_thread.stop()
    animation_thread.set_color(red=r, green=g, blue=b)
    message = 'Set color to rgb %d, %d, %d' % (r, g, b)
    return json.dumps({'status': 'success', 'message': message})


@main.route('/color/')
@main.route('/color')
@error_to_json
def get_color_rgb():
    color = animation_thread.get_color()
    message = 'Current color ' + str(color)
    return json.dumps({'status': 'success', 'message': message, 'color': color})


@main.route('/color/off/')
@main.route('/color/off')
@error_to_json
def turn_off():
    animation_thread.stop()
    animation_thread.turn_off()
    message = 'Turned light off'
    return json.dumps({'status': 'success', 'message': message})


@main.route('/animation/stop')
@error_to_json
def animation_stop():
    animation_thread.stop()
    message = 'Animations stopped'
    return json.dumps({'status': 'success', 'message': message})


@main.route('/animation/random')
@error_to_json
def animation_random():
    animation_thread.random()
    message = 'Random animation started'
    return json.dumps({'status': 'success', 'message': message})


@main.route('/animation/fire')
@error_to_json
def animation_fire():
    animation_thread.fire()
    message = 'Fire animation started'
    return json.dumps({'status': 'success', 'message': message})


@main.route('/animation/strobe')
@error_to_json
def animation_strobe():
    animation_thread.strobe()
    message = 'Strobe started'
    return json.dumps({'status': 'success', 'message': message})
