from threading import Thread
from time import sleep

import os

from blinkstick import blinkstick
from queue import Queue
from random import randint

RND_CMD = 'random'
FIRE_CMD = 'fire'
STOP_CMD = 'stop'
STROBE_CMD = 'strobe'

FIRE_COLORS = ['#120903', '#1B0D05', '#251206', '#321407', '#4C1005', '#660B04',
               '#800602', '#9A0200', '#AB0601', '#B31403', '#BA2205', '#C12F08', '#C93D0A', '#D35E14',
               '#DE8522', '#E9AD2F', '#F4D43C', '#FFFC4A']


class Animations(Thread):
    def __init__(self, app=None):
        """
        Sets up everything required, connects with the blinkstick and registers with the app

        :param app: flask-app to register with
        """
        Thread.__init__(self)
        self.daemon = True
        self.queue = Queue()
        self.running = False

        # Find blinckstick and set mode
        self.led = blinkstick.find_first()
        if self.led is not None:
            self.led.set_mode(3)
        else:
            raise Exception('Blinkstick not found')

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
        """
        Morph from one random color into another
        """
        self.running = True
        while self.queue.empty():
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)

            self.led.morph(red=r, green=g, blue=b, duration=1000, steps=50)
            sleep(0.01)  # a short pause is required, diving in the next loop causes a crash
        self.running = False

    def __fire(self):
        """
        Morph over fire-ish colors at random speeds
        """
        self.running = True

        while self.queue.empty():
            new_color = FIRE_COLORS[randint(0, len(FIRE_COLORS)-1)]

            speed = 600 + randint(0, 700)

            self.led.morph(hex=new_color, duration=speed, steps=int(speed/10))
            sleep(0.01)  # a short pause is required, diving in the next loop causes a crash

        self.running = False

    def __strobe(self):
        """
        Strobe light (about 10Hz)
        """
        self.running = True

        while self.queue.empty():
            self.set_color(name="white")
            sleep(0.05)
            self.set_color(name="black")
            sleep(0.05)

        self.running = False

    def is_running(self):
        """
        Checks if an animation is currently running

        :return: boolean True if an animation is currently running
        """
        return self.running

    def set_color(self, *args, **kwargs):
        """
        Wraps blinksticks set_color
        """
        self.led.set_color(*args, **kwargs)

    def get_color(self):
        """
        Wraps blinksticks get_color
        """
        return self.led.get_color()

    def turn_off(self):
        """
        Turns the light off
        """
        self.led.turn_off()

    def random(self):
        """
        Puts command to start the random animation on the queue
        """
        self.queue.put(RND_CMD)

    def fire(self):
        """
        Puts command to start the fire animation on the queue
        """
        self.queue.put(FIRE_CMD)

    def strobe(self):
        """
        Puts command to start the strobe light on the queue
        """
        self.queue.put(STROBE_CMD)

    def stop(self, wait=True):
        """
        Puts command to stop animations on the queue

        :param wait: if True the function will wait until the current animation is finished
        """
        self.queue.put(STOP_CMD)
        while self.is_running() and wait:
            sleep(0.1)

    def get_queue(self):
        """
        Returns the queue
        :return: the current queue
        """
        return self.queue

    def get_led(self):
        """
        Returns the led
        :return: the current led
        """
        return self.led

    def run(self):
        """
        Function that runs when the thread is started, checks the queue and acts accordingly
        """
        while True:
            task = None if self.queue.empty() else self.queue.get()

            if task is None:
                self.running = False
                sleep(0.1)
            elif task == RND_CMD:
                self.__random()
            elif task == FIRE_CMD:
                self.__fire()
            elif task == STROBE_CMD:
                self.__strobe()
            elif task == STOP_CMD:
                self.running = False
