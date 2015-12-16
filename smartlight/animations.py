from threading import Thread
from time import sleep

from random import randint

class Animations(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.daemon = True
        self.queue = queue

    def __timer(self):
        count = 1
        while True:
            sleep(1)
            print("Sleeping for %d seconds" % count)
            count += 1

            if not self.queue.empty():
                return True

    def __random(self):
        count = 1
        while True:
            sleep(1)
            print("Random number", randint(0, 100))
            count += 1

            if not self.queue.empty():
                break

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
