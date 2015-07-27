#!/usr/bin/env python

import sys
import curses

f = open(sys.argv[1], 'r')

def main(stdscr):

    line = f.readline()
    stdscr.addstr(line)

    curses.echo()
    
    buffer = ""
    while buffer != line:
        buffer += chr(stdscr.getch())
    stdscr.addstr(buffer)

    stdscr.addstr("yay")

curses.wrapper(main)
