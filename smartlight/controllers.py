from flask import Blueprint, render_template

from smartlight import queue, led, animation_thread

from time import sleep
import json

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('main.html')


@main.route('/color/name/<name>')
def set_color_name(name):
    queue.put("Stop")
    while animation_thread.is_running():
        sleep(0.1)

    try:
        led.set_color(name=name)
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})
    else:
        return json.dumps({'status': 'success', 'message': 'Set color to ' + name})


@main.route('/color/hex/<hex>')
def set_color_hex(hex):
    queue.put("Stop")
    while animation_thread.is_running():
        sleep(0.1)

    try:
        led.set_color(hex='#'+hex)
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})
    else:
        return json.dumps({'status': 'success', 'message': 'Set color to #' + hex})


@main.route('/color/rgb/<int:r>/<int:g>/<int:b>')
def set_color_rgb(r, g, b):
    queue.put("Stop")
    while animation_thread.is_running():
        sleep(0.1)

    try:
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
        led.turn_off()
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})
    else:
        message = 'Turned light off.'
        return json.dumps({'status': 'success', 'message': message})


@main.route('/thread/timer')
def create_thread_timer():
    queue.put("Timer")
    return str(list(queue.queue))


@main.route('/thread/stop')
def stop_thread():
    queue.put("Stop")
    return str(list(queue.queue))


@main.route('/thread/random')
def create_thread_random():
    queue.put("Random")
    return str(list(queue.queue))
