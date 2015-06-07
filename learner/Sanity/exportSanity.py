__author__ = 'amir'


import random
import csv
import os
import math
import Agent.results
import winsound

def optimize(inds_bef, mat, priors):
    inds=[]
    newPriors = []
    newMat = [[] for t in mat]
    for i in range(len(mat[0])-1):
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


def SanityProbs(pBug,pFix, priorProbs):
    probs=[]
    for i in priorProbs:
        if i==1:
            probs=probs+[pBug]
        else:
            probs=probs+[pFix]
    return probs

def SanityBugs(nComps,nPacks,threshBug):
    pBug=1
    pFix=0
    probs=[]
    bugs=[]
    for i in range(nComps):
        rand= random.uniform(0,1)
        if (rand <threshBug):
            probs=probs+[pBug]
            bugs=bugs+[i]
        else:
            probs=probs+[pFix]
    return (probs,bugs)

def SanityMatrix(nTests,nComps,nPacks,threshCover,const, bugs,packSize, packCloseness=0.85):
    mat=[]
    for i in range(nTests):
        test=[]
        pss=1
        for i in range(nPacks):
            rand= random.uniform(0,1)
            if( rand < threshCover):
                for j in range(packSize):
                    rand= random.uniform(0,1)
                    if( rand < packCloseness):
                        test=test+["1"]
                        if( i* packSize +j in bugs):
                            pss=pss*const
                    else:
                        test=test+["0"]
            else:
                for j in range(packSize):
                    test=test+["0"]
        print len(test)
        threshFail=random.uniform(0,1)
        if( pss >= threshFail):
            test=test+["0"]
        else:
            test=test+["1"]
        mat=mat+[test]
    return mat

def used_elements(tm,O):
    new_tm=[i[:len(i)-1] for i in tm]
    inds=[]
    for i in range(len(new_tm[0])):
        for j in new_tm:
            if j[i]=='1':
                    inds=inds+[i]
    inds=list(set(inds))
    with open(O, 'wb') as f:
        f.write(str(inds))
    return inds


def TestDetails(tm):
    ans=[]
    names=[]
    for test in tm:
        trace=[]
        for i in range(len(test)-1):
            if test[i]=="1":
                trace=trace+[i]
        toAdd = [tm.index(test), trace, trace, test[len(test) - 1]]
        ans=ans+ [toAdd]
        names=names+[[toAdd[0]]]
    return ans,names

def exportSanityPlanner( Out,  pBug,pValid,tm,priorProbs,Bugs):
    wek =SanityProbs(pBug,pValid,priorProbs)
    #tm_bef=SanityMatrix(nTests,nComps,threshCover,threshFail,const,yes_bef)
    dets,names=TestDetails(tm)
    rows=[["[Priors]"]]+ [[wek]]
    rows=rows+[ ["[Bugs]"]]+ [[bug] for bug in Bugs]+ [["[InitialTests]"]]+names[0:150]+ [["[TestDetails]"]]+dets
    with open(Out, 'wb') as f:
        writer = csv.writer(f,delimiter=";")
        writer.writerows(rows)

def exportSanityBarinel(Out,  pBug,pValid,tm,priorProbs,Bugs):
    priors =SanityProbs(pBug,pValid,priorProbs)
    #tm_bef=SanityMatrix(nTests,nComps,threshCover,threshFail,const,yes_bef)
    mat=[priors]+tm
    rows=mat
    with open(Out, 'wb') as f:
        writer = csv.writer(f,delimiter=",")
        writer.writerows(rows)

def exportBugsFiles(outbugs_Files, filesCount,Bugs):
    with open(outbugs_Files, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows([["Files"],range(filesCount),["Bugged"],Bugs] )


def exportAll(outDir,nTests,nPacks,threshCover,const,threshBug,experiments,packSize,packCloseness):
    #packSize=5

    nComps=packSize*nPacks
    bugsFiles = outDir+"bugs_Files\\"
    if not (os.path.isdir(outDir)):
        os.mkdir(outDir)
    if not (os.path.isdir(bugsFiles)):
        os.mkdir(bugsFiles)
    barinelDir = outDir + "barinel\\"
    if not (os.path.isdir(barinelDir)):
        os.mkdir(barinelDir)
    outDir = outDir + "out\\"
    if not (os.path.isdir(outDir)):
        os.mkdir(outDir)
    probsBugs=[]
    mats=[]

    for m in range(experiments):
        proBug=SanityBugs(nComps,nPacks,threshBug)
        tm=SanityMatrix(nTests,nComps,nPacks,threshCover,const,proBug[1],packSize,packCloseness)
        inds_bef=range(len(proBug[0]))
        inds, tm, newP = optimize( inds_bef, tm, proBug[0])
        #inds, tm, newP =  inds_bef, tm, proBug[0]
        proBug = newP,proBug[1]
        bugged=[]
        for y in proBug[1]:
         if y in inds:
             bugged=bugged+[inds.index(y)]
        proBug=proBug[0],bugged
        probsBugs=probsBugs+[proBug]
        mats=mats+[tm]
        bus_files_out=bugsFiles+str(m)+ ".txt"
       # print tm
        if(len(tm)==0):
            continue
        l=len(tm[0])
        exportBugsFiles(bus_files_out ,l,proBug[1])

    for i in range(11):
        pBug = i / 10.0
        for j in range(i+1):  # pValid < pBug
            pValid = j / 10.0
            for k in range(experiments):
                file = str(pBug) + "_" + str(pValid) + "_" + str(k)
                out = barinelDir + file + ".csv"

                #exportSanityPlanner(out,pBug+0.01,pValid+0.01,mats[k],probsBugs[k][0],probsBugs[k][1])
                exportSanityBarinel(out,pBug+0.01,pValid+0.01,mats[k],probsBugs[k][0],probsBugs[k][1])



def get_diag(diagFile):
    diags=[]
    probs=[]
    with open(diagFile,"r") as f:
        reader =csv.reader(f)
        for i in reader:
            diags.append(i[:len(i)-2])
            probs.append(i[len(i)-1])
    return  (diags[:1],probs[:1])

def get_used(usedFile):
    sen=open(usedFile).readlines()
    sen1=sen[0].split()
    sen=sen1[1:(len(sen1)-1)]
    ans=[]
    for s in sen1:
        if '[' in s:
            s=s.split('[')[1]
        if ',' in s:
            s=s.split(',')[0]
        if ']' in s:
            s=s.split(']')[0]
        ans=ans+[s]
    return ans

def yes_inds(fil):
    with open(fil, 'r') as f:
        reader = csv.reader(f)
        return [i for i in reader]

def resultsOne(usedFile, yesFile,DiagFile):
    used = get_used(usedFile)
    yes=yes_inds(yesFile)
    no=[str(i2) for i2 in range(len(used)) if str(i2) not in yes]
    used_no= [ttt for ttt in used if ttt in no]
    used_yes=[ttt for ttt in used if ttt in yes]
    diag,prob=get_diag(DiagFile)
    for dg,pr,orde in zip(diag,prob,[i3+1 for i3 in range(len(diag))]):
        fp=len([i1 for i1 in dg if i1 in used_no])
        fn=len([i1 for i1 in used_yes if i1 not in dg])
        tp=len([i1 for i1 in dg if i1 in used_yes])
        tn=len([i1 for i1 in used_no if i1 not in dg])
        if((tp+fp)==0):
            accur="undef"
        else:
            accur=(tp+0.0)/float(tp+fp)
            accur=accur*float(pr)
        if((tp+fn)==0):
            recall="undef"
        else:
            recall=tp/float(tp+fn)
            recall=recall*float(pr)
        r=[dg,pr,fp,fn,tp,tn,accur,recall]
        return r





def resultsAll(outputFile):
    dirI = "C:\\GitHub\\Sanity\\mats\\"
    yesDir = dirI + "yes\\"
    usedDir = dirI + "used\\"
    output=[]
    for i in range(10):
        pBug = i / 10.0
        for j in range(10):  # pValid < pBug
            if ( i <= j):
                break
            pValid = j / 10.0
            acc_avg=0
            acc_count=0
            for k in range(10):
                file = str(pBug) + "_" + str(pValid) + "_" + str(k)
                yes = yesDir + file + ".txt"
                used = usedDir + file + ".txt"
                DiagFile = dirI +"out\\DIFG_check_"+ file + ".txt.csv"
                #print(DiagFile)
                dg,pr,fp,fn,tp,tn,accur,recall=resultsOne(used, yes,DiagFile)
                if(not math.isnan(accur)):
                    print accur
                    acc_count=acc_count+1
                    acc_avg=acc_avg+accur
            acc_avg=acc_avg/acc_count
            output=output+[[pBug,pValid,acc_avg]]
    with open(outputFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(output)

#def exportDiagnoser():


def recordsOne(i, j, k,dir):
    lines=[]
    #dir="C:\Users\\amir\workspace\Program_Diagnoser\\resultsMore\\records\\"
    file=str(i) + "_" + str(j) + "_" + str(k)+".txt"+".csv"
    expr=dir+file
    with open(expr,"r") as f:
        reader =csv.reader(f)
        lines=[l for l in reader]
        #print(lines)
    precision_avg = 0
    recall_avg = 0
    steps_avg = 0
    ind=0
    for l in lines:
        if(l[10]=="normal"):
            ind=ind+1
            precision_avg = precision_avg + float(l[7])
            recall_avg = recall_avg + float(l[6])
            steps_avg = steps_avg + float(l[8])
    ln=ind
    if (ind==0):
        return 0,0,0
    recall_avg=recall_avg/ln
    precision_avg=precision_avg/ln
    steps_avg=steps_avg/ln
    return precision_avg, recall_avg,steps_avg


def records_i_j(i, j,dir):
    precision_avg = 0
    recall_avg = 0
    steps_avg = 0
    for k in range(10):
        precision, recall,steps = recordsOne(i, j, k,dir)
        precision_avg=precision_avg+precision
        recall_avg=recall_avg+recall
        steps_avg=steps_avg+steps
    return precision_avg/10.0, recall_avg/10.0,steps_avg/10.0


def experiments_recordes( outputFile,dir):
    out_lines=[]
    for i in range(10):
        pBug = i / 10.0
        for j in range(10):  # pValid < pBug
            if ( i <= j):
                break
            pValid = j / 10.0
            precision_avg, recall_avg,steps_avg = records_i_j(pBug, pValid,dir)
            out_lines=out_lines+[[pBug,pValid,precision_avg,recall_avg,steps_avg]]
    with open(outputFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(out_lines)


dir="C:\\Users\\amir\\workspace\\Program_Diagnoser\\results\\records\\"
outFile="C:\\GitHub\\agent\\experimentsPacks3\\planner.csv"
experiments_recordes(outFile,dir)



exit()
BaseworkingPlace = "C:\GitHub\\Sanity\\Barinel2\\"
nTests = 200 # 500 fine
nPacks = 40
packSize=1 #3 fine
const = 0.2  #
threshBug = 0.1  # C for barinel
threshCover=0.2  # r for barinel
experiments=5
packCloseness=1
res_tresh = 1
''' Nice res
nTests = 200 # 500 fine
nPacks = 40
packSize=1 #3 fine
const = 0.2  #
threshBug = 0.2  # C for barinel
threshCover=0.2  # r for barinel
experiments=5
packCloseness=1
res_tresh = 1
'''
exportAll(BaseworkingPlace,nTests,nPacks,threshCover,const,threshBug,experiments,packSize,packCloseness)

bat_ = "cmd.exe /X /C \"c: & cd  " + BaseworkingPlace + " & " + BaseworkingPlace + "barinelRun.bat\""
os.system(bat_)
for i in range(1):
    acc=0+ float(i)/10
    path=BaseworkingPlace+"AA"+str(acc)+".csv"
    Agent.results.resultsAllBarinel(path,"%sbarinelOptA2.csv" % BaseworkingPlace,  BaseworkingPlace, res_tresh,experiments)
winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
exit()


for j in range(10):
    threshCover=1+ j/10.0
    for i in range(1):
        workingPlace=BaseworkingPlace+str('packSize')
        if(not os.path.isdir(workingPlace)):
            os.mkdir(workingPlace)
        workingPlace=workingPlace+"\\"+str(j)
        if(not os.path.isdir(workingPlace)):
            os.mkdir(workingPlace)
        workingPlace=workingPlace+"\\"
        exportAll(workingPlace,nTests,nPacks,threshCover,const,threshBug,experiments,packSize,packCloseness)
        CopyStatement = "cmd /x /c \"c: & copy C:\\GitHub\\Sanity\\Barinel2\\barinelRun.bat %sbarinelRun.bat & copy C:\\GitHub\\Sanity\\Barinel2\\Tom.jar %sTom.jar\"" % (
            workingPlace, workingPlace)
        os.system(CopyStatement)
        bat_ = "cmd.exe /X /C \"c: & cd  " + workingPlace + " & " + workingPlace + "barinelRun.bat\""
        os.system(bat_)
        path=BaseworkingPlace+"j="+str(j)+".csv"
        Agent.results.resultsAllBarinel(path,"%sbarinelOptA2.csv" % workingPlace,  workingPlace,0.75,experiments)
winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
#resultsAllBarinel("C:\\GitHub\\Sanity\\graph.csv")



