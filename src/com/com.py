"""
Communication module
"""

from collections import deque
from threading import Lock

from pyeventbus3.pyeventbus3 import Mode, PyBus, subscribe

from com.mailbox.mailbox import MailBox
from com.messages.generic import Message
from com.messages.multiple import MultipleMessage
from com.messages.personal import PersonalMessage
from com.messages.sync_personal import SyncPersonalMessage


class Com:
    """Communicator class"""

    nbProcessCreated = 0
    mutexNbProcesses = Lock()
    mutexProcesses = Lock()

    def __init__(self):
        super().__init__()

        self.my_id = None
        self.set_id()
        PyBus.Instance().register(self, self)
        self.mailbox: MailBox = MailBox()
        self.clock = 0
        self.keep_token: bool = False
        self.have_token = False

        self.global_lock: Lock = Lock()

        self.sync_messages: deque[Message] = deque()
        self.access_sync_messages: Lock = Lock()

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
        with Com.mutexNbProcesses:
            res = Com.nbProcessCreated
        return res

    def set_id(self):
        if self.my_id is None:
            with Com.mutexNbProcesses:
                res = Com.nbProcessCreated
                Com.nbProcessCreated += 1
            self.my_id = res

    def request_s_c(self):
        self.keep_token = True

    def release_s_c(self):
        self.keep_token = False

    def broadcast(self, message: str):
        """Send an asynchronous message to every other Communicator

        :param message: The string to send to the communicator
        :type message: str
        return: True if the message was well sent, False otherwise
        :rtype: bool
        """
        dests = list(range(self.get_nb_process()))
        self.clock += 1
        m = MultipleMessage(self.my_id, self.clock, message, dests)
        print(f"{self.my_id} broadcast {m} with clock {self.clock}")
        PyBus.Instance().post(m)

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
        print(f"Personal {self.my_id} send: {m} to {dest}")
        PyBus.Instance().post(m)

    def send_to_sync(self, message: str, dest: int):
        """Send a synchronous message to another Communicator

        :param message: The string to send to the communicator
        :type message: str
        :param dest: The id of the communicator
        :type dest: int
        return: True if the message was well sent, False otherwise
        :rtype: bool
        """
        self.clock += 1
        m = PersonalMessage(self.my_id, self.clock, message, dest)
        print(f"Personal {self.my_id} send: {m} to {dest}")
        PyBus.Instance().post(m)
        with self.access_sync_messages:
            self.sync_messages.append(m)

    def synchronize(self):
        raise NotImplementedError()

    def recev_from_sync(self, message: list[str], sender: int) -> str:
        raise NotImplementedError()

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MultipleMessage)
    def on_broadcast(self, event: MultipleMessage):
        if self.get_my_id() != event.get_sender():
            self.clock = 1 + max(self.clock, event.get_clock())
            self.mailbox.add_msg(event)
            print(
                f"{self.my_id} received broadcast {event.get_message()} from {event.get_sender()} with clock {self.clock}"
            )

    @subscribe(threadMode=Mode.PARALLEL, onEvent=PersonalMessage)
    def on_receive(self, event):
        if self.my_id == event.dest:
            self.clock = 1 + max(self.clock, event.get_clock())
            self.mailbox.add_msg(event)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=SyncPersonalMessage)
    def on_sync_receive(self, event):
        if self.my_id == event.dest:
            self.clock = 1 + max(self.clock, event.get_clock())
            print(
                f"{self.my_id} received personal {event.get_message()} from {event.get_sender()} with clock {self.clock}"
            )
