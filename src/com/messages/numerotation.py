from dataclasses import dataclass


@dataclass
class Numerotation:
    """Generic class for system messages."""

    def __init__(self, sender: str):
        self.sender = sender
