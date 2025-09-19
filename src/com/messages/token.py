from com.messages.system import SystemMessage


class TokenMessage(SystemMessage):
    """Class for the token transmission"""

    def __init__(self, sender: int, dest: int):
        super().__init__(sender)
        self.dest = dest

    def get_dest(self) -> int:
        return self.dest
