__author__ = 'amir'

import csv
import scipy
import sys, string, os


def properties(file):
    f=open(file,"r")
    reader=csv.reader(f)
    tp=0
    tn=0
    fn=0
    fp=0
    for line in reader:
        if line==[]:
            break
        actual=line[2]
        prediction=line[3]
        if actual=="1:bugged":
            if prediction=="1:bugged":
                tp=tp+1
            else:
               if prediction=="2:valid":
                fn=fn+1
        if actual=="2:valid":
            if prediction=="1:bugged":
                fp=fp+1
            else:
               if prediction=="2:valid":
                tn=tn+1
    precision=float(tp)/(tp+fp)
    recall=float(tp)/(tp+fn)
    accuracy=float(tp+tn)/(tp+tn+fn+fp)
    print ['precision','recall','accuracy','tp','tn','fn','fp']
    print [precision,recall,accuracy,tp,tn,fn,fp]

def getRates(modelFile):
    f=open(modelFile,"r")
    lines=f.readlines()
    ind = lines.index(
        "                 TP Rate  FP Rate  Precision  Recall   F-Measure  MCC      ROC Area  PRC Area  Class\n")
    lines=lines[ind:ind+3]
    tp=[i for i in lines[1].split(" ") if i!=''][0]
    fp=[i for i in lines[2].split(" ") if i!=''][1]
    return float(tp),float(fp)

def priorsCreation(namesFile,wekaOutFile,outFile, modelFile):
    names=[["FileName"]]+[x for x in csv.reader(open(namesFile,"r"))]
    weka=[x for x in csv.reader(open(wekaOutFile,"r"))]
    writer=csv.writer(open(outFile,"wb"))
    both=[]
    if modelFile=="":
        i=0
        for a,b in zip(names,weka):
            if(i==0):
                both.append(a+b)
            else:
                if (b[2]=="2:no") or (b[2]=="2:valid"):
                    both.append(a+b[:4]+[str(1-float(b[4]))])
                else:
                    both.append(a+b[:4]+[str(float(b[4]))])
            i=i+1
    else:
        tp,fp=getRates(modelFile)
        for a,b in  zip(names,weka):
            if b[2]=="2:valid":
                b[4]=fp
            if b[2]=="1:bugged":
                b[4]=tp
            both.append(a+b)
    writer.writerows(both)


def buggedprobabilities(buggedFiles,wekaFile):
    names=[x[0] for x in csv.reader(open(buggedFiles,"r"))][1:]
    wekaPriors={}
    first=0
    with open(wekaFile,"r") as f:
        reader=csv.reader(f)
        for l in reader:
            if(first==0):
                first=1
                continue
            prior=l[5]
            if( "*" in prior):
                prior="".join(list(prior[1:]))
            prior=float(prior)
            if(l[3]=="2:no"):
                prior=1-prior
            wekaPriors[l[0]]=prior+0.01
    priorsBugged={}
    for x in wekaPriors:
        if x in names:
            priorsBugged[x]=wekaPriors[x]
    return priorsBugged

#properties('C:\GitHub\weka\outOnly.csv')
#properties('C:\GitHub\weka\out.csv')


def method_name():
    global priors, vals, x
    priors = buggedprobabilities('C:\GitHub\weka\\bugged.csv', 'C:\GitHub\weka\outNew.csv')
    print scipy.average(priors.values())
    print max(priors.values())
    print min(priors.values())
    print sorted(priors.items(), key=lambda r: r[1])
    vals = priors.values()
    print len(vals)
    print len([x for x in vals if x > 0.1])
    print len([x for x in vals if x > 0.2])
    print len([x for x in vals if x > 0.3])
    print len([x for x in vals if x > 0.4])
    print len([x for x in vals if x > 0.5])
    print len([x for x in vals if x > 0.6])
    print len([x for x in vals if x > 0.7])
    print len([x for x in vals if x > 0.8])


#create_bp_script_file()
#print properties('C:\GitHub\weka\more\CDT_8_1_2_lastVer_bugs_OnlyNames.csv')
#priorsCreation('C:\GitHub\\experiments\weka\CDT_8_1_2_Style_OnlyNames.csv','C:\GitHub\\experiments\\weka.classifiers.trees.J48_Style23.csv','C:\GitHub\\experiments\\weka.classifiers.trees.J48_Style23.csv',"")
#exit()
if __name__=="__main__":
    model=""
    if (len(sys.argv)==4):
        model=sys.argv[3]
    priorsCreation(sys.argv[1],sys.argv[2],sys.argv[2],model)
#print getRates("C:\\GitHub\\experiments\\1_training.txt")