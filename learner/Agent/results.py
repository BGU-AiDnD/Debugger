__author__ = 'amir'

import csv
import math
import os.path

def get_diag(diagFile):
    diags=[]
    probs=[]
    with open(diagFile,"r") as f:
        reader =csv.reader(f)
        for i in reader:
            diags.append(i[:len(i)-2])
            probs.append(i[len(i)-1])
    return  (diags,probs)


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


def precision_recall_diag(buggedComps, dg, pr, validComps):
    fp = len([i1 for i1 in dg if i1 in validComps])
    fn = len([i1 for i1 in buggedComps if i1 not in dg])
    tp = len([i1 for i1 in dg if i1 in buggedComps])
    tn = len([i1 for i1 in validComps if i1 not in dg])
    if ((tp + fp) == 0):
        precision = "undef"
    else:
        precision = (tp + 0.0) / float(tp + fp)
        a = precision
        precision = precision * float(pr)
    if ((tp + fn) == 0):
        recall = "undef"
    else:
        recall = (tp + 0.0) / float(tp + fn)
        recall = recall * float(pr)
    return precision, recall


def results(files, bugged,DiagFile,thresholdPorbs):
    valids=[str(i2) for i2 in range(len(files)) if str(i2) not in bugged]
    validComps= [ttt for ttt in files if ttt in valids]
    buggedComps=[ttt for ttt in files if ttt in bugged]
    diag,prob=get_diag(DiagFile)
    accumlate=0
    countPrios=0
    for p in prob:
        accumlate=accumlate+float(p)
        countPrios=countPrios+1
        if(accumlate>=thresholdPorbs):
            break

    diag=diag[:countPrios]
    prob=[float(p)/float(accumlate) for p in prob[:countPrios]]

    recall_accum=0
    precision_accum=0
    for dg,pr in zip(diag,prob):
        precision, recall = precision_recall_diag(buggedComps, dg, pr, validComps)
        if(recall!="undef"):
            recall_accum=recall_accum+recall
        if(precision!="undef"):
            precision_accum=precision_accum+precision
        #return accurA
    return recall_accum,precision_accum


def diagsToCompsProbs(files, bugged,DiagFile,thresholdPorbs):
    valids=[str(i2) for i2 in range(len(files)) if str(i2) not in bugged]
    validComps= [ttt for ttt in files if ttt in valids]
    buggedComps=[ttt for ttt in files if ttt in bugged]
    diag,prob=get_diag(DiagFile)
    accumlate=0
    countPrios=0
    dict={}
    for i in range(len(diag)):
        d=diag[i]
        p=float(prob[i])
        for comp in d:
            if comp in dict:
                dict[comp]=dict[comp]+p
            else:
                dict[comp]=p

    pr=0.0
    dg=[]
    dict2={}
    for comp in dict:
        p=dict[comp]
        if p in dict2:
            dict2[p].append(comp)
        else:
            dict2[p]=[comp]
    vals=sorted(dict2.items(),key=lambda t :t[0],reverse=True)
    #exit()
    #vals=sorted(dict.items(),key=lambda t :t[1],reverse=True)
    points=set()
    points.add((0.0,1.0))
    dg=[]
    for p,comps in vals:
        dg.extend(comps)
        precision, recall = precision_recall_diag(buggedComps, dg, 1, validComps)
        if(precision!="undef" and recall!="undef"):
            #precision_accum=precision_accum+precision
            if recall!=0.0 or precision!=0.0:
                points.add((recall,precision))
    precision, recall = precision_recall_diag(buggedComps, files, 1, validComps)
    if(precision!="undef" and recall!="undef"):
        #precision_accum=precision_accum+precision
        if recall!=0.0 or precision!=0.0:
            points.add((recall,precision))
    pointsSort=sorted(list(points),key=lambda t :t[1],reverse=True)
    pointsSort=sorted(list(pointsSort),key=lambda t :t[0])
    auc=0
    for i in range(len(pointsSort)-1):
        x1,y1=pointsSort[i]
        x2,y2=pointsSort[i+1]
        auc=auc+(x2-x1)*(y1+y2)/2
    return auc


def readBugFile(bug_f):
    f = open(bug_f, "r")
    lines = [x.split("\n")[0] for x in f.readlines()]
    f.close()
    used = lines[1].split(",")
    bugged = lines[3].split(",")
    BugsIds = len(lines[5].split(",")) - 2
    testsCount = int(lines[7].split(",")[0])
    pack = lines[9].split(",")[0]
    return BugsIds, bugged, pack, testsCount, used

def aucCheck(DiagFile,bug_f,thresholdPorbs):
    BugsIds, bugged, pack, testsCount, files = readBugFile(bug_f)
    auc =diagsToCompsProbs(files, bugged,DiagFile,thresholdPorbs)
    return auc

def ExperimentsAuc(outputFile,output2File,baseDir, thresholdPorbs,weka,experiments):
    dirI = baseDir+"out\\"
    #bugsDir = baseDir+"Opt\\"
    bugsDir = baseDir+"bugs_Files\\"
    output=[]
    output2=[]
    if  weka:
        output=output+[["algorithm","auc" ]]
        output2=output2+[["algorithm","index","auc" ]]
        files=["weka","uniform"]
        for f in files:
            recall_avg=0
            accA_count=0
            precision_avg=0
            accB_count=0
            tests_avg=0.0
            files_avg=0
            bugged_avg=0
            for k in range(experiments):
                file =  f+"_" + str(k)
                rowToAdd=[f,k]
                bug_f=bugsDir+ str(k)+ ".txt"
                if (not os.path.isfile(bug_f)):
                    continue
                DiagFile = baseDir+"\\out\\DIFG_check_"+ file + ".csv.csv"
                if (not os.path.isfile(DiagFile)):
                    continue
                accA_count, accB_count,precision_avg,recall_avg,tests_avg,files_avg,bugged_avg = one_file_res(DiagFile, accA_count, accB_count, bug_f, precision_avg, recall_avg,tests_avg,files_avg,bugged_avg, rowToAdd, thresholdPorbs)

                output2=output2+[rowToAdd]
            recall_avg=recall_avg/accA_count
            precision_avg=precision_avg/accB_count
            tests_avg=tests_avg/experiments
            files_avg=files_avg/experiments
            bugged_avg=bugged_avg/experiments
            output=output+[[f,precision_avg,recall_avg,tests_avg,files_avg,bugged_avg]]
    else:
        output=output+[["pBug","pValid","auc" ]]
        output2=output2+[["pBug","pValid","index","auc","tests","files","bugged","bugsIDS","pack" ]]
        for i in range(10):
            pBug = i / 10.0
            for j in range(10):  # pValid < pBug
                if ( i <= j):
                    break
                pValid = j / 10.0
                auc_avg=0
                accA_count=0.0
                tests_avg=0.0
                files_avg=0
                bugged_avg=0
                for k in range(experiments):
                    file = str(pBug) + "_" + str(pValid) + "_" + str(k)
                    rowToAdd=[pBug,pValid,k]
                    bug_f=bugsDir+ str(k)+ ".txt"
                    if (not os.path.isfile(bug_f)):
                        continue
                    DiagFile = baseDir+"\\out\\DIFG_check_"+ file + ".csv.csv"
                    auc = aucCheck(DiagFile, bug_f, thresholdPorbs)
                    auc_avg=auc_avg+auc
                    accA_count=accA_count+1
                    output2=output2+[rowToAdd]
                auc_avg=auc_avg/accA_count
                tests_avg=tests_avg/experiments
                files_avg=files_avg/experiments
                bugged_avg=bugged_avg/experiments
                output=output+[[pBug,pValid,auc_avg,tests_avg,files_avg,bugged_avg]]
    with open(outputFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(output)
    with open(output2File, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(output2)


def one_file_res(DiagFile, accA_count, accB_count, bug_f, precision_avg, recall_avg,tests_avg,files_avg,bugged_avg, rowToAdd, thresholdPorbs):
    BugsIds, bugged, pack, testsCount, files = readBugFile(bug_f)
    filesCount=len(files)
    buggedCount=len(bugged)
    tests_avg=tests_avg+testsCount
    files_avg=files_avg+filesCount
    bugged_avg=bugged_avg+buggedCount
    #print(DiagFile)
    recall, precision = results(files, bugged, DiagFile, thresholdPorbs)
    if (precision != 'undef'):
        if (not ( math.isnan(precision) )):
            rowToAdd.append(precision)
            accB_count = accB_count + 1
            precision_avg = precision_avg + precision
        else:
            rowToAdd.append('Nan')
    else:
        rowToAdd.append('undef')

    if (recall != 'undef'):
        if (not ( math.isnan(recall) )):
            rowToAdd.append(recall)
            accA_count = accA_count + 1
            recall_avg = recall_avg + recall
        else:
            rowToAdd.append('Nan')
    else:
        rowToAdd.append('undef')
    rowToAdd.append(testsCount)
    rowToAdd.append(filesCount)
    rowToAdd.append(buggedCount)
    rowToAdd.append(BugsIds)
    rowToAdd.append(pack)

    return accA_count, accB_count,precision_avg,recall_avg,tests_avg,files_avg,bugged_avg




def resultsAllBarinel(outputFile,output2File,baseDir, thresholdPorbs,weka,experiments,outDirName="out",
                      bugsfilesDir="bugs_Files\\"):
    dirI = baseDir+"outUniform\\"
    #bugsDir = baseDir+"Opt\\"
    bugsDir = baseDir+ bugsfilesDir
    output=[]
    output2=[]
    if  weka:
        output=output+[["algorithm","precision_avg","recall_avg","auc_avg","tests_avg","files_avg","bugged_avg" ]]
        output2=output2+[["algorithm","index","precision","recall","auc","tests","files","bugged","bugsIDS","pack" ]]
        files=["weka","uniform"]

        for f in files:
            recall_avg=0
            accA_count=0
            auc_count=0
            auc_avg=0.0
            precision_avg=0
            accB_count=0
            tests_avg=0.0
            files_avg=0
            bugged_avg=0
            for k in range(experiments):
                file =  f+"_" + str(k)
                rowToAdd=[f,k]
                bug_f=bugsDir+ str(k)+ ".txt"
                if (not os.path.isfile(bug_f)):
                    continue
                DiagFile = baseDir+"\\"+outDirName+"\\DIFG_check_"+ file + ".csv.csv"
                if (not os.path.isfile(DiagFile)):
                    continue
                accA_count, accB_count,precision_avg,recall_avg,tests_avg,files_avg,bugged_avg = one_file_res(DiagFile, accA_count, accB_count, bug_f, precision_avg, recall_avg,tests_avg,files_avg,bugged_avg, rowToAdd, thresholdPorbs)
                auc = aucCheck(DiagFile, bug_f, thresholdPorbs)
                auc_avg=auc_avg+auc
                auc_count=auc_count+1
                output2=output2+[rowToAdd[:4]+[auc]+rowToAdd[4:]]
            recall_avg=recall_avg/accA_count
            auc_avg=auc_avg/auc_count
            precision_avg=precision_avg/accB_count
            tests_avg=tests_avg/experiments
            files_avg=files_avg/experiments
            bugged_avg=bugged_avg/experiments
            output=output+[[f,precision_avg,recall_avg,auc_avg,tests_avg,files_avg,bugged_avg]]
    else:
        output=output+[["pBug","pValid","precision_avg","recall_avg","auc_avg","tests_avg","files_avg","bugged_avg" ]]
        output2=output2+[["pBug","pValid","index","precision","recall","auc","tests","files","bugged","bugsIDS","pack" ]]
        for i in range(10):
            pBug = i / 10.0
            for j in range(10):  # pValid < pBug
                if ( i <= j):
                    break
                pValid = j / 10.0
                recall_avg=0
                accA_count=0
                auc_count=0
                auc_avg=0.0
                precision_avg=0
                accB_count=0
                tests_avg=0.0
                files_avg=0
                bugged_avg=0
                for k in range(experiments):
                    file = str(pBug) + "_" + str(pValid) + "_" + str(k)
                    rowToAdd=[pBug,pValid,k]
                    bug_f=bugsDir+ str(k)+ ".txt"
                    if (not os.path.isfile(bug_f)):
                        continue
                    DiagFile = baseDir+"\\"+outDirName+"\\DIFG_check_"+ file + ".csv.csv"
                    accA_count, accB_count,precision_avg,recall_avg,tests_avg,files_avg,bugged_avg = one_file_res(DiagFile, accA_count, accB_count, bug_f, precision_avg, recall_avg,tests_avg,files_avg,bugged_avg, rowToAdd, thresholdPorbs)
                    auc = aucCheck(DiagFile, bug_f, thresholdPorbs)
                    auc_avg=auc_avg+auc
                    auc_count=auc_count+1
                    output2=output2+[rowToAdd[:5]+[auc]+rowToAdd[5:]]
                recall_avg=recall_avg/accA_count
                auc_avg=auc_avg/auc_count
                precision_avg=precision_avg/accB_count
                tests_avg=tests_avg/experiments
                files_avg=files_avg/experiments
                bugged_avg=bugged_avg/experiments
                output=output+[[pBug,pValid,precision_avg,recall_avg,auc_avg,tests_avg,files_avg,bugged_avg]]
    with open(outputFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(output)
    with open(output2File, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(output2)


def resultsMultyWekaAndSanity(outputFile,output2File,baseDir, thresholdPorbs,experiments,timesArr,wekaAnsArr):
    outDirName="out"
    bugsfilesDir="bugs_Files\\"
    dirI = baseDir+"outUniform\\"
    #bugsDir = baseDir+"Opt\\"
    bugsDir = baseDir+ "bugs_Files\\"
    output=[]
    output2=[]
    output=output+[["algorithm","pBug","pValid","times","precision_avg","recall_avg","auc_avg","tests_avg","files_avg","bugged_avg" ]]
    output2=output2+[["algorithm","pBug","pValid","times","index","precision","recall","auc","tests","files","bugged","bugsIDS","pack" ]]
    for t in range(len(timesArr)):
        times=timesArr[t]
        filePre=str(times)+"_"
        files=[filePre +"uniform_"]+[filePre+"weka_" +x[1] for x in wekaAnsArr]
        for f,name in zip(files,["uniform"]+[x[1] for x in wekaAnsArr]):
            recall_avg=0.0
            accA_count=0.0
            auc_count=0.0
            auc_avg=0.0
            precision_avg=0.0
            accB_count=0.0
            tests_avg=0.0
            files_avg=0.0
            bugged_avg=0.0
            for k in range(experiments):
                file =  f + str(k)
                rowToAdd=[name,0,0,times,k]
                bug_f=bugsDir+filePre+ str(k)+ ".txt"
                if (not os.path.isfile(bug_f)):
                    continue
                DiagFile = baseDir+"\\out\\DIFG_check_"+ file + ".csv.csv"
                if (not os.path.isfile(DiagFile)):
                    continue
                #print DiagFile, accA_count, accB_count, bug_f, precision_avg, recall_avg,tests_avg,files_avg,bugged_avg, rowToAdd, thresholdPorbs
                accA_count, accB_count,precision_avg,recall_avg,tests_avg,files_avg,bugged_avg = one_file_res(DiagFile, accA_count, accB_count, bug_f, precision_avg, recall_avg,tests_avg,files_avg,bugged_avg, rowToAdd, thresholdPorbs)
                auc = aucCheck(DiagFile, bug_f, thresholdPorbs)
                auc_avg=auc_avg+auc
                auc_count=auc_count+1
                output2=output2+[rowToAdd[:7]+[auc]+rowToAdd[7:]]
            recall_avg=recall_avg/accA_count
            auc_avg=auc_avg/auc_count
            precision_avg=precision_avg/accB_count
            tests_avg=tests_avg/experiments
            files_avg=files_avg/experiments
            bugged_avg=bugged_avg/experiments
            output=output+[[name,0,0,times,precision_avg,recall_avg,auc_avg,tests_avg,files_avg,bugged_avg]]
        pBug = 0.6
        for j in range(3):  # pValid < pBug
            pValid = j / 10.0
            recall_avg=0
            accA_count=0
            auc_count=0
            auc_avg=0.0
            precision_avg=0
            accB_count=0
            tests_avg=0.0
            files_avg=0
            bugged_avg=0
            for k in range(experiments):
                file =filePre+ str(pBug) + "_" + str(pValid) + "_" + str(k)
                rowToAdd=["Sanity", pBug,pValid,times,k]
                bug_f=bugsDir+filePre+ str(k)+ ".txt"
                if (not os.path.isfile(bug_f)):
                    continue
                DiagFile = baseDir+"\\"+outDirName+"\\DIFG_check_"+ file + ".csv.csv"
                if (not os.path.isfile(DiagFile)):
                    continue
                accA_count, accB_count,precision_avg,recall_avg,tests_avg,files_avg,bugged_avg = one_file_res(DiagFile, accA_count, accB_count, bug_f, precision_avg, recall_avg,tests_avg,files_avg,bugged_avg, rowToAdd, thresholdPorbs)
                auc = aucCheck(DiagFile, bug_f, thresholdPorbs)
                auc_avg=auc_avg+auc
                auc_count=auc_count+1
                output2=output2+[rowToAdd[:5]+[auc]+rowToAdd[5:]]
            recall_avg=recall_avg/accA_count
            auc_avg=auc_avg/auc_count
            precision_avg=precision_avg/accB_count
            tests_avg=tests_avg/experiments
            files_avg=files_avg/experiments
            bugged_avg=bugged_avg/experiments
            output=output+[[pValid,pBug,pValid,times,precision_avg,recall_avg,auc_avg,tests_avg,files_avg,bugged_avg]]
    with open(outputFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(output)
    with open(output2File, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(output2)


def recordsOne(i, j, k,instancesPath,retCode,file):
    lines=[]
    #dir="C:\Users\\amir\workspace\Program_Diagnoser\\resultsMore\\records\\"

    expr=instancesPath+file
    with open(expr,"r") as f:
        reader =csv.reader(f)
        lines=[l for l in reader]
        #print(lines)
    precision_avg = 0
    recall_avg = 0
    steps_avg = 0
    ind=0
    initials=0
    tests=0
    for l in lines:
        if(l[10]==retCode or "all"==retCode):
            ind=ind+1
            precision_avg = precision_avg + float(l[7])
            recall_avg = recall_avg + float(l[6])
            steps_avg = steps_avg + float(l[8])
            initials=float(l[11])
            tests=float(l[12])
    ln=ind
    if (ind==0):
        return 0,0,0,0,0
    recall_avg=recall_avg/ln
    precision_avg=precision_avg/ln
    steps_avg=steps_avg/ln
    return precision_avg, recall_avg,steps_avg,initials,tests


def records_i_j(i, j,instancesPath,experiments,retCode,file,exps,bug_f_start):

    precision_avg = 0.0
    recall_avg = 0.0
    files_avg = 0.0
    bugged_avg = 0.0
    steps_avg = 0.0
    medianLines=[]
    #lst=range(experiments)
    #lst=[1,2,3,5,7,15,16,22,23,32,33,35,38,39]
    #lst=[2,4,5,8,9,10,20,23,27,29,32,33,35,38,39,14,28]
    #lst=[0,1,2,3,4,6,7,8,9]
    initials_avg=0
    tests_avg=0
    for k in exps:
        #file=str(i) + "_" + str(j) + "_" + str(k)+".txt"+".csv"
        bug_f=bug_f_start+ str(k)+ ".txt"
        BugsIds, bugged, pack, testsCount, files = readBugFile(bug_f)
        filesCount=len(files)
        buggedCount=len(bugged)
        f=file+str(k)+".txt"+".csv"
        precision, recall,steps,initials,tests = recordsOne(i, j, k,instancesPath,retCode,f)
        medianLines=medianLines+[[i, j, k,precision, recall,steps,tests,filesCount,buggedCount,initials,tests]]
        precision_avg=precision_avg+precision
        recall_avg=recall_avg+recall
        steps_avg=steps_avg+steps
        initials_avg=initials_avg+initials
        tests_avg=tests_avg+tests
        files_avg=files_avg+filesCount
        bugged_avg=bugged_avg+buggedCount

    return precision_avg/len(exps), recall_avg/len(exps),steps_avg/len(exps),initials_avg/len(exps),tests_avg/len(exps),medianLines,files_avg/len(exps),bugged_avg/len(exps)


def planner_recordes( outputFile,medoutputFile,instancesPath,experiments,retCode,weka,exps):
    out_lines=[["pBug","pValid","precision","recall","steps","initials","tests"]]
    med_lines=[["pBug","pValid","index","precision","recall","steps","initials","tests"]]
    if (not weka):
        for i in range(10):
            pBug = i / 10.0
            for j in range(10):  # pValid < pBug
                if ( i <= j):
                    break
                pValid = j / 10.0
                file=str(pBug) + "_" + str(pValid) + "_"
                #file=""
                precision_avg, recall_avg,steps_avg,initials,tests,meds = records_i_j(pBug, pValid,instancesPath,experiments,retCode,file,exps)
                #out_lines=out_lines+[[precision_avg,recall_avg,steps_avg]]
                out_lines=out_lines+[[pBug,pValid,precision_avg,recall_avg,steps_avg,initials,tests]]
                med_lines.extend(meds)
    else:
        file="weka_"
        precision_avg, recall_avg,steps_avg,initials,tests,meds = records_i_j(0, 0,instancesPath,experiments,retCode,file,exps)
        out_lines=out_lines+[["weka",precision_avg,recall_avg,steps_avg,initials,tests]]
        meds=[ ["weka"]+m[2:] for m in meds ]
        #med_lines.extend(meds)
        file="uniform_"
        precision_avg, recall_avg,steps_avg,initials,tests,meds2 = records_i_j(0, 0,instancesPath,experiments,retCode,file,exps)
        out_lines=out_lines+[["uniform",precision_avg,recall_avg,steps_avg,initials,tests]]
        meds2=[ ["uniform"]+m[2:] for m in meds2 ]
        med_lines.extend([a+b for a,b in zip(meds,meds2)])
    with open(outputFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(out_lines)
    with open(medoutputFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(med_lines)

def planner_resultsMultyWekaAndSanity( outputFile,medoutputFile,instancesPath,experiments,retCode,weka,timesArr,wekaAnsArr):
    bugsDir = instancesPath+ "bugs_Files\\"
    out_lines=[]#[["pBug","pValid","precision","recall","steps","initials","tests"]]
    #out_lines=[["pBug","pValid","precision","recall","steps","initials","tests"]]
    out_lines=out_lines+[["algorithm","pBug","pValid","times","precision_avg","recall_avg","steps","tests_avg","files_avg","bugged_avg","initials","tests" ]]
    #med_lines=[["pBug","pValid","index","precision","recall","steps","initials","tests"]]
    med_lines=[]#[["pBug","pValid","index","precision","recall","steps","initials","tests"]]
    med_lines=med_lines+[["algorithm","pBug","pValid","times","index","precision_avg","recall_avg","steps","tests_avg","files_avg","bugged_avg","initials","tests" ]]
    exps=range(experiments)
    for t in range(len(timesArr)):
        times=timesArr[t]
        filePre=str(times)+"_"
        files=[filePre +"uniform_"]+[filePre+"weka_" +x[1] for x in wekaAnsArr]
        for f,name in zip(files,["uniform"]+[x[1] for x in wekaAnsArr]):
            bug_f_start=bugsDir+filePre
            precision_avg, recall_avg,steps_avg,initials,tests,meds,files_avg,bugged_avg = records_i_j(0, 0,instancesPath+"\\plannerRecords\\",experiments,retCode,f,exps,bug_f_start)
            out_lines=out_lines+[[name,0,0,times,precision_avg,recall_avg,steps_avg,tests,files_avg,bugged_avg,initials,tests]]
            meds=[ [name]+m[:2]+[times]+m[2:] for m in meds ]
            med_lines.extend(meds)
        pBug = 0.6
        for j in range(3):  # pValid < pBug
            pValid = j / 10.0
            file=str(times) + "_"+str(pBug) + "_" + str(pValid) + "_"
            #file=""
            bug_f_start=bugsDir+filePre
            precision_avg, recall_avg,steps_avg,initials,tests,meds,files_avg,bugged_avg = records_i_j(pBug, pValid,instancesPath+"\\plannerRecords\\",experiments,retCode,file,exps,bug_f_start)
            out_lines=out_lines+[[str(pValid),pBug,pValid,times,precision_avg,recall_avg,steps_avg,tests,files_avg,bugged_avg,initials,tests]]
            meds=[ [str(pValid)]+m[:2]+[times]+m[2:] for m in meds ]
            med_lines.extend(meds)
    with open(outputFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(out_lines)
    with open(medoutputFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(med_lines)


if __name__ == "__main__":

    #print aucCheck("C:\\GitHub\\agent\\learner\\exWekaLOWER\\out\\DIFG_check_uniform_1.csv.csv","C:\\GitHub\\agent\\learner\\exWekaLOWER\\bugs_Files\\1.txt",1)
    #print aucCheck("C:\\GitHub\\agent\\learner\\exWekaLOWER\\out\\DIFG_check_weka_1.csv.csv","C:\\GitHub\\agent\\learner\\exWekaLOWER\\bugs_Files\\1.txt",1)

    accA_count, accB_count,precision_avg,recall_avg,tests_avg,files_avg,bugged_avg=one_file_res("C:\GitHub\\all-all\\out\DIFG_check_25_uniform_0.csv.csv", 0.0, 0.0, "C:\GitHub\\all-all\\bugs_Files\\25_0.txt", 0.0, 0.0, 0.0, 0.0, 0.0, ['uniform', 0, 0, 25, 0], 1)
    print accA_count, accB_count,precision_avg,recall_avg,tests_avg,files_avg,bugged_avg

    d="C:\GitHub\\all-all"
    numOfExperiments=50
    numOfPacks=1
    numOfrepeats=1
    numOfBugs=[2]
    times=[25,40,70,100,130]
    wekaAlgs=[ "weka.classifiers.trees.RandomForest" ]
    wekaBase="C:\\GitHub\\experiments\\wekOut\\"
    wekaAnsArr=[(wekaBase+"CDT_8_1_2_AllFiles_1_Only.csv",w) for w in wekaAlgs]+[(wekaBase+"weka.classifiers.trees.RandomForest_Style2.csv","prev")] #all

    resultsMultyWekaAndSanity("%s\\1.csv" % d, "%s\\2.csv" % d, "%s\\" % d, 1,
                                      numOfExperiments, times, wekaAnsArr)

    exit()
    outPath="C:\\GitHub\\agent\\learner\\exWekaCheck38"
    sizes=[30,40,70]
    for s in sizes:
        experiments=57
        b="bugs_Files"+str(s)+"\\"
        resultsAllBarinel(outPath+"\\Auc"+str(s)+".csv" ,outPath+"\\Auc2"+str(s)+".csv", "%s\\" % outPath,1,False,experiments,"out"+str(s),b)
        resultsAllBarinel(outPath+"\\AucW"+str(s)+".csv" ,outPath+"\\Auc2W"+str(s)+".csv" , "%s\\" % outPath,1,True,experiments,"outW"+str(s),b)

    exit()
    outPath="C:\\GitHub\\agent\\exWekaSaniBAR5"
    #print aucCheck("C:\\GitHub\\agent\\exWekaSaniBAR5\\out\\DIFG_check_0.0_0.0_1.csv.csv","C:\\GitHub\\agent\\exWekaSaniBAR5\\bugs_Files\\1.txt",1)
    #resultsAllBarinel("%s\\Auc.csv" % outPath,"%s\\Auc2.csv" % outPath, "%s\\" % outPath,1,False,23)
    if(3==3):
        outPath="C:\\GitHub\\agent\\learner\\exWekaSaniBAR5"
        resultsAllBarinel("%s\\Auc.csv" % outPath,"%s\\Auc2.csv" % outPath, "%s\\" % outPath,1,False,12)
        outPath="C:\\GitHub\\agent\\learner\\exWekaSaniBAR4"
        resultsAllBarinel("%s\\Auc.csv" % outPath,"%s\\Auc2.csv" % outPath, "%s\\" % outPath,1,False,12)
        outPath="C:\\GitHub\\agent\\learner\\exWekaSaniBAR3"
        resultsAllBarinel("%s\\Auc.csv" % outPath,"%s\\Auc2.csv" % outPath, "%s\\" % outPath,1,False,23)
    outPath="C:\\GitHub\\agent\\learner\\exWekaLOWER"
    resultsAllBarinel("%s\\Auc.csv" % outPath,"%s\\Auc2.csv" % outPath, "%s\\" % outPath,1,True,197)
    outPath="C:\\GitHub\\agent\\learner\\exWekaLOWER"
    resultsAllBarinel("%s\\AucT040.csv" % outPath,"%s\\Auc2T040.csv" % outPath, "%s\\" % outPath,1,True,143)
    outPath="C:\\GitHub\\agent\\learner\\exWekaCheck39"
    resultsAllBarinel("%s\\Auc.csv" % outPath,"%s\\Auc2.csv" % outPath, "%s\\" % outPath,1,True,57)
    outPath="C:\\GitHub\\agent\\learner\\exWekaCheck3"
    resultsAllBarinel("%s\\Auc.csv" % outPath,"%s\\Auc2.csv" % outPath, "%s\\" % outPath,1,True,373)
    #print aucCheck("C:\\GitHub\\agent\\exWekaSaniBAR5\\out\\DIFG_check_0.0_0.0_1.csv.csv","C:\\GitHub\\agent\\exWekaSaniBAR5\\bugs_Files\\1.txt",1)
