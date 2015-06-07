__author__ = 'amir'

import sys
import os

while(1==1):
    l=sys.stdin.readline()
    #if l.startswith("A       "):
    #print l[len("A       "):].split("\n")[0]
    if l=="":
        break
    print ("archive\\watchdog\\"+(l.split("\n")[0]).replace("/","\\"))

