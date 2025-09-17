from collections import deque

from com.messages.communication import CommunicationMessage


class MailBox:
    """MailBox class, that wil receive the messages"""

    def __init__(self):
        super().__init__()
        self.msgs: deque[CommunicationMessage] = deque()

    def isEmpty(self) -> bool:
        return len(self.msgs) > 0

    def getMsg(self) -> CommunicationMessage:
        return self.msgs.popleft()

    def addMsg(self, message: CommunicationMessage):
        return self.msgs.append(message)
