__author__ = 'amir'

import os
import sys
import csv
import utilsConf
import shutil
import wekaMethods.ParseWekaOutput
import transferLearning

def mkOneDir(dir):
    if not os.path.isdir(dir):
            os.mkdir(dir)

def Mkdirs(workingDir,projects):
    mkOneDir(workingDir)
    for d in ["AllFiles","AllMethods","MostFiles","MostMethods"]:
        Path1=os.path.join(workingDir,d)
        mkOneDir(Path1)
        for family in ["Fam_One","Fam_All"]:
            Path=os.path.join(Path1,family)
            mkOneDir(Path)
            for name,wekaPath in projects:
                pro=os.path.join(Path,name)
                mkOneDir(pro)
                for type in ["Appended","Only"]:
                    training=os.path.join(pro,type)
                    mkOneDir(training)
            out=os.path.join(Path,"out")
            mkOneDir(out)
            for name,wekaPath in projects:
                pro=os.path.join(out,name)
                mkOneDir(pro)
                for name,wekaPath in projects:
                    pro1=os.path.join(pro,name)
                    mkOneDir(pro1)

def copyByType(sourceD,destD,type):
    for i in range(17):
        source = os.path.join(sourceD, str(i) + "_" + type + ".arff")
        dest = os.path.join(destD, str(i) + "_" + type + ".arff")
        if os.path.exists(source):
            shutil.copyfile(source, dest)

def copyArffs(project,transferDir):
    name,wekaPath=project
    for buggedType in ["All","Most"]:
        for component in ["Files","Methods"]:
            for family in ["Fam_One","Fam_All"]:
                sourceD=os.path.join(os.path.join(os.path.join(wekaPath,buggedType),component),family)
                for training in ["Appended","Only"]:
                    destD=os.path.join(os.path.join(os.path.join(os.path.join(transferDir,buggedType+component),family),name),training)
                    copyByType(sourceD,destD,training)

def ConfFileTowekaPathName(conf):
    vers, gitPath,bugsPath, workingDir=utilsConf.configure(conf)
    name=conf.split("\\")[-1].replace("Conf.txt","")
    print name,workingDir
    return name,workingDir


def writeBatchFile(outF):
    data="""REM params: <Train>  <projectsDir> <model> <outDir>
REM Build one model
REM delete model
REM evaluate on other projects > outDir
for /L %%a   in (0,1,16) do (
call java -Xmx2024m  -cp "C:\Program Files\Weka-3-7\weka.jar" weka.Run weka.classifiers.trees.RandomForest -I 1000 -K 0 -S 1 -num-slots 1  -t %1\%%a_Appended.arff -x 10 -d %3
For %%p in (ant,cdt,poi,jackson-databind,orientdb) do (
call java -Xmx4048m  -cp "C:\Program Files\Weka-3-7\weka.jar" weka.Run weka.classifiers.trees.RandomForest  -l %6 -T %2\%%p\Only\%%a_Only.arff   > %4\%%p\%%a.txt
)
del /F %4
)
    """
    f=open(outF,"wb")
    f.write(data)
    f.close()



def BuildAndEval(project,transferDir,AllOnebat):
    for buggedType in ["All","Most"]:
        for component in ["Files","Methods"]:
            for family in ["Fam_One","Fam_All"]:
                FamilyDir = os.path.join(os.path.join(transferDir, buggedType + component), family)
                outDir = os.path.join(os.path.join(FamilyDir, "out"),project)
                model = os.path.join(FamilyDir, "model.model")
                trainFile=os.path.join(os.path.join(FamilyDir,project),"Appended")
                params=[trainFile,FamilyDir,model,outDir]
                params=" ".join(params)
                bat_run = "start /b cmd /x /c \" "+AllOnebat+" " + params +"\""
                os.system(bat_run)





def transferAllOne(projectsConfs, globalConf,transferDir):
    projectsNamesWeka=[ ConfFileTowekaPathName(x) for x in projectsConfs]
    Mkdirs(transferDir,projectsNamesWeka)
    #for project in projectsNamesWeka:
    #    copyArffs(project,transferDir)
    projects=[x[0] for x in projectsNamesWeka]
    AllOnebat = os.path.join(transferDir, "AllOne.bat")
    writeBatchFile(AllOnebat)
    for project in projects:
        BuildAndEval(project,transferDir,AllOnebat)

if __name__ == '__main__':
    args=list(sys.argv)[1:]
    args=["D:\\Amir_Almishali\\projs\\"+x+"Conf.txt" for x in args]
    transferAllOne(args,"D:\\Amir_Almishali\\projs\\Debugger\\globalConf.txt","D:\\Amir_Almishali\\projs\\TransferAllOne")

