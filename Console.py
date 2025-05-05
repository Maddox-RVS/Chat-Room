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
    def __init__(self):
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

    def close(self):
        curses.endwin()

    def print(self, string: str):
        self.console.addstr(string, curses.color_pair(0))
        self.console.refresh()
    def println(self, string: str):
        self.print(string + LINESEP)

    def printBlue(self, string: str):
        self.console.addstr(string, curses.color_pair(COLOR_BLUE))
        self.console.refresh()
    def printlnBlue(self, string: str):
        self.printBlue(string + LINESEP)

    def printRed(self, string: str):
        self.console.addstr(string, curses.color_pair(COLOR_RED))
        self.console.refresh()
    def printlnRed(self, string: str):
        self.printRed(string + LINESEP)

    def printGreen(self, string: str):
        self.console.addstr(string, curses.color_pair(COLOR_GREEN))
        self.console.refresh()
    def printlnGreen(self, string: str):
        self.printGreen(string + LINESEP)

    def printDim(self, string: str):
        self.console.addstr(string, curses.color_pair(COLOR_DIM))
        self.console.refresh()
    def printlnDim(self, string: str):
        self.printDim(string + LINESEP)

    def printError(self, string: str):
        self.console.addstr(string, curses.color_pair(COLOR_ERROR))
        self.console.refresh()
    def printlnError(self, string: str):
        self.printError(string + LINESEP)

    def clear(self):
        self.console.clear()
        self.console.refresh()

    def clearLine(self):
        self.console.clrtoeol()
        self.console.refresh()

    def move(self, x, y):
        self.console.move(y, x)
        self.console.refresh()

    def moveUp(self):
        yMax, xMax = self.console.getmaxyx()
        yMax -= 1
        xMax -= 1
        y, x = self.console.getyx()
        newY = max(0, min(y - 1, yMax))
        self.console.move(newY, x)
        self.console.refresh()

    def moveDown(self):
        yMax, xMax = self.console.getmaxyx()
        yMax -= 1
        xMax -= 1
        y, x = self.console.getyx()
        newY = max(0, min(y + 1, yMax))
        self.console.move(newY, x)
        self.console.refresh()

    def moveFront(self):
        y, x = self.console.getyx()
        self.console.move(y, 0)
        self.console.refresh()

    def getCursorPos(self) -> tuple[int, int]:
        y, x = self.console.getyx()
        return (x, y)
    
    def getLineText(self):
        text: str = ''
        y, x = self.console.getyx()
        yMax, xMax = self.console.getmaxyx()
        yMax -= 1
        xMax -= 1
        for i in range(xMax):
            charAndAttr: int = self.console.inch(y, i)
            charCode: int = charAndAttr & 0xFF
            character: str = chr(charCode)
            text += character
        return text.strip()
    

if __name__ == '__main__':
    console: Console = Console()
    console.printlnBlue('Blue Text')
    console.printlnRed('Red Text')
    console.printlnGreen('Green Text')
    console.printlnDim('Dim Text')
    console.printlnError('Error Text')
    console.println('This is normal text')
    console.println('hello! how is everyone!')
    console.moveUp()
    text: str = console.getLineText()
    console.moveDown()
    console.moveFront()
    # text: str = console.getBackText(10)
    console.println(text)
    input('')
    console.close()