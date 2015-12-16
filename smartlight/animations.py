from threading import Thread
from time import sleep

from random import randint


class Animations(Thread):
    def __init__(self, queue, led):
        Thread.__init__(self)
        self.daemon = True
        self.queue = queue
        self.led = led
        self.running = False

    def __timer(self):
        count = 1
        while self.queue.empty():
            sleep(1)
            print("Sleeping for %d seconds" % count)
            count += 1

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

    def run(self):
        while True:
            task = None if self.queue.empty() else self.queue.get()

            if task is None:
                sleep(0.1)
            elif task == 'Timer':
                self.__timer()
            elif task == 'Random':
                self.__random()
            elif task == 'Stop':
                print("Animations Stopped...")
