#!/usr/bin/env python3
import time

solves = []
i=0.00
x=1

def countdown():
    for num in range(15, 0, -1):
        if num<=9:
            print ('0'+'{0}'.format(num), end="\r")
        else:
            print ('{0}'.format(num), end="\r")
        if num!=0:
            time.sleep(1)

def time_format(time):
    if time == None:
    	return None
    x = lambda time: '{0:.2f}'.format(time) if time < 60 else '%d:%05.2f' % divmod(time, 60)
    return x(time)

def stopwatch(t):
    try:
        while x!=0:
            print(time_format(t), end="\r")
            time.sleep(0.01)
            t+=0.01
    except KeyboardInterrupt:
        return t

countdown()
print (solves)
solves.append(time_format(stopwatch(i)))
print (solves)

