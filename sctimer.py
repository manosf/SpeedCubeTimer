#!/usr/bin/env python3
import time
import datetime
import curses 
import os
import argparse

#Initializing the curses module.
stdscr=curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.nodelay(1)

sct_parser=argparse.ArgumentParser(description='''
            **A terminal based timer for SpeedCubing***
            ''')
sct_parser.add_argument('--countdown', action='store_true',
                help='Disable the countdown function.')
sct_parser.add_argument('-f', dest='filename',
                default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'times.txt'),
                help='Specify file where your solve times will be exported.')

sct_options = sct_parser.parse_args()

solves = []

def countdown():
    try:
        key=None
        for num in range(15, 0, -1):
            if key!=ord(' '):
                key=stdscr.getch()
                if num !=0:
                    if num>9:
                        print ('{0}'.format(num), end="\r")
                    else:
                        print ('0'+'{0}'.format(num), end="\r")
                    time.sleep(1)
                else:
                    key=ord(' ')
            else:
                break
    except KeyboardInterrupt:
        termination_handler()

def time_format(time):
    if time == None:
    	return None
    x = lambda time: '{0:.2f}'.format(time) if time < 60 else '%d:%05.2f' % divmod(time, 60)
    return x(time)

def stopwatch(t):
    try:
        key=None
        while key!=ord(' '):
            key=stdscr.getch()
            print(time_format(t), end="\r")
            time.sleep(0.01)
            t+=0.01
        return t
    except KeyboardInterrupt:
        termination_handler()

def export_times(filepath, current_solves):
    with open(filepath, 'w' if not os.path.isfile(filepath) else 'a') as times_file:
        times_file.write(str(datetime.datetime.now().date())+': '+str(current_solves)+'\n')

#Terminating properly the application by reversing the 'curses' settings
def termination_handler():
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    raise SystemExit

def main():
    while 1:
        try:
            key=stdscr.getch()
            if key==ord(' '):   #The solve count starts after pressing SPACEBAR
                if not sct_options.countdown:
                    countdown()
                solves.append(time_format(stopwatch(0.00)))
                print ("\rYour solves for this session: {0}".format(solves), end="\n\r")
            elif key==27:       #The application exits after pressing ESCAPE
                if len(solves)>0:
                    export_times(sct_options.filename, solves)
                termination_handler()
        except KeyboardInterrupt:
            termination_handler()
    
if __name__=="__main__":
    main()
