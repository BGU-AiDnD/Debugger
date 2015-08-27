__author__ = 'User'

import re
import numpy
import datetime
import time
import glob
import commsSpaces
from collections import Counter

#git blame --show-stats --score-debug -p --line-porcelain -l core\org.eclipse.cdt.core.win32\src\org\eclipse\cdt\internal\core\win32\ProcessList.java  >blame.txt

def oneRecordParse(lines):
    first=lines[0].split(' ')
    commitId=first[0]
    group=0
    if len(first)==4:
        group=int(first[3])
    committer=' '.join(lines[5].split(' ')[1:])
    committerTime=datetime.datetime.fromtimestamp(float(lines[7].split(' ')[1]))#.strftime('%Y-%m-%d %H:%M:%S')
    committerTime=time.mktime(committerTime.timetuple())
    #committerTime=time.mktime(time.strptime(lines[7].split(' ')[1], "%Y-%m-%d %H:%M:%S"))
    previous=''
    if lines[-3].startswith("previous "):
        previous=lines[-3].split(' ')[1]
    return commitId,committer,committerTime,previous,group


def stamp(x):
    if numpy.isnan(x):
        datetime.date(2008, 6, 24)
    return datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')

def monthlyDate(x):
    d=datetime.datetime.fromtimestamp(x)
    d=d.replace(hour=0, minute=0,second=0,day=1)
    return time.mktime(d.timetuple())

def most_common(lst):
    return max(set(lst), key=lst.count)

def listStats(lst,isTime):
    counts= Counter(lst)
    l=len(lst)+0.0
    countsPre=dict([(x,counts[x]/l) for x in counts ])
    #print countsPre
    p01= sum([countsPre[x] for x in countsPre if countsPre[x]<=0.1])
    p02= sum([countsPre[x] for x in countsPre if countsPre[x]<=0.2])
    p05= sum([countsPre[x] for x in countsPre if countsPre[x]<=0.5])
    mx=0
    if len(countsPre)>0:
        mx= max([countsPre[x] for x in countsPre])
    if isTime:
        if lst==[]:
            return 0, 0, 0, 0, 0, 0,0,0,0,0
        mean = stamp(numpy.mean(lst))
        median = stamp(numpy.median(lst))
        numpy_var = numpy.var(lst)
        max_lst = stamp(maxCheck(lst))
        min_lst = stamp(minCheck(lst))
        return len(lst), mean, median, numpy_var, max_lst, min_lst,p01,p02,p05,mx
    return len(lst),numpy.mean(lst),numpy.median(lst),numpy.var(lst),maxCheck(lst),minCheck(lst),p01,p02,p05,mx

def commitersFeatures(lst):
    counts= Counter(lst)
    l=len(lst)+0.0
    countsPre=dict([(x,counts[x]/l) for x in counts ])
    #print countsPre
    p01= sum([countsPre[x] for x in countsPre if countsPre[x]<=0.1])
    p02= sum([countsPre[x] for x in countsPre if countsPre[x]<=0.2])
    p05= sum([countsPre[x] for x in countsPre if countsPre[x]<=0.5])
    mx= maxCheck([countsPre[x] for x in countsPre])
    return len(lst),p01,p02,p05,mx

def countsLines( times):
    counts = Counter(times)
    l = len(times) + 0.0
    countsPre = dict([(x, counts[x] / l) for x in counts])
    ones = len([x for x in counts if counts[x] == 1])
    twos = len([x for x in counts if counts[x] == 2])
    less5 = len([x for x in counts if counts[x] <= 5])
    less10 = len([x for x in counts if counts[x] <= 10])
    return  ones, twos,less5,less10

def intCheck(s):
    if s.isdigit():
        return int(s)
    return 0

def fileParse(file, prevVersionCommitterTime):
    prevVersionCommitterTime=time.mktime(time.strptime(prevVersionCommitterTime,'%Y-%m-%d %H:%M:%S'))
    f=open(file,"r")
    lines=[l.split('\n')[0] for l in  f.readlines()]
    if len(lines)==0:
        return 0
    commsFile=file.replace("\\blame\\","\\commentsSpaces\\")+".txt"
    print commsFile
    comms,spaces=commsSpaces.read(commsFile)
    discard=comms+spaces
    inds=[0] # find where line start with "filename " +1
    ind=0
    name=''
    for l in lines:
        if not None==re.match('^filename ',l):
                name=l.split(' ')[1]
                inds.append(ind+2)
        ind=ind+1
    commits=[]
    commitsApproved=[]
    committersApproved={}
    committers={}
    times=[]
    timesApproved=[]
    previousComms=[]
    previousCommsApproved=[]

    groups=[]
    for i in range(len(inds)-1):
        commitId,committer,committerTime,previous,group= oneRecordParse(lines[inds[i]:inds[i+1]])
        commits.append(commitId)
        if not committer in committers:
            committers[committer]=1
        else:
            committers[committer]=1+committers[committer]
        times.append(committerTime)
        previousComms.append(previous)
        if group!=0:
            groups.append(group)
        if i not in discard:
            commitsApproved.append(commitId)
            if not committer in committersApproved:
                committersApproved[committer]=1
            else:
                committersApproved[committer]=1+committersApproved[committer]
            timesApproved.append(committerTime)
            previousCommsApproved.append(previous)
    numBlobs=intCheck(lines[-3].split(' ')[-1])
    numPatchs=intCheck(lines[-2].split(' ')[-1])
    numCommits=intCheck(lines[-1].split(' ')[-1])
    comms = set([c for c in times if c>prevVersionCommitterTime])
    commsApproved = set([c for c in timesApproved if c>prevVersionCommitterTime])
    difftimes=list(set(times))
    difftimesApproved=list(set(timesApproved))
    #print "times",times
    #print "months",[monthlyDate(x) for x in times]
    groupsApproved=[]
    s=""
    if len(commitsApproved)>0:
        s=commitsApproved[0]
    countS=1
    for i in range(len(commitsApproved))[1:]:
        if s==commitsApproved[i]:
            countS=countS+1
        else:
            groupsApproved.append(countS)
            countS=1
            s=commitsApproved[i]
    groupsApproved.append(countS)
    #return name,len(set(commits)),len(comms),len(groups),len(set(committers)),stamp(numpy.mean(times)),stamp(numpy.median(times)),stamp(max(times)),stamp(min(times)),numpy.var(times),stamp(most_common(times)),max(times)- min(times),stamp(numpy.mean(difftimes)),stamp(numpy.median(difftimes)),numpy.var(difftimes),
    ret= [name,len(set(commits)),len(comms),len(set(commitsApproved)),len(commsApproved),numBlobs,numPatchs,numCommits]
    ret.extend(list(listStats(times,True))+[maxCheck(times)- minCheck(times)])
    ret.extend(list(countsLines( times)))
    ret.extend(list(listStats(difftimes,True))+[maxCheck(difftimes)- minCheck(difftimes)])
    ret.extend(list(countsLines( difftimes)))
    ret.extend(list(commitersFeatures( committers)))
    ret.extend(list(listStats(timesApproved,True))+[maxCheck(timesApproved) - minCheck(timesApproved)])
    ret.extend(list(countsLines( timesApproved)))
    ret.extend(list(listStats(difftimesApproved,True))+[maxCheck(difftimesApproved)- minCheck(difftimesApproved)])
    ret.extend(list(countsLines( difftimesApproved)))
    
    ret.extend(list(commitersFeatures( committersApproved)))
    ret.extend(list(listStats(groups,False)))
    ret.extend(list(listStats(groupsApproved,False)))
    return tuple(ret)

def maxCheck(x):
    m=0
    if x!=[]:
        m=max(x)
    return m
def minCheck(x):
    m=0
    if x!=[]:
        m=min(x)
    return m
def blameBuild(blamePath,prevVersionCommitterTime,max):
    docs=[]
    lst= glob.glob(blamePath+"/*.java")
    i=0
    for doc in lst:
        print doc
        if (i==max):
            break
        i=i+1
        x=fileParse(doc,prevVersionCommitterTime)
        if x!=0:
            docs.append(x)
    return docs

if __name__ == "__main__":
    prevVersionCommitterTime='2012-06-10 23:45:00'
    f="C:\projs\\ant11Working\\vers\ANT_170_B1\\blame\Junk9.java"
    print f
    fileParse(f,prevVersionCommitterTime)
