from enum import Enum
from dataclasses import dataclass

class TextJustification(Enum):
    LEFT = "left"
    RIGHT = "right"
    CENTRE = "centre"

@dataclass()
class TextPadding:
    padding_top: int
    padding_bottom: int
    padding_left: int
    padding_right: int