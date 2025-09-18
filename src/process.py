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
                self.com.send_to("j'appelle 2 et je te recontacte après", 1)

                # self.com.sendToSync(
                #   "J'ai laissé un message à 2, je le rappellerai après, on se sychronise tous et on attaque la partie ?",
                #   2,
                # )
                # self.com.recevFromSync(msg, 2)

                # self.com.sendToSync(
                #   "2 est OK pour jouer, on se synchronise et c'est parti!", 1
                # )

                # self.com.synchronize()

                # self.com.request_s_c()
                # if self.com.mailbox.is_empty():
                #     print("Catched !")
                #     self.com.broadcast("J'ai gagné !!!")
                # else:
                #     msg = self.com.mailbox.get_msg()
                #     print(str(msg.get_sender()) + " à eu le jeton en premier")
                # self.com.release_s_c()

            if self.name == "P1":
                if not self.com.mailbox.is_empty():
                    msg = self.com.mailbox.get_msg()
                    print(f"{self.name} received {msg}")
                    # self.com.recevFromSync(msg, 0)

                    # self.com.synchronize()

                #     self.com.request_s_c()
                #     if self.com.mailbox.is_empty():
                #         print("Catched !")
                #         self.com.broadcast("J'ai gagné !!!")
                #     else:
                #         msg = self.com.mailbox.get_msg()
                #         print(str(msg.get_sender()) + " à eu le jeton en premier")
                #     self.com.release_s_c()

            # if self.name == "P2":
            # msg = [""]
            # self.com.recevFromSync(msg, 0)
            # self.com.sendToSync("OK", 0)

            # self.com.synchronize()

            # self.com.request_s_c()
            # if self.com.mailbox.is_empty():
            #     print("Catched !")
            #     self.com.broadcast("J'ai gagné !!!")
            # else:
            #     msg = self.com.mailbox.get_msg()
            #     print(str(msg.get_sender()) + " à eu le jeton en premier")
            # self.com.release_s_c()

            loop += 1
        print(self.name + " stopped")

    def stop(self):
        self.alive = False

    def waitStopped(self):
        self.join()
