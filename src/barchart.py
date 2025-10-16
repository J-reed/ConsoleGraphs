
from __future__ import annotations
import logging

logger = logging.getLogger('ConsoleGraphLogs')


from dataclasses import dataclass
from curses import window
import curses

from typing import Any

from .better_curses.pad import Pad
from .utils.utils import Coord

@dataclass
class BarChartStyling:
    bar_colour: str
    background_colour: str


@dataclass()
class BarChartData:
    bar_lengths: list[int]
    styling: BarChartStyling


# Todo: Update this method to use barchart data objects
def draw_bar_chart(bar_lengths: list[int], bar_width: int =1, bar_spacing: int=1, original_offset: Coord = Coord(1,1), bar_chart_position: Coord = Coord(0,0)):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)

    bar_chart: Pad = Pad(
        original_offset.x + (bar_spacing +bar_width) * len(bar_lengths), 
        max(bar_lengths)+original_offset.y+1,
        relative_display_top_left_corner_coord=bar_chart_position
    )
    bar_chart_curses_pad:window = bar_chart.get_curses_pad()
    bar_chart_curses_pad.box()
    bar_chart_curses_pad.bkgd(' ', curses.color_pair(0) | curses.A_BOLD)
    bar_chart._update()

    
    bars: list[Pad] = []
    for index, bar_length in enumerate(bar_lengths):
        logger.debug(f"{index}a")
        bar: Pad = Pad(
            bar_width,
            bar_length,
            relative_display_top_left_corner_coord=Coord(original_offset.x +(bar_spacing +bar_width) * index, bar_chart.display_height - bar_length - original_offset.y),
            parent_pad=bar_chart
        )
        
        logger.debug(f"{index}b")

        curses_bar_pad: window = bar.get_curses_pad()
        curses_bar_pad.box()
        curses_bar_pad.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
        bar._update()

        bars.append(bar)


def barchart_data_parser(barchart_data: dict) -> BarChartData:

    if barchart_data.get("bar_lengths") is None:
        raise Exception(f"[ERRORCODE a04574b0-2bd2-4e8f-93a1-b2e61ca7f284] Barchart data did not supply a 'bar_lengths' field. Data provided: {barchart_data}")
    
    if not isinstance(barchart_data.get("bar_lengths"), list):
        raise Exception(f"[ERRORCODE 2605c9f2-7af5-4f82-86f5-b8c51fbb8ba6] Barchart data field 'bar_lengths' must be a list of integers. Data provided: {barchart_data}") 

    
    for item in barchart_data.get("bar_lengths"):
        if not isinstance(item, int):
            raise Exception(f"[ERRORCODE 5a294cbf-4ece-45e3-b8c3-81dfb890e7e3] Barchart data field 'bar_lengths' must be a list of integers. Data provided: {barchart_data}") 


    if barchart_data.get("styling") is None:
        raise Exception(f"[ERRORCODE db456fba-b917-449c-9fa5-c04a84fc3602] Barchart data did not supply a 'styling' field. Data provided: {barchart_data}")
    
    if barchart_data.get("styling").get("bar_colour") is None:
        raise Exception(f"[ERRORCODE ea43f215-6a86-4829-b3fa-8f3fad712a13] Barchart data did not supply a 'bar_colour' field in its 'styling' object. Data provided: {barchart_data}")
    
    if barchart_data.get("styling").get("background_colour") is None:
        raise Exception(f"[ERRORCODE ecc0ec2b-ab87-4cbf-8121-0937e433fc21] Barchart data did not supply a 'background_colour' field in its 'styling' object. Data provided: {barchart_data}")
    
    supported_colours = {
        "black" : curses.COLOR_BLACK, 
        "blue": curses.COLOR_BLUE, 
        "cyan": curses.COLOR_CYAN,
        "green": curses.COLOR_GREEN,
        "magenta": curses.COLOR_MAGENTA,
        "red": curses.COLOR_RED,
        "white": curses.COLOR_WHITE,
        "yellow": curses.COLOR_YELLOW
    }

    if supported_colours.get(barchart_data.get("styling").get("bar_colour")) is None:
        raise Exception(f"[ERRORCODE d654cc66-8acd-4fb2-93f5-7075583cb9a3] The colour provided in the supplied barchart data for the 'bar_colour' field in its 'styling' object is invalid. Bar colour provided: {barchart_data.get("styling").get("bar_colour")}. Supported colours: {supported_colours.keys()}")
   
    if supported_colours.get(barchart_data.get("styling").get("background_colour")) is None:
        raise Exception(f"[ERRORCODE 170d9db6-3cac-438f-816e-c4ea02c05677] The colour provided in the supplied barchart data for the 'background_colour' field in its 'styling' object is invalid. Background colour provided: {barchart_data.get("styling").get("background_colour")}. Supported colours: {supported_colours.keys()}")
    
    return BarChartData(
        bar_lengths = barchart_data["bar_lengths"],
        styling = BarChartStyling(
            bar_colour=barchart_data["styling"]["bar_colour"],
            background_colour=barchart_data["styling"]["background_colour"],
        )
    )

class InvalidBarChartDataException(Exception): ...
class BarChartBackground:
    def __init__():
        pass

class BarChartBar:
    def __init__():
        pass
class BarChart:

    def __init__(self, barchart_data: BarChartData):

        if not isinstance(barchart_data, BarChart):
            raise InvalidBarChartDataException("[ERRORCODE: d68b50bc-d987-4fd7-b130-a4f2c54997a1] BarCharts must be initialised with BarChartData")

        self.barchart_data: BarChartData = barchart_data

        self.bars: list[BarChartBar] = []
        self.background: BarChartBackground = BarChartBackground()

    @staticmethod
    def create_barchart(barchart_data: dict) -> BarChart:

        if barchart_data.get("bar_lengths") is None:
            raise Exception(f"[ERRORCODE a04574b0-2bd2-4e8f-93a1-b2e61ca7f284] Barchart data did not supply a 'bar_lengths' field. Data provided: {barchart_data}")
        
        if not isinstance(barchart_data.get("bar_lengths"), list):
            raise Exception(f"[ERRORCODE 2605c9f2-7af5-4f82-86f5-b8c51fbb8ba6] Barchart data field 'bar_lengths' must be a list of integers. Data provided: {barchart_data}") 

        
        for item in barchart_data.get("bar_lengths"):
            if not isinstance(item, int):
                raise Exception(f"[ERRORCODE 5a294cbf-4ece-45e3-b8c3-81dfb890e7e3] Barchart data field 'bar_lengths' must be a list of integers. Data provided: {barchart_data}") 


        if barchart_data.get("styling") is None:
            raise Exception(f"[ERRORCODE db456fba-b917-449c-9fa5-c04a84fc3602] Barchart data did not supply a 'styling' field. Data provided: {barchart_data}")
        
        if barchart_data.get("styling").get("bar_colour") is None:
            raise Exception(f"[ERRORCODE ea43f215-6a86-4829-b3fa-8f3fad712a13] Barchart data did not supply a 'bar_colour' field in its 'styling' object. Data provided: {barchart_data}")
        
        if barchart_data.get("styling").get("background_colour") is None:
            raise Exception(f"[ERRORCODE ecc0ec2b-ab87-4cbf-8121-0937e433fc21] Barchart data did not supply a 'background_colour' field in its 'styling' object. Data provided: {barchart_data}")
        
        supported_colours = {
            "black" : curses.COLOR_BLACK, 
            "blue": curses.COLOR_BLUE, 
            "cyan": curses.COLOR_CYAN,
            "green": curses.COLOR_GREEN,
            "magenta": curses.COLOR_MAGENTA,
            "red": curses.COLOR_RED,
            "white": curses.COLOR_WHITE,
            "yellow": curses.COLOR_YELLOW
        }

        if supported_colours.get(barchart_data.get("styling").get("bar_colour")) is None:
            raise Exception(f"[ERRORCODE d654cc66-8acd-4fb2-93f5-7075583cb9a3] The colour provided in the supplied barchart data for the 'bar_colour' field in its 'styling' object is invalid. Bar colour provided: {barchart_data.get("styling").get("bar_colour")}. Supported colours: {supported_colours.keys()}")
    
        if supported_colours.get(barchart_data.get("styling").get("background_colour")) is None:
            raise Exception(f"[ERRORCODE 170d9db6-3cac-438f-816e-c4ea02c05677] The colour provided in the supplied barchart data for the 'background_colour' field in its 'styling' object is invalid. Background colour provided: {barchart_data.get("styling").get("background_colour")}. Supported colours: {supported_colours.keys()}")
        
        BarChart(barchart_data=BarChartData(
            bar_lengths = barchart_data["bar_lengths"],
            styling = BarChartStyling(
                bar_colour=barchart_data["styling"]["bar_colour"],
                background_colour=barchart_data["styling"]["background_colour"],
            )
        ))


class BarChartBuilder:

    def __init__(self):
        self.bars: dict[str,BarChartBar] = dict()

    def add_bar(self, bar_id: str):
        self.bars[bar_id]=BarChartBar()

    def set_bar_styling(self, bar_id: str, attribute: str, value: Any):
        bar: BarChartBar = self.bars.get(bar_id)

    def set_background(self):
        self.background: BarChartBackground = BarChartBackground()


    def build(self) -> BarChart:

        barchart_data: BarChartData = BarChartData()
        return BarChart(barchart_data)