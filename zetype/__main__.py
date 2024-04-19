import curses

from zetype import App


def main():
    app: App = curses.wrapper(App)
    app.initialize()
    app.run()
    exit(0)


if __name__ == '__main__':
    main()
