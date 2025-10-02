from dataclasses import dataclass

@dataclass()
class Coord:
    x: int
    y: int

@dataclass()
class PadVisibilityCoords:
    starting_position_in_pad: Coord
    window_top_left: Coord
    window_bottom_right: Coord