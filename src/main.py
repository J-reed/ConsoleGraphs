import logging
import pathlib

logging.basicConfig(filename=f"{pathlib.Path(__file__).parent.resolve()}/console_graph.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

from curses import wrapper, window
from .utils.utils import Coord
from .barchart import draw_bar_chart, barchart_data_parser, BarChartData

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


    barchart1_data = {
        "bar_lengths" : [5,2,3,1,10,15,12], 
        "styling": {
            "bar_colour" : "blue",
            "background_colour" : "black"
        }
    }

    

    barchart2_data = {
        "bar_lengths" : [5,14,12,15,13,1,4], 
        "styling": {
            "bar_colour" : "red",
            "background_colour" : "cyan"
        }
    }

    bc1_d: BarChartData = barchart_data_parser(barchart1_data)
    bc2_d: BarChartData = barchart_data_parser(barchart2_data)


    draw_bar_chart(bar_lengths = bc1_d.bar_lengths, bar_chart_position=Coord(0,1))
    stdscr.getch()
    draw_bar_chart(bar_lengths = bc2_d.bar_lengths, bar_chart_position=Coord(17,1))
    stdscr.getch()

    

if __name__ == "__main__":
    # This wrapper ensures that if the application crashes unexpectedly
    # the cli is still returned to normal when the program exits
    wrapper(main)