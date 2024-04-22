"""zetype entry-point"""

import curses
import sys
from os import system, name

from zetype.app import App


def main():
    """First executed function on run."""
    app: App = curses.wrapper(App)
    app.initialize()
    app.run()
    system("cls" if name == 'nt' else "clear")
    sys.exit(0)


if __name__ == '__main__':
    main()
