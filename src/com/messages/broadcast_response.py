from com.messages.system import SystemMessage


class BroadcastSyncResponse(SystemMessage):
    """Class for the token transmission"""

    def __init__(self, sender: int, emiter: int):
        super().__init__(sender)
        self.emiter = emiter

    def get_emiter(self) -> int:
        return self.emiter
