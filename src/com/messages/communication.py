from com.messages.generic import Message


class CommunicationMessage(Message):
    """Class for messages that contain a message."""

    def __init__(self, sender: int, message: str):
        super().__init__(sender)
        self.message = message
