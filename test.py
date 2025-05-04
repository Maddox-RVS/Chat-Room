from typing import Optional
import curses

def main(stdscr: Optional[curses.window]):
    stdscr.clear()  # Clear the screen
    stdscr.addstr(0, 0, "Hello")  # Print "Hello" at (0, 0)
    stdscr.refresh()  # Update the display

    y, x = stdscr.getyx()  # Get current cursor position (which is after the 'o')
    stdscr.move(y, x - 1)  # Move cursor back one position (to the 'o')
    char_code = stdscr.inch() & 0xFF  # Get the character code at the cursor
    character = chr(char_code)  # Convert the character code to a character

    stdscr.addstr(2, 0, f"The character at the 'o' position is: {character}")  # Display the character
    stdscr.refresh()  # Update the display

    stdscr.getch()  # Wait for a key press before exiting

if __name__ == '__main__':
    curses.wrapper(main)