from flask import Blueprint, render_template

from smartlight import animation_thread
from smartlight.utils import error_to_json

import json

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """
    Control for the index/main page

    :return: html response with main page
    """
    return render_template('main.html')


@main.route('/color/name/<name>')
@error_to_json
def set_color_name(name):
    """
    Sets the color of the connected light.

    :param name: CSS name of the color to set the light to
    :return: json string with success status and message
    """
    animation_thread.stop()
    animation_thread.set_color(name=name)
    return json.dumps({'status': 'success', 'message': 'Set color to ' + name})


@main.route('/color/hex/<hex>')
@error_to_json
def set_color_hex(hex):
    """
    Sets the color of the connected light.

    :param hex: hex value of the color to set the light to
    :return: json string with success status and message
    """
    animation_thread.stop()
    animation_thread.set_color(hex='#'+hex)
    return json.dumps({'status': 'success', 'message': 'Set color to #' + hex})


@main.route('/color/rgb/<int:r>/<int:g>/<int:b>')
@error_to_json
def set_color_rgb(r, g, b):
    """
    Sets the color of the connected light.

    :param r: intensity 0-255 of the red channel
    :param g: intensity 0-255 of the green channel
    :param b: intensity 0-255 of the blue channel
    :return: json string with success status and message
    """
    animation_thread.stop()
    animation_thread.set_color(red=r, green=g, blue=b)
    message = 'Set color to rgb %d, %d, %d' % (r, g, b)
    return json.dumps({'status': 'success', 'message': message})


@main.route('/color/')
@main.route('/color')
@error_to_json
def get_color_rgb():
    """
    Gets the color of the connected light

    :return: json string with success status, message and current color
    """
    color = animation_thread.get_color()
    message = 'Current color ' + str(color)
    return json.dumps({'status': 'success', 'message': message, 'color': color})


@main.route('/color/off/')
@main.route('/color/off')
@error_to_json
def turn_off():
    """
    Switches the light off
    :return: json string with success status and message
    """
    animation_thread.stop()
    animation_thread.turn_off()
    message = 'Turned light off'
    return json.dumps({'status': 'success', 'message': message})


@main.route('/animation/stop')
@error_to_json
def animation_stop():
    """
    Stops the current animation
    :return: json string with success status and message
    """
    animation_thread.stop()
    message = 'Animations stopped'
    return json.dumps({'status': 'success', 'message': message})


@main.route('/animation/random')
@error_to_json
def animation_random():
    """
    Starts random animation: morphing from one random color to the next
    :return: json string with success status and message
    """
    animation_thread.random()
    message = 'Random started'
    return json.dumps({'status': 'success', 'message': message})


@main.route('/animation/fire')
@error_to_json
def animation_fire():
    """
    Starts fire animation: morphing from a color from the fire palette to the next at random speeds
    :return: json string with success status and message
    """
    animation_thread.fire()
    message = 'Fire started'
    return json.dumps({'status': 'success', 'message': message})


@main.route('/animation/strobe')
@error_to_json
def animation_strobe():
    """
    Starts strobe light: at about 10Hz frequency
    :return: json string with success status and message
    """
    animation_thread.strobe()
    message = 'Strobe started'
    return json.dumps({'status': 'success', 'message': message})
