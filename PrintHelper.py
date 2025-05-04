from colorama import Fore, Back, Style
from blessed import Terminal
import shutil
import sys

def printBlue(string: str):
    print(Fore.BLUE + string + Style.RESET_ALL)

def printGreen(string: str):
    print(Fore.GREEN + string + Style.RESET_ALL)

def printRed(string: str):
    print(Fore.RED + string + Style.RESET_ALL)

def printDim(string: str):
    print(Style.DIM + string + Style.RESET_ALL)

def printError(string: str):
    print(Back.RED + 'ERROR' + Back.RESET + Fore.RED + f' {string}' + Style.RESET_ALL)

def printOverwriteLine(string: str):
    sys.stdout.write('\r')  # Move the cursor to the beginning of the current line
    sys.stdout.write('\033[2K')  # Clear the entire current line
    sys.stdout.write(string)
    sys.stdout.flush()

def printOverwrite(originalText: str, newText: str):
    term = Terminal()
    width = shutil.get_terminal_size().columns

    originalLines = []
    for i in range(0, len(originalText), width):
        originalLines.append(originalText[i:i + width])

    numOriginalLines = len(originalLines)
            
    sys.stdout.write('\033[1A') # Move the cursor up 1 line
    sys.stdout.flush()
    for i in range(numOriginalLines):
        sys.stdout.write('\033[2K')  # Clear the entire current line
        if i != numOriginalLines - 1: 
            sys.stdout.write('\033[1A') # Move the cursor up 1 line
        sys.stdout.flush()

    print(newText)