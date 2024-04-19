import curses


class Colors:
    _background = 235
    _foreground = 15
    _red = 203

    PRIMARY = 1
    PRIMARY_INVERTED = 2
    WRONG = 3

    @staticmethod
    def initialize():
        curses.init_pair(Colors.PRIMARY, Colors._foreground, Colors._background)
        curses.init_pair(Colors.PRIMARY_INVERTED, Colors._background, Colors._foreground)
        curses.init_pair(Colors.WRONG, Colors._red, Colors._background)
