__author__ = 'amir'

import sqlite3
import os
import csv

def wekaAns(filename):
    probs=[]
    yesMin=1
    noMax=0
    with open(filename) as f:
        content = f.readlines()
        content=content[content.index(" inst#     actual  predicted error prediction\n")+1:]
        content=content[:content.index("\n")-1]
        for i in content:
            s=i.split()
            if(len(s)==0):
                break
            #print(s)
            ind=3
            if(len(s)==5 or len(s)==6):
                ind=4
            p=s[ind]
            if(p[0] not in list("0123456789")):
                p=p[1:]
            x = float(p)
            if(s[2]=="2:no"):
                x=1-x
                noMax=max(noMax,x)
            else:
                yesMin=min(yesMin,x)
            probs.append(x)
    return probs



def BugDetails(bug,tests,dbPath,files,priors):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    names=set()
    traces=[]
    outcomes=[]
    for t in tests:
        trace=[]
        for f in c.execute("select distinct fileName from testsFiles where Test==\""+t+"\""):
            trace=trace+[files.index(f[0])]
            names.add(f[0])
        traces=traces+[trace]
        for o in c.execute("select outcome from tests where Test==\""+t+"\""):
            outcomes=outcomes+[o[0]]
    bugged=[]
    for b in c.execute("select distinct fileName from buggedFiles where BugId=="+bug):
        if(b[0] in files):
            bugged=bugged+[files.index(b[0])]
    UsedPriors=[]
    UsedInds=[]
    for b in names:
        ind=files.index(b)
        app=-0.1
        if (ind<len(priors)):
            app=priors[ind]
        UsedPriors.append(app)
        UsedInds.append(ind)

    return UsedPriors,UsedInds,bugged,tests,traces,outcomes

def exportBarinel(barinel,bugID,UsedPriors,UsedInds,bugged,testsNames,traces,outcomes):
    lines=[UsedPriors]
    l=len(UsedPriors)
    for t in traces:
        line=[]
        for i in UsedInds:
            if i in t:
                line.append("1")
            else:
                line.append("0")
        line.append(outcomes[traces.index(t)])
        lines.append(line)
    with open(barinel+bugID+".csv", 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(lines)

def exportPlanner(planner,bugID,UsedPriors,UsedInds,bugged,testsNames,traces,outcomes):
    lines=[["[Priors]"]]+ [[UsedPriors]]
    lines=lines+[ ["[Bugs]"]]+[[bugged]]
    lines=lines+[ ["[InitialTests]"]]+[[testsNames[0]]]
    details=zip(testsNames,traces,traces,outcomes)
    lines=lines+[ ["[TestDetails]"]]+details
    with open(planner+bugID+".csv", 'wb') as f:
        writer = csv.writer(f,delimiter=";")
        writer.writerows(lines)


def exportRealBugs(realBugsPath,bugID,UsedPriors,UsedInds,bugged,testsNames,traces,outcomes):
    allUsed=set()
    for t in traces:
        for t1 in t:
            allUsed.add(t1)
    lines=[list(allUsed),bugged]
    with open(realBugsPath+bugID+".csv", 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(lines)


def exportAll(dbPath,filesPath,wekaPath,outPath):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    c2 = conn.cursor()
    barinel=outPath+"\\barinel"
    if not (os.path.isdir(barinel)):
        os.mkdir(barinel)
    barinel=barinel+"\\"
    planner=outPath+"\\planner"
    if not (os.path.isdir(planner)):
        os.mkdir(planner)
    planner=planner+"\\"
    realBugsPath=outPath+"\\realBugs"
    if not (os.path.isdir(realBugsPath)):
        os.mkdir(realBugsPath)
    realBugsPath=realBugsPath+"\\"
    for r in c.execute("select distinct BugId from buggedFiles"):
        bugID=str(r[0])
        testsNames=[]
        s="select distinct Test from testsFiles where fileName in ( select fileName from buggedFiles where BugId="+str(bugID)+ " )"
        for t in c2.execute(s):
            testsNames=testsNames+[t[0]]
        if len(testsNames)==0:
            continue
        f=open(filesPath,"rb")
        files=[row.split("\n")[0] for row in f.readlines()]
        f.close()
        priors=wekaAns(wekaPath)
        UsedPriors,UsedInds,bugged,testsNames,traces,outcomes=BugDetails(bugID,testsNames,dbPath,files,priors)
        exportBarinel(barinel,bugID,UsedPriors,UsedInds,bugged,testsNames,traces,outcomes)
        exportPlanner(planner,bugID,UsedPriors,UsedInds,bugged,testsNames,traces,outcomes)
        exportRealBugs(realBugsPath,bugID,UsedPriors,UsedInds,bugged,testsNames,traces,outcomes)


wekaPath="C:\\GitHub\\vers\\ML\\WEKA_07_09.txt"
dbPath="C:\\GitHub\\agent\\testsBugs.db"
filesPath="C:\\GitHub\\agent\\allFiles.txt"
outPath="C:\\GitHub\\agent\\benchmark2\\"
exportAll(dbPath,filesPath,wekaPath,outPath)

