__author__ = 'amir'


import sys
import os
def pathToSvn(path):
    return "/".join(path.split("\\")[5:])

while(1==1):
    l=sys.stdin.readline()
    #if l.startswith("A       "):
    #print l[len("A       "):].split("\n")[0]
    if l=="" or l=="\n":
        break
    print pathToSvn(l.split("\n")[0])

