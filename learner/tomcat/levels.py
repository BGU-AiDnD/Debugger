__author__ = 'amir'

baseFile="C:\projs\git\svn\\22\\watchREM.txt"
import sys
def mindepth():
    return min([len(x.split("/") ) for x in open(baseFile, "r").readlines()])

def depthCreate(depth):
    print "depth is ", depth
    outF = open("C:\projs\git\svn\\22\\watchREMDepth.txt", "w")
    s=set()
    for x in open(baseFile, "r").readlines():
        l=x.split("\n")[0]
        ls=l.split("\\")
        ls=ls[:depth]
        s.add("/".join(ls))
    for x1 in s:
        outF.write(x1+"\n")


depthCreate(int(sys.argv[1]))
#depthCreate(5)