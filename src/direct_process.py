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
                msg = ["Hello"]
                self.com.send_to_sync(msg, 1)

            if self.name == "P1":
                msg = []
                print("P1 will receive now")
                self.com.recev_from_sync(msg, 0)
                print(f"P1 received {msg[0]=}")
                # msg = []
                # self.com.recev_from_sync(msg, 2)
                # print(f"P1 received {msg[0]=}")

            # if self.name == "P2":
            # msg = ["world!"]
            # self.com.send_to_sync(msg, 1)

            loop += 1
        print(self.name + " stopped")

    def stop(self):
        self.com.stop()
        self.alive = False

    def waitStopped(self):
        self.join()
