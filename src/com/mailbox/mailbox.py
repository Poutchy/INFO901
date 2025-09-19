from collections import deque
from threading import Lock
from typing import Optional

from com.messages.communication import CommunicationMessage


class MailBox:
    """MailBox class, that wil receive the messages"""

    def __init__(self):
        super().__init__()
        self.protection_lock: Lock = Lock()
        self.msgs: deque[CommunicationMessage] = deque()

    def is_empty(self) -> bool:
        with self.protection_lock:
            print(f"will say {len(self.msgs) == 0}")
            return len(self.msgs) == 0

    def get_msg(self) -> CommunicationMessage:
        """Function that answer with the first message of the MailBox

        raise: IndexError
        return: The first message to arrive if there are some, None if not
        :rtype: CommunicationMessage
        """
        if self.is_empty():
            raise IndexError()
        with self.protection_lock:
            res = self.msgs.popleft()
            return res

    def add_msg(self, message: CommunicationMessage):
        with self.protection_lock:
            return self.msgs.append(message)
