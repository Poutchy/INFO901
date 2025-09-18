from com.messages.communication import CommunicationMessage


class SyncPersonalMessage(CommunicationMessage):
    """Class for messages to one persone only"""

    def __init__(self, sender: int, clock: int, message: str, dest: int):
        super().__init__(sender, clock, message)
        self.dest = dest

    def get_dest(self) -> int:
        return self.dest
