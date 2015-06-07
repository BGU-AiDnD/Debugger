__author__ = 'amir'

import weka.checkReport
import os


def commitAnalyze(Path,commit_id,CodeDir):
    if not os.path.isfile(Path+"\\checkBef.xml"):
        print Path
    if not os.path.isfile(Path+"\\checkAfter.xml"):
        print Path
    before = weka.checkReport.fileRead(Path+"\\checkBef.xml",-1,True,CodeDir)
    after = weka.checkReport.fileRead(Path+"\\checkAfter.xml",-1,True,CodeDir)
    befDict={}
    for x in before:
       n=x[0].split("\\")[-1]
       n=n.replace("_","\\")
       befDict[n]=x
    afDict={}
    for x in after:
       n=x[0].split("\\")[-1]
       n=n.replace("_","\\")
       afDict[n]=x
    names=list(set(befDict.keys()+afDict.keys()))
    ans=[]
    for n in names:
        fileP=[commit_id,n]
        fileBef=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        if n in befDict:
            fileBef=befDict[n][1:]
        fileAf=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        if n in afDict:
            fileAf=afDict[n][1:]
        for i in range(len(fileBef)):
            fileP.append(fileAf[i]-fileBef[i])
        t=tuple(fileP)
        ans=ans+[t]
    return ans

#for p in paths:
#    x=commitAnalyze(p,'076d4c7899608c0f2ce711a725d44d3a9725cec1')
#    for a in x:
#        if len(a)!=83:
#            print len(a),p,a
