from collections import deque
from typing import Optional

from com.messages.communication import CommunicationMessage


class MailBox:
    """MailBox class, that wil receive the messages"""

    def __init__(self):
        super().__init__()
        self.msgs: deque[CommunicationMessage] = deque()

    def is_empty(self) -> bool:
        return len(self.msgs) == 0

    def get_msg(self) -> CommunicationMessage:
        """Function that answer with the first message of the MailBox

        raise: IndexError
        return: The first message to arrive if there are some, None if not
        :rtype: CommunicationMessage
        """
        if self.is_empty():
            raise IndexError()
        return self.msgs.popleft()

    def add_msg(self, message: CommunicationMessage):
        return self.msgs.append(message)
