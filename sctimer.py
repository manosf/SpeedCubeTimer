#!/usr/bin/env python3
import time
import datetime
import curses 
import os
import argparse
import random
from configparser import SafeConfigParser
from collections import namedtuple

SCT_CONF_PATH=os.path.dirname(os.path.abspath(__file__))
SCT_CONF_FILE=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sctimer.conf')

sct_parser=argparse.ArgumentParser(description='''
            ***A terminal based timer for SpeedCubing***
           ----------------------------------------------
            ''')
sct_parser.add_argument('-c', '--no_countdown', action='store_true',
                help='Omit the countdown function.')
sct_parser.add_argument('-f', '--file', action='store', dest='filename',
                default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'times.txt'),
                help='Specify file where your solve times will be exported.')
sct_parser.add_argument('-s', '--stats', action='store_true',
                help='Return solve time statisticss.')
sct_parser.add_argument('-r', '--scramble', action='store', dest='scramble_length', type=int,
                help='Reverse the default option for printing scrambles.')
sct_parser.add_argument('-o', '--config', action='store', dest='cfgfile',
                help='Run SpeedCubingTimer using a different configuration file.')

sct_options = sct_parser.parse_args()

#Initializing the 'curses' module.
stdscr=curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.nodelay(1)

solves = []

def config():
    conf_parser=SafeConfigParser()
    if sct_options.cfgfile:
        if os.path.isfile(sct_options.cfgfile):
            conf_file=sct_options.cfgfile
        else:
            conf_file=SCT_CONF_FILE
            print('Configuration file {} not found. Using default conf file{}.'.format(sct_options.cfgfile, SCT_CONF_FILE), end='\n')
    else:
        conf_file=SCT_CONF_FILE
    try:
        conf_parser.read(conf_file)
        try:
            countdown=conf_parser.getboolean('Countdown', 'Countdown_on')
        except ConfigParser.NoOptionError:
            countdown=True
        try:
            export=conf_parser.getboolean('Exporting', 'Export_always')
        except ConfigParser.NoOptionError:
            export=True
        try:
            filename=conf_parser.get('Exporting', 'Export_file')
        except ConfingParser.NoOptionError:
            filename='times.txt'
        try:
            scramble=conf_parser.getboolean('Scrambles', 'Scramble')
        except ConfigParser.NoOptionError:
            scramble=True
        try:
            scramble_length=conf_parser.getint('Scrambles', 'Length')
        except ConfigParser.NoOptionError:
            scramble_length=10
    except (ConfigParser.NoSectionError,
            ConfigParser.MissingSectionHeaderError):
        print('File {} contains no section headers.'.format(conf_file), end='\r')
        termination_handler()
    Configuration=namedtuple('Config', 'countdown export filename scramble scramble_length')
    config=Configuration(countdown=countdown, export=export, filename=filename, scramble=scramble, scramble_length=scramble_length)
    return config

def scrambler(length):
    try:
        faces = ['R', 'R\'', 'L', 'L\'', 'U', 'U\'', 'D', 'D\'', 'F', 
                'F\'', 'B', 'B\'', 'R2', 'L2', 'U2', 'D2', 'F2', 'B2']
        scramble=''
        for move in range(length):
            turn=random.randint(0, len(faces)-1)
            if move>0:
                while faces[turn]==previous_turn or int(turn/2)==int(previous_num/2):
                    turn=random.randint(0, len(faces)-1)
            scramble+=' '+faces[turn]
            previous_num=turn
            previous_turn=faces[turn]
        print(scramble, end='\n\r')
        key=None
        for i in range(120):
            if key!=ord(' '):
                key=stdscr.getch()
                time.sleep(0.5)
    except KeyboardInterrupt:
        termination_handler()

def countdown():
    try:
        key=None
        for num in range(30, 0, -1):
            if key!=ord(' '):
                key=stdscr.getch()
                if key==27:
                    print('Terminated by user, no times were exported for this session', end='\r')
                    raise KeyboardInterrupt
                if int(num/2) !=0:
                    if int(num/2)>9:
                        print (int(num/2), end="\r")
                    else:
                        print ('0'+'{}'.format(int(num/2)), end="\r")
                    time.sleep(0.5)
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
            if key==27:
                t='DNF'
                break
            print(time_format(t), end="\r")
            time.sleep(0.01)
            t+=0.01
        return t
    except KeyboardInterrupt:
        termination_handler()

'''Reading and parsing times in order to use them in various operations.
   The function reads the times_file, splits it into lines and then replaces
   all quotes and square brackets and appends the words to an empty list.
   The format in which the words are appended after parsing, makes it easier
   to use in later operations.
'''
def statistics(solves_count, filepath):
    try:
        with open(filepath, 'r') as times_file:
            stats_list=[]
            for line in times_file.read().splitlines():
                for word in line.split(':')[-1].split('\','):
                    word=word.replace('\'', '')
                    if len(stats_list)<=solves_count-1:
                        stats_list.append(word.strip('[ ]'))
                    else:
                        break
        return stats_list
    except OSError:
        print('There is no such times\' file. Pass \'-h\' for help.')
        termination_handler()

def avg_x(solves_count, filepath):
    if len(statistics(solves_count, filepath))<solves_count or len(statistics(solves_count, filepath))==0:
        result='--:--'
    else:
        if solves_count==3:
            try:
                avg=sum(float(solve) for solve in statistics(solves_count, filepath))/solves_count
                result=time_format(avg)
            except ValueError:
                result='DNF'
        else:
            avg=[] 
            for solve in statistics(solves_count, filepath):
                try:
                    if solve!=max(statistics(solves_count, filepath)) and solve!=min(statistics(solves_count, filepath)):
                        avg.append(float(solve))
                except ValueError:
                    avg.append(max(statistics(solves_count, filepath)))
            avg=(sum(solve for solve in avg))/(solves_count-2)
            result=time_format(avg)
    return result

def export_times(filepath, current_solves):
    with open(filepath, 'w+' if not os.path.isfile(filepath) else 'r+') as times_file:
        previous_times=times_file.read()
        times_file.seek(0, 0)
        times_file.write(str(datetime.datetime.now().date())+': '+str(current_solves)+'\n'+previous_times)

#Terminating properly the application by reversing the 'curses' settings
def termination_handler():
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    raise SystemExit

def main():
    export_file=sct_options.filename if sct_options.filename else config().filename
    if sct_options.stats:
        print('Your last 5 solves are: {}'.format(statistics(12, export_file)), end='\n\r')
        print('Your mean of the last 3 solves is: {}'.format(avg_x(3, export_file)), end='\n\r')
        print('Your average of the last 5 solves is: {}'.format(avg_x(5, export_file)), end='\n\r')
        print('Your average of the last 12 solves is: {}'.format(avg_x(12, export_file)), end='\n\r')
        print('Your average of the last 100 solves is: {}'.format(avg_x(100, export_file)), end ='\n\r')
        termination_handler()
    else:
        while 1:
            try:
                key=stdscr.getch()
                if key==ord(' '):                                               #The solve count starts after pressing SPACEBAR
                    if not sct_options.scramble_length:                         #Check whether or not a scramble will be displayed and what its length will be
                        if config().scramble:
                            scrambler(config().scramble_length)
                    else:
                        scrambler(sct_options.scramble_length)
                    if not sct_options.no_countdown and config().countdown:     #Check whether or not the countdown will be displayed
                        countdown()
                    if stopwatch(0.00)!='DNF':
                        solves.append(time_format(stopwatch(0.00)))
                    else:
                        solves.append(stopwatch(0.00))
                    print ('Your solves for this session: {}'.format(solves), end='\n\r')
                elif key==27:                                                   #The application exits after pressing ESCAPE
                    if config().export and len(solves)>0:
                        export_times(export_file, solves)
                    termination_handler()
            except KeyboardInterrupt:
                termination_handler()
    
if __name__=="__main__":
    main()
