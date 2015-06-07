__author__ = 'Amir-pc'


import glob
from xml.dom import minidom
import os
import csv


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



def filesSorted(tracesPath):
    docs=[]
    lst= glob.glob(tracesPath+"\\*")
    for doc in lst:
        if(os.path.isdir(doc)):
            continue
        d=doc.split("\\")
        d=d[len(d)-1]
        num=int(d.split("_")[0])
        docs=docs+ [(num,d)]
    docs=sorted(docs,key=lambda d1: d1[0])
    sort=[d[1].split("_")[1] for d in docs]
    return zip(sort,[d[1] for d in docs])


def build(f="C:\Users\Amir-pc\Documents\GitHub\\backkup\CDescriptorTests\\report\TEST-org.eclipse.cdt.core.cdescriptor.tests.CDescriptorTests.xml",
          path="C:\Users\Amir-pc\Documents\GitHub\\backkup\CDescriptorTests\\",
          out="C:\Users\Amir-pc\Documents\GitHub\\backkup\CDescriptorTests\\tracesByTests\\out.csv" , namesDB=[]):
    tests = xmlReadTest(f)
    names = []
    for t in tests:
        a, b = t
        names = names + [a]
    files = filesSorted(path)

    sortedNames = [f[0] for f in files]
    inds = []
    for n in names:
        if n in sortedNames:
            inds=inds+[sortedNames.index(n)]
    sortedPaths = [f[1] for f in files]
    testsSorted = sorted(zip(inds, tests), key=lambda d: d[0])
    inds = [t[0] for t in testsSorted]
    testFiles = []
    inds = inds + [len(sortedNames)]
    for i in range(len(inds) - 1):
        testFiles = testFiles + [sortedPaths[inds[i]:inds[i + 1]]]
    FullTraces = []
    for tf in testFiles:
        OneTrace = []
        for fi in tf:
            lines = [line.split("\n")[0] for line in open(path + fi, "r+").readlines()]
            OneTrace = OneTrace + lines
        trac = list(set(OneTrace))
        FullTraces = FullTraces + [trac]
    tom=[]
    j=0
    for ft in FullTraces:
        Onetom=[]
        for i in namesDB:
            a=0
            if i in ft:
                a=1
            Onetom=Onetom+[a]
        tom=tom+[Onetom+[testsSorted[j][1][1]]]
        j=j+1
    with open(out, 'wb') as f:
                writer = csv.writer(f)
                writer.writerows(tom)


def matrixMulti(basepath="C:\Users\Amir-pc\Documents\GitHub\matrix", namesPath="C:\Users\Amir-pc\Documents\GitHub\\backkup\\namesDB.txt"):
    lst= glob.glob(basepath+"\\*")
    namesDB=[line.split("\n")[0] for line in open(namesPath, "r+").readlines()]
    for path in lst:
        if not (os.path.isdir(path)):
            continue
        print(path)
        f=os.path.join(path,"surefire-reports")
        out=os.path.join(path,"tracesByTests")
        if not (os.path.isdir(out)):
            os.mkdir(out)
        f=glob.glob(f+"\\*.xml")[0]
        build(f,path+"\\",out+"\\out1.csv",namesDB)

def appendOuts(basepath="C:\Users\Amir-pc\Documents\GitHub\matrix", mat="C:\Users\Amir-pc\Documents\GitHub\\backkup\\mat.csv"):
    lst= glob.glob(basepath+"\\*")
    all=[]
    for path in lst:
        if not (os.path.isdir(path)):
            continue
        out=os.path.join(path,"tracesByTests")
        cs= out+"\\out1.csv"
        reader = csv.reader(open(cs, "r"))
        all=all+  [j for j in reader]
    with open(mat, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(all)




if __name__ == '__main__':
    appendOuts()






