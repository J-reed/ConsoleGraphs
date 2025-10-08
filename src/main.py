import logging
import pathlib

logging.basicConfig(filename=f"{pathlib.Path(__file__).parent.resolve()}/console_graph.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

from curses import wrapper, window, newpad
import curses

from .better_curses.pad import Pad
from .utils.utils import Coord

logger = logging.getLogger('ConsoleGraphLogs')
logger.info("-"*120)
logger.info("Running ConsoleGraphLogs")

def main(stdscr: window):

    stdscr.clear()
    stdscr.refresh()
    
    stdscr.resize(70,70)

    logger.debug(f" Screen size (y,x): {stdscr.getmaxyx()}")

    stdscr.addstr(0,0, f"{stdscr.getmaxyx()}")
    stdscr.refresh()
    stdscr.getch()

    stdscr.clear()
    stdscr.refresh()

    draw_bar_chart_better_curses_example(stdscr=stdscr, bar_lengths = [5,2,3,1,10,15,12], bar_chart_position=Coord(0,1))
    stdscr.getch()
    draw_bar_chart_better_curses_example(stdscr=stdscr, bar_lengths = [5,14,12,15,13,1,4], bar_chart_position=Coord(17,1))
    stdscr.getch()


def draw_bar_chart_better_curses_example(stdscr, bar_lengths: list[int], bar_width: int =1, bar_spacing: int=1, original_offset: Coord = Coord(1,1), bar_chart_position: Coord = Coord(0,0)):
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
    

if __name__ == "__main__":
    # This wrapper ensures that if the application crashes unexpectedly
    # the cli is still returned to normal when the program exits
    wrapper(main)