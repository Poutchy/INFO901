"""
Communication module
"""

from threading import Lock

from pyeventbus3.pyeventbus3 import PyBus

from com.mailbox.mailbox import MailBox


class Com:
    """Communicator class"""

    nbProcessCreated = 0
    mutexNbProcesses = Lock()
    mutexProcesses = Lock()

    def __init__(self):
        super().__init__()

        PyBus.Instance().register(self, self)
        self.my_id: int = self.set_id()
        self.mailbox: MailBox = MailBox()
        self.keep_token: bool = False
        self.have_token = False

    def getMyId(self) -> int:
        """Getter for the Communicator id

        :returns: The id of the current communicator
        :rtype: int
        """
        return self.my_id

    def getNbProcess(self) -> int:
        """Getter for the number of Actual communicatore

        :returns: The id of the current communicator
        :rtype: int
        """
        with Com.mutexNbProcesses:
            res = Com.nbProcessCreated
        return res

    def set_id(self) -> int:
        with Com.mutexNbProcesses:
            res = Com.nbProcessCreated
            Com.nbProcessCreated += 1
        return res

    def requestSC(self):
        self.keep_token = True

    def releaseSC(self):
        self.keep_token = False

    def broadcast(self, message: str) -> bool:
        """Send an asynchronous message to every other Communicator

        :param message: The string to send to the communicator
        :type message: str
        return: True if the message was well sent, False otherwise
        :rtype: bool
        """
        raise NotImplementedError()

    def sendTo(self, message: str, dest: int) -> bool:
        """Send an asynchronous message to another Communicator

        :param message: The string to send to the communicator
        :type message: str
        :param dest: The id of the communicator
        :type dest: int
        return: True if the message was well sent, False otherwise
        :rtype: bool
        """
        raise NotImplementedError()

    def sendToSync(self, message: str, dest: int) -> bool:
        """Send a synchronous message to another Communicator

        :param message: The string to send to the communicator
        :type message: str
        :param dest: The id of the communicator
        :type dest: int
        return: True if the message was well sent, False otherwise
        :rtype: bool
        """
        raise NotImplementedError()

    def synchronize(self):
        raise NotImplementedError()

    def recevFromSync(self, message: list[str], sender: int) -> str:
        raise NotImplementedError()
