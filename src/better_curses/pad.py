from __future__ import annotations
import logging
import pathlib

logging.basicConfig(filename=f"{pathlib.Path(__file__).parent.resolve()}/console_graph.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger('ConsoleGraphLogs')

import curses
from curses import window
from ..utils.utils import Coord


class PadVisibleFrame:

    def __init__(self, frame_top_left_position_in_pad: Coord, pad:Pad):
        self.pad: Pad = pad
        self.frame_top_left = frame_top_left_position_in_pad
        self.frame_top_left, self.frame_bottom_right = self.get_displayed_portion_of_pad_in_frame()
        self.frame_bottom_right = Coord(self.frame_top_left.x + self.get_frame_width(),self.frame_top_left.y + self.get_frame_height())

    def get_frame_width(self) -> int:
        return self.pad.display_width

    def get_frame_height(self) -> int:
        return self.pad.display_height

    def get_displayed_portion_of_pad_in_frame(self) -> tuple[Coord, Coord]:

        frame_bottom_right: Coord = Coord(
            self.frame_top_left.x + self.get_frame_width(),
            self.frame_top_left.y + self.get_frame_height()
        )
        return (self.frame_top_left, frame_bottom_right)

    def set_frame_position_in_pad(self,new_frame_top_left: Coord) -> None:
        
        new_frame_top_left, new_frame_bottom_right = self.get_displayed_portion_of_pad_in_frame(new_frame_top_left)

        std_err_debug_info: str = f"Frame Coords: [TopLeft: {new_frame_top_left}, BottomRight: {new_frame_bottom_right} | PadWidth: {self.pad.pad_width}, PadHeight: {self.pad.pad_height}]"

        if new_frame_top_left.x < 0 or new_frame_top_left.x >= new_frame_bottom_right.x:
            raise Exception(f"Top left x co-ordinate of the frame view must be within its pad and must be to the left of the bottom right x co-ordinate of the frame view. {std_err_debug_info}")

        if new_frame_top_left.y < 0 or new_frame_top_left.y >= new_frame_bottom_right.y:
            raise Exception(f"Top left y co-ordinate of the frame view must be within its pad and must be above of the bottom right y co-ordinate of the frame view. {std_err_debug_info}")
 
        if new_frame_bottom_right.x > self.pad.pad_width:
            raise Exception(f"Bottom right x co-ordinate of the frame view must be inside the pad. {std_err_debug_info}")
        
        if new_frame_bottom_right.y > self.pad.pad_height:
            raise Exception(f"Bottom right y co-ordinate of the frame view must be inside the pad. {std_err_debug_info}")

        self.frame_top_left = new_frame_top_left
        self.frame_bottom_right = new_frame_bottom_right

        pad_absolute_top_left, pad_absolute_bottom_right = self.pad.get_absolute_position_of_display_area_of_pad_on_screen()

        curses_pad: window = self.pad.get_curses_pad()
        curses_pad.refresh(new_frame_top_left.y, new_frame_top_left.x, pad_absolute_top_left.y, pad_absolute_top_left.x, pad_absolute_bottom_right.y, pad_absolute_bottom_right.x)


class Pad:
    def __init__(self, display_width: int, display_height:int, pad_width: int | None = None, pad_height:int | None = None, pad_top_left_corner_position:Coord = Coord(0,0), relative_display_top_left_corner_coord: Coord = Coord(0,0), parent_pad: Pad=None):

        if not pad_width:
            pad_width = display_width

        if not pad_height:
            pad_height = display_height

        if not parent_pad:
            self._pad = curses.newpad(pad_height, pad_width)
        else:
            self._pad = parent_pad.get_curses_pad().subpad(pad_height, pad_width, relative_display_top_left_corner_coord.y,relative_display_top_left_corner_coord.x)

        self.top_left_corner_coord: Coord = relative_display_top_left_corner_coord

        self.parent: window = parent_pad

        self.pad_width = pad_width
        self.pad_height = pad_height

        self.display_width = display_width
        self.display_height = display_height

        self.frame = PadVisibleFrame(pad_top_left_corner_position, self)

        self._update()

    def get_pad_size(self) -> tuple[int,int]:
        return (self.width, self.height)
    
    def get_display_size(self) -> tuple[int,int]:
        return self.top

    def get_curses_pad(self) -> window:
        return self._pad
    
    def get_relative_top_left_coord(self) -> Coord:
        return self.top_left_corner_coord
    
    def set_relative_top_left_coord(self, top_left_corner_coord: Coord) -> None:
        self.top_left_corner_coord = top_left_corner_coord
        
    def set_display_width(self, new_display_width: int):
        self.display_width = new_display_width
        self._update()

    def set_display_height(self, new_display_height: int):
        self.display_height = new_display_height
        self._update()

    def get_parent(self) -> Pad:
        if self.parent:
            return self.parent
        
        return None
    
    def get_absolute_position_of_display_area_of_pad_on_screen(self) -> tuple[Coord,Coord]:
        pad_top_left_coord: Coord = self.get_relative_top_left_coord()
        
        parent_absolute_top_left, _ = self.get_absolute_position_display_area_of_parent_on_screen()
        
        pad_absolute_top_left_coord: Coord = Coord(parent_absolute_top_left.x + pad_top_left_coord.x, parent_absolute_top_left.y + pad_top_left_coord.y)
        pad_absolute_bottom_right_coord: Coord = Coord(pad_absolute_top_left_coord.x + self.display_width, pad_absolute_top_left_coord.y+self.display_height)

        return (pad_absolute_top_left_coord, pad_absolute_bottom_right_coord)
    
    def get_absolute_position_display_area_of_parent_on_screen(self) -> tuple[Coord,Coord]:

        logger.debug('I')

        if not self.parent:
            return (Coord(0,0), Coord(self.display_width, self.display_height))
        
        pad_absolute_top_left_x: int = 0
        pad_absolute_top_left_y: int = 0

        recursive_parent: Pad = self
        while recursive_parent:=recursive_parent.get_parent():
            recursive_parent_top_left: Coord = recursive_parent.get_relative_top_left_coord()
            pad_absolute_top_left_x += recursive_parent_top_left.x
            pad_absolute_top_left_y += recursive_parent_top_left.y
            logger.debug(f'II: {recursive_parent}')
        
        
        logger.debug('III')
        absolute_top_left_coord: Coord = Coord(pad_absolute_top_left_x,pad_absolute_top_left_y)
        absolute_bottom_right_coord: Coord = Coord(pad_absolute_top_left_x + self.display_width, pad_absolute_top_left_y+self.display_height)

        return (absolute_top_left_coord, absolute_bottom_right_coord)

    def _update(self):
        
        display_pos_top_left, display_pos_bottom_right = self.get_absolute_position_of_display_area_of_pad_on_screen()
        
        frame_top_left_coord, _ = self.frame.get_displayed_portion_of_pad_in_frame()
        

        logger.debug(f"New refresh points: {frame_top_left_coord.y},{frame_top_left_coord.x}, {display_pos_top_left.y}, {display_pos_top_left.x}, {display_pos_bottom_right.y}, {display_pos_bottom_right.x}")
        self._pad.refresh(frame_top_left_coord.y,frame_top_left_coord.x, display_pos_top_left.y, display_pos_top_left.x, display_pos_bottom_right.y, display_pos_bottom_right.x)
        