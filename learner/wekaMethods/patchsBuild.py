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
    fileName=lines[0].split()[2]
    fileName=fileName[2:]
    fileName=fileName.replace("/","_")
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

        beforeFile = os.path.join(outPath, "before", fileName)
        AfterFile = os.path.join(outPath, "after", fileName)
        delsIns = os.path.join(outPath, fileName + "_deletsIns.txt")
        with open(beforeFile,"w+") as bef:
            bef.writelines(befLines)
        with open(AfterFile, "w+") as after:
            after.writelines(afterLines)
        with open(delsIns, "w+") as f:
            f.writelines(["deleted\n",str(deletedInds)+"\n","added\n",str(addedInds)])
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
    proc = subprocess.Popen(run_commands, stdout=subprocess.PIPE, shell=True)
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


def checkStyleCreateDict2(lines ):
    methods={}
    for o in lines:
        if o == "":
            continue
        if not "@" in o:
            continue
        file, data = o.split(" ")
        file=file.split(".java")[0]+".java"
        key = ""
        inds = []
        dataFile=""
        if "before" in file:
            key = "deletions"
            dataFile = file.replace("before\\", "")+"_deletsIns.txt"
            deleted, insertions = readDataFile(dataFile)
            inds = deleted
        if "after" in file:
            key = "insertions"
            dataFile = file.replace("after\\", "")+"_deletsIns.txt"
            deleted, insertions = readDataFile(dataFile)
            inds = insertions
        name, begin, end = data.split("@")
        rng = [str(x) for x in range(int(begin)-1, int(end) )]
        both=[x for x in inds if x in rng]
        keyChange = len(both)
        if keyChange==0:
            continue
        fileNameSplited = file.split("\\")
        fileName = fileNameSplited[-1].replace("_", "\\")
        commitID = fileNameSplited[fileNameSplited.index("commitsFiles") + 1]
        methodDir = fileName + "$" + name
        if not methodDir in methods:
            methods[methodDir] = {}
        methods[methodDir][key] = keyChange
        if not "methodName" in methods[methodDir]:
            methods[methodDir]["methodName"] = name
        if not "fileName" in methods[methodDir]:
            methods[methodDir]["fileName"] = fileName
        if not "commitID" in methods[methodDir]:
            methods[methodDir]["commitID"] = commitID
    return methods



def checkStyleCreateDictDebug(lines,Ids,insides ):
    methods={}
    insideCounter=set()
    for o in lines:
        if o == "":
            continue
        if not "@" in o:
            continue
        file, data = o.split(" ")
        file=file.split(".java")[0]+".java"
        fileNameSplited = file.split("\\")
        commitID = fileNameSplited[fileNameSplited.index("commitsFiles") + 1]
        if Ids !=[]:
            if not commitID in Ids:
                continue
        if commitID in insides:
            insideCounter.add(commitID)
        key = ""
        inds = []
        dataFile=""
        if "before" in file:
            key = "deletions"
            dataFile = file.replace("before\\", "")+"_deletsIns.txt"
            deleted, insertions = readDataFile(dataFile)
            inds = deleted
        if "after" in file:
            key = "insertions"
            dataFile = file.replace("after\\", "")+"_deletsIns.txt"
            deleted, insertions = readDataFile(dataFile)
            inds = insertions
        name, begin, end = data.split("@")
        rng = [str(x) for x in range(int(begin)-1, int(end) )]
        both=[x for x in inds if x in rng]
        keyChange = len(both)
        if keyChange==0:
            continue
        fileNameSplited = file.split("\\")
        fileName = fileNameSplited[-1].replace("_", "\\")
        methodDir = fileName + "$" + name
        tup=(methodDir,commitID)
        if tup in methods and methods[tup]["commitID"]!= commitID:
            print "bug!!!!"
        if not tup in methods:
            methods[tup] = {}
        methods[tup][key] = keyChange
        if not "methodName" in methods[tup]:
            methods[tup]["methodName"] = name
        if not "fileName" in methods[tup]:
            methods[tup]["fileName"] = fileName
        if not "commitID" in methods[tup]:
            methods[tup]["commitID"] = commitID
    print "insideCounter",len(insideCounter)
    return methods


def checkStyleCreateDict(lines ,changesDict):
    methods={}
    for o in lines:
        if o == "":
            continue
        if not "@" in o:
            continue
        file, data = o.split(" ")
        file=file.split(".java")[0]+".java"
        fileNameSplited = file.split("\\")
        fileName = fileNameSplited[-1].replace("_", "\\")
        commitID = fileNameSplited[fileNameSplited.index("commitsFiles") + 1]
        key = ""
        inds = []
        dataFile=""
        if "before" in file:
            key = "deletions"
            dataFile = file.replace("before\\", "")+"_deletsIns.txt"
            #deleted, insertions = readDataFile(dataFile)
            if not (fileName,commitID) in changesDict:
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
        rng = [str(x) for x in range(int(begin)-1, int(end) )]
        both=[x for x in inds if x in rng]
        keyChange = len(both)
        if keyChange==0:
            continue
        fileNameSplited = file.split("\\")
        fileName = fileNameSplited[-1].replace("_", "\\")
        commitID = fileNameSplited[fileNameSplited.index("commitsFiles") + 1]
        methodDir = fileName + "$" + name
        tup=(methodDir,commitID)
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
    f=open(change,"r")
    lines=[x.split("\n")[0] for x in f.readlines()]
    f.close()
    dict={}
    rows=[]
    for x in lines:
        fileName,commitSha,dels,Ins=x.split("@")
        fileName=fileName.replace("_", "\\")
        dels=[x.lstrip() for x in dels.replace("[","").replace("]","").split(",")]
        Ins=[x.lstrip() for x in Ins.replace("[","").replace("]","").split(",")]
        dict[(fileName,commitSha)]=[dels,Ins]
        rows.append([fileName,commitSha,str(len(dels)),str(len(Ins)),str(len(dels)+len(Ins))])
    return dict,rows



def analyzeCheckStyle(checkOut,changeFile):
    f=open(checkOut,"r")
    lines=f.readlines()
    f.close()
    lines=lines[1:-3]
    ans=[]
    changesDict,filesRows=readChangesFile(changeFile)
    methods=checkStyleCreateDict(lines,changesDict)
    for tup  in methods:
        methodDir,comm=tup
        dels=0
        ins=0
        fileName=""
        methodName=""
        commitID=""
        if "deletions" in methods[tup]:
            dels=methods[tup]["deletions"]
        if "insertions" in methods[tup]:
            ins=methods[tup]["insertions"]
        if "fileName" in methods[tup]:
            fileName=methods[tup]["fileName"]
        if "methodName" in methods[tup]:
            methodName=methods[tup]["methodName"]
        if "commitID" in methods[tup]:
            commitID=methods[tup]["commitID"]
        row=[commitID,methodDir,fileName,methodName,str(dels),str(ins),str(dels+ins)]
        ans.append(row)
    return ans,filesRows


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



if __name__ == '__main__':
    do_all(r"C:\Users\User\Downloads\poi", r"C:\Users\User\Documents\GitHub\Debugger\utils\checkstyle-6.8-SNAPSHOT-all.jar", r"C:\Users\User\Documents\GitHub\Debugger\utils\methodNameLines.xml")
    exit()
    patch_file = r"C:\Users\User\Downloads\antWorking\repo\patch\12906-adapting-code-and-tests-since-Apt-is-not-available-.patch"
    patch_file = r"C:\Users\User\Downloads\antWorking\repo\patch\2125-Fix-up-packaging-of-bzip-utilities.patch"
    f=open(patch_file, "wb")
    oneFile(patch_file,r"C:\Users\User\Downloads\\p",f)

    #build("C:\GitHub\\try\org.eclipse.cdt")
    #build("C:\\tomcat\code\\try\\tomcat8","C:\\tomcat\code\\try\\tomcat8")
    #do_all("C:\projs\\antWorking\\antC")
    #do_all("C:\\projs\\poi2Working\\poi")
    #do_all("C:\\projs\\grizMasterWorking\\repo")
    #do_all("C:\projs\ptry\\repo")
    """
    ans,filesRows=analyzeCheckStyle("C:\projs\ptry\\repo\commitsFiles\\CheckStyle.txt","C:\projs\ptry\\repo\commitsFiles\\Ins_dels.txt")
    s=set()
    for f in filesRows:
        s.add(f[1])
    print len(s), len(filesRows)
    """
    #debugPatchs("C:\\projs\\ant5Working\\repo\patch","C:\\projs\\ant5Working\\repo\patchHeads.txt")
    #buildPatchs("C:\\projs\\grizMasterWorking\\repo\\patch","C:\\projs\\grizMasterWorking\\repo\\commitsFiles2")
    #buildPatchs("C:\\projs\\grizMasterWorking\\repo\\patch","C:\\projs\\grizMasterWorking\\repo\\commitsFiles2")
    #mkDirs("C:\projs\\antWorking\\antC\CommitsFiles","amir")
    #oneFile("C:\projs\\antWorking\\antC\CommitsFiles\\282f346ca230a8dec8d1956af05fcc9d511ad672\\0007-Misc-doc-scoping-style-and-error-recovery-issues.patch","C:\projs\\antWorking\\antC\CommitsFiles\\amir")