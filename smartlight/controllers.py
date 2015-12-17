from flask import Blueprint, render_template

from smartlight import animation_thread

import json

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('main.html')


@main.route('/color/name/<name>')
def set_color_name(name):
    animation_thread.stop()

    try:
        animation_thread.set_color(name=name)
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})
    else:
        return json.dumps({'status': 'success', 'message': 'Set color to ' + name})


@main.route('/color/hex/<hex>')
def set_color_hex(hex):
    animation_thread.stop()

    try:
        animation_thread.set_color(hex='#'+hex)
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})
    else:
        return json.dumps({'status': 'success', 'message': 'Set color to #' + hex})


@main.route('/color/rgb/<int:r>/<int:g>/<int:b>')
def set_color_rgb(r, g, b):
    animation_thread.stop()

    try:
        animation_thread.set_color(red=r, green=g, blue=b)
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})
    else:
        message = 'Set color to rgb %d, %d, %d' % (r, g, b)
        return json.dumps({'status': 'success', 'message': message})


@main.route('/color/')
@main.route('/color')
def get_color_rgb():
    try:
        color = animation_thread.get_color()
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})
    else:
        message = 'Current color ' + str(color)
        return json.dumps({'status': 'success', 'message': message, 'color': color})


@main.route('/color/off/')
@main.route('/color/off')
def turn_off():
    animation_thread.stop()

    try:
        animation_thread.turn_off()
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})
    else:
        message = 'Turned light off'
        return json.dumps({'status': 'success', 'message': message})


@main.route('/animation/stop')
def animation_stop():
    animation_thread.stop()
    message = 'Animations stopped'
    return json.dumps({'status': 'success', 'message': message})


@main.route('/animation/random')
def animation_random():
    animation_thread.random()
    message = 'Random animation started'
    return json.dumps({'status': 'success', 'message': message})
