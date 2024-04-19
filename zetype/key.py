import curses


class Key:
    """Constants for special keyboard keys"""
    BLANK = -1
    ABORT = 3
    ESCAPE = 27
    RETURN = 10
    ENTER = 13
    SPACE = 32
    BACKSPACE = 8
    DELETE = 127
    DIR_DOWN = 258
    DIR_UP = 259
    DIR_LEFT = 260
    DIR_RIGHT = 261
    RESIZE = curses.KEY_RESIZE
