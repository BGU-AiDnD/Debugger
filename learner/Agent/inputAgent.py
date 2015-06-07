__author__ = 'Amir-pc'
import sys
import os
import fileinput
import sqlite3



from xml.dom import minidom
# type methods.txt con | jdb -connect com.sun.jdi.SocketAttach:hostname=localhost,port=1044 |python input.py


def test(c):
    fail=c.getElementsByTagName("failure")
    out=len(fail)
    err=c.getElementsByTagName("error")
    if out==0:
        out=len(err)
    return (c.attributes["classname"].value+"."+c.attributes["name"].value,out)


def xmlReadTest(doc):
    outs=[]
    xmldoc=minidom.parse(open(doc,"r"))
    suite=xmldoc.getElementsByTagName("testsuite")[0]
    tests= suite.getElementsByTagName("testcase")
    for i in range(len(tests)):
        outs.append(test(tests[i]))
    return outs

#tests= testsClasses("D:\\Amir_Almishali\\agent\\all.xml")
tests= xmlReadTest("C:\\GitHub\\agent\\reports\\all.xml")
base0="D:\\Amir_Almishali\\agent\\testMem\\"
if not (os.path.isdir(base0)):
        os.mkdir(base0)
i=1




while(1==1):
    l=sys.stdin.readline()
    if(l== "[INFO] BUILD SUCCESS\n"):
        print l
        break
    if(l!= " T E S T S\n"):
        continue
    print l
    base=base0
    filename="1_start.txt"
    file=open(base+filename,"wb")
    toWrite=set()
    while(1==1):
        line=sys.stdin.readline()
        spl=line.split()
        if(len(spl)==0):
            continue
        if(spl[0]!="[inst2]"):
            continue
        name=spl[2].split(".")
        name=".".join(name)
        print name
        if name in tests:
            print 2222
            file.writelines(toWrite)
            file.flush()
            toWrite=set()
            file.close()
            i=i+1
            filename=str(i)+"_"+name
            file=open(base+filename,"wb")
        #file.write(str(names.index(name))+"\n")
        toWrite.add(name+"\n")
    file.writelines(toWrite)
    file.flush()
    toWrite=set()
    file.close()
