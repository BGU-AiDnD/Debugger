__author__ = 'amir'

def func(s):
	f=open(s,"r")
	l=f.readlines()
	return set(l[11].split(","))


def conesOptimize2(allFiles, allTests,outcomes, allBugs,priors,testsChoosedNames):
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
    print "toCheck", to_check
    print "to_check_valids", to_check_valids
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


    print "toCheck", to_check
    print "to_check_valids", to_check_valids
    print "distinctFiles", distinctFiles
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
    if(priors!=[]):
        priors=[priors[i] for i in distinctFiles]
    newFiles=range(len(distinctFiles))
    return newFiles, testsRet,newOutcomes,newBugs,priors,testsChoosedNamesNew



o="C:\GitHub\weka\m5\pca2\\"
outL=[]
for i in [16,26,38,59,68,78,94,104]:
    lines=open(o+str(i)+"_testing.txt","r").readlines()
    ind=lines.index("=== Detailed Accuracy By Class ===\n")+3
    outL.append(str(i)+"\n")
    outL.extend(lines[ind:ind+4])

print "".join(outL)
