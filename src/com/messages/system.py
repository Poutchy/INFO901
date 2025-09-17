from com.messages.generic import Message


class SystemMessage(Message):
    """Generic class for system messages."""

    def __init__(self, sender: int):
        super().__init__(sender)
