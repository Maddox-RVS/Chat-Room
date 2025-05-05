from dataclasses import dataclass
from typing import Optional
import curses
import time
import os

COLOR_BLUE: int = 10
COLOR_RED: int = 20
COLOR_GREEN: int = 30
COLOR_DIM: int = 40
COLOR_ERROR: int = 50

LINESEP: str = '\n'

class Console():
    @dataclass
    class Log:
        text: str
        startX: int
        startY: int

    def __init__(self):
        self.backlog: list[Console.Log] = []

        self.console: Optional[curses.window] = curses.initscr()
        curses.start_color()
        curses.init_pair(COLOR_BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(COLOR_ERROR, curses.COLOR_WHITE, curses.COLOR_RED)
        if curses.can_change_color(): 
            curses.init_color(COLOR_DIM, 170, 170, 170) 
            curses.init_pair(COLOR_DIM, COLOR_DIM, curses.COLOR_BLACK)
        else: 
            self.console.addstr('WARINING', curses.color_pair(COLOR_ERROR))
            self.console.addstr(' Custom color isn\'t supported by your terminal. Reverting to default colors...')
            self.console.refresh()
            curses.init_pair(COLOR_DIM, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def __log__(self, text: str, x: int, y: int):
        self.backlog.append(Console.Log(text, x, y))
        self.backlog.sort(key=lambda log: log.startY)

    def close(self):
        curses.endwin()

    def print(self, string: str):
        y, x = self.console.getyx()
        self.__log__(string, x, y)
        self.console.addstr(string, curses.color_pair(0))
        self.console.refresh()
    def println(self, string: str):
        self.print(string + LINESEP)

    def printBlue(self, string: str):
        y, x = self.console.getyx()
        self.__log__(string, x, y)
        self.console.addstr(string, curses.color_pair(COLOR_BLUE))
        self.console.refresh()
    def printlnBlue(self, string: str):
        self.printBlue(string + LINESEP)

    def printRed(self, string: str):
        y, x = self.console.getyx()
        self.__log__(string, x, y)
        self.console.addstr(string, curses.color_pair(COLOR_RED))
        self.console.refresh()
    def printlnRed(self, string: str):
        self.printRed(string + LINESEP)

    def printGreen(self, string: str):
        y, x = self.console.getyx()
        self.__log__(string, x, y)
        self.console.addstr(string, curses.color_pair(COLOR_GREEN))
        self.console.refresh()
    def printlnGreen(self, string: str):
        self.printGreen(string + LINESEP)

    def printDim(self, string: str):
        y, x = self.console.getyx()
        self.__log__(string, x, y)
        self.console.addstr(string, curses.color_pair(COLOR_DIM))
        self.console.refresh()
    def printlnDim(self, string: str):
        self.printDim(string + LINESEP)

    def printError(self, string: str):
        y, x = self.console.getyx()
        self.__log__(string, x, y)
        self.console.addstr(string, curses.color_pair(COLOR_ERROR))
        self.console.refresh()
    def printlnError(self, string: str):
        self.printError(string + LINESEP)

    def clear(self):
        self.backlog.clear()
        self.console.clear()
        self.console.refresh()

    def clearLine(self):
        self.backlog.pop()
        self.console.clrtoeol()
        self.console.refresh()

    def move(self, x, y):
        self.console.move(y, x)
        self.console.refresh()

    def getCursorPos(self) -> tuple[int, int]:
        y, x = self.console.getyx()
        return (x, y)
    
    # def getBackText(self, amount):
    #     text: str = ''
    #     y, x = self.console.getyx()
    #     for i in range(amount):

if __name__ == '__main__':
    console: Console = Console()
    console.printlnBlue('Blue Text')
    console.printlnRed('Red Text')
    console.printlnGreen('Green Text')
    console.printlnDim('Dim Text')
    console.printlnError('Error Text')
    console.println('This is normal text')
    console.println('This test will be erased and replaced with "hello!" in 2 seconds...')
    time.sleep(2)
    x, y = console.getCursorPos()
    console.move(x, y - 1)
    console.clearLine()
    console.print('hello!')
    text: str = console.getBackText(5) 
    console.println(text)
    input('')
    console.close()