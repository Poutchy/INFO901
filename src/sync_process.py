from threading import Thread
from time import sleep

from com.com import Com


class Process(Thread):

    def __init__(self, name):
        Thread.__init__(self)

        self.com = Com()

        self.nbProcess = self.com.get_nb_process()

        self.myId = self.com.get_my_id()
        self.name = name

        self.alive = True
        self.start()

    def run(self):
        loop = 0
        while self.alive:
            print(self.name + " Loop: " + str(loop))
            sleep(1)

            if self.name == "P0":
                self.com.synchronize()
                print("P0 SYNC")

            if self.name == "P1":
                self.com.synchronize()
                print("P1 SYNC")

            if self.name == "P2":
                self.com.synchronize()
                print("P2 SYNC")

            loop += 1
        print(self.name + " stopped")

    def stop(self):
        self.com.stop()
        self.alive = False

    def waitStopped(self):
        self.join()
