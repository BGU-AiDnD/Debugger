__author__ = 'amir'

import os
import sys
import csv
import utilsConf
import shutil
import wekaMethods.ParseWekaOutput


def mkOneDir(dir):
    if not os.path.isdir(dir):
            os.mkdir(dir)

def Mkdirs(workingDir,projects):
    mkOneDir(workingDir)
    for d in ["AllFiles","AllMethods","MostFiles","MostMethods"]:
        Path=os.path.join(workingDir,d)
        mkOneDir(Path)
        for type in ["training","testing"]:
            training=os.path.join(Path,type)
            mkOneDir(training)
        out=os.path.join(Path,"out")
        mkOneDir(out)
        for name,wekaPath in projects:
            pro=os.path.join(out,name)
            mkOneDir(pro)



def ConfFileTowekaPathName(conf):
    vers, gitPath,bugsPath, workingDir=utilsConf.configure(conf)
    wekaPath=os.path.join(workingDir,"weka")
    name=conf.split("\\")[-1].replace("Conf.txt","")
    print name,wekaPath
    return name,wekaPath

def copyArffs(project,transferDir):
    name,wekaPath=project
    for buggedType in ["All","Most"]:
        for training in ["training","testing"]:
            for component in ["Files","Methods"]:
                arff=os.path.join(wekaPath,"_".join([buggedType,training,component.lower()])+".arff")
                Path=os.path.join(transferDir,buggedType+component)
                Path=os.path.join(Path,training)
                Path=os.path.join(Path,name+".arff")
                shutil.copyfile(arff, Path)


def buildModel(wekaDir,trainingArff,project,wekaJar):
    algorithm="weka.classifiers.trees.RandomForest -I 1000 -K 0 -S 1 -num-slots 1 "
    os.system("cd /d  "+wekaDir +" & java -Xmx2024m  -cp "+wekaJar+" weka.Run " +algorithm+ " -x 10 -d .\\model_"+project+".model -t "+trainingArff+" >"+project+".txt")


def evalModel(wekaDir,testingArff,outTxt,wekaJar,project):
    algorithm="weka.classifiers.trees.RandomForest "
    os.system("cd /d  "+wekaDir +" & java -Xmx2024m  -cp "+wekaJar+" weka.Run " +algorithm+ " -l .\\model_"+project+".model -T "+testingArff+" >"+outTxt)


def BuildAndEval(project,projects,transferDir,wekaJar):
    for buggedType in ["All","Most"]:
        for component in ["Files","Methods"]:
            Path=os.path.join(transferDir,buggedType+component)
            arff=os.path.join(Path,"training")
            arff=os.path.join(arff,project+".arff")
            buildModel(Path,arff,project,wekaJar)
            testing=os.path.join(Path,"testing")
            outPath=os.path.join(Path,"out")
            outPath=os.path.join(outPath,project)
            for p in projects:
                testingArff=os.path.join(testing,p+".arff")
                outTxt=os.path.join(outPath,p+".txt")
                evalModel(Path,testingArff,outTxt,wekaJar,project)


def resDictToCsv(dict, projects,outPath):
    lines=[[[""]+projects]]
    for p1 in projects:
        p1_lines=[p1]
        for p2 in projects:
            p1_lines.append(dict[p1][p2])
        lines.append(p1_lines)
    with open(outPath, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(lines)

def results(projects,transferDir):
    for buggedType in ["All","Most"]:
        for component in ["Files","Methods"]:
            Path=os.path.join(transferDir,buggedType+component)
            outPath=os.path.join(Path,"out")
            outCsv=Path+".csv"
            dict_AUC={}
            for project in projects:
                outPath=os.path.join(outPath,project)
                dict_AUC[project]={}
                for p in projects:
                    outTxt=os.path.join(outPath,p+".txt")
                    parsedDict=wekaMethods.ParseWekaOutput.Parse(outTxt)
                    dict_AUC[project][p]=parsedDict["both"]["ROC Area"]
            resDictToCsv(dict_AUC,projects,outCsv)


def transferLearning(projectsConfs, globalConf,transferDir):
    projectsNamesWeka=[ ConfFileTowekaPathName(x) for x in projectsConfs]
    docletPath,sourceMonitorEXE,checkStyle57,checkStyle68,allchecks,methodsNamesXML,wekaJar,RemoveBat,utilsPath=utilsConf.globalConfig()
    Mkdirs(transferDir,projectsNamesWeka)
    for project in projectsNamesWeka:
        copyArffs(project,transferDir)
    projects=[x[0] for x in projectsNamesWeka]
    for project in projects:
        BuildAndEval(project,projects,transferDir,wekaJar)
    results(projects,transferDir)


if __name__ == '__main__':
    args=list(sys.argv)[1:]
    args=["D:\\Amir_Almishali\\projs\\"+x+"Conf.txt" for x in args]
    transferLearning(args,"D:\\Amir_Almishali\\projs\\Debugger\\globalConf.txt","D:\\Amir_Almishali\\projs\\Transfer")
