from com.messages.communication import CommunicationMessage


class MultipleMessage(CommunicationMessage):
    """Class for messages to one persone only"""

    def __init__(self, sender: int, message: str, dests: list[int]):
        super().__init__(sender, message)
        self.dests = dests
