from dataclasses import dataclass
from enum import Enum
import math
from curses import window

from ..text.text_styling import TextJustification, TextPadding

class BarChartOrientation(Enum):
    HORIZONTAL_BARS = "horizontal"
    VERTICAL_BARS = "vertical"

@dataclass()
class BarChartAxis:
    min_value: float
    max_value: float
    label: list[str]
    label_row_length_max: int

@dataclass(eq=True, frozen=True)
class BarChartBar:
    title: list[str]
    title_row_length_max: int
    value: float
    colour: str

@dataclass()
class BarChartConfiguration:
    unit_symbol: str
    unit_value: float
    orientation: BarChartOrientation
    bar_spacing: int
    title_row_padding: int
    title_row_length_max: int
    value_label_padding: int

class BarChart:
    
    def __init__(self, title: list[str], data: set[BarChartBar], axis: BarChartAxis, config: BarChartConfiguration):
        self.title: list[str] = title
        self.bars: set[BarChartBar] = data
        self.axis: BarChartAxis = axis
        self.config: BarChartConfiguration = config

    def determine_height(self) -> int:
        match self.config.orientation:
            case BarChartOrientation.HORIZONTAL_BARS:
                return len(self.title) + self.config.title_row_padding + \
                    (self.config.bar_spacing * len(self.bars)) + \
                    self.config.value_label_padding + len(self.axis.label)
            case BarChartOrientation.VERTICAL_BARS:
                return len(self.title) + self.config.title_row_padding + \
                    (math.ceil(self.axis.max_value - self.axis.min_value)) + \
                    max([len(bar.title) for bar in self.bars]) + \
                    self.config.value_label_padding + self.axis.label_row_length_max

        raise Exception(f"[ERRORCODE: 3758caaa-f3de-4853-a205-0fe1f48d9269] Could not determine height of bar chart. {self.__repr__()}")
    
    def determine_width(self) -> int:
        match self.config.orientation:
            case BarChartOrientation.HORIZONTAL_BARS:
                return max([bar.title_row_length_max for bar in self.bars]) + \
                    (math.ceil(self.axis.max_value - self.axis.min_value))

            case BarChartOrientation.VERTICAL_BARS:
                return self.axis.label_row_length_max + \
                    (self.config.bar_spacing * len(self.bars)) + \
                    max([bar.title_row_length_max for bar in self.bars])

        raise Exception(f"[ERRORCODE: b65e5c9c-481d-4127-8717-9439f042755c] Could not determine width of bar chart. {self.__repr__()}")
    
    def draw_to_window(self, window: window):

        title_pad = self.draw_title(window, 0, 0, self.title, justification=TextJustification.CENTRE, padding=TextPadding(1,1,1,1))
        

        y += self.config.title_row_padding

        # Draw Graph
        graph_height = self.determine_height()
        graph_width = self.determine_width()

        match self.config.orientation:
            case BarChartOrientation.HORIZONTAL_BARS:
                for gy in range(graph_height):
                    for gx in range(graph_width):
                        pass

            case BarChartOrientation.VERTICAL_BARS:
                for gy in range(graph_height):
                    for gx in range(graph_width):
                        pass

        raise Exception(f"[ERRORCODE: fa7259ed-d6a4-4683-b2d0-6b2d604461ed] Could not draw bar chart. {self.__repr__()}")
    
    def draw_title(self, parent_pad: window, x: int, y: int, title: list[str], justification: TextJustification, padding: TextPadding) -> window:
        
        longest_line: int = max([len(line) for line in title])
        
        title_pad: window = parent_pad.subpad(
            padding.padding_top + len(title) + padding.padding_bottom,
            padding.padding_left + longest_line  + padding.padding_right,
            x,
            y
        )

        justification_func = {
            TextJustification.LEFT : lambda string: string.ljust(longest_line, " "),
            TextJustification.RIGHT : lambda string: string.rjust(longest_line, " "),
            TextJustification.CENTRE : lambda string: string.center(longest_line, " "),
        }

        justified_title: list[str] = list(map(lambda line: justification_func[justification](line), title))

        for line_no in range(len(justified_title)):
            title_line = justified_title[line_no]
            title_pad.addnstr(padding.padding_top + line_no, 0, title_line, self.config.title_row_length_max)

        return title_pad


    def draw_one_bar(self, parent_pad: window, x: int, y: int, bar: BarChartBar) -> window:
        height,width = 0
        bar_pad: window = parent_pad.subpad(nlines=height, ncols=width, begin_x=x, begin_y=y)
        
        # TODO: Add bar content to pad

        return bar_pad

    def __repr__(self) -> str:
        return f"self.title: {self.title} | self.bars: {self.bars} | self.axis: {self.axis} | self.config: {self.config}"