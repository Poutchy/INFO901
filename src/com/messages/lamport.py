from com.messages.generic import Message


class LamportMessage(Message):
    """Generic class of messages"""

    def __init__(self, sender: int, clock):
        super().__init__(sender)
        self.clock = clock

    def get_clock(self) -> int:
        return self.clock
