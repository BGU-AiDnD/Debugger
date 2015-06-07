__author__ = 'Amir-pc'
import sys
import os
import sqlite3



from xml.dom import minidom
#-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=1044
# -agentlib:jdwp=transport=dt_shmem,address=1044,server=y,suspend=y
#mvndebug integration-test
#mvn -Dmaven.surefire.debug install
# cat methods.txt -| jdb -attach 8000 | \..\Python27x86\python.exe input.py
# cat methods.txt -| jdb -connect com.sun.jdi.SocketAttach:hostname=localhost,port=1044 | \..\Python27x86\python.exe input.py
# type methods.txt con | jdb -connect com.sun.jdi.SocketAttach:hostname=localhost,port=1044 |python input.py
def test(c):
    fail=c.getElementsByTagName("failure")
    out=len(fail)
    return (c.attributes["classname"].value+"."+c.attributes["name"].value,out)

def xmlReadTest(doc):
    outs=[]
    xmldoc=minidom.parse(open(doc,"r"))
    suite=xmldoc.getElementsByTagName("testsuite")[0]
    tests= suite.getElementsByTagName("testcase")
    for i in range(len(tests)):
        outs.append(test(tests[i]))
    return outs

def namesDB(dbpath):
    conn = sqlite3.connect(dbpath)
    conn.text_factory = str
    c = conn.cursor()
    names=[]
    for row in c.execute(str('select distinct name from haelsTfiles order by name')):
        lst=row[0].split('\\')[3:]

        name=list(".".join(lst))
        name="".join(name[:len(name)-5])
        names.append(name)
    conn.close()
    return names

def testsClasses(methodsFile):
    lines=open(methodsFile,"r").readlines()
    lines=lines[:len(lines)-3]
    spl=[l.split(" ")[2] for l in lines]
    spl=[s.split("(")[0] for s in spl]
    #classes=[l[len(l)-2:] for l in spl]
    testCl=[]
    for c in spl:
        a=c.split(".")
        a=a[len(a)-2]
        if "Test" in a:
            testCl=testCl+[c]
    return testCl


def namesFromFile(path):
    return [r.split("\n")[0] for r in open(path,"r").readlines()]
tests= testsClasses("C:\Users\Amir-pc\Documents\GitHub\\backkup\\methods.txt")
#tests= testsClasses("D:\Amir_Almishali\\methods.txt")
#names=namesDB("C:\Users\Amir-pc\Documents\GitHub\\vers\dbMaccAll\CDT_8_2_0.db")
#xmlReadTest("C:\Users\Amir-pc\Documents\GitHub\\backkup\CDT_8_2_0\org.eclipse.cdt\core\org.eclipse.cdt.core.tests\\target\\surefire-reports\TEST-org.eclipse.cdt.core.suite.AutomatedIntegrationSuite.xml")
#dirName=sys.argv[1]
#print dirName
#base="D:\Amir_Almishali\\matrix\\"+dirName+"\\"
base="C:\Users\Amir-pc\Documents\GitHub\\amir"
if not (os.path.isdir(base)):
        os.mkdir(base)
i=1
filename="1_start.txt"
#open("C:\Users\Amir-pc\Documents\GitHub\\backkup\\namesDB2.txt","wb").writelines([n+"\n" for n in  names])
#names= namesFromFile("D:\Amir_Almishali\\namesDB2.txt")
names= namesFromFile("C:\Users\Amir-pc\Documents\GitHub\\backkup\\namesDB2.txt")
#print(names)
file=open(base+filename,"wb")
toWrite=set()
while(1==1):
    line=sys.stdin.readline()
    spl=line.split()
    if(len(spl)==0):
        continue
	
    if(spl[0]=="The" and  spl[1]=="application" and spl[2]=="exited"):
        break
    if(spl[0]!="Breakpoint"):
        continue
    name=spl[3].split(".")
    name=".".join(name[:len(name)-1])
    method=spl[3].split("(")[0]
    if method in tests:
        file.writelines(toWrite)
        file.flush()
        toWrite=set()
        file.close()
        i=i+1
        filename=str(i)+"_"+method
        file=open(base+filename,"wb")
    #file.write(str(names.index(name))+"\n")
    toWrite.add(name+"\n")
file.writelines(toWrite)
file.flush()
toWrite=set()
file.close()
