__author__ = 'Amir-pc'

import os
import csv
import sqlite3
import Agent.results
import Agent.experiments


def allFiles(path):
    acc=[]
    pathLen=len(path)+1 # one for the \
    for root, dirs, files in os.walk(path): # Walk directory tree
        for f in files:
            path_join = "".join(list(os.path.join(root, f))[pathLen:])
            acc=acc+[path_join]
    return acc

def conesOptimize(allFiles, allTests,outcomes, allBugs):
    to_check=[]
    newBugs = []
    newTests = []
    newOutcomes=[]
    distinctFiles=[]
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
        ind=ind+1

    newBugs=[distinctFiles.index(i) for i in allBugs if i in distinctFiles]
    newFiles=range(len(distinctFiles))
    return newFiles, testsRet,newOutcomes,newBugs

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

def exportBarinel(out,pBug,pValid,allBugs,allFiles,allTests,outcomes):
    lines=[]
    priors=[]
    for f in allFiles:
        if(f in allBugs):
            priors.append(pBug)
        else:
            priors.append(pValid)
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


def optimizeVeyCommonFiles(allFiles, allTests,outcomes, allBugs):
    newFiles=[]
    newBugs = []
    newTests = []
    newOutcomes=[]
    treshold=0.8*len(allTests)

    for i in allFiles:
        count=0
        ind=0
        for elem in allTests:
            if elem[i] == "1":
                count=count+1
            ind=ind+1
        if count <= treshold:
            newFiles.append(i)
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
        ind=ind+1

    newBugs=[newFiles.index(i) for i in newBugs]
    newFiles=range(len(newFiles))
    return newFiles, testsRet,newOutcomes,newBugs



def exportBugs_Files(outbugs_Files,allBugs,allFiles):
    bugsInds=[]
    for b in allBugs:
        if (b in allFiles):
            bugsInds.append(allFiles.index(b))
    with open(outbugs_Files, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows([["Files"],range(len(allFiles)),["Bugged"],bugsInds] )


def sfd():
    global outPath, allFiles, allTests, outcomes, allBugs, exp, file, readBarinelF, i, pBug, j, pValid, k, file1, outBarinel, outbugs_Files
    outPath = "C:\GitHub\\agent\\experimentsSortedBug"
    allFiles, allTests, outcomes, allBugs = readBarinel("C:\GitHub\\agent\\0.2_0.0_0.csv", 0.21)
    allFiles, allTests, outcomes, allBugs = optimizeVeyCommonFiles(allFiles, allTests, outcomes, allBugs)
    exportBarinel("C:\GitHub\\agent\\OPT.csv", 0.41, 0.11, allBugs, allFiles, allTests, outcomes)
    exit()
    for exp in range(10):
        file = str(0.1) + "_" + str(0.0) + "_" + str(exp)
        readBarinelF = outPath + "\\barinel\\" + file + ".csv"
        if (not os.path.isfile(readBarinelF)):
            continue
        allFiles, allTests, outcomes, allBugs = readBarinel(readBarinelF, 0.11)
        allFiles, allTests, outcomes, allBugs = conesOptimize(allFiles, allTests, outcomes, allBugs)
        for i in range(11):
            pBug = i / 10.0
            for j in range(i + 1):  # pValid < pBug
                pValid = j / 10.0
                for k in range(10):
                    file = str(pBug) + "_" + str(pValid) + "_" + str(exp)
                    file1 = str(exp)
                    readBarinelF = outPath + "\\barinel\\" + file + ".csv"
                    outBarinel = outPath + "\\barinelOpt\\" + file + ".csv"
                    outbugs_Files = outPath + "\\Opt\\" + file1 + ".txt"
                    if (not os.path.isfile(readBarinelF)):
                        continue
                    if (pValid == 0):
                        exportBugs_Files(outbugs_Files, allBugs, allFiles)
                    exportBarinel(outBarinel, pBug + 0.01, pValid + 0.01, allBugs, allFiles, allTests, outcomes)


#files=allFiles("C:\Users\Amir-pc\Documents\GitHub\org.eclipse.cdt")

def pathToPack(path):
    name=path.split(".java")[0]
    name=name.split("\\org\\")[1]
    name="org."+name
    name=name.replace("\\",".")
    return name
    '''
    print (files)
    print len(files)
    '''
    dbpath="C:\\GitHub\\vers\\db2\\CDT_8_1_24.db"
    dbpath2="C:\\GitHub\\agent\\testsBugs.db"
    commonFiles=[]
    res=[]
    res2=[]
    conn = sqlite3.connect(dbpath)
    conn.text_factory = str
    c = conn.cursor()
    for x in c.execute(' select distinct name from haelsTfiles order by name'):
        res.append(pathToPack(x[0]))
    conn.close()

    conn = sqlite3.connect(dbpath2)
    conn.text_factory = str
    c = conn.cursor()
    for x in c.execute(' select distinct fileName from testsFiles order by fileName'):
        res2.append(x[0])
    conn.close()
    print len(res2)
    x=0
    #print res[0]
    for r in res2:
        if( not r in res):
            #print r
            x=x+1
    print x

    for r in res:
        print r


if __name__ == "__main__":
    sizes=[30,40,70]
    for s in sizes:
        outPath="C:\\GitHub\\agent\\learner\\exWekaCheck38"
        o = outPath + "\\out"+str(s)+"\\"
        if not (os.path.isdir(o)):
            os.mkdir(o)
        o = outPath + "\\bugs_Files"+str(s)+"\\"
        if not (os.path.isdir(o)):
            os.mkdir(o)
        outDir = outPath + "\\barinel" +str(s)+"\\"
        if not (os.path.isdir(outDir)):
            os.mkdir(outDir)
        o = outPath + "\\outW"+str(s)+"\\"
        if not (os.path.isdir(o)):
            os.mkdir(o)
        outDirW = outPath + "\\barinelW" +str(s)+"\\"
        if not (os.path.isdir(outDirW)):
            os.mkdir(outDirW)
        experiments=57
        for exp in range(experiments):
            if exp==0:
                continue
            allFiles, allTests,outcomes, bugs,priors=readBarinel(outPath+"\\barinel\\weka_"+str(exp)+".csv")
            allTests=allTests[:s+1]
            outcomes=outcomes[:s+1]
            bug_f=outPath+"\\bugs_Files\\"+str(exp)+".txt"
            BugsIds, allBugged, pack, testsCount, files = Agent.results.readBugFile(bug_f)
            bugsCount=len(allBugged)
            allBugged=[int(x) for x in allBugged]
            files=[int(f) for f in files]
            testsChoosedNames=["amir" for t in allTests]
            files, allTests, outcomes, allBugged,priors,testsChoosedNames = Agent.experiments.optimizeAll(files, allTests, outcomes, allBugged,priors,testsChoosedNames)
            files, allTests, outcomes, allBugged,priors,testsChoosedNames = Agent.experiments.conesOptimize2(files, allTests, outcomes, allBugged,priors,testsChoosedNames)
            files, allTests, outcomes, allBugged,priors,testsChoosedNames = Agent.experiments.optimizeVeyCommonFiles(files, allTests, outcomes, allBugged,priors,testsChoosedNames)
            file =  str(exp)
            diff=bugsCount-len(allBugged)
            buggedAdd=[-1-x for x in range(diff)]
            #buggedAdd=[]
            outbugs_Files = outPath+"\\bugs_Files"+str(s)+"\\" + str(exp) + ".txt"
            Agent.experiments.exportBugs_Files(outbugs_Files,allBugged,files,[],len(allTests),pack,testsChoosedNames,buggedAdd)
            continue
            outBarinel = outPath+"\\barinelW"+str(s)+"\\weka_" + file + ".csv"
            Agent.experiments.exportBarinel(outBarinel,priors,allBugged,allFiles,allTests,outcomes)
            outBarinel = outPath+"\\barinelW"+str(s)+"\\uniform_" + file + ".csv"
            priors=[0.1 for p in priors]
            Agent.experiments.exportBarinel(outBarinel,priors,allBugged,allFiles,allTests,outcomes)
            continue
            for i in range(11):
                            pBug = i / 10.0
                            for j in range(i+1):  # pValid < pBug
                                pValid = j / 10.0
                                file = str(pBug) + "_" + str(pValid) + "_" + str(exp)
                                outBarinel = outDir+"\\" + file + ".csv"
                                priors=Agent.experiments.priorsByPbugPvalid(allBugged, files, pBug+0.01, pValid+0.01)
                                Agent.experiments.exportBarinel(outBarinel,priors,allBugged,files,allTests,outcomes)
    print( len(files), len(tests) ,len(bugs))