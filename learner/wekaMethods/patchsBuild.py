__author__ = 'amir'


import sys
import os
import glob
import re
import subprocess
import shutil
import sqlite3
import utilsConf

# git format-patch --root origin

def mkDirs(outDir,commitID):
    o=outDir+"\\"+commitID
    if not (os.path.isdir(o)):
        os.mkdir(o)
    o=outDir+"\\"+commitID+"\\before"
    if not (os.path.isdir(o)):
        os.mkdir(o)
    o=outDir+"\\"+commitID+"\\after"
    if not (os.path.isdir(o)):
        os.mkdir(o)
    o=outDir+"\\"+commitID+"\\parser"
    if not (os.path.isdir(o)):
        os.mkdir(o)


def oneFileParser(methods,javaFile,inds,key):
    if not ".java" in javaFile:
        return
    f=open(javaFile)
    lines=f.readlines()
    f.close()
    if len([l for l in lines if l.lstrip()!=""])==0:
        return
    run_commands = ["java", "-jar", "C:\projs\checkstyle-6.8-SNAPSHOT-all.jar ", "-c", "C:\projs\methodNameLines.xml",
             javaFile]
    proc = subprocess.Popen(run_commands, stdout=subprocess.PIPE, shell=True,cwd=r'C:\projs')
    (out, err) = proc.communicate()
    out=out.replace("\n","").split("\r")[1:-3]
    fileName=javaFile.split("\\")[-1]
    fileName=fileName.replace("_","\\")
    for o in  out:
        if o=="":
            continue
        if not "@" in o:
            continue
        file,data=o.split(" ")
        name,begin,end=data.split("@")
        methodDir=fileName+"$"+name
        if not methodDir in methods:
            methods[methodDir]={}
        if not "methodName" in methods[methodDir]:
            methods[methodDir]["methodName"]=name
        if not "fileName" in methods[methodDir]:
            methods[methodDir]["fileName"]=fileName
        rng=range(int(begin),int(end)+1)
        if methodDir not in methods:
            methods[methodDir]={}
        methods[methodDir][key]=len(list(set(rng) & set(inds)))



def FileToMethods(beforeFile,AfterFile,deletedInds,addedInds, outPath,commitID):
    methods={}
    oneFileParser(methods,beforeFile,deletedInds,"deleted")
    oneFileParser(methods,AfterFile,addedInds,"inserted")
    f=open(outPath,"w")
    for methodDir  in methods:
        dels=0
        ins=0
        fileName=""
        methodName=""
        if "deleted" in methods[methodDir]:
            dels=methods[methodDir]["deleted"]
        if "inserted" in methods[methodDir]:
            ins=methods[methodDir]["inserted"]
        if "fileName" in methods[methodDir]:
            fileName=methods[methodDir]["fileName"]
        if "methodName" in methods[methodDir]:
            methodName=methods[methodDir]["methodName"]
        row=[commitID,methodDir,fileName,methodName,str(dels),str(ins),str(dels+ins)]
        f.write(",".join(row))
    f.close()


def fixEnum(l):
    if "enum =" in l:
        l=l.replace("enum =","enumAmir =")
    if "enum=" in l:
        l=l.replace("enum=","enumAmir=")
    if "enum," in l:
        l=l.replace("enum,","enumAmir,")
    if "enum." in l:
        l=l.replace("enum.","enumAmir.")
    if "enum;" in l:
        l=l.replace("enum;","enumAmir;")
    if "enum)" in l:
        l=l.replace("enum)","enumAmir)")
    return l


def fixAssert(l):
    if "assert " in l:
        l=l.replace("assert ","assertAmir ")
        if ":" in l:
            l=l.replace(":",";//")
    if "assert(" in l:
        l=l.replace("assert(","assertAmir(")
        if ":" in l:
            l=l.replace(":",";//")
    return l


def OneClass(lines, outPath,commitID,change):
    if len(lines)==0:
        return []
    fileName=lines[0].split()
    if len(fileName)<3:
        return []
    fileName = lines[0].split()[2]
    fileName = fileName[2:]
    fileName = os.path.normpath(fileName).replace(os.path.sep,"_")
    if not ".java" in fileName:
        return []
    fileName = fileName.split('.java')[0] + '.java'
    if len(lines) > 3:
        # isNew="new file " in lines[1]
        # isdeleted="deleted file " in lines[1]
        # reducedFile=lines[3]
        # addedFile=lines[4]
        lines=lines[5:]
        befLines=[]
        afterLines=[]
        deletedInds=[]
        addedInds=[]
        delind=0
        addind=0
        for l in lines:
            if "\ No newline at end of file" in l:
                continue
            if "1.9.4.msysgit.2" in l:
                continue
            if "- \n"== l:
                continue
            if "-- \n"== l:
                continue
            l=fixEnum(l)
            l=fixAssert(l)
            replaced=re.sub('@@(-|\+|,| |[0-9])*@@','',l)
            if replaced.startswith("*"):
                replaced="\\"+replaced
            if replaced.startswith("+"):
               afterLines.append(replaced[1:])
               addedInds.append(addind)
               addind=addind+1
            elif replaced.startswith("-"):
               befLines.append(replaced[1:])
               deletedInds.append(delind)
               delind=delind+1
            else:
                afterLines.append(replaced)
                befLines.append(replaced)
                delind=delind+1
                addind=addind+1
        with open(os.path.join(outPath, "before", fileName), "wb") as bef:
            bef.writelines(befLines)
        with open(os.path.join(outPath, "after", fileName), "wb") as after:
            after.writelines(afterLines)
        with open(os.path.join(outPath, fileName + "_deletsIns.txt"), "wb") as f:
            f.writelines(["deleted\n", str(deletedInds)+"\n","added\n", str(addedInds)])
        change.write(fileName+"@"+str(commitID)+"@"+str(deletedInds)+"@"+str(addedInds)+"\n")


def oneFile(PatchFile, outDir,change):
    f=open(PatchFile,'r')
    lines=f.readlines()
    if len(lines)==0:
        return []
    commitSha=lines[0].split()[1] # line 0 word 1
    commitID=str(commitSha)
    mkDirs(outDir, commitID)
    inds=[lines.index(l) for l in lines if "diff --git" in l]+[len(lines)] #lines that start with diff --git
    shutil.copyfile(PatchFile, outDir+"\\"+commitID+"\\"+PatchFile.split("\\")[-1])
    for i in range(len(inds)-1):
        OneClass(lines[inds[i]:inds[i+1]],outDir+"\\"+commitID,commitID,change)
    return commitSha





def debugPatchs(Path,outFile):
    lst= glob.glob(Path+"/*.patch")
    i=0
    allComms=[]
    ou=open(outFile,"wt")
    for doc in lst:
        i=i+1
        f=open(doc,'r')
        lines=f.readlines()[:9]
        ou.writelines(lines)
    ou.close()


def buildPatchs(Path,outDir,changedFile):
    lst= glob.glob(Path+"/*.patch")
    i=0
    if not os.path.isdir(outDir):
        os.mkdir(outDir)
    allComms=[]
    change=open(changedFile,"wb")
    for doc in lst:
        i=i+1
        print doc
        comm=oneFile(doc,outDir,change)
        allComms.append(comm)

def mkdir(d):
    if not os.path.isdir(d):
        os.mkdir(d)


def DbAdd(dbPath,allComms):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    c.execute('''CREATE TABLE commitedMethods (commitID INT, methodDir text, fileName text, methodName text, deletions INT , insertions INT , lines INT )''')
    for com in allComms:
        c.execute("INSERT INTO commitedMethods VALUES (?,?,?,?,?,?,?)",com)
    conn.commit()
    conn.close()

def RunCheckStyle(workingDir,outPath,checkStyle68,methodNameLines):
    run_commands = ["java" ,"-jar" ,checkStyle68 ,"-c" ,methodNameLines ,"javaFile" ,"-o",outPath,workingDir]
    proc = subprocess.Popen(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

def detectFromConf(lines,lineInd):
    deleted = (lines[lineInd])
    deleted = deleted.replace("[","").replace("]","").replace("\n","")
    deleted = deleted.split(",")
    return [x.lstrip() for x in deleted]


def readDataFile(Dfile):
    f=open(Dfile,"r")
    lines=f.readlines()
    f.close()
    deleted=detectFromConf(lines,1)
    insertions=detectFromConf(lines,3)
    return deleted,insertions


def checkStyleCreateDict(checkOut, changesDict):
    methods = {}
    lines = []
    with open(checkOut, "r") as f:
        lines = f.readlines()[1:-3]
    for line in lines:
        if line == "":
            continue
        if not "@" in line:
            continue
        if not len(line.split(" ")) == 2:
            # case of error
            continue
        file, data = line.split(" ")
        file = file.split(".java")[0]+".java"
        fileNameSplited = file.split(os.path.sep)
        fileName = fileNameSplited[-1].replace("_", os.path.sep)
        commitID = fileNameSplited[fileNameSplited.index("commitsFiles") + 1]
        key = ""
        inds = []
        dataFile=""
        if "before" in file:
            key = "deletions"
            dataFile = file.replace("before\\", "")+"_deletsIns.txt"
            if not (fileName, commitID) in changesDict:
                continue
            deleted, insertions = changesDict[(fileName,commitID)]
            inds = deleted
        if "after" in file:
            key = "insertions"
            dataFile = file.replace("after\\", "")+"_deletsIns.txt"
            #deleted, insertions = readDataFile(dataFile)
            if not (fileName,commitID) in changesDict:
                continue
            deleted, insertions = changesDict[(fileName,commitID)]
            inds = insertions
        name, begin, end = data.split("@")
        rng = map(str, range(int(begin)-1, int(end)))
        both = filter(lambda x: x in rng, inds)
        keyChange = len(both)
        if keyChange == 0:
            continue
        methodDir = fileName + "$" + name
        tup = (methodDir, commitID)
        if not tup in methods:
            methods[tup] = {}
        methods[tup][key] = keyChange
        if not "methodName" in methods[tup]:
            methods[tup]["methodName"] = name
        if not "fileName" in methods[tup]:
            methods[tup]["fileName"] = fileName
        if not "commitID" in methods[tup]:
            methods[tup]["commitID"] = commitID
    return methods


def readChangesFile(change):
    dict = {}
    rows = []
    with open(change, "r") as f:
        for line in f:
            fileName, commitSha, dels, Ins = line.strip().split("@")
            fileName = fileName.replace("_", os.path.sep)
            dict[(fileName, commitSha)] = [eval(dels), eval(Ins)]
            rows.append(map(str, [fileName,commitSha, len(dels), len(Ins), len(dels)+len(Ins)]))
    return dict, rows


def analyzeCheckStyle(checkOut, changeFile):
    changesDict, filesRows = readChangesFile(changeFile)
    methods = checkStyleCreateDict(checkOut, changesDict)
    ans = []
    for tup in methods:
        methodDir = tup[0]
        dels = methods[tup].getdefault("deletions", 0)
        ins = methods[tup].getdefault("insertions", 0)
        fileName = methods[tup].getdefault("fileName", "")
        methodName = methods[tup].getdefault("methodName", "")
        commitID = methods[tup].getdefault("commitID", "")
        ans.append(map(str, [commitID, methodDir, fileName, methodName, dels, ins, dels+ins]))
    return ans, filesRows


# @utilsConf.marker_decorator(utilsConf.PATCHS_FEATURES_MARKER)
def do_all(workingDir, checkStyle68, methodNameLines):
    patchD = os.path.join(workingDir, "patch")
    commitsFiles = os.path.join(workingDir, "commitsFiles")
    changedFile = os.path.join(workingDir, "commitsFiles", "Ins_dels.txt")
    mkdir(patchD)
    mkdir(commitsFiles)
    run_commands = "git format-patch --root -o patch --function-context --unified=9000".split()
    proc = subprocess.Popen(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=utilsConf.to_short_path(workingDir))
    proc.communicate()
    buildPatchs(patchD, commitsFiles, changedFile)
    checkOut = os.path.join(commitsFiles, "CheckStyle.txt")
    RunCheckStyle(commitsFiles, checkOut, checkStyle68, methodNameLines)
