import curses
from curses import wrapper, window
from .curses_dataclasses import PadVisibilityCoordsStruct

def terminate_curses_session(stdscr: window):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def initialise_screen() -> window:
    stdscr: window = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    stdscr.refresh()

    return stdscr

def new_window(height: int, width: int, x: int, y: int) -> window:
    # (0,0) is top left corner
    return curses.newwin(height, width, y, x)

def new_pad(height: int,width: int) -> window:
    # Pads can be larger than the console size
    curses.newpad(height, width)

def update_pad(pad: window, pad_visibility_coords: PadVisibilityCoordsStruct):
    pad.refresh(
        pad_visibility_coords.pad_top_left_x, 
        pad_visibility_coords.pad_top_left_y, 
        pad_visibility_coords.window_top_left_x, 
        pad_visibility_coords.window_top_left_y, 
        pad_visibility_coords.window_bottom_right_x, 
        pad_visibility_coords.window_bottom_right_y
    )

def update_window(window: window):
    window.refresh()

def update(windows: list[window], pads: dict[window, PadVisibilityCoordsStruct]):
    for window in windows:
        update_window(window)

    for pad, visibility_coords in pads.items():
        update_pad(pad, visibility_coords)