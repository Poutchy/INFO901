from com.messages.communication import CommunicationMessage


class PersonalMessage(CommunicationMessage):
    """Class for messages to one persone only"""

    def __init__(self, sender: int, message: str, dest: int):
        super().__init__(sender, message)
        self.dest = dest
