from curses import wrapper, window, newpad
import curses
from curses_management.curses_manager import CursesManager
from curses_management.graphs.bar_chart import BarChart, BarChartAxis, BarChartConfiguration, BarChartOrientation
from curses_management.text.text_styling import TextJustification, TextPadding
from curses_management.curses_dataclasses import PadVisibilityCoords, Coord

def main(stdscr):

    stdscr.clear()
    stdscr.refresh()
    
    curses_box_test(stdscr)

    # whole_screen: window = curses_manager.initialise_screen()

    # main_pad = newpad(10,50)

    # main_pad.addnstr(0,0,"hello there", 5)
    # curses_manager.update([],{main_pad: PadVisibilityCoordsStruct(1,1,1,1,1,1)})

    # bar_chart = BarChart(
    #     title= ["BarChartTitle", "Subtitle"], 
    #     data=set(), 
    #     axis=BarChartAxis(0,100, "axis label", 100), 
    #     config=BarChartConfiguration("*",1,BarChartOrientation.HORIZONTAL_BARS, 1, 1, 9, 1)
    # )

    # title_pad = bar_chart.draw_title(main_pad, 1,1, bar_chart.title, TextJustification.CENTRE, TextPadding(1,1,3,3))
    # curses_manager.update([whole_screen], {
    #     main_pad: PadVisibilityCoordsStruct(1,1,1,1,1,1),
    #     title_pad: PadVisibilityCoordsStruct(1,1,1,1,1,1)
    # })
    # input()
    # curses_manager.terminate_curses_session(whole_screen)


def curses_box_test(stdscr: window):
    stdscr.clear()
    stdscr.refresh()

    curses_manager = CursesManager(stdscr=stdscr)

    curses_manager.new_window("test_window", 30,30, 1,1)
    for i in range(20):
        window = curses_manager.get_window("test_window")
        window.box()
        window.addstr(i+1, 0, "*"*20, curses.A_BOLD)

    curses_manager.new_pad("test_pad", 10,10, PadVisibilityCoords(Coord(0,0),Coord(1,1),Coord(3,4)))
    curses_manager.get_pad("test_pad").box()
    curses_manager.update()
    stdscr.getch()

    for i in range(2):
        for j in range(2):
            for k in range(2):
                if k < i:
                    continue
                for l in range(2):
                    if l < j:
                        continue
                    
                    stdscr.clear()
                    stdscr.refresh()

                    for n in range(20):
                        window = curses_manager.get_window("test_window")
                        window.box()
                        window.addstr(n+1, 0, "*"*20, curses.A_BOLD)


                    curses_manager.update_pad_position("test_pad", PadVisibilityCoords(Coord(0,0),Coord(i,j),Coord(k,l)))
                    curses_manager.get_pad("test_pad").box()
                    curses_manager.update()
                    
                    
                    stdscr.getch() 

if __name__ == "__main__":
    # This wrapper ensures that if the application crashes unexpectedly
    # the cli is still returned to normal when the program exits
    wrapper(main)