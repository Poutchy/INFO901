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
                if loop == 0:
                    msg = ["Hell"]
                elif loop == 1:
                    msg = ["o wo"]
                elif loop == 2:
                    msg = ["rld"]
                else:
                    msg = ["!!"]
                self.com.broadcast_sync(msg, 0)

            if self.name == "P1":
                self.com.synchronize()
                print("P1 SYNC")
                msg = []
                self.com.broadcast_sync(msg, 0)
                print(f"P1 received {msg[0]=}")

            if self.name == "P2":
                self.com.synchronize()
                print("P2 SYNC")
                msg = []
                self.com.broadcast_sync(msg, 0)
                print(f"P2 received {msg[0]=}")

            loop += 1
        print(self.name + " stopped")

    def stop(self):
        self.com.stop()
        self.alive = False

    def waitStopped(self):
        self.join()
