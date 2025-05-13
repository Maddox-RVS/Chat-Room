from typing import Optional
import curses
import time
import math

# Define constants for color pair numbers for better readability
COLOR_BLUE: int = 10
COLOR_RED: int = 20
COLOR_GREEN: int = 30
COLOR_DIM: int = 40
COLOR_ERROR: int = 50

LINESEP: str = '\n'

class Console():
    '''
    A wrapper class for the curses library to provide a simpler console interface.
    Handles initialization, color pairs, printing with colors, and basic cursor manipulation.
    '''

    def __init__(self):
        '''
        Initializes the curses console window and color pairs.
        Sets up basic color pairs and attempts to set up a custom dim color.
        '''

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
        '''
        Closes the curses window and restores the terminal to its normal state.
        '''

        curses.endwin()

    def print(self, string: str):
        '''
        Prints a string to the console at the current cursor position.

        Args:
            string (str): The string to print.
        '''

        self.console.addstr(string, curses.color_pair(0))
        self.console.refresh()
    def println(self, string: str):
        '''
        Prints a string to the console followed by a newline.

        Args:
            string (str): The string to print.
        '''

        self.print(string + LINESEP)

    def printBlue(self, string: str):
        '''
        Prints a string in blue color.

        Args:
            string (str): The string to print.
        '''

        self.console.addstr(string, curses.color_pair(COLOR_BLUE))
        self.console.refresh()
    def printlnBlue(self, string: str):
        '''
        Prints a string in blue color followed by a newline.

        Args:
            string (str): The string to print.
        '''

        self.printBlue(string + LINESEP)

    def printRed(self, string: str):
        '''
        Prints a string in red color.

        Args:
            string (str): The string to print.
        '''

        self.console.addstr(string, curses.color_pair(COLOR_RED))
        self.console.refresh()
    def printlnRed(self, string: str):
        '''
        Prints a string in red color followed by a newline.

        Args:
            string (str): The string to print.
        '''

        self.printRed(string + LINESEP)

    def printGreen(self, string: str):
        '''
        Prints a string in green color.

        Args:
            string (str): The string to print.
        '''

        self.console.addstr(string, curses.color_pair(COLOR_GREEN))
        self.console.refresh()
    def printlnGreen(self, string: str):
        '''
        Prints a string in green color followed by a newline.

        Args:
            string (str): The string to print.
        '''

        self.printGreen(string + LINESEP)

    def printDim(self, string: str):
        '''
        Prints a string in dim color.

        Args:
            string (str): The string to print.
        '''

        self.console.addstr(string, curses.color_pair(COLOR_DIM))
        self.console.refresh()
    def printlnDim(self, string: str):
        '''
        Prints a string in dim color followed by a newline.

        Args:
            string (str): The string to print.
        '''

        self.printDim(string + LINESEP)

    def printError(self, string: str):
        '''
        Prints an error message with 'ERROR' in a highlighted color.

        Args:
            string (str): The error message string.
        '''

        self.console.addstr('ERROR', curses.color_pair(COLOR_ERROR))
        self.console.addstr(f' {string}', curses.color_pair(0))
        self.console.refresh()
    def printlnError(self, string: str):
        '''
        Prints an error message followed by a newline.

        Args:
            string (str): The error message string.
        '''

        self.printError(string + LINESEP)

    def clear(self):
        '''
        Clears the entire console screen.
        '''
        
        self.console.clear()
        self.console.refresh()

    def clearLine(self):
        '''
        Clears the current line from the cursor position to the end.
        '''

        self.console.clrtoeol()
        self.console.refresh()

    def getCurrentLineText(self) -> str:
        '''
        Retrieves the text content of the current line.

        Returns:
            str: The text content of the current line, stripped of leading/trailing whitespace.
        '''

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
        '''
        Retrieves the text content of a specific line.

        Args:
            y (int): The row index of the line.

        Returns:
            str: The text content of the specified line, stripped of leading/trailing whitespace.
        '''

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
        '''
        Moves the cursor to a specific position.

        Args:
            x: The column index.
            y: The row index.
        '''

        self.console.move(y, x)
        self.console.refresh()

    def moveUp(self):
        '''
        Moves the cursor one line up.
        '''

        yMax, xMax = self.console.getmaxyx()
        yMax -= 1
        xMax -= 1
        y, x = self.console.getyx()
        newY = max(0, min(y - 1, yMax))
        self.console.move(newY, x)
        self.console.refresh()

    def moveDown(self):
        '''
        Moves the cursor one line down.
        '''

        yMax, xMax = self.console.getmaxyx()
        yMax -= 1
        xMax -= 1
        y, x = self.console.getyx()
        newY = max(0, min(y + 1, yMax))
        self.console.move(newY, x)
        self.console.refresh()

    def moveFront(self):
        '''
        Moves the cursor to the beginning of the current line (column 0).
        '''

        y, x = self.console.getyx()
        self.console.move(y, 0)
        self.console.refresh()

    def moveFrontText(self):
        '''
        Moves the cursor to the end of the text on the current line.
        '''

        text: str = self.getCurrentLineText()
        y, x = self.console.getyx()
        self.console.move(y, len(text))
        self.console.refresh()

    def getCursorPos(self) -> tuple[int, int]:
        '''
        Gets the current cursor position.

        Returns:
            tuple[int, int]: A tuple containing the column (x) and row (y) of the cursor.
        '''

        y, x = self.console.getyx()
        return (x, y)
    
    def getBackText(self, amount: int) -> str:
        '''
        Retrieves a specified amount of text backwards from the current cursor position.
        Handles wrapping across lines.

        Args:
            amount (int): The number of characters to retrieve.

        Returns:
            str: The retrieved text.
        '''

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
        '''
        Retrieves text backwards from the current cursor position until a specific string is found.
        Includes a timeout to prevent infinite loops.

        Args:
            string (str): The string to search for.
            timeoutSeconds (float): The maximum time to search before returning the default string.
            defaultString (str): The string to return if the timeout is reached.
        
        Returns:
            str: The retrieved text after the search string, or the default string if timed out.
        '''

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
        '''
        Calculates the number of lines a given string will cover in the console based on its width.

        Args:
            string (str): The string to calculate lines for.

        Returns:
            int: The number of lines the string will cover.
        '''

        maxY, maxX = self.console.getmaxyx()
        linesCovered: int = math.ceil(len(string) / maxX)
        return linesCovered
    
    def input(self):
        '''
        Enables echoing and gets user input from the console.
        Disables echoing after input is received.

        Returns:
            str: The user's input string.
        '''
        
        curses.echo()
        inputBytes: bytes = self.console.getstr()
        curses.noecho()
        input: str = inputBytes.decode('utf-8')
        return input