class Message:
    """Generic class of messages"""

    def __init__(self, sender: int):
        super().__init__()
        self.sender = sender

    def getSender(self) -> int:
        return self.sender
