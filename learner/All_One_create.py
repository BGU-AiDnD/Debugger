__author__ = 'amir'


import arff
import os


def arff_build(attributes, data,desc,relation):
    dict={}
    dict['attributes']=attributes
    dict['data']=data
    dict['description']=desc
    dict['relation']=relation
    return dict


def write_to_arff(data,filename):
    f = open(filename, 'w')
    f.write(arff.dumps(data))
    f.close()

def load_arff(filename):
    f = open(filename, 'r')
    arf= arff.loads(f.read())
    f.close()
    return arf


def attributeSelect(sourceFile, outFile,inds):
    source=load_arff(sourceFile)
    attributes=[]
    ind=0
    last=len(source['attributes'])-1
    for x in source['attributes']:
        if ind in inds or ind==last:
            attributes.append(x)
        ind=ind+1
    data=[]
    for x in source['data']:
        ind=0
        d=[]
        for y in x:
            if ind in inds or ind==last:
                d.append(y)
            ind=ind+1
        if(d!=[]):
            data.append(d)
    arff_data=arff_build(attributes, data,str([]),"selected")
    write_to_arff(arff_data, outFile)

def Copy(path):
    CopyStatement = "cmd /x /c \"D: & copy D:\Amir_Almishali\weka\\BuildEval.bat " + path + "\\BuildEval.bat\""
    os.system(CopyStatement)


def All_one(sourcePathTrain,sourcePathTest,oned,alld,packsInds):
    red=list(set(reduce(lambda x, y: x+y, packsInds)))
    if not os.path.isdir(oned):
            os.mkdir(oned)
    if not os.path.isdir(alld):
            os.mkdir(alld)
    Copy(oned)
    Copy(alld)
    for ind in range(len(packsInds)):
        p=packsInds[ind]
        lst=list(red)
        for x in p:
            lst.remove(x)
        reduce1=lst
        print len(reduce1),len(p),len(reduce1)+len(p)
        outPathTrain=oned+"\\CDT_8_1_1_AllFiles_"+str(ind)+"_Appended.arff"
        outPathTest=oned+"\\CDT_8_1_2_AllFiles_"+str(ind)+"_Only.arff"
        attributeSelect(sourcePathTrain,outPathTrain,p)
        attributeSelect(sourcePathTest,outPathTest,p)
        outPathTrain=alld+"\\CDT_8_1_1_AllFiles_"+str(ind)+"_Appended.arff"
        outPathTest=alld+"\\CDT_8_1_2_AllFiles_"+str(ind)+"_Only.arff"
        attributeSelect(sourcePathTrain,outPathTrain, reduce1)
        attributeSelect(sourcePathTest,outPathTest,reduce1)
    os.system("start /b cmd /x /c \"D: & cd  " + oned +" &  " + oned + "\\BuildEval.bat\"")
    os.system("start /b cmd /x /c \"D: & cd  " + alld + " &  " + alld + "\\BuildEval.bat\"")

def mkdirs(d):
    d1=d
    if not os.path.isdir(d1):
            os.mkdir(d1)
    d1=d+"\\out"
    if not os.path.isdir(d1):
            os.mkdir(d1)
    d1=d+"\\training"
    if not os.path.isdir(d1):
            os.mkdir(d1)
    d1=d+"\\models"
    if not os.path.isdir(d1):
            os.mkdir(d1)

"""
@echo off
REM bat <indices>  <inputTrain> <outputTrain> <inputTest> <outputTest> <model> <training> <testing>
call java -Xmx2024m  -cp "C:\Program Files\Weka-3-7\weka.jar" weka.filters.unsupervised.attribute.Remove -R  %1 -V -i %2 -o %3
call java -Xmx2024m  -cp "C:\Program Files\Weka-3-7\weka.jar" weka.filters.unsupervised.attribute.Remove -R  %1 -V -i %4 -o %5
call java -Xmx2024m  -cp "C:\Program Files\Weka-3-7\weka.jar" weka.Run weka.classifiers.trees.RandomForest -I 1000 -K 0 -S 1 -num-slots 1  -t %3 -x 10 -d %6 > %7
call /b cmd.exe /x /c "java -Xmx4048m  -cp "C:\Program Files\Weka-3-7\weka.jar" weka.Run weka.classifiers.trees.RandomForest  -l %6 -T %5   > %8"
del /F %6
"""


def RemoveBuildEval(indices,inputTrain,outputTrain,inputTest,outputTest,model,training,testing,RemoveBat,classInd):
    inds=[x+1 for x in indices]
    inds=[x+1 for x in indices]+[classInd]
    print classInd,inds
    print classInd,inds
    print classInd,inds
    lst = [str(inds).replace('[','"').replace(']','"'), inputTrain, outputTrain, inputTest, outputTest, model, training, testing]
    params=" ".join([str(x) for x in lst])
    #bat_run = "start /b cmd /x /c \"D: & cd  D:\\Amir_Almishali\\weka\\ & D:\\Amir_Almishali\\weka\\RemoveBuildEval.bat " + params +"\""
    bat_run = "start /b cmd /x /c \" "+RemoveBat+" " + params +"\""
    os.system(bat_run)
    #exit()
    #print inputTrain, outputTrain, inputTest, outputTest, model, training, testing

def All_one_parallel(sourcePathTrain,sourcePathTest,oned,alld,packsInds,names,RemoveBat):
    red=list(set(reduce(lambda x, y: x+y, packsInds)))
    classInd = max(red)+2
    mkdirs(oned)
    mkdirs(alld)
    Copy(oned)
    Copy(alld)
    for p, name,ind in zip(packsInds,names,range(len(packsInds))):
        lst=list(red)
        for x in p:
            lst.remove(x)
        reduce1=lst
        
        print len(reduce1),len(p),len(reduce1)+len(p)
        outPathTrain=oned+"\\"+str(ind)+"_Appended.arff"
        outPathTest=oned+"\\"+str(ind)+"_Only.arff"
        RemoveBuildEval(p,sourcePathTrain,outPathTrain, sourcePathTest, outPathTest, oned+"\\models\\"+str(ind)+".model",oned+"\\training\\"+str(ind)+".txt",oned+"\\out\\"+str(ind)+".txt",RemoveBat,classInd)
        outPathTrain=alld+"\\"+str(ind)+"_Appended.arff"
        outPathTest=alld+"\\"+str(ind)+"_Only.arff"
        RemoveBuildEval(reduce1,sourcePathTrain,outPathTrain, sourcePathTest, outPathTest, alld+"\\models\\"+str(ind)+".model",alld+"\\training\\"+str(ind)+".txt",alld+"\\out\\"+str(ind)+".txt",RemoveBat,classInd)


def indsFamilies(packsInds,Wanted):
    RonipacksInds=[]
    for p in Wanted:
        lst = [packsInds[x] for x in p]
        RonipacksInds.append(reduce(lambda x, y: x + y, lst))
    return RonipacksInds



def allFamilies(d,packs,packsSizes,sourcePathTrain, sourcePathTest,RemoveBat):
    methods = packs
    packsInds=[]
    for i in range(len(packsSizes)-1):
        packsInds.append([x+packsSizes[i] for x in range(packsSizes[i+1]-packsSizes[i])])
    indsMethods = indsFamilies(packsInds, [[packs.index(x)] for x in methods])
    All_one_parallel(sourcePathTrain, sourcePathTest, d + "\\Fam_one", d + "\\Fam_all", indsMethods, methods,RemoveBat)

def familiesTypesFiles(d,packs,packsInds,sourcePathTrain, sourcePathTest,RemoveBat):
    OO_old = ["methodsArticles", "hirarcy", "fieldsArticles", "constructorsArticles"]
    OO_new = OO_old + ["bugs"]
    names = ["OO_old", "OO_new"]
    indsMethods = indsFamilies(packsInds, [[packs.index(y) for y in OO_old], [packs.index(y) for y in OO_new]])
    All_one_parallel(sourcePathTrain, sourcePathTest, d + "\\OO_add_one", d + "\\OO_add_all", indsMethods, names,RemoveBat)
    OO_old = ["haelstead", "sourceMonitor", "checkStyle"]
    OO_new = OO_old + ["bugs"]
    indsMethods = indsFamilies(packsInds, [[packs.index(y) for y in OO_old], [packs.index(y) for y in OO_new]])
    names = ["complexity_old", "complexity_new"]
    All_one_parallel(sourcePathTrain, sourcePathTest, d + "\\complexity_add_one", d + "\\complexity_add_all",
                     indsMethods, names,RemoveBat)
    OO_old = ["simpleProcessArticles"]
    OO_new = OO_old + ["bugs"]
    indsMethods = indsFamilies(packsInds, [[packs.index(y) for y in OO_old], [packs.index(y) for y in OO_new]])
    names = ["process_old", "process_new"]
    All_one_parallel(sourcePathTrain, sourcePathTest, d + "\\process_add_one", d + "\\process_add_all", indsMethods,
                     names,RemoveBat)
    OO_old = ["simpleProcessArticles"] + ["methodsArticles", "hirarcy", "fieldsArticles", "constructorsArticles"] + [
        "haelstead", "sourceMonitor", "checkStyle"]
    OO_new = OO_old + ["bugs"]
    indsMethods = indsFamilies(packsInds, [[packs.index(y) for y in OO_old], [packs.index(y) for y in OO_new]])
    names = ["old", "new"]
    All_one_parallel(sourcePathTrain, sourcePathTest, d + "\\All_one", d + "\\All_all", indsMethods, names,RemoveBat)


if __name__ == "__main__":
    buggedTypes=[]
    buggedTypes.append("AllFiles")
    d="D:\\Amir_Almishali\\weka\\p"
    sourcePathTrain=d+"\\REL_3_8_FINAL_AllFiles_all_Appended.arff"
    sourcePathTest=d+"\\REL_3_9_AllFiles_all_Only.arff"
	
    packs=["haelstead","g2","g3","methodsArticles","methodsAdded","hirarcy","fieldsArticles","fieldsAdded","constructorsArticles","constructorsAdded","lastProcess","simpleProcessArticles","simpleProcessAdded","bugs","sourceMonitor","checkStyle","blame"]#,"analyzeComms"]
    packsSizes=[0,10,34,54,68,92,104,111,133,138,162,176,190,199,280,333,369,405]#,650]
    packsInds=[]
    for i in range(len(packsSizes)-1):
        packsInds.append([x+packsSizes[i] for x in range(packsSizes[i+1]-packsSizes[i])])
    Ronipack=["OC" ,"OC_OOO" ,"OC_OOO_OP" ,"OC_OOO_DFA" ,"OC_OOO_IBW" ,"OC_OOO_IBW_PWCOO"]
    Roni=[[10,11,8],[10,11,6,7,5,8,9],[10,11,6,7,5,8,9,0,1],[10,11,6,7,5,8,9,0,1,3,4],[10,11,6,7,5,8,9,0,1,3,4,2],[10,11,6,7,5,8,9,0,1,3,4,2,12,13]]
    RonipacksInds=indsFamilies(packsInds,Roni)
    if not os.path.isdir(d):
        os.mkdir(d)

    allFamilies(d,packs,packsInds)
    familiesTypes(d,packs,packsInds)

    exit()

    #All_one(sourcePathTrain,sourcePathTest,d+"\\oneR",d+"\\allR",RonipacksInds)
    #exit()
	
	
    #methods=packs
    #indsMethods=indsFamilies(packsInds,[[packs.index(x)] for x in methods])
    #All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\Fam_one",d+"\\Fam_all",indsMethods,methods)

    #exit()
    if 1==2:
        All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\one",d+"\\all",packsInds,packs)


        methods=["methodsArticles", "methodsAdded"]
        indsMethods=indsFamilies(packsInds,[[packs.index(x)] for x in methods])
        All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\Methods_one",d+"\\Methods_all",indsMethods,methods)

        methods=["fieldsArticles", "fieldsAdded"]
        indsMethods=indsFamilies(packsInds,[[packs.index(x)] for x in methods])
        All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\Fields_one",d+"\\Fields_all",indsMethods,methods)
        methods=["constructorsArticles", "constructorsAdded"]
        indsMethods=indsFamilies(packsInds,[[packs.index(x)] for x in methods])
        All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\constructors_one",d+"\\constructors_all",indsMethods,methods)


        methods=["simpleProcessArticles","simpleProcessAdded"]
        indsMethods=indsFamilies(packsInds,[[packs.index(x)] for x in methods])
        All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\simpleprocess_one",d+"\\simpleprocess_all",indsMethods,methods)
        exit()

        OO=["g2","g3","methodsArticles","methodsAdded","hirarcy","fieldsArticles","fieldsAdded","constructorsArticles","constructorsAdded"]
        indsMethods=indsFamilies(packsInds,[[packs.index(x)] for x in OO])
        All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\OO_one",d+"\\OO_all",indsMethods,OO)

        process=["lastProcess","simpleProcessArticles","simpleProcessAdded","bugs","blame","analyzeComms"]
        indsMethods=indsFamilies(packsInds,[[packs.index(x)] for x in process])
        All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\process_one",d+"\\process_all",indsMethods,process)

	

	
    OO_old=["methodsArticles","hirarcy","fieldsArticles","constructorsArticles"]
    OO_new=OO_old+["bugs"]
    names=["OO_old","OO_new"]
    indsMethods=indsFamilies(packsInds,[ [packs.index(y) for y in  OO_old  ],[packs.index(y) for y in OO_new ]])
    All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\OO_add_one",d+"\\OO_add_all",indsMethods,names)
	
		
    OO_old=["haelstead","sourceMonitor","checkStyle"]
    OO_new=OO_old+["bugs"]
    indsMethods=indsFamilies(packsInds,[ [packs.index(y) for y in  OO_old  ],[packs.index(y) for y in OO_new ]])
    names=["complexity_old","complexity_new"]
    All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\complexity_add_one",d+"\\complexity_add_all",indsMethods,names)
	
    OO_old=["simpleProcessArticles"]
    OO_new=OO_old+["bugs"]
    indsMethods=indsFamilies(packsInds,[ [packs.index(y) for y in  OO_old  ],[packs.index(y) for y in OO_new ]])
    names=["process_old","process_new"]
    All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\process_add_one",d+"\\process_add_all",indsMethods,names)

    OO_old=["simpleProcessArticles"]+["methodsArticles","hirarcy","fieldsArticles","constructorsArticles"]+["haelstead","sourceMonitor","checkStyle"]
    OO_new=OO_old+["bugs"]
    indsMethods=indsFamilies(packsInds,[ [packs.index(y) for y in  OO_old  ],[packs.index(y) for y in OO_new ]])
    names=["old","new"]
    All_one_parallel(sourcePathTrain,sourcePathTest,d+"\\All_one",d+"\\All_all",indsMethods,names)

    exit()