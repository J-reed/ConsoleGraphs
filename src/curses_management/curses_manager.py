import curses
from curses import wrapper, window
from .curses_dataclasses import PadVisibilityCoords
from dataclasses import dataclass

@dataclass
class PadManager:
    pad: window
    pad_visibility_coords: PadVisibilityCoords

class CursesManager:

    def __init__(self, stdscr: window):
        self.windows: dict[str,window] = dict()
        self.pads: dict[str, PadManager]  = dict()

    def new_window(self, name: str, height: int, width: int, y: int, x: int):
        self.windows[name] = curses.newwin(height, width, y, x)

    def new_pad(self, name: str, height: int, width: int, pad_visibility_coords: PadVisibilityCoords):
        self.pads[name] = PadManager(pad=curses.newpad(height, width), pad_visibility_coords=pad_visibility_coords)

    def update(self):

        for window in self.windows.values():
            window.refresh()
        
        for pad_manager in self.pads.values():

            visibility_coords: PadVisibilityCoords = pad_manager.pad_visibility_coords

            self.validate_pad_visibility_coord(visibility_coords)

            pad_manager.pad.refresh(
                visibility_coords.starting_position_in_pad.y, 
                visibility_coords.starting_position_in_pad.x, 
                visibility_coords.window_top_left.y,
                visibility_coords.window_top_left.x,
                visibility_coords.window_bottom_right.y,
                visibility_coords.window_bottom_right.x
            )
    
    def update_pad_position(self, pad_name: str, pad_visibility_coords: PadVisibilityCoords):
        self.pads[pad_name] = PadManager(self.pads[pad_name].pad, pad_visibility_coords)

    def __repr__(self):
        return f"Windows: {self.windows.keys()} | Pads: {self.pads.keys()}"
    
    def get_pad_visibility_coords(self, pad_name: str) -> PadVisibilityCoords:
        return self.pads[pad_name].pad_visibility_coords
    
    def get_pad(self, pad_name) -> window:
        return self.pads[pad_name].pad
    
    def validate_pad_visibility_coord(self, pad_visibility_coord: PadVisibilityCoords):
        if pad_visibility_coord.window_top_left.x > pad_visibility_coord.window_bottom_right.x:
            raise Exception(f"[ERRORCODE: b1f37533-c35f-46c1-bbdf-4b308112488c] Pad's top left coordinate when embedded in a window cannot be to the right of its bottom right co-ordinate in the window: {pad_visibility_coord}")
        
        if pad_visibility_coord.window_top_left.y > pad_visibility_coord.window_bottom_right.y:
            raise Exception(f"[ERRORCODE: 46076f33-3259-4ceb-b3b6-5fffe5360459] Pad's top left coordinate when embedded in a window cannot be below its bottom right co-ordinate in the window: {pad_visibility_coord}")
        
    def get_window(self, window_name) -> window:
        return self.windows[window_name]