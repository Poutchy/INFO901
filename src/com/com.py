"""
Communication module
"""

from threading import Condition, Lock, Thread
from typing import Optional
from uuid import uuid4

from pyeventbus3.pyeventbus3 import Mode, PyBus, subscribe, time

from com.mailbox.mailbox import MailBox
from com.messages.broadcast_response import BroadcastSyncResponse
from com.messages.multiple import MultipleMessage
from com.messages.numerotation import Numerotation
from com.messages.personal import PersonalMessage
from com.messages.personal_response import PersonalSyncResponse
from com.messages.sync_multiple import SyncMultipleMessage
from com.messages.sync_personal import SyncPersonalMessage
from com.messages.sync_response import SyncResponse
from com.messages.token import TokenMessage


class Com:
    """Communicator class"""

    def __init__(self):
        super().__init__()
        self.alive = True

        # ID parameters
        self.temp_id: str = str(uuid4())
        self.registry: dict[str, int] = {}
        self.registry_lock: Lock = Lock()
        self.my_id: Optional[int] = None

        PyBus.Instance().register(self, self)
        self.mailbox: MailBox = MailBox()
        self.clock = 0

        # token parameters
        self.token_started: bool = False
        self.want_token: Lock = Lock()
        self.release_token: Lock = Lock()

        # Synchronisation parameters
        self.awaiters: set[int] = set()
        self.await_synchronisation: Condition = Condition()

        # Broadcast Sync parameters
        self.broadcast_lock: Lock = Lock()
        self.await_broadcast: Lock = Lock()
        self.broadcast_message: Optional[str] = None
        self.broadcast_awaiters: list[int] = []

        # Direct Sync parameters
        self.received_from: list[tuple[int, str]] = []
        self.await_direct: Condition = Condition()

        self.announce()
        # if self.my_id == 2:
        #     self.send_token()

    def announce(self):
        """Function to announce our existence in the network"""
        PyBus.Instance().post(Numerotation(self.temp_id))

    def update_ids(self):
        """Automatic numerotation of the communicators
        note pour le professeur:
        à cause de la réussite d'implémentation tardive, seulement les fonctions de broadcast et de synchronisation fonctionne avec ce modèle. Pour avoir accès aux fonctions qui fonctionnent MAIS qui n'ont pas la numérotation automatique, regardez le commit précédent
        """
        with self.registry_lock:
            sorted_ids = sorted(self.registry.keys())
            for idx, tid in enumerate(sorted_ids):
                self.registry[tid] = idx
            self.my_id = self.registry[self.temp_id]
            if self.my_id == 0 and not self.token_started:
                self.token_started = True
                Thread(target=self._start_token_after_init, daemon=True).start()

    def _start_token_after_init(self):
        time.sleep(0.5)
        self.send_token()

    def get_my_id(self) -> int:
        """Getter for the Communicator id

        :returns: The id of the current communicator
        :rtype: int
        """
        return self.my_id

    def get_nb_process(self) -> int:
        """Getter for the number of Actual communicators

        :returns: The id of the current communicator
        :rtype: int
        """
        return len(self.registry)

    def stop(self):
        """Function that stop the rounds of the token
        ALWAYS FINISH ALL PROCESS BY THAT FUNCTION BEFORE DYING
        """
        self.alive = False

    def request_s_c(self):
        """Function to start a critical section"""
        self.release_token.acquire()
        print("I want the token")
        self.want_token.acquire()

    def release_s_c(self):
        """Function that end a critical section"""
        self.release_token.release()
        print("I don't want the token anymore")

    def broadcast(self, message: str):
        """Send an asynchronous message to every other Communicator

        :param message: The string to send to the communicator
        :type message: str
        return: True if the message was well sent, False otherwise
        :rtype: bool
        """
        dests = list(range(self.get_nb_process()))
        dests.remove(self.my_id)
        self.clock += 1
        m = MultipleMessage(self.my_id, self.clock, message, dests)
        PyBus.Instance().post(m)

    def broadcast_sync(self, message: list[str], sender: int):
        """Send a synchronous message to every other Communicator

        :param message: The string to send to the communicator
        :type message: str
        return: True if the message was well sent, False otherwise
        :rtype: bool
        """
        self.broadcast_lock.acquire()
        if self.my_id == sender:
            self.broadcast_awaiters.append(self.my_id)
            dests = list(range(self.get_nb_process()))
            dests.remove(self.my_id)
            self.clock += 1
            m = SyncMultipleMessage(self.my_id, self.clock, message[0], dests)
            PyBus.Instance().post(m)
        if self.my_id != sender:
            if self.broadcast_message is not None:
                message.append(self.broadcast_message)
                self.broadcast_lock.release()
                self.broadcast_message = None
                return
            with self.broadcast_lock:
                message.append(self.broadcast_message)
                self.broadcast_message = None

    def send_to(self, message: str, dest: int):
        """Send an asynchronous message to another Communicator

        :param message: The string to send to the communicator
        :type message: str
        :param dest: The id of the communicator
        :type dest: int
        return: True if the message was well sent, False otherwise
        :rtype: bool
        """
        self.clock += 1
        m = PersonalMessage(self.my_id, self.clock, message, dest)
        PyBus.Instance().post(m)

    def send_to_sync(self, message: str, dest: int):
        """Send an asynchronous message to another Communicator

        :param message: The string to send to the communicator
        :type message: str
        :param dest: The id of the communicator
        :type dest: int
        """
        # print(f"send message from {self.my_id} to {dest}")
        self.await_direct.acquire()
        self.clock += 1
        m = SyncPersonalMessage(self.my_id, self.clock, message, dest)
        PyBus.Instance().post(m)
        # print("finish sending the message")

    def recev_from_sync(self, message: list[str], fromm: int):
        """Receive a synchronous message from another Communicator

        :param message: A list that contains the message in it's last position
        :type message: list[str]
        :param dest: The id of the communicator
        :type dest: int
        """
        self.await_direct.acquire()
        if fromm in [indices for (indices, _) in self.received_from]:
            element = next(
                (item for item in self.received_from if item[0] == fromm), None
            )
            self.received_from = [
                item for item in self.received_from if item[0] != fromm
            ]
            _, m = element
            message.append(m)
            self.await_direct.release()
            m = PersonalSyncResponse(self.my_id, fromm)
            PyBus.Instance().post(m)
            return
        while True:
            with self.await_direct:
                if fromm in [indices for (indices, _) in self.received_from]:
                    element = next(
                        (item for item in self.received_from if item[0] == fromm), None
                    )
                    self.received_from = [
                        item for item in self.received_from if item[0] != fromm
                    ]
                    _, m = element
                    message.append(m)
                    m = PersonalSyncResponse(self.my_id, fromm)
                    PyBus.Instance().post(m)
                    return
            self.await_direct.acquire()

    def synchronize(self):
        """Method to synchronize all the Processes of the program
        ALL PROCESSES HAVE TO RUN THE COMMAND ONE TIME OR ANOTHER
        """
        with self.await_synchronisation:
            m = SyncResponse(self.my_id)
            PyBus.Instance().post(m)
            while True:
                with self.registry_lock:
                    expected_users = set(self.registry.values())
                print(expected_users)

                if expected_users.issubset(self.awaiters):
                    break
                self.await_synchronisation.wait()
            self.awaiters.clear()

        # self.await_synchronisation.acquire()
        # self.clock += 1
        # all_users = set(list(range(self.get_nb_process())))
        # print(all_users)
        # self.awaiters.append(self.my_id)
        # if set(self.awaiters) == all_users:
        #     self.awaiters = []
        #     self.await_synchronisation.release()
        # m = SyncResponse(self.my_id)
        # PyBus.Instance().post(m)

    def send_token(self):
        """Utilisty function that make the token make rounds in all processes
        NEVER USE THAT FUNCTION
        """
        nb = self.get_nb_process()
        dest = (self.my_id + 1) % nb
        m = TokenMessage(self.my_id, dest)
        PyBus.Instance().post(m)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MultipleMessage)
    def on_broadcast(self, event: MultipleMessage):
        """Subscriber to the MultipleMessage, sent by broadcast"""
        if self.my_id in event.get_dests():
            self.clock = 1 + max(self.clock, event.get_clock())
            self.mailbox.add_msg(event)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=PersonalMessage)
    def on_receive(self, event):
        """Subscriber to the PersonalMessage, sent by send_to"""
        if self.my_id == event.dest:
            self.clock = 1 + max(self.clock, event.get_clock())
            self.mailbox.add_msg(event)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=TokenMessage)
    def on_token_receive(self, event):
        """Subscriber to the TokenMessage reception, sent by send_token"""
        self.token_started = True
        if self.my_id == event.get_dest():
            if self.want_token.locked():
                self.want_token.release()
                print("I have the token and I want to keep it")
                with self.release_token:
                    if self.alive:
                        print("I don't want the token anymore, here it is")
                        self.send_token()
                    else:
                        print("J'ai le token mais je suis mort...")
            else:
                self.send_token()

    @subscribe(threadMode=Mode.PARALLEL, onEvent=SyncResponse)
    def on_sync_response(self, event: SyncResponse):
        """Subscriber to the SyncResponse, sent by synchronise"""
        with self.await_synchronisation:
            self.awaiters.add(event.get_sender())
            self.await_synchronisation.notify_all()
        # if self.my_id == event.get_sender():
        #     return
        # all_users = list(range(self.get_nb_process()))
        # self.awaiters.append(event.get_sender())
        # if set(self.awaiters) == set(all_users):
        #     self.await_synchronisation.release()
        #     self.awaiters = []

    @subscribe(threadMode=Mode.PARALLEL, onEvent=SyncMultipleMessage)
    def on_broadcast_sync(self, event: SyncMultipleMessage):
        """Subscriber to the SyncMultipleMessage, sent by broadcast_sync"""
        if self.my_id in event.get_dests():
            self.clock = 1 + max(self.clock, event.get_clock())
            self.broadcast_message = event.get_message()
            if self.broadcast_lock.locked():
                self.broadcast_lock.release()
            m = BroadcastSyncResponse(self.my_id, event.get_sender())
            PyBus.Instance().post(m)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=SyncPersonalMessage)
    def on_receive_sync(self, event: SyncPersonalMessage):
        """Subscriber to the SyncPersonalMessage, sent by send_to_sync"""
        if self.my_id == event.get_dest():
            self.clock = 1 + max(self.clock, event.get_clock())
            temp = (event.get_sender(), event.get_message())
            self.received_from.append(temp)
            if self.await_direct.locked():
                self.await_direct.release()

    @subscribe(threadMode=Mode.PARALLEL, onEvent=BroadcastSyncResponse)
    def on_broadcast_response(self, event: BroadcastSyncResponse):
        """Subscriber to the BroadcastSyncResponse, sent by the SyncMultipleMessage subscriber"""
        if self.my_id == event.get_emiter():
            all_users = list(range(self.get_nb_process()))
            self.broadcast_awaiters.append(event.get_sender())
            if set(self.broadcast_awaiters) == set(all_users):
                self.broadcast_lock.release()
                self.broadcast_awaiters = []

    @subscribe(threadMode=Mode.PARALLEL, onEvent=PersonalSyncResponse)
    def on_personal_response(self, event: PersonalSyncResponse):
        """Subscriber to the PersonalSyncResponse, sent by the SyncPersonalMessage subscriber"""
        if self.my_id == event.get_emiter():
            self.await_direct.release()

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Numerotation)
    def on_numerotation(self, event: Numerotation):
        """Subscriber for the Numerotation, sent by set_id"""
        with self.registry_lock:
            if event.sender not in self.registry:
                self.registry[event.sender] = -1
            if self.temp_id not in self.registry:
                self.registry[self.temp_id] = -1
        self.update_ids()
