from dataclasses import dataclass
from enum import Enum
import math
from curses import window

class BarChartOrientation(Enum):
    HORIZONTAL_BARS = "horizontal"
    VERTICAL_BARS = "vertical"

@dataclass()
class BarChartAxis:
    min_value: float
    max_value: float
    label: list[str]

@dataclass(eq=True, frozen=True)
class BarChartBar:
    title: list[str]
    value: float
    colour: str

@dataclass()
class BarChartConfiguration:
    unit_symbol: str
    unit_value: float
    orientation: BarChartOrientation
    bar_spacing: int
    title_row_padding: int
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
                    self.config.value_label_padding + len(self.axis.label)

        raise Exception(f"[ERRORCODE: 3758caaa-f3de-4853-a205-0fe1f48d9269] Could not determine height of bar chart. {self.__repr__()}")
    
    def determine_width(self) -> int:
        pass

    def draw_to_window(self, window: window):
        pass

    def __repr__(self) -> str:
        return f"self.title: {self.title} | self.bars: {self.bars} | self.axis: {self.axis} | self.config: {self.config}"