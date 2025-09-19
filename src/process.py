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

                self.com.send_to_sync(
                    "J'ai laissé un message à 2, je le rappellerai après, on se sychronise tous et on attaque la partie ?",
                    2,
                )
                msg = []
                self.com.recev_from_sync(msg, 2)
                print(f"Received {msg=} from 2")

                self.com.send_to_sync(
                    "2 est OK pour jouer, on se synchronise et c'est parti!", 1
                )

                self.com.synchronize()
                print("P0 synchronised")

                self.com.request_s_c()
                print("I WANT TO HAVE ACCES AND I TAKE IT BLABLABLA")
                if self.com.mailbox.is_empty():
                    print("prout")
                    print("Catched !")
                    self.com.broadcast("J'ai gagné !!!")
                else:
                    print("fa")
                    msg = self.com.mailbox.get_msg()
                    print("fa")
                    print(str(msg.get_sender()) + " à eu le jeton en premier")
                self.com.release_s_c()

            if self.name == "P1":
                if not self.com.mailbox.is_empty():
                    print("papo")
                    msg = self.com.mailbox.get_msg()
                    print(f"{self.name} received {msg}")
                    msg = []
                    self.com.recev_from_sync(msg, 0)
                    print(f"Received {msg=} from 0")

                    self.com.synchronize()
                    print("P1 synchronised")

                    self.com.request_s_c()
                    if self.com.mailbox.is_empty():
                        print("Catched !")
                        self.com.broadcast("J'ai gagné !!!")
                    else:
                        print("fi")
                        msg = self.com.mailbox.get_msg()
                        print("fi")
                        print(str(msg.get_sender()) + " à eu le jeton en premier")
                    self.com.release_s_c()

            if self.name == "P2":
                msg = []
                self.com.recev_from_sync(msg, 0)
                print(f"Received {msg=} from 0")
                self.com.send_to_sync("OK", 0)

                self.com.synchronize()
                print("P2 synchronised")

                self.com.request_s_c()
                if self.com.mailbox.is_empty():
                    print("Catched !")
                    self.com.broadcast("J'ai gagné !!!")
                else:
                    print("fofo")
                    msg = self.com.mailbox.get_msg()
                    print("fu")
                    print(str(msg.get_sender()) + " à eu le jeton en premier")
                    print("fu")
                self.com.release_s_c()

            loop += 1
        print(self.name + " stopped")

    def stop(self):
        self.com.stop()
        self.alive = False

    def waitStopped(self):
        self.join()
