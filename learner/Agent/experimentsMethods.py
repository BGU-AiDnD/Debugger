__author__ = 'amir'

import glob
import random
import csv
import os
import math
import sqlite3
import shutil
import results
import subprocess
import wekaMethods.wekaAccuracy
import utilsConf


def optimize(inds_bef, mat, priors):
    inds=[]
    newPriors = []
    newMat = [[] for t in mat]
    len_mat0_ = len(mat[0]) - 1
    for i in range(len_mat0_):
        need = False
        for elem in mat:
            if elem[i] == "1":
                if elem[len(elem) - 1] == "1":
                    need = True
                    break
        if need == True:
            newPriors = newPriors + [priors[i]]
            inds = inds + [inds_bef[i]]
            for ind in range(len(newMat)):
                newMat[ind] = newMat[ind] + [mat[ind][i]]
    i = len(mat[0]) - 1
    for ind in range(len(newMat)):
        newMat[ind] = newMat[ind] + [mat[ind][i]]
    newTm=[]
    last=len(newMat[0])-1
    if(last==-1):
        newTm=[]
    else:
        for i in range(len(newMat)):
            if ("1" in newMat[i][:last]):
                newTm=newTm+[newMat[i]]
    return inds, newTm, newPriors

def optimizeAll(allFiles, allTests,outcomes, allBugs,priors,testsChoosedNames,FileNames):
    newFiles=[]
    newFileNames=[]
    newBugs = []
    newTests = []
    newOutcomes=[]
    testsChoosedNamesNew=[]
    # remove irrelevant files: files that participate just in pass tests
    for index in range(len(allFiles)):
        i=allFiles[index]
        need = False
        ind=0
        for elem in allTests:
            if elem[i] == "1":
                if outcomes[ind] == "1":
                    need = True
                    break
            ind=ind+1
        if need == True:
            newFiles.append(i)
            newFileNames.append(FileNames[index])
            if i in allBugs:
                newBugs.append(i)
    # update tests
    for t in allTests:
        test={}
        for i in newFiles:
            if (t[i]=="1"):
                test[newFiles.index(i)]="1"
            else:
                test[newFiles.index(i)]="0"
        newTests.append(test)
        ind=ind+1
    ind=0
    testsRet=[]
    # remove tests without files
    for t in newTests:
        need = False
        for i in t:
            if(t[i]=="1"):
                need=True
                break
        if (need==True):
            # check if there is a test with same components and result
            if not (t in testsRet and outcomes[ind] == outcomes[testsRet.index(t)]):
                testsRet.append(t)
                newOutcomes.append(outcomes[ind])
                testsChoosedNamesNew.append(testsChoosedNames[ind])
        ind=ind+1
    newBugs=[newFiles.index(i) for i in newBugs ]
    if(priors!=[]):
        priors=[priors[newFiles.index(i)] for i in newFiles]
    newFiles=range(len(newFiles))
    return newFiles, testsRet,newOutcomes,newBugs,priors,testsChoosedNamesNew,newFileNames

def conesOptimize2(allFiles, allTests,outcomes, allBugs,priors,testsChoosedNames,FileNames):
    to_check=[]
    to_check_valids=[]
    newBugs = []
    newTests = []
    newOutcomes=[]
    distinctFiles=[]
    testsChoosedNamesNew=[]
    # cones on bugs

    for f in allFiles:
        if( f not in allBugs):
            to_check_valids.append(f)
    to_check=list(allBugs)
    while(len(to_check)!=0):
        comp=to_check[0]
        to_check=to_check[1:]
        distinctFiles.append(comp)
        new_check=[]
        new_check_valids=[]
        for c in to_check:
            dup=True
            for t in allTests:
                if (t[comp] !=t[c]):
                    dup=False
                    break
            if(not dup):
                new_check.append(c)
        to_check=list(new_check)
        for c in to_check_valids:
            dup=True
            for t in allTests:
                if (t[comp] !=t[c]):
                    dup=False
                    break
            if(not dup):
                new_check_valids.append(c)
        to_check_valids=list(new_check_valids)

    # cones on others
    while(len(to_check_valids)!=0):
        comp=to_check_valids[0]
        to_check_valids=to_check_valids[1:]
        distinctFiles.append(comp)
        new_check=[]
        for c in to_check_valids:
            dup=True
            for t in allTests:
                if (t[comp] !=t[c]):
                    dup=False
                    break
            if(not dup):
                new_check.append(c)
        to_check_valids=list(new_check)

    ind=0
    for t in allTests:
        test={}
        for i in distinctFiles:
            if (t[i]=="1"):
                test[distinctFiles.index(i)]="1"
            else:
                test[distinctFiles.index(i)]="0"
        newTests.append(test)
        ind=ind+1
    ind=0
    testsRet=[]
    for t in newTests:
        need = False
        for i in t:
            if(t[i]=="1"):
                need=True
                break
        if (need==True):
            testsRet.append(t)
            newOutcomes.append(outcomes[ind])
            testsChoosedNamesNew.append(testsChoosedNames[ind])
        ind=ind+1

    newBugs=[distinctFiles.index(i) for i in allBugs if i in distinctFiles]
    newFileNames=[FileNames[allFiles.index(f)] for f in distinctFiles]
    if(False):
        for index in range(len(allFiles)):
            if allFiles[index] in distinctFiles:
                newFileNames.append(FileNames[index])
    if(priors!=[]):
        priors=[priors[i] for i in distinctFiles]
    newFiles=range(len(distinctFiles))
    return newFiles, testsRet,newOutcomes,newBugs,priors,testsChoosedNamesNew,newFileNames


def conesOptimize(allFiles, allTests,outcomes, allBugs,priors,testsChoosedNames):
    to_check=[]
    newBugs = []
    newTests = []
    newOutcomes=[]
    distinctFiles=[]
    testsChoosedNamesNew=[]
    # cones on bugs
    to_check=list(allBugs)
    while(len(to_check)!=0):
        comp=to_check[0]
        to_check=to_check[1:]
        distinctFiles.append(comp)
        new_check=[]
        for c in to_check:
            dup=True
            for t in allTests:
                if (t[comp] !=t[c]):
                    dup=False
                    break
            if(not dup):
                new_check.append(c)
        to_check=list(new_check)

    # cones on others
    for f in allFiles:
        if( f not in allBugs):
            to_check.append(f)
    while(len(to_check)!=0):
        comp=to_check[0]
        to_check=to_check[1:]
        distinctFiles.append(comp)
        new_check=[]
        for c in to_check:
            dup=True
            for t in allTests:
                if (t[comp] !=t[c]):
                    dup=False
                    break
            if(not dup):
                new_check.append(c)
        to_check=list(new_check)

    ind=0
    for t in allTests:
        test={}
        for i in distinctFiles:
            if (t[i]=="1"):
                test[distinctFiles.index(i)]="1"
            else:
                test[distinctFiles.index(i)]="0"
        newTests.append(test)
        ind=ind+1
    ind=0
    testsRet=[]
    for t in newTests:
        need = False
        for i in t:
            if(t[i]=="1"):
                need=True
                break
        if (need==True):
            testsRet.append(t)
            newOutcomes.append(outcomes[ind])
            testsChoosedNamesNew.append(testsChoosedNames[ind])
        ind=ind+1

    newBugs=[distinctFiles.index(i) for i in allBugs if i in distinctFiles]
    if(priors!=[]):
        priors=[priors[i] for i in distinctFiles]
    newFiles=range(len(distinctFiles))
    return newFiles, testsRet,newOutcomes,newBugs,priors,testsChoosedNamesNew

def optimizeVeyCommonFiles(allFiles, allTests,outcomes, allBugs,priors,testsChoosedNames,FileNames):
    newFiles=[]
    newFileNames=[]
    newBugs = []
    newTests = []
    newOutcomes=[]
    testsChoosedNamesNew=[]
    treshold=0.75*len(allTests)

    for index in range(len(allFiles)):
        i=allFiles[index]
        count=0
        ind=0
        for elem in allTests:
            if elem[i] == "1":
                count=count+1
            ind=ind+1
        if count <= treshold:
            newFiles.append(i)
            newFileNames.append(FileNames[index])
            if i in allBugs:
                newBugs.append(i)

    for t in allTests:
        test={}
        for i in newFiles:
            if (t[i]=="1"):
                test[newFiles.index(i)]="1"
            else:
                test[newFiles.index(i)]="0"
        newTests.append(test)
        ind=ind+1
    ind=0
    testsRet=[]
    for t in newTests:
        need = False
        for i in t:
            if(t[i]=="1"):
                need=True
                break
        if (need==True):
            testsRet.append(t)
            newOutcomes.append(outcomes[ind])
            testsChoosedNamesNew.append(testsChoosedNames[ind])
        ind=ind+1

    newBugs=[newFiles.index(i) for i in newBugs]
    if(priors!=[]):
        priors=[priors[i] for i in newFiles]
    newFiles=range(len(newFiles))
    return newFiles, testsRet,newOutcomes,newBugs,priors,testsChoosedNames,newFileNames

def barinelAppend(bugsFiles,barinelFiles):
    allFiles=set()
    allBugged=set()
    Tests=[]
    for bugF,barF in zip(bugsFiles,barinelFiles):
        f=open(bugF,"r")
        reader =csv.reader(f)
        read=[]
        for r1 in reader:
            read.append(r1)
        bfiles=read[0]
        bBugs=read[1]
        allFiles= allFiles | set(bfiles)
        allBugged=allBugged | set(bBugs)
        f.close()
        f=open(barF,"r")
        reader =csv.reader(f)
        read=[]
        for r1 in reader:
            read.append(r1)
        reader=read[1:]
        for line in reader:
            test={}
            length=len(line)
            for comp,bf in zip(line[:length-1],bfiles):# without outcome
                test[bf]=comp
            if(test not in Tests):
                Tests.append(test)
        f.close()
    AllTests=[]
    for test in Tests:
        for file in allFiles:
            if (not (file in test)):
                test[file]="0"
        AllTests.append(test)

    l=len(AllTests[0])
    return allBugged,allFiles,AllTests

def getBuggedFilesTestsByBugsIDs(dbPath,bugsIDS,package,times,priorsByFiles, buggedTestsChooser,notRand,buggedTable):
    allFiles=[]
    FileNames=[]
    allBugged=[]
    allTests=[]
    testsNames=[]
    Newpriors=[]
    testsSorted=['amir']
    testsChoosedNames=[]
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    indexA="CREATE INDEX IF NOT EXISTS FilesNames ON testsFiles (fileName)"
    c.execute(indexA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS FilesTests ON testsFiles (Test)"
    c.execute(indexA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS FilesBugged ON buggedFiles (BugId)"
    c.execute(indexA)
    conn.commit()

    if( type(package) is list):
        package="or testsFiles.fileName like ".join(["\"%"+ pack+"%\" " for pack in package])
    else:
        package="\"%"+ package+"%\" "
    s="select distinct Test from testsFiles where testsFiles.fileName like "+package
    for r in c.execute(s):
        testsNames.append(r[0])
    s="select Test,c from (select Test,count(fileName) as c from testsFiles  where testsFiles.fileName like" +package+"  group by Test) where c>=2  order by c DESC"
    s="select Test,c/(a+0.0) as d,c ,a from (select Test,count(fileName) as a, count(case When fileName like "+package+" Then 1 Else Null End) as c from testsFiles  group by Test) where c>0 order by d DESC"
    #s="select Test, a-c as d,c ,a from (select Test,count(fileName) as a, count(case When fileName like "+package+" Then 1 Else Null End) as c from testsFiles  group by Test) where c>0 order by d"
    for r in c.execute(s):
        if(r[0] in testsNames):
                testsSorted.append(r[0])
    testsTup = str(tuple(testsSorted))
    if (len(testsSorted)==1 ):
        return [],[],[],[],[]
    s="select distinct fileID,fileName  from testsFiles where Test in "+ testsTup
    for r in c.execute(s):
        allFiles.append(r[0])
        FileNames.append(r[1])

    bugsTup = str(tuple(bugsIDS))
    buggedNames=[]
    s="select distinct fileID,fileName from "+buggedTable+" where BugId in "+ bugsTup
    for r in c.execute(s):
        if(r[0] in allFiles):
            allBugged.append(r[0])
            buggedNames.append(r[1])
    testZerosToCopy={}
    for ind in range(len(allFiles)):
       testZerosToCopy[ind]="0"
    testsIndex=[]
    testsDict={}
    buggesTests=[]
    validTests=[]
    for i in range(times):
        if(buggedTestsChooser!=-1):
            if(i % buggedTestsChooser ==0):
                buggesTests.append(i)
            else:
                validTests.append(i)
        testsIndex.append(i)
        testsDict[i]=None
    testsDict[times]=None

    if(buggedTestsChooser==-1):
        validTests=testsIndex
        buggesTests=testsIndex


    for ind  in range(len(testsSorted)):
        if len(testsSorted)==0:
            break
        tn=[]
        if notRand:
            tn=testsSorted[0]
        else:
            tn=random.choice(testsSorted)
        testsSorted.remove(tn)
        testsChoosedNames.append(tn)
        isbugged=False
        if len(testsDict)==times:
            break
        s2="select testsFiles.Test as Test ,testsFiles.fileID as fileID from testsFiles where testsFiles.Test=\""+tn +"\""
        testTrace=testZerosToCopy.copy()
        for r in c.execute(s2):
            testNa=r[0]
            fileID=r[1]
            testTrace[allFiles.index(fileID)]="1"
            if fileID in allBugged:
                isbugged=True
        if(isbugged):
            if len(buggesTests)==0:
                continue
            testsDict[buggesTests[0]]=testTrace
            buggesTests.remove(buggesTests[0])
        else:
            if len(validTests)==0:
                continue
            testsDict[validTests[0]]=testTrace
            validTests.remove(validTests[0])
    vals=testsDict.values()
    min1 = min(vals.index(None), times)
    allTests=vals[:min1]
    if(priorsByFiles!=None):
        for f in allFiles:
            if( f in priorsByFiles):
                Newpriors.append(priorsByFiles[f])
            else:
                Newpriors.append(0.01)
    allBugged=[allFiles.index(x) for x in allBugged]
    allFiles=range(len(allFiles))

    return allBugged,allFiles,allTests,Newpriors,testsChoosedNames,FileNames


def getBuggedFilesTestsByBugsIDsMethods(dbPath,bugsIDS,package,times,priorsByFiles, buggedTestsChooser,notRand,buggedTable,testTable):
    allFiles=[]
    FileNames=[]
    allBugged=[]
    allTests=[]
    testsNames=[]
    Newpriors=[]
    testsSorted=['amir']
    testsChoosedNames=[]
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    indexA="CREATE INDEX IF NOT EXISTS FilesNames ON testsMethods (methodName)"
    c.execute(indexA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS FilesTests ON testsMethods (Test)"
    c.execute(indexA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS FilesBugged ON buggedFiles (BugId)"
    c.execute(indexA)
    conn.commit()

    if( type(package) is list):
        package=("or "+testTable+".name like ").join(["\"%"+ pack+"%\" " for pack in package])
    else:
        package="\"%"+ package+"%\" "
    s="select distinct Test from "+testTable+" where "+testTable+".name like "+package
    for r in c.execute(s):
        testsNames.append(r[0])
    s="select Test,c from (select Test,count(name) as c from "+testTable+"  where "+testTable+".name like" +package+"  group by Test) where c>=2  order by c DESC"
    s="select Test,c/(a+0.0) as d,c ,a from (select Test,count(name) as a, count(case When name like "+package+" Then 1 Else Null End) as c from "+testTable+"  group by Test) where c>0 order by d DESC"
    for r in c.execute(s):
        if(r[0] in testsNames):
                testsSorted.append(r[0])
    testsTup = str(tuple(testsSorted))
    if (len(testsSorted)==1 ):
        return [],[],[],[],[],[]
    s="select distinct name,name  from "+testTable+" where Test in "+ testsTup
    for r in c.execute(s):
        allFiles.append(r[0])
        FileNames.append(r[1])

    bugsTup = str(tuple(bugsIDS))
    buggedNames=[]
    s="select distinct name,BugId  from "+buggedTable+" where BugId in "+ bugsTup
    for r in c.execute(s):
        if(r[0] in allFiles):
            allBugged.append(r[0])
            buggedNames.append(r[1])
    testZerosToCopy={}
    for ind in range(len(allFiles)):
       testZerosToCopy[ind]="0"
    testsIndex=[]
    testsDict={}
    buggesTests=[]
    validTests=[]
    for i in range(times):
        if(buggedTestsChooser!=-1):
            if(i % buggedTestsChooser ==0):
                buggesTests.append(i)
            else:
                validTests.append(i)
        testsIndex.append(i)
        testsDict[i]=None
    testsDict[times]=None

    if(buggedTestsChooser==-1):
        validTests=testsIndex
        buggesTests=testsIndex


    for ind  in range(len(testsSorted)):
        if len(testsSorted)==0:
            break
        tn=[]
        if notRand:
            tn=testsSorted[0]
        else:
            tn=random.choice(testsSorted)
        testsSorted.remove(tn)
        testsChoosedNames.append(tn)
        isbugged=False
        if len(testsDict)==times:
            break
        s2="select "+testTable+".Test as Test ,"+testTable+".name as name from "+testTable+" where "+testTable+".Test=\""+tn +"\""
        testTrace=testZerosToCopy.copy()
        for r in c.execute(s2):
            testNa=r[0]
            fileID=r[1]
            testTrace[allFiles.index(fileID)]="1"
            if fileID in allBugged:
                isbugged=True
        if(isbugged):
            if len(buggesTests)==0:
                continue
            testsDict[buggesTests[0]]=testTrace
            buggesTests.remove(buggesTests[0])
        else:
            if len(validTests)==0:
                continue
            testsDict[validTests[0]]=testTrace
            validTests.remove(validTests[0])
    vals=testsDict.values()
    min1 = min(vals.index(None), times)
    allTests=vals[:min1]
    if(priorsByFiles!=None):
        for f in allFiles:
            if( f in priorsByFiles):
                Newpriors.append(priorsByFiles[f])
            else:
                Newpriors.append(0.01)
    allBugged=[allFiles.index(x) for x in allBugged]
    allFiles=range(len(allFiles))

    return allBugged,allFiles,allTests,Newpriors,testsChoosedNames,FileNames


def exportBarinel(out,priors,allBugs,allFiles,allTests,outcomes):
    lines=[]
    ind=0
    mat=[]
    for t in allTests:
        srt=sorted(t.items(),key=lambda tup: tup[0])
        srt=[s[1] for s in srt]+[outcomes[ind]]
        ind=ind+1
        mat.append(srt)
    inds=range(len(allFiles))
    #inds, newMat, newPriors = optimize( inds, mat, priors)
    inds, newMat, newPriors =  inds, mat, priors
    lines=[newPriors]+newMat
    with open(out, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(lines)

def plannerTestsRows(allFiles,allTests,outcomes):
    dets = []
    names = []
    ind = 0
    for t in allTests:
        trace=sorted(t.items(),key=lambda tup: tup[0])
        trace=[allFiles.index(tr[0]) for tr in trace if tr[1]=="1"]
        dets.append([ind,trace,trace,outcomes[ind]])
        names.append([ind])
        ind += 1
    return names,dets


def priorsByPbugPvalid(allBugs, allFiles, pBug, pValid):
    priors=[]
    for f in allFiles:
        if (f in allBugs):
            priors.append(pBug)
        else:
            priors.append(pValid)
    return priors


def exportPlanner(out,priors,allBugs,allFiles,allTests,outcomes,initials, failsProb ):
    names,dets=plannerTestsRows(allFiles,allTests,outcomes)
    lines=[["[Priors]"]]+ [[priors]]
    lines=lines+[ ["[Bugs]"]]+ [[allFiles.index(bug)] for bug in allBugs]
    initFailed=[]
    initpassed=[]
    for i in range(len(outcomes)):
        if outcomes[i]=="1":
            if( len(initFailed) <= failsProb *initials):
                initFailed.append(names[i])
        else:
            if( len(initpassed) <=(1-failsProb)*initials):
                initpassed.append(names[i])
    lines=lines + [["[InitialTests]"]]+initFailed+initpassed
    #lines=lines + [["[InitialTests]"]]+names
    lines=lines+ [["[TestDetails]"]]+dets
    with open(out, 'wb') as f:
        writer = csv.writer(f,delimiter=";")
        writer.writerows(lines)



def generateOutcomes(allBugs,allFiles,allTests,const):
    outcomes=[]
    setBugs = set(allBugs)
    for t in allTests:
        comps=[a[0] for a in t.items() if a[1]=="1"]
        pss=math.pow(const,len(setBugs & set(comps)))
        threshFail=random.uniform(0,1)
        if( pss >= threshFail):
            outcomes=outcomes+["0"]
        else:
            outcomes=outcomes+["1"]
    return outcomes

def exportBugs_Files(outbugs_Files,allBugs,allFiles,bugsIDS,TestsCount,pack,testsChoosedNames,addition,FileNames):
    bugsInds=[]
    for b in allBugs:
        if (b in allFiles):
            bugsInds.append(allFiles.index(b))
    with open(outbugs_Files, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows([["Files"],addition+range(len(allFiles)),["Bugged"],addition+bugsInds,["BugsIds"],bugsIDS,["TestsCount"],[TestsCount],["pack"],[pack],["testsChoosedNames"],testsChoosedNames,["FileNames"],FileNames] )

def allBugsFromDB(dbPath,package,weka, table="buggedFiles"):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    bugs=[]
    query = "select distinct BugId from "+table+" where "+table+".fileName like \"%" + package + "%\"  "
    if (weka):
        #query=query+"and BugId in (select * from [8_1_2Bugs])"
        query=query+"and BugId in (select BugId from buggedFiles)"
    #print query
    for r in c.execute(query):
        bugID=str(r[0])
        bugs.append(bugID)
    return bugs

def allBugsFromDBMethods(dbPath,package,weka, table):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    bugs=[]
    query = "select distinct BugId from "+table+" where "+table+".methodDir like \"%" + package + "%\"  "
    if (weka):
        #query=query+"and BugId in (select * from [8_1_2Bugs])"
        query=query+"and BugId in (select BugId from "+table+")"
    #print query
    for r in c.execute(query):
        bugID=str(r[0])
        bugs.append(bugID)
    return bugs


def dirStruct(outPath):
    o = outPath
    if not (os.path.isdir(o)):
        os.mkdir(o)
    o = outPath + "\\barinel\\"
    if not (os.path.isdir(o)):
        os.mkdir(o)
    o = outPath + "\\planner\\"
    if not (os.path.isdir(o)):
        os.mkdir(o)
    o = outPath + "\\plannerRecords\\"
    if not (os.path.isdir(o)):
        os.mkdir(o)
    o = outPath + "\\out\\"
    if not (os.path.isdir(o)):
        os.mkdir(o)
    o = outPath + "\\bugs_Files\\"
    if not (os.path.isdir(o)):
        os.mkdir(o)

def getAllpacks(packsPath):
    f=open(packsPath,"r")
    l=[line.split("\n")[0] for line in f.readlines()]
    f.close()
    return l

def priorsFromWeka(dbPathTests,wekaAns,FileNames,allFiles):
    wekaPriors={}
    filesPriors={}
    first=0
    with open(wekaAns,"r") as f:
        reader=csv.reader(f)
        for l in reader:
            if(first==0):
                first=1
                continue
            prior=l[5]
            if( "*" in prior):
                prior="".join(list(prior[1:]))
            prior=float(prior)
            if(l[3]=="2:no") or (l[3]=="2:valid") :
                #prior=1-prior
                prior=prior
            wekaPriors[l[0]]=prior+0.01
    if FileNames==[]:
        conn = sqlite3.connect(dbPathTests)
        conn.text_factory = str
        c = conn.cursor()
        for x in c.execute(' select distinct methodName,methodName from testsMethods order by methodName'):
            if (x[0] not in wekaPriors):
                filesPriors[x[1]]=0.01
            else:
                filesPriors[x[1]]=wekaPriors[x[0]]
        conn.close()

    if FileNames!=[]:
        for i in range(len(FileNames)):
            name=FileNames[i]
            ind=allFiles[i]
            if name not in wekaPriors:
                filesPriors[ind]=0.01
            else:
                filesPriors[ind]=wekaPriors[name]
    return  filesPriors



def allPackBugs(dbPath, numOfBugs, packsPath,numOfExperiments,weka,table="buggedFiles"):
    packsList = getAllpacks(packsPath)
    bugspathsAndpaths = []
    for p in packsList:
        lst1 = []
        if "Files" in table:
			lst1 = allBugsFromDB(dbPath, p,weka,table)
        if "Methods" in table:
			lst1 = allBugsFromDBMethods(dbPath, p,weka,table)
        bugspathsAndpaths.append((lst1, p))
    #bugs = [x for x in bugspathsAndpaths if len(x[0]) >= numOfBugs]
    bugspathsAndpaths=sorted(bugspathsAndpaths,key=lambda r: len(r[0]),reverse=True)
    bugs = [x for x in bugspathsAndpaths if len(x[0]) >= numOfBugs]
    bugs = [x for x in bugspathsAndpaths if len(x[0]) >= 1]
    #bugs = [x for x in bugspathsAndpaths ]
    return bugs

def allPackBugsMethods(dbPath, numOfBugs, packsPath,numOfExperiments,weka,table):
    packsList = getAllpacks(packsPath)
    bugspathsAndpaths = []
    for p in packsList:
        lst1 = allBugsFromDBMethods(dbPath, p,weka,table)
        bugspathsAndpaths.append((lst1, p))
    #bugs = [x for x in bugspathsAndpaths if len(x[0]) >= numOfBugs]
    bugspathsAndpaths=sorted(bugspathsAndpaths,key=lambda r: len(r[0]),reverse=True)
    bugs = [x for x in bugspathsAndpaths if len(x[0]) >= numOfBugs]
    return bugs

def choosePackBug(bugs, numOfBugs,order,numOfPacks,chooseThis):
    bugsChoose= list(bugs)
    choosed=[]
    if( chooseThis==[]):
        for x in range(numOfPacks):
            if (len(bugsChoose) == 0):
                break
            b = random.choice(bugsChoose)
            choosed.append(b)
            bugsChoose.remove(b)
    else:
        for i in chooseThis:
            b = bugsChoose[i]
            choosed.append(b)
            #bugsChoose.remove(b)
    lst1=[x[0] for x in choosed]
    l=[]
    for item in lst1:
        for i in item:
            l.append(i)
    pack =[x[1] for x in choosed]
    lst1=list(l)
    bugsIDS = ['-1']
    for i in range(numOfBugs):
        if (len(lst1) == 0):
            break
        b = random.choice(lst1)
        bugsIDS.append(b)
        lst1.remove(b)
    return bugsIDS, pack

def readBarinel(path):
    files=[]
    tests=[]
    bugs=[]
    outs=[]
    f=open(path,"r")
    reader=csv.reader(f)
    lines=[r for r in reader]
    priors=lines[0]
    files=range(len(priors))
    inde=0
    for i in priors:
        if i==str(-0.01):
            bugs.append(inde)
        inde=inde+1
    lines=lines[1:]
    for l in lines:
        outs.append(l[len(l)-1])
        test={}
        for i in range(len(l)-1):
            test[i]=l[i]
        tests.append(test)
    return files, tests,outs, bugs,priors

def readBugFile(bug_f):
    f = open(bug_f, "r")
    lines = [x.split("\n")[0] for x in f.readlines()]
    f.close()
    used = lines[1].split(",")
    bugged = lines[3].split(",")
    BugsIds = lines[5].split(",")
    testsCount = int(lines[7].split(",")[0])
    pack = lines[9].split(",")[0]
    testsChoosedNames=lines[11].split(",")
    FileNames=lines[13].split(",")
    return BugsIds, bugged, pack, testsCount, used,testsChoosedNames,FileNames

def optimizations(FileNames, allBugged, allFiles, allTests, outcomes, priors, testsChoosedNames):
    allFiles, allTests, outcomes, allBugged, priors, testsChoosedNames, FileNames = optimizeAll(allFiles, allTests, outcomes, allBugged, priors,testsChoosedNames,FileNames)
    allFiles, allTests, outcomes, allBugged, priors, testsChoosedNames, FileNames = conesOptimize2(allFiles, allTests, outcomes, allBugged, priors, testsChoosedNames, FileNames)
    allFiles, allTests, outcomes, allBugged, priors, testsChoosedNames, FileNames = optimizeVeyCommonFiles(allFiles, allTests, outcomes,allBugged,priors, testsChoosedNames, FileNames)
    return FileNames, allBugged, allFiles, allTests, outcomes, priors, testsChoosedNames


def buildInstanceAndOptimize(bugsIDS, const, dbPath, pack, times,priorsByFiles,buggedTestsChooser,notRand,buggedTable):
    allBugged, allFiles, allTests,priors,testsChoosedNames,FileNames = getBuggedFilesTestsByBugsIDs(dbPath, bugsIDS, pack, times,priorsByFiles,buggedTestsChooser,notRand,buggedTable)
    if(len(allTests)==0 or len(allBugged)==0):
        return [],[],[],[],[],[]
    outcomes = generateOutcomes(allBugged, allFiles, allTests, const)
    FileNames, allBugged, allFiles, allTests, outcomes, priors, testsChoosedNames = optimizations(FileNames, allBugged,allFiles, allTests,outcomes, priors,testsChoosedNames)
    return allBugged, allFiles, allTests, outcomes,priors,testsChoosedNames,FileNames

def buildInstanceAndOptimizeMethods(bugsIDS, const, dbPath, pack, times,priorsByFiles,buggedTestsChooser,notRand,buggedTable,testTable):
    allBugged, allFiles, allTests,priors,testsChoosedNames,FileNames = getBuggedFilesTestsByBugsIDsMethods(dbPath, bugsIDS, pack, times,priorsByFiles,buggedTestsChooser,notRand,buggedTable,testTable)
    if(len(allTests)==0 or len(allBugged)==0 or len(allBugged)==1):
        return [],[],[],[],[],[],[]
    outcomes = generateOutcomes(allBugged, allFiles, allTests, const)
    FileNames, allBugged, allFiles, allTests, outcomes, priors, testsChoosedNames = optimizations(FileNames, allBugged,allFiles, allTests,outcomes, priors,testsChoosedNames)
    return allBugged, allFiles, allTests, outcomes,priors,testsChoosedNames,FileNames

def readInstance( exp,times,copyPath):
    filePre=str(times)+"_"
    outbugs_Files =copyPath+"\\bugs_Files\\"+filePre + str(exp) + ".txt"
    outBarinel = copyPath+"\\barinel\\"+filePre +"uniform_" + str(exp) + ".csv"
    allFiles, allTests,outcomes, bugs,priors=readBarinel(outBarinel)
    BugsIds, allBugged, pack, testsCount, files,testsChoosedNames,FileNames = readBugFile(outbugs_Files)
    allBugged=[int(x) for x in allBugged]
    files=[int(f) for f in files]
    return allBugged, files, allTests, outcomes, priors,testsChoosedNames,FileNames


def wekaProbs(outPath,dbPath,packsPath,numOfExperiments,numOfBugsARR,timesArr,const,minimalTests,maximalTests,wekaAns,initials,order,numOfPacks,buggedTestsChooser,initialsChooser,notRand):
    priorsByFiles=priorsFromWeka(dbPath,wekaAns,[],[])
    exp=-1
    conf_file = outPath+"conf.txt"
    exportConf(conf_file,packsPath,numOfExperiments,numOfBugsARR,timesArr,const,minimalTests,maximalTests,initials,order,numOfPacks,buggedTestsChooser,notRand)
    expIND=0
    for numOfBugs in numOfBugsARR:
        bugs = allPackBugs(dbPath, 50  , packsPath,numOfExperiments,True)
        start = min([20, len(bugs)-1])
        for choo in [-1]:
            bugsIDS, pack=choosePackBug(bugs, numOfBugs,order,numOfPacks,[choo])

            for t in range(len(timesArr)):
                times=timesArr[t]
                exp=-1
                cont=0
                while exp <numOfExperiments:
                    #bugsIDS, pack = choosePackBug(bugs, numOfBugs,order,numOfPacks,[])
                    if(len(bugsIDS)==1): # (-1,)
                        break
                    allBugged, allFiles, allTests, outcomes, priors,testsChoosedNames,FileNames = buildInstanceAndOptimize(bugsIDS, const, dbPath, pack, times,priorsByFiles,buggedTestsChooser,notRand)
                    if(len(allTests)<=minimalTests or len(allTests)>maximalTests or  len(allBugged)==0):
                        cont=cont+1
                        if( cont==1):
                            cont=0
                            break
                        else:
                            continue
                    exp=exp+1
                    expIND=expIND+1
                    outbugs_Files = outPath+"\\bugs_Files\\" + str(expIND) + ".txt"
                    exportBugs_Files(outbugs_Files,allBugged,allFiles,bugsIDS,len(allTests),pack,testsChoosedNames,[],FileNames)
                    file =  str(expIND)
                    outBarinel = outPath+"\\barinel\\weka_" + file + ".csv"
                    outPlanner = outPath+"\\planner\\weka_" + file + ".txt"
                    exportBarinel(outBarinel,priors,allBugged,allFiles,allTests,outcomes)
                    exportPlanner(outPlanner,priors,allBugged,allFiles,allTests,outcomes,initials,initialsChooser)
                    outBarinel = outPath+"\\barinel\\uniform_" + file + ".csv"
                    outPlanner = outPath+"\\planner\\uniform_" + file + ".txt"
                    priors=[0.1 for p in priors]
                    exportBarinel(outBarinel,priors,allBugged,allFiles,allTests,outcomes)
                    exportPlanner(outPlanner,priors,allBugged,allFiles,allTests,outcomes,initials,initialsChooser)
    return expIND

def allBuggedFilesDB(dbPath,FileNames,buggedTable):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    bugsTup = str(tuple(FileNames))
    s="select distinct fileName from "+buggedTable+" where fileName in "+ bugsTup
    buggedNames=[b[0] for b in c.execute(s) ]
    buggedInds=[FileNames.index(b) for b in buggedNames ]
    return buggedInds



def MultyWekaAndSanity(outPath,dbPath,packsPath,numOfExperiments,numOfBugsARR,timesArr,const,minimalTests,maximalTests,wekaAnsArr,initialsFactor,order,numOfPacks,buggedTestsChooser,initialsChooser,notRand,copybool,copyPath,buggedTable,pureSanity, bugsPacks=[]):
    #priorsByFiles=priorsFromWeka(dbPath,wekaAns)
    exp=-1
    conf_file = outPath+"conf.txt"
    exportConf(conf_file,packsPath,numOfExperiments,numOfBugsARR,timesArr,const,minimalTests,maximalTests,initialsFactor,order,numOfPacks,buggedTestsChooser,notRand,initialsChooser,buggedTable,pureSanity)
    exp=-1
    expIND=-1
    timesMax=max(timesArr)
    bugs = allPackBugs(dbPath, 20  , packsPath,numOfExperiments,True)
    if bugsPacks==[]:
        bugsPacks=[choosePackBug(bugs, 20,order,numOfPacks,[]) for x in range(numOfExperiments)]
    print "start Experiment"
    while exp <numOfExperiments:
        bugsIDS, pack=bugsPacks[exp]
        if(len(bugsIDS)==1): # (-1,)
            break
        if copybool:
            allBuggedExp, allFilesExp, allTestsExp, outcomesExp, priorsExp,testsChoosedNamesExp,FileNamesExp = readInstance(exp+1,timesMax,copyPath)
        else:
            allBuggedExp, allFilesExp, allTestsExp, outcomesExp, priorsExp,testsChoosedNamesExp,FileNamesExp = buildInstanceAndOptimize(bugsIDS, const, dbPath, pack, timesMax,[],buggedTestsChooser,notRand,buggedTable)
            if(len(allTestsExp)<=minimalTests or len(allTestsExp)>maximalTests or  len(allBuggedExp)==0):
                continue
        exp=exp+1
        expIND=expIND+1
        for t in range(len(timesArr)):
            times=timesArr[t]
            filePre=str(times)+"_"
            outbugs_Files =outPath+"\\bugs_Files\\"+filePre + str(expIND) + ".txt"
            allTests=allTestsExp[:times+1]
            outcomes=outcomesExp[:times+1]
            FileNames, allBugged, allFiles, allTests, outcomes, priors, testsChoosedNames = optimizations(FileNamesExp, allBuggedExp,allFilesExp, allTests,outcomes, priorsExp,testsChoosedNamesExp)
            exportBugs_Files(outbugs_Files,allBugged,allFiles,bugsIDS,len(allTests),pack,testsChoosedNames,[],FileNames)
            outBarinel = outPath+"\\barinel\\"+filePre +"uniform_" + str(expIND) + ".csv"
            outPlanner = outPath+"\\planner\\"+filePre +"uniform_" +  str(expIND) + ".txt"
            priors=[0.1 for p in FileNames]
            exportBarinel(outBarinel,priors,allBugged,allFiles,allTests,outcomes)
            initials=int(initialsFactor*times)
            exportPlanner(outPlanner,priors,allBugged,allFiles,allTests,outcomes,initials,initialsChooser)
            for wekaAns,name in wekaAnsArr:
                priorsByFiles=priorsFromWeka(dbPath,wekaAns,FileNames,allFiles)
                outBarinel = outPath+"\\barinel\\"+filePre +"weka_" +name+  str(expIND) + ".csv"
                outPlanner = outPath+"\\planner\\"+filePre +"weka_" +name+  str(expIND) + ".txt"
                exportBarinel(outBarinel,priorsByFiles.values(),allBugged,allFiles,allTests,outcomes)
                exportPlanner(outPlanner,priorsByFiles.values(),allBugged,allFiles,allTests,outcomes,initials,initialsChooser)
            pBug = 0.6
            if(pureSanity):
                allBugged=allBuggedFilesDB(dbPath,FileNames,buggedTable)
            for j in range(2+1):  # pValid < pBug
                pValid = j / 10.0
                file = filePre +str(pBug) + "_" + str(pValid) + "_" + str(expIND)
                outBarinel = outPath+"\\barinel\\" + file + ".csv"
                outPlanner = outPath+"\\planner\\" + file + ".txt"
                priors=priorsByPbugPvalid(allBugged, allFiles, pBug+0.01, pValid+0.01)
                exportBarinel(outBarinel,priors,allBugged,allFiles,allTests,outcomes)
                exportPlanner(outPlanner,priors,allBugged,allFiles,allTests,outcomes,initials,initialsChooser)
    return expIND

def MultyWekaAndSanityMethods(outPath,dbPath,packsPath,numOfExperiments,numOfBugsARR,timesArr,const,minimalTests,maximalTests,wekaAnsArr,initialsFactor,order,numOfPacks,buggedTestsChooser,initialsChooser,notRand,copybool,copyPath,buggedTable,pureSanity, bugsPacks,testTable):
    #priorsByFiles=priorsFromWeka(dbPath,wekaAns)
    exp=-1
    conf_file = outPath+"conf.txt"
    exportConf(conf_file,packsPath,numOfExperiments,numOfBugsARR,timesArr,const,minimalTests,maximalTests,initialsFactor,order,numOfPacks,buggedTestsChooser,notRand,initialsChooser,buggedTable,pureSanity,testTable)
    exp=-1
    expIND=-1
    timesMax=max(timesArr)
    bugs = allPackBugs(dbPath, 20  , packsPath,numOfExperiments,True)
    if bugsPacks==[]:
        bugsPacks=[choosePackBug(bugs, 20,order,numOfPacks,[]) for x in range(numOfExperiments)]
    print "start Experiment"
    while exp <numOfExperiments:
        bugsIDS, pack=bugsPacks[exp]
        if(len(bugsIDS)==1): # (-1,)
            break
        if copybool:
            allBuggedExp, allFilesExp, allTestsExp, outcomesExp, priorsExp,testsChoosedNamesExp,FileNamesExp = readInstance(exp+1,timesMax,copyPath)
        else:
            allBuggedExp, allFilesExp, allTestsExp, outcomesExp, priorsExp,testsChoosedNamesExp,FileNamesExp = buildInstanceAndOptimizeMethods(bugsIDS, const, dbPath, pack, timesMax,[],buggedTestsChooser,notRand,buggedTable,testTable)
            if(len(allTestsExp)<=minimalTests or len(allTestsExp)>maximalTests or  len(allBuggedExp)==0):
                exp=exp+1
                continue
        exp=exp+1
        expIND=expIND+1
        for t in range(len(timesArr)):
            times=timesArr[t]
            filePre=str(times)+"_"
            outbugs_Files =outPath+"\\bugs_Files\\"+filePre + str(expIND) + ".txt"
            allTests=allTestsExp[:times+1]
            outcomes=outcomesExp[:times+1]
            FileNames, allBugged, allFiles, allTests, outcomes, priors, testsChoosedNames = optimizations(FileNamesExp, allBuggedExp,allFilesExp, allTests,outcomes, priorsExp,testsChoosedNamesExp)
            exportBugs_Files(outbugs_Files,allBugged,allFiles,bugsIDS,len(allTests),pack,testsChoosedNames,[],FileNames)
            outBarinel = outPath+"\\barinel\\"+filePre +"uniform_" + str(expIND) + ".csv"
            outPlanner = outPath+"\\planner\\"+filePre +"uniform_" +  str(expIND) + ".txt"
            priors=[0.1 for p in FileNames]
            exportBarinel(outBarinel,priors,allBugged,allFiles,allTests,outcomes)
            initials=int(initialsFactor*times)
            exportPlanner(outPlanner,priors,allBugged,allFiles,allTests,outcomes,initials,initialsChooser)
            for wekaAns,name in wekaAnsArr:
                priorsByFiles=priorsFromWeka(dbPath,wekaAns,FileNames,allFiles)
                outBarinel = outPath+"\\barinel\\"+filePre +"weka_" +name+  str(expIND) + ".csv"
                outPlanner = outPath+"\\planner\\"+filePre +"weka_" +name+  str(expIND) + ".txt"
                exportBarinel(outBarinel,priorsByFiles.values(),allBugged,allFiles,allTests,outcomes)
                exportPlanner(outPlanner,priorsByFiles.values(),allBugged,allFiles,allTests,outcomes,initials,initialsChooser)
            pBug = 0.6
            if(pureSanity):
                allBugged=allBuggedFilesDB(dbPath,FileNames,buggedTable)
            for j in range(2+1):  # pValid < pBug
                pValid = j / 10.0
                file = filePre +str(pBug) + "_" + str(pValid) + "_" + str(expIND)
                outBarinel = outPath+"\\barinel\\" + file + ".csv"
                outPlanner = outPath+"\\planner\\" + file + ".txt"
                priors=priorsByPbugPvalid(allBugged, allFiles, pBug+0.01, pValid+0.01)
                exportBarinel(outBarinel,priors,allBugged,allFiles,allTests,outcomes)
                exportPlanner(outPlanner,priors,allBugged,allFiles,allTests,outcomes,initials,initialsChooser)
    return expIND

def exportConf(conf_file,packsPath,numOfExperiments,numOfBugs,times,const,minimalTests,maximalTests,initials,order,numOfPacks,buggedTestsChooser,notRand,initialsChooser,buggedTable,pureSanity,testTable):
    with open(conf_file, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows([["packsPath"],[packsPath],["buggedTable"],[buggedTable],["testTable"],[testTable],
                          ["numOfExperiments"],[numOfExperiments],
                          ["numOfBugs"],[numOfBugs],
                          ["times"],[times],
                          ["const"],[const],
                          ["minimalTests"],[minimalTests],
                          ["maximalTests"],[maximalTests],
                          ["initials"],[initials],
                          ["order"],[order],
                          ["buggedTestsChooser"],[buggedTestsChooser],
                          ["notRand"],[notRand],
                          ["pureSanity"],[pureSanity],
                          ["initialsChooser"],[initialsChooser],
                          ["numOfPacks"],[numOfPacks]] )


def sanityProbs(outPath,dbPath,packsPath,numOfExperiments,numOfBugsARR,timesArr,const,minimalTests,maximalTests,initials,order,numOfPacks,buggedTestsChooser,initialsChooser,notRand):
    #bugs = allPackBugs(dbPath, numOfBugs, packsPath,numOfExperiments,False)
    conf_file = outPath+"conf.txt"
    exportConf(conf_file,packsPath,numOfExperiments,numOfBugsARR,timesArr,const,minimalTests,maximalTests,initials,order,numOfPacks,buggedTestsChooser,notRand)
    expIND=0
    for numOfBugs in numOfBugsARR:
        bugs = allPackBugs(dbPath, 30  , packsPath,numOfExperiments,True)
        start = min([20, len(bugs)-1])
        for choo in [-1]:
            bugsIDS, pack=choosePackBug(bugs, numOfBugs,order,numOfPacks,[choo])
            for t in range(len(timesArr)):
                times=timesArr[t]
                exp=-1
                cont=0
                while exp <numOfExperiments:
                    if(len(bugsIDS)==1): # (-1,)
                        break
                    allBugged, allFiles, allTests, outcomes, priors,testsChoosedNames = buildInstanceAndOptimize(bugsIDS, const, dbPath, pack, times,None,buggedTestsChooser,notRand)
                    if(len(allTests)<=minimalTests or len(allTests)>=maximalTests or  len(allBugged)==0):
                        cont=cont+1
                        if( cont==5):
                            cont=0
                            break
                        else:
                            continue
                    exp=exp+1
                    expIND=expIND+1
                    outbugs_Files = outPath+"\\bugs_Files\\" + str(expIND) + ".txt"
                    exportBugs_Files(outbugs_Files,allBugged,allFiles,bugsIDS,len(allTests),pack,testsChoosedNames)
                    for i in range(11):
                        pBug = i / 10.0
                        for j in range(i+1):  # pValid < pBug
                            pValid = j / 10.0
                            file = str(pBug) + "_" + str(pValid) + "_" + str(expIND)
                            outBarinel = outPath+"\\barinel\\" + file + ".csv"
                            outPlanner = outPath+"\\planner\\" + file + ".txt"
                            priors=priorsByPbugPvalid(allBugged, allFiles, pBug+0.01, pValid+0.01)
                            exportBarinel(outBarinel,priors,allBugged,allFiles,allTests,outcomes)
                            exportPlanner(outPlanner,priors,allBugged,allFiles,allTests,outcomes,initials,1/initialsChooser)
    return expIND

def statisticalInfo(dbPath,packsPath):
    packsBugs=allPackBugs(dbPath, 0, packsPath,0,False)
    packsInfo=[]
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    ans=[]
    for pack in packsBugs:
        bugs,package=pack
        testsFiles=[]
        testsNames=[]
        s="select distinct Test from testsFiles where testsFiles.fileName like \""+package+".%\" "
        for r in c.execute(s):
            testsNames.append(r[0])
        s="select distinct fileName from testsFiles where testsFiles.fileName like \""+package+".%\" "
        for r in c.execute(s):
            testsFiles.append(r[0])
        ans.append([package,len(bugs),len(testsNames),len(testsFiles)])
    return ans

def statisticalInfoMethods(dbPath,packsPath):
    packsBugs=allPackBugsMethods(dbPath, 0, packsPath,0,False,"buggedMethods")
    packsInfo=[]
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    ans=[]
    for pack in packsBugs:
        bugs,package=pack
        testsFiles=[]
        testsNames=[]
        s="select distinct Test from testsMethods where testsMethods.methodName like \"%"+package+"%\" "
        for r in c.execute(s):
            testsNames.append(r[0])
        s="select distinct methodName from testsMethods where testsMethods.methodName like \"%"+package+"%\" "
        for r in c.execute(s):
            testsFiles.append(r[0])
        ans.append([package,len(bugs),len(testsNames),len(testsFiles)])
    return ans

def copySTMS(outPath,utilsPath):
    outPath=outPath+"\\"
    lines=[["Components Table:",""]]+[[str(i),str(i)] for i in range(9000)]
    shutil.copyfile(os.path.join(utilsPath,"conv_comp_table.csv"),  outPath + "planner\\conv_comp_table.csv")
    shutil.copyfile(os.path.join(utilsPath,"barinel.jar"), outPath + "barinel.jar")
    shutil.copyfile(os.path.join(utilsPath,"planner150.jar"), outPath + "planner150.jar")
    shutil.copyfile(os.path.join(utilsPath,"barinelRun.bat"), outPath + "barinelRun.bat")

def transposeBugs():
    global bugs, d, x, lst, p, b
    bugs = allPackBugs(dbPath, numOfBugs, packsPath, 0, False)
    d = {}
    for x in bugs:
        lst, p = x
        for b in lst:
            if b in d:
                d[b] = (d[b]).append(p)
            else:
                d[b] = [p]

def Most_All_Mkdirs(outPath,experimentsInstances):
    dirs=[]
    for training,testing, weka, table in experimentsInstances:
        o = outPath + "\\"+training+"-"+testing+"\\"
        if not (os.path.isdir(o)):
            os.mkdir(o)
        dirStruct(o)
        dirs.append(o)
    return dirs


def RunAndResults(buggedTestsChooser, bugsPacks, const, copy, copyPath, outpath, dbPath, initialsChooser, initialsFactor,
                  maximalTests, minimalTests, numOfBugs, numOfExperiments, numOfPacks, packsPath, pureSanity, table,
                  times,  wekaAnsArr,testTable):
    numOfExperiments = MultyWekaAndSanityMethods(outpath, dbPath, packsPath, numOfExperiments, numOfBugs, times, const, minimalTests,
                                          maximalTests, wekaAnsArr, initialsFactor, False, numOfPacks, buggedTestsChooser,
                                          initialsChooser, False, copy, copyPath, table, pureSanity, bugsPacks,testTable)
    weka = True
    run_commands = ["java", "-jar", "planner150.jar","1", outpath + "\\planner\\", outpath + "\\plannerRecords\\", str(0.7)]
    proc = subprocess.Popen(run_commands, stdout=subprocess.PIPE, shell=True,cwd=outpath)
    (out, err) = proc.communicate()

    run_commands = ["barinelRun.bat"]
    proc = subprocess.Popen(run_commands, stdout=subprocess.PIPE, shell=True,cwd=outpath)
    (out, err) = proc.communicate()
    types = ["all", "normal", "can't advance"]
    a = 0
    for t in types:
        a = a + 1
        results.planner_resultsMultyWekaAndSanity(outpath + "\\plannerRes" + t + ".csv", outpath + "\\plannerMEDRes" + t + ".csv", outpath,
                                                  numOfExperiments, t, weka, times, wekaAnsArr)
        # results.planner_recordes(outPath+"plannerRes"+t+".csv",outPath+"plannerMEDRes"+t+".csv",outPath+"\\plannerRecords\\",numOfExperiments,t,weka,exps)
    # results.resultsAllBarinel("%s\\barinelOptA.csv" % outPath,"%s\\barinelOptA2.csv" % outPath, "%s\\" % outPath,1,weka,numOfExperiments)
    results.resultsMultyWekaAndSanity("%s\\barinelOptA.csv" % outpath, "%s\\barinelOptA2.csv" % outpath, "%s\\" % outpath, 1,
                                      numOfExperiments, times, wekaAnsArr)


def RunAndResultsMethods(buggedTestsChooser, bugsPacks, const, copy, copyPath, d, dbPath, initialsChooser, initialsFactor,
                  maximalTests, minimalTests, numOfBugs, numOfExperiments, numOfPacks, packsPath, pureSanity, table,
                  times,  wekaAnsArr):
    numOfExperiments = MultyWekaAndSanityMethods(d, dbPath, packsPath, numOfExperiments, numOfBugs, times, const, minimalTests,
                                          maximalTests, wekaAnsArr, initialsFactor, False, numOfPacks, buggedTestsChooser,
                                          initialsChooser, False, copy, copyPath, table, pureSanity, bugsPacks)
    weka = True
    plannerRunSTMT = "cmd /x /c  \" cd  /d " + d + " & java -jar planner150.jar %s %s %s %s \"" % (
    str(1), d + "\\planner\\", d + "plannerRecords\\", str(0.7))
    os.system(plannerRunSTMT)
    bat_ = "cmd.exe /X /C \" cd /d " + d + " & " + d + "barinelRun.bat\""
    os.system(bat_)
    types = ["all", "normal", "can't advance"]
    a = 0
    for t in types:
        a = a + 1
        results.planner_resultsMultyWekaAndSanity(d + "plannerRes" + t + ".csv", d + "plannerMEDRes" + t + ".csv", d,
                                                  numOfExperiments, t, weka, times, wekaAnsArr)
        # results.planner_recordes(outPath+"plannerRes"+t+".csv",outPath+"plannerMEDRes"+t+".csv",outPath+"\\plannerRecords\\",numOfExperiments,t,weka,exps)
    # results.resultsAllBarinel("%s\\barinelOptA.csv" % outPath,"%s\\barinelOptA2.csv" % outPath, "%s\\" % outPath,1,weka,numOfExperiments)
    results.resultsMultyWekaAndSanity("%s\\barinelOptA.csv" % d, "%s\\barinelOptA2.csv" % d, "%s\\" % d, 1,
                                      numOfExperiments, times, wekaAnsArr)


def Most_All_Real(outPath,dbPath,packsPath,wekaBase,numOfExperiments,numOfBugs,times,const,minimalTests,maximalTests,initialsFactor,numOfPacks,buggedTestsChooser,initialsChooser,copy,copyPath,pureSanity):
    experimentsInstances=[] # tuple of training,testing, weka, table
    wekaAlgs=["weka.classifiers.trees.J48" ,"weka.classifiers.bayes.NaiveBayes" , "weka.classifiers.trees.RandomForest" ]
    wekaAlgs=[ "weka.classifiers.trees.RandomForest" ]

    wekaAnsArr=[(wekaBase+"CDT_8_1_2_AllFiles_1_Only.csv",w) for w in wekaAlgs]#+[(wekaBase+"weka.classifiers.trees.RandomForest_Style2.csv","prev")] #all
    experimentsInstances.append(["all","all",wekaAnsArr, "buggedFiles" ] )
    if 0==1:
        experimentsInstances.append(["all","real",wekaAnsArr, "buggedFilesChecked" ] )
        wekaAnsArr=[(wekaBase+w+"_Most_blameP.csv",w) for w in wekaAlgs] #most
        experimentsInstances.append(["most","most",wekaAnsArr, "buggedFilesOne" ] )
        experimentsInstances.append(["most","real",wekaAnsArr, "buggedFilesChecked" ] )
    if 0==1:
        wekaAnsArr=[(wekaBase+w+"_CleanAll.csv",w) for w in wekaAlgs] #all+
        experimentsInstances.append(["allP","allP",wekaAnsArr, "buggedFiles" ] )
        experimentsInstances.append(["allP","real",wekaAnsArr, "buggedFilesChecked" ] )
        wekaAnsArr=[(wekaBase+w+"_Most_Clean.csv",w) for w in wekaAlgs] #most+
        experimentsInstances.append(["mostP","mostP",wekaAnsArr, "buggedFilesOne" ] )
        experimentsInstances.append(["mostP","real",wekaAnsArr, "buggedFilesChecked" ] )
    bugs = allPackBugs(dbPath, 2  , packsPath,numOfExperiments,True,"buggedFilesChecked")
    bugsPacks=[choosePackBug(bugs, 7,False,1,[])for x in range(numOfExperiments)]
    dirs=Most_All_Mkdirs(outPath,experimentsInstances)
    for ei,d in zip(experimentsInstances,dirs):
        copySTMS(d)
    for ei,d in zip(experimentsInstances,dirs):
        training,testing, weka, table=ei
        RunAndResults(buggedTestsChooser, bugsPacks, const, copy, copyPath, d, dbPath, initialsChooser, initialsFactor,
                      maximalTests, minimalTests, numOfBugs, numOfExperiments, numOfPacks, packsPath, pureSanity, table,
                      times,  wekaAnsArr)
    linesWrite=[]
    linesWrite.append(["training","testing", "algorithm","pBug","pValid","times","precision_avg","recall_avg","auc_avg","tests_avg","files_avg","bugged_avg" ])
    for ei,d in zip(experimentsInstances,dirs):
        training,testing, weka, table=ei
        bar= d+"\\barinelOptA.csv"
        reader= csv.reader(open(bar,"r"))
        i=0
        for r in reader:
            i=i+1
            if i==1:
                continue
            linesWrite.append([training,testing]+r)
    with open(outPath+"\\barinelOptA.csv", 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(linesWrite)
    linesWrite=[]
    linesWrite.append(["training","testing", "algorithm","pBug","pValid","times","precision_avg","recall_avg","steps","tests_avg","files_avg","bugged_avg","initials","tests" ])
    for ei,d in zip(experimentsInstances,dirs):
        training,testing, weka, table=ei
        t="all"
        bar= d+"plannerRes"+t+".csv"
        reader= csv.reader(open(bar,"r"))
        i=0
        for r in reader:
            i=i+1
            if i==1:
                continue
            linesWrite.append([training,testing]+r)
    with open(outPath+"\\plannerRes.csv", 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(linesWrite)









def Old_main():
    dbPath="C:\\GitHub\\agent\\testsBugs.db"
    outPath="C:\\GitHub\\experiments\\check4\\"
    #copyPath="C:\\GitHub\\experiments\\WekaNet\\"
    copyPath="C:\\GitHub\\experiments\\ManyPacks6\\"
    copy=False
    packsPath="C:\\GitHub\\agent\\PacksFiltered.txt"
    wekaBase="C:\\GitHub\\experiments\\"
    wekaAlgs=["weka.classifiers.trees.J48" ,"weka.classifiers.bayes.NaiveBayes" , "weka.classifiers.trees.RandomForest" ]
    wekaAlgs=[ "weka.classifiers.trees.RandomForest" ]
    wekaAnsArr=[(wekaBase+w+"_Style2.csv",w) for w in wekaAlgs] #all
    wekaAnsArr=[(wekaBase+w+"_OneBug2.csv",w) for w in wekaAlgs] #most
    wekaAnsArr=[(wekaBase+w+"_CleanAll.csv",w) for w in wekaAlgs] #all+
    wekaAnsArr=[(wekaBase+w+"_Most_Clean.csv",w) for w in wekaAlgs] #most+
    wekaAnsArr=[(wekaBase+"CDT_8_1_2_AllFiles_1_Only.csv",w) for w in wekaAlgs] #most+
    numOfExperiments=10
    buggedTable="buggedFiles"
    #buggedTable="buggedFilesOne"
    #buggedTable="buggedFilesChecked"
    numOfPacks=1
    numOfrepeats=1
    numOfBugs=[2]
    times=[25,40,70,100,130]
    const=0.2
    minimalTests=100
    maximalTests=220
    buggedTestsChooser=10
    initialsFactor=0.1
    initialsChooser=0.5
    tresh=0.7
    pureSanity=True

    tresh=0.7
    outPath="C:\\GitHub\\experiments\\"+str("Ext")+"\\"
    o=outPath
    if not (os.path.isdir(o)):
        os.mkdir(o)
    dirStruct(outPath)
    #outPath,dbPath,packsPath,wekaBase,numOfExperiments,numOfBugs,times,const,minimalTests,maximalTests,initialsFactor,numOfPacks,buggedTestsChooser,initialsChooser,copy,copyPath,pureSanity
    #Most_All_Real(outPath,dbPath,packsPath,numOfExperiments,numOfBugs,times,const,minimalTests,maximalTests,wekaAnsArr,initialsFactor,numOfPacks,buggedTestsChooser,initialsChooser,copy,copyPath,pureSanity)
    numOfExperiments=MultyWekaAndSanity(outPath,dbPath,packsPath,numOfExperiments,numOfBugs,times,const,minimalTests,maximalTests,wekaAnsArr,initialsFactor,False,numOfPacks,buggedTestsChooser,initialsChooser,False,copy,copyPath,buggedTable,pureSanity)
    weka=True
    copySTMS(outPath)
    plannerRunSTMT="cmd /x /c \"c: & cd C:\\GitHub\\agent & java -jar planner150.jar %s %s %s %s \"" %(str(numOfrepeats),outPath+"\\planner\\",outPath+"plannerRecords\\",str(tresh))

    os.system(plannerRunSTMT)
    bat_ = "cmd.exe /X /C \"c: & cd  " + outPath + " & " + outPath + "barinelRun.bat\""
    os.system(bat_)
    exps=range(numOfExperiments+1)[1:]
    types=["all","normal","can't advance"]
    a=0
    for t in types:
        a=a+1
        results.planner_resultsMultyWekaAndSanity(outPath+"plannerRes"+t+".csv" , outPath+"plannerMEDRes"+t+".csv",outPath,numOfExperiments,t,weka,times,wekaAnsArr)
        #results.planner_recordes(outPath+"plannerRes"+t+".csv",outPath+"plannerMEDRes"+t+".csv",outPath+"\\plannerRecords\\",numOfExperiments,t,weka,exps)
    #results.resultsAllBarinel("%s\\barinelOptA.csv" % outPath,"%s\\barinelOptA2.csv" % outPath, "%s\\" % outPath,1,weka,numOfExperiments)
    results.resultsMultyWekaAndSanity("%s\\barinelOptA.csv" % outPath,"%s\\barinelOptA2.csv" % outPath, "%s\\" % outPath,1,numOfExperiments,times,wekaAnsArr)


def eclipse():
    dbPath="C:\\GitHub\\agent\\testsBugs.db"
    outPath="C:\\GitHub\\experiments\\E8\\"
    packsPath="C:\\GitHub\\agent\\PacksFiltered.txt"
    wekaBase="C:\\GitHub\\experiments\\wekOut\\"
    numOfExperiments=10
    numOfPacks=1
    numOfrepeats=1
    numOfBugs=[2]
    times=[25,40,70,100,130]
    const=0.2
    minimalTests=25
    maximalTests=220
    buggedTestsChooser=10
    initialsFactor=0.1
    initialsChooser=0.5
    tresh=0.7
    pureSanity=False
    if not (os.path.isdir(outPath)):
        os.mkdir(outPath)
    #Old_main()
    Most_All_Real(outPath,dbPath,packsPath,wekaBase,numOfExperiments,numOfBugs,times,const,minimalTests,maximalTests,initialsFactor,numOfPacks,buggedTestsChooser,initialsChooser,False,"",pureSanity)


def POI():
    dbPath="C:\projs\poi2Working\\testsBugs.db"
    outPath="C:\\GitHub\\experiments\\POI\\"
    packsPath="C:\projs\poiWorking\\POIpacks.txt"
    numOfExperiments=10
    numOfPacks=1
    numOfrepeats=1
    numOfBugs=[2]
    times=[25,40,70,100,130]
    #times=[10,20,30,40]
    const=0.2
    minimalTests=25
    maximalTests=220
    buggedTestsChooser=10
    initialsFactor=0.1
    initialsChooser=0.5
    tresh=0.7
    pureSanity=False
    copyPath="C:\\GitHub\\experiments\\POI50E2\\"
    for i in range(1):
        outPath="C:\\GitHub\\experiments\\PO8"+str(i)+"\\"
        copy=False
        o=outPath
        if not (os.path.isdir(o)):
            os.mkdir(o)
        bugs = allPackBugs(dbPath, 2  , packsPath,numOfExperiments,True,"buggedFiles")
        bugsPacks=[choosePackBug(bugs, 6,False,5,[])for x in range(numOfExperiments)]
        dirStruct(outPath)
        copySTMS(outPath)
        wekaAnsArr=[("C:\GitHub\weka\poi\\poiRF.csv","randomForest")]#+[(wekaBase+"weka.classifiers.trees.RandomForest_Style2.csv","prev")] #all
        RunAndResults(buggedTestsChooser, bugsPacks, const, copy, copyPath, outPath, dbPath, initialsChooser, initialsFactor,
                  maximalTests, minimalTests, numOfBugs, numOfExperiments, numOfPacks, packsPath, pureSanity, "buggedFiles" ,
                  times,  wekaAnsArr)


def POIMethods():
    dbPath="C:\projs\poi2Working\\testsBugsMethods.db"
    outPath="C:\\GitHub\\experiments\\POIMethods4\\"
    packsPath="C:\projs\poi2Working\\POIpacks14.txt"
    #statisticalInfoMethods(dbPath,packsPath)
    if not os.path.isfile(packsPath):
        packFileCreate(dbPath,1,-1,packsPath)
    numOfExperiments=10
    numOfPacks=1
    numOfrepeats=1
    numOfBugs=[2]
    times=[25,40,70,100,130]
    #times=[10,20,30,40]
    const=0.2
    minimalTests=25
    maximalTests=220
    buggedTestsChooser=10
    initialsFactor=0.1
    initialsChooser=0.5
    tresh=0.7
    pureSanity=False
    copyPath="C:\\GitHub\\experiments\\POI50E2\\"
    for i in range(5):
        copy=False
        outPath="C:\\GitHub\\experiments\\POIMethods12"+str(i)+"\\"
        o=outPath
        if not (os.path.isdir(o)):
            os.mkdir(o)
        #bugs = allPackBugs(dbPath, 2  , packsPath,numOfExperiments,True,"buggedFiles")
        bugs = allPackBugsMethods(dbPath, 1 , packsPath,numOfExperiments,True,"buggedMethods")
        bugsPacks=[choosePackBug(bugs, 20,False,15,[])for x in range(numOfExperiments)]
        dirStruct(outPath)
        copySTMS(outPath)
        wekaAnsArr=[("C:\projs\poi2Working\weka\selected\\weka.classifiers.bayes.NaiveBayes_AllFiles_3.csv","randomForest")]#+[(wekaBase+"weka.classifiers.trees.RandomForest_Style2.csv","prev")] #all
        RunAndResults(buggedTestsChooser, bugsPacks, const, copy, copyPath, outPath, dbPath, initialsChooser, initialsFactor,
                  maximalTests, minimalTests, numOfBugs, numOfExperiments, numOfPacks, packsPath, pureSanity, "buggedMethods" ,
                  times,  wekaAnsArr)


def RunExperiments(dbPath,outPath,packsPath,wekaPath,Unit,buggedType,utilsPath):
    print "RunExperiments"
    numOfExperiments=20
    numOfPacks=1
    times=[25,40,70,100,130, 180]
    const=0.05
    minimalTests=25
    maximalTests=250
    buggedTestsChooser=10
    initialsFactor=0.1
    initialsChooser=0.5
    tresh=0.7
    pureSanity=False
    table=""
    testTable=""
    if (Unit=="File"):
        testTable="testsFiles"
        if (buggedType=="All"):
            table="buggedFiles"
        if (buggedType=="Most"):
            table="buggedFilesMostModified"
    if (Unit=="method"):
        testTable="testsMethods"
        if (buggedType=="All"):
            table="buggedMethods"
        if (buggedType=="Most"):
            table="buggedMethodsMostModified"
    dirStruct(outPath)
    copySTMS(outPath,utilsPath)
    bugs = allPackBugs(dbPath, 1  , packsPath,numOfExperiments,True,table)
    bugsPacks=[choosePackBug(bugs, 2,False,10,[])for x in range(numOfExperiments)]
    wekaAnsArr=[(wekaPath,"randomForest")]#+[(wekaBase+"weka.classifiers.trees.RandomForest_Style2.csv","prev")] #all
    RunAndResults(buggedTestsChooser, bugsPacks, const, False, "", outPath, dbPath, initialsChooser, initialsFactor,
              maximalTests, minimalTests, [2], numOfExperiments, numOfPacks, packsPath, pureSanity, table ,
              times,  wekaAnsArr,testTable)

@utilsConf.marker_decorator(utilsConf.PACKS_FILE_MARKER)
def packFileCreate(dbpath, startInd, endInd,outPath):
    conn = sqlite3.connect(dbpath)
    conn.text_factory = str
    c = conn.cursor()
    lines=set()
    #wanted_files='select distinct name from haelsTfiles   order by name'
    wanted_files='select distinct fileName from buggedFiles   order by fileName'
    for row in c.execute(wanted_files):
        r=row[0]
        r=r.split("\\")
        #r=r[startInd:endInd]
        r=r[:-1]
        concat=[]
        for elem in r:
         concat.append(elem)
         lines.add("\\".join(concat))
        #r=r
        #lines.add("\\".join(r))
    f=open(outPath,"wb")
    writer=csv.writer(f)
    writer.writerows([[x] for x in list(lines)])
    f.close()
    ans=statisticalInfoMethods(dbpath,outPath)
    newLines=[]
    for row in ans:
        pack,a,b,c=row
        if a>0 and b>0 and c>0:
            newLines.append(pack)
    f=open(outPath,"wb")
    writer=csv.writer(f)
    writer.writerows([[x] for x in list(newLines)])
    f.close()



if __name__ == "__main__":
    RunExperiments(os.path.join(workingDir,"testsBugsMethods.db"), outPath,packsPath,outCsv,"method",buggedType)
    #RunExperiments("C:\projs\\antWorking\\testsBugs.db","C:\\GitHub\\experiments\\ant1\\","C:\projs\\antWorking\\antPacks.txt","C:\GitHub\weka\\ant\\antRF.csv")
    #packFileCreate("C:\projs\\antWorking\\dbAdd\\ANT_182.db",3,-2,"C:\projs\\antWorking\\antPacks.txt")
    exit()


    dbPath="C:\\GitHub\\agent\\testsBugs.db"
    outPath="C:\\GitHub\\experiments\\POI\\"
    packsPath="C:\\GitHub\\agent\\PacksFiltered.txt"
    wekaBase="C:\\GitHub\\experiments\\wekOut\\"


    dbPath="C:\projs\poiWorking\\testsBugs3.db"
    outPath="C:\\GitHub\\experiments\\POI\\"
    packsPath="C:\projs\poiWorking\\POIpacks.txt"
    numOfExperiments=50
    numOfPacks=1
    numOfrepeats=1
    numOfBugs=[2]
    times=[25,40,70,100,130]
    const=0.2
    minimalTests=25
    maximalTests=220
    buggedTestsChooser=10
    initialsFactor=0.1
    initialsChooser=0.5
    tresh=0.7
    pureSanity=True
    copyPath="C:\\GitHub\\experiments\\TenPure1\\"
    for i in range(5):
        outPath="C:\\GitHub\\experiments\\POI50E"+str(i)+"\\"
        copy=False
        o=outPath
        if not (os.path.isdir(o)):
            os.mkdir(o)
        #Old_main()
        #Most_All_Real(outPath,dbPath,packsPath,wekaBase,numOfExperiments,numOfBugs,times,const,minimalTests,maximalTests,initialsFactor,numOfPacks,buggedTestsChooser,initialsChooser,copy,copyPath,pureSanity)
        #statisticalInfo(dbPath,packsPath)
        #exit()
        bugs = allPackBugs(dbPath, 4  , packsPath,numOfExperiments,True,"buggedFiles")
        bugsPacks=[choosePackBug(bugs, 15,False,8,[])for x in range(numOfExperiments)]

        dirStruct(outPath)
        copySTMS(outPath)
        wekaAnsArr=[(wekaBase+"CDT_8_1_2_AllFiles_1_Only.csv","f")]#+[(wekaBase+"weka.classifiers.trees.RandomForest_Style2.csv","prev")] #all
        wekaAnsArr=[("C:\GitHub\weka\m29\\poiRF.csv","randomForest")]#+[(wekaBase+"weka.classifiers.trees.RandomForest_Style2.csv","prev")] #all
        RunAndResults(buggedTestsChooser, bugsPacks, const, copy, copyPath, outPath, dbPath, initialsChooser, initialsFactor,
                  maximalTests, minimalTests, numOfBugs, numOfExperiments, numOfPacks, packsPath, pureSanity, "buggedFiles" ,
                  times,  wekaAnsArr)