from threading import Thread
from time import sleep

import os

from blinkstick import blinkstick
from queue import Queue
from random import randint


class Animations(Thread):
    def __init__(self, app=None):
        Thread.__init__(self)
        self.daemon = True
        self.queue = Queue()
        self.running = False

        # Find blinckstick and set mode
        self.led = blinkstick.find_first()
        if self.led is not None:
            self.led.set_mode(3)
        else:
            raise "BlinkStick not found!"

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialise the blinkstick wrapper for app.
        :param app: Flask application
        :type app: Flask
        """

        # register extension with app
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['flask-blinkstick'] = self

        # Check this to make sure the Werkzeug reloader doesn't spawn an extra thread !
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not app.config['DEBUG']:
            print("Starting animations thread...")
            self.start()

    def __random(self):
        self.running = True
        while self.queue.empty():
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)

            self.led.morph(red=r, green=g, blue=b, duration=1000, steps=50)
            sleep(0.01)  # a short pause is required, diving in the next loop causes a crash
        self.running = False

    def is_running(self):
        return self.running

    def set_color(self, *args, **kwargs):
        self.led.set_color(*args, **kwargs)

    def get_color(self):
        return self.led.get_color()

    def turn_off(self):
        return self.led.turn_off()

    def random(self):
        self.queue.put("Random")

    def stop(self):
        self.queue.put("Stop")
        while self.is_running():
            sleep(0.1)

    def get_queue(self):
        return self.queue

    def get_led(self):
        return self.led

    def run(self):
        while True:
            task = None if self.queue.empty() else self.queue.get()

            if task is None:
                self.running = False
                sleep(0.1)
            elif task == 'Random':
                self.__random()
            elif task == 'Stop':
                self.running = False
                print("Animations Stopped...")
