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
                self.com.request_s_c()
                print("0 is in the critical")
                self.com.release_s_c()
                print("0 is out of the critical")

            if self.name == "P1":
                self.com.request_s_c()
                print("1 is in the critical")
                self.com.release_s_c()
                print("1 is out of the critical")

            if self.name == "P2":
                self.com.request_s_c()
                print("2 is in the critical")
                self.com.release_s_c()
                print("2 is out of the critical")

            loop += 1
        print(self.name + " stopped")

    def stop(self):
        self.com.stop()
        self.alive = False

    def waitStopped(self):
        self.join()
