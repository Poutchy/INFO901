from com.messages.lamport import LamportMessage


class CommunicationMessage(LamportMessage):
    """Class for messages that contain a message."""

    def __init__(self, sender: int, clock: int, message: str):
        super().__init__(sender, clock)
        self.message = message

    def get_message(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{self.get_sender()} sent {self.get_message()}"
