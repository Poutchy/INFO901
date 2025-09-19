from com.messages.communication import CommunicationMessage


class SyncMultipleMessage(CommunicationMessage):
    """Class for messages to one persone only"""

    def __init__(self, sender: int, clock: int, message: str, dests: list[int]):
        super().__init__(sender, clock, message)
        self.dests = dests

    def get_dests(self) -> list[int]:
        return self.dests
