__author__ = 'amir'

import csv


def Parse(file):
    print(file)
    f=open(file,"r")
    lines=f.readlines()
    ind=lines.index('=== Detailed Accuracy By Class ===\n')
    details=[x.lstrip().replace("Weighted Avg.","").split() for x in lines[ind+3: ind+6]]
    titles=["TP Rate","FP Rate","Precision","Recall"," F-Measure","MCC","ROC Area","PRC Area"]
    classes=['bugged',"valid","both"]
    details[0]=details[0][:-1]
    details[1]=details[1][:-1]
    dict={}
    for c,p in zip(classes,details):
        dict[c]={}
        for metric,title in zip(p,titles):
            dict[c][title]=metric
    return dict


#print Parse('C:\GitHub\\weka\weka.classifiers.trees.J48_AllFiles_all_Normal_testing.txt')

def ParseDir(d,rangeInd):
    dict={}
    classes=['bugged',"valid","both"]
    for i in range(rangeInd):
        file=d+"\\"+str(i)+".txt"
        dict[i]={}
        parsedDict=Parse(file)
        for c in classes:
            dict[i][c]=parsedDict[c]["ROC Area"]
    return dict

def comprasion(oned,alld, outPath,Family):
    rangeInd=len(Family)
    output=[["Family","index","class","one but all","all but one" ]]
    oneP=ParseDir(oned,rangeInd)
    allP=ParseDir(alld,rangeInd)
    classes=['bugged',"valid","both"]
    classes=["both"]
    for i in range(rangeInd):
        for c in classes:
           output.append([Family[i],i,c,oneP[i][c],allP[i][c]])
    with open(outPath, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(output)

		

def indsFamilies(packsInds,Wanted):
	return []
def All_one_parallel(sourcePathTrain,sourcePathTest,oned,alld,packsInds,names):
	comprasion(oned+"\\out",alld+"\\out", d+"\\"+"_".join(names)+".csv",names)

def allFamilies(d,packs,packsInds):
    methods = packs
    indsMethods = indsFamilies(packsInds, [[packs.index(x)] for x in methods])
    All_one_parallel(sourcePathTrain, sourcePathTest, d + "\\Fam_one", d + "\\Fam_all", indsMethods, methods)

def familiesTypes(d,packs,packsInds):
    OO_old = ["methodsArticles", "hirarcy", "fieldsArticles", "constructorsArticles"]
    OO_new = OO_old + ["bugs"]
    names = ["OO_old", "OO_new"]
    indsMethods = indsFamilies(packsInds, [[packs.index(y) for y in OO_old], [packs.index(y) for y in OO_new]])
    All_one_parallel(sourcePathTrain, sourcePathTest, d + "\\OO_add_one", d + "\\OO_add_all", indsMethods, names)
    OO_old = ["haelstead", "sourceMonitor", "checkStyle"]
    OO_new = OO_old + ["bugs"]
    indsMethods = indsFamilies(packsInds, [[packs.index(y) for y in OO_old], [packs.index(y) for y in OO_new]])
    names = ["complexity_old", "complexity_new"]
    All_one_parallel(sourcePathTrain, sourcePathTest, d + "\\complexity_add_one", d + "\\complexity_add_all",
                     indsMethods, names)
    OO_old = ["simpleProcessArticles"]
    OO_new = OO_old + ["bugs"]
    indsMethods = indsFamilies(packsInds, [[packs.index(y) for y in OO_old], [packs.index(y) for y in OO_new]])
    names = ["process_old", "process_new"]
    All_one_parallel(sourcePathTrain, sourcePathTest, d + "\\process_add_one", d + "\\process_add_all", indsMethods,
                     names)
    OO_old = ["simpleProcessArticles"] + ["methodsArticles", "hirarcy", "fieldsArticles", "constructorsArticles"] + [
        "haelstead", "sourceMonitor", "checkStyle"]
    OO_new = OO_old + ["bugs"]
    indsMethods = indsFamilies(packsInds, [[packs.index(y) for y in OO_old], [packs.index(y) for y in OO_new]])
    names = ["old", "new"]
    All_one_parallel(sourcePathTrain, sourcePathTest, d + "\\All_one", d + "\\All_all", indsMethods, names)


d="D:\\Amir_Almishali\\weka\\ant"+"\\1"

packs=["haelstead","g2","g3","methodsArticles","methodsAdded","hirarcy","fieldsArticles","fieldsAdded","constructorsArticles","constructorsAdded","lastProcess","simpleProcessArticles","simpleProcessAdded","bugs","sourceMonitor","checkStyle","blame"]#,"analyzeComms"]

packsInds=[]
sourcePathTrain=""
sourcePathTest=""


allFamilies(d,packs,packsInds)
familiesTypes(d,packs,packsInds)

exit()


OO_old=["haelstead","sourceMonitor","checkStyle"]
OO_new=OO_old+["bugs"]
indsMethods=indsFamilies(packsInds,[ [packs.index(y) for y in  OO_old  ],[packs.index(y) for y in OO_new ]])
names=["Complexity_old","Complexity_new"]
All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\complexity_add_one",d+"\\complexity_add_all",indsMethods,names)


OO_old=["simpleProcessArticles"]
OO_new=OO_old+["bugs"]
indsMethods=indsFamilies(packsInds,[ [packs.index(y) for y in  OO_old  ],[packs.index(y) for y in OO_new ]])
names=["process_old","process_new"]
All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\process_add_one",d+"\\process_add_all",indsMethods,names)

exit()
OO_old=["methodsArticles","hirarcy","fieldsArticles","constructorsArticles"]
OO_new=OO_old+["bugs"]
names=["OO_old","OO_new"]
indsMethods=indsFamilies(packsInds,[ [packs.index(y) for y in  OO_old  ],[packs.index(y) for y in OO_new ]])
All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\OO_add_one",d+"\\OO_add_all",indsMethods,names)

OO_old=["simpleProcessArticles"]
OO_new=OO_old+["bugs"]
indsMethods=indsFamilies(packsInds,[ [packs.index(y) for y in  OO_old  ],[packs.index(y) for y in OO_new ]])
names=["process_old","process_new"]
All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\process_add_one",d+"\\process_add_all",indsMethods,names)

OO_old=["haelstead","sourceMonitor","checkStyle"]
OO_new=OO_old+["bugs"]
indsMethods=indsFamilies(packsInds,[ [packs.index(y) for y in  OO_old  ],[packs.index(y) for y in OO_new ]])
names=["complexity_old","complexity_new"]
All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\complexity_add_one",d+"\\complexity_add_all",indsMethods,names)


OO_old=["haelstead","methodsArticles","hirarcy","fieldsArticles","constructorsArticles","simpleProcessArticles","sourceMonitor","checkStyle"]
OO_new=OO_old+["bugs"]
indsMethods=indsFamilies(packsInds,[ [packs.index(y) for y in  OO_old  ],[packs.index(y) for y in OO_new ]])
names=["old","new"]
All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\add_one",d+"\\add_all",indsMethods,names)