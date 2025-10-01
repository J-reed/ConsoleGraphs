from curses import wrapper, window, newpad
import curses_management.curses_manager as curses_manager
from curses_management.graphs.bar_chart import BarChart, BarChartAxis, BarChartConfiguration, BarChartOrientation
from curses_management.text.text_styling import TextJustification, TextPadding
from curses_management.curses_dataclasses import PadVisibilityCoordsStruct

def main():
    whole_screen: window = curses_manager.initialise_screen()

    main_pad = newpad(10,50)

    bar_chart = BarChart(
        title= ["BarChartTitle", "Subtitle"], 
        data=set(), 
        axis=BarChartAxis(0,100, "axis label", 100), 
        config=BarChartConfiguration("*",1,BarChartOrientation.HORIZONTAL_BARS, 1, 1, 9, 1)
    )

    title_pad = bar_chart.draw_title(main_pad, 1,1, bar_chart.title, TextJustification.CENTRE, TextPadding(1,1,3,3))
    curses_manager.update([whole_screen], {
        main_pad: PadVisibilityCoordsStruct(1,1,1,1,1,1),
        title_pad: PadVisibilityCoordsStruct(1,1,1,1,1,1)
    })
    input()
    curses_manager.terminate_curses_session(whole_screen)

if __name__ == "__main__":
    # This wrapper ensures that if the application crashes unexpectedly
    # the cli is still returned to normal when the program exits
    wrapper(main())