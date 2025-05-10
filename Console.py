from typing import Optional
import curses
import time
import math

COLOR_BLUE: int = 10
COLOR_RED: int = 20
COLOR_GREEN: int = 30
COLOR_DIM: int = 40
COLOR_ERROR: int = 50

LINESEP: str = '\n'

class Console():
    def __init__(self):
        self.console: Optional[curses.window] = curses.initscr()
        self.console.scrollok(True)
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
        self.console.addstr('ERROR', curses.color_pair(COLOR_ERROR))
        self.console.addstr(f' {string}', curses.color_pair(0))
        self.console.refresh()
    def printlnError(self, string: str):
        self.printError(string + LINESEP)

    def clear(self):
        self.console.clear()
        self.console.refresh()

    def clearLine(self):
        self.console.clrtoeol()
        self.console.refresh()

    def getCurrentLineText(self) -> str:
        text: str = ''
        originalY, originalX = self.console.getyx()
        yMax, xMax = self.console.getmaxyx()
        yMax -= 1
        xMax -= 1
        for i in range(xMax):
            charAndAttr: int = self.console.inch(originalY, i)
            charCode: int = charAndAttr & 0xFF
            character: str = chr(charCode)
            text += character
        self.console.move(originalY, originalX)
        return text.strip()
    
    def getLineText(self, y: int) -> str:
        text: str = ''
        originalY, originalX = self.console.getyx()
        yMax, xMax = self.console.getmaxyx()
        yMax -= 1
        xMax -= 1
        for i in range(xMax):
            charAndAttr: int = self.console.inch(y, i)
            charCode: int = charAndAttr & 0xFF
            character: str = chr(charCode)
            text += character
        self.console.move(originalY, originalX)
        return text.strip()

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

    def moveFrontText(self):
        text: str = self.getCurrentLineText()
        y, x = self.console.getyx()
        self.console.move(y, len(text))
        self.console.refresh()

    def getCursorPos(self) -> tuple[int, int]:
        y, x = self.console.getyx()
        return (x, y)
    
    def getBackText(self, amount: int) -> str:
        text: str = ''
        y, x = self.console.getyx()
        while len(text) < amount:
            currentLine: str = self.getLineText(y)
            amountNeeded: int = (amount - len(text))
            if amountNeeded > len(currentLine):
                text += currentLine[::-1]
                y -= 1
            else: text += currentLine[len(currentLine) - amountNeeded:][::-1]
        return text[::-1]
    
    def getBackTextToString(self, string: str, timeoutSeconds: float, defaultString: str) -> str:
        startTimeSeconds: float = time.time_ns() / math.pow(10, 9)
        text: str = ''
        y, x = self.console.getyx()
        while True:
            currentTimeSeconds: float = time.time_ns() / math.pow(10, 9)
            if currentTimeSeconds - startTimeSeconds > timeoutSeconds: return defaultString
            currentLine: str = self.getLineText(y)
            characterIndex: int = currentLine.find(string)
            if characterIndex == -1:
                text += currentLine[::-1]
                y -= 1
            else: 
                characterIndex += len(string)
                text += currentLine[characterIndex:][::-1]
                break
        return text[::-1]
    
    def getLinesCovered(self, string: str):
        maxY, maxX = self.console.getmaxyx()
        linesCovered: int = math.ceil(len(string) / maxX)
        return linesCovered
    
    def input(self):
        curses.echo()
        inputBytes: bytes = self.console.getstr()
        curses.noecho()
        input: str = inputBytes.decode('utf-8')
        return input