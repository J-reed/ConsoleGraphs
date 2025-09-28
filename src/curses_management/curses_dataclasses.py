from dataclasses import dataclass

@dataclass()
class PadVisibilityCoordsStruct:
    pad_top_left_x: int
    pad_top_left_y: int
    window_top_left_x: int
    window_top_left_y: int
    window_bottom_right_x: int
    window_bottom_right_y: int