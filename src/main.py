from curses import wrapper, window
import curses_management.curses_manager as curses_manager


def main():
    whole_screen: window = curses_manager.initialise_screen()


    curses_manager.terminate_curses_session(whole_screen)

if __name__ == "__main__":
    # This wrapper ensures that if the application crashes unexpectedly
    # the cli is still returned to normal when the program exits
    wrapper(main())