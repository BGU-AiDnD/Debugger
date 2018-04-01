__author__ = 'amir'
import shutil
import os
import glob
import utilsConf
import re
import subprocess
import sqlite3

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
    print(javaFile)
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


def OneClass(lines, outPath,commitID):
    fileName=lines[0].split()[2]
    fileName=fileName[2:]
    fileName=fileName.replace("/","_")
    if not ".java" in fileName:
        return []
    if len(lines) >3:
        isNew="new file " in lines[1]
        isdeleted="deleted file " in lines[1]
        reducedFile=lines[3]
        addedFile=lines[4]
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
            if "enum =" in l:
                l=l.replace("enum =","enumAmir =")
            if "enum." in l:
                l=l.replace("enum.","enumAmir.")
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

        beforeFile=outPath+"\\before\\"+fileName
        bef=open(beforeFile,"wb")
        bef.writelines(befLines)
        bef.close()
        AfterFile=outPath+"\\after\\"+fileName
        af=open(AfterFile,"wb")
        af.writelines(afterLines)
        af.close()
        af=open(outPath+"\\"+fileName,"wb")
        af.writelines(["deleted\n",str(deletedInds)+"\n","added\n",str(addedInds)])
        af.close()
        #methodsData=FileToMethods(beforeFile,AfterFile,deletedInds,addedInds, outPath+"\\parser\\"+fileName,commitID)
        #ans.extend(methodsData)


def oneFile(PatchFile, outDir):
    lines = []
    with open(PatchFile) as f:
        lines = f.readlines()
    if len(lines) == 0:
        return []
    commitID=lines[0].split()[1] # line 0 word 1
    commitID=str(int("".join(list(commitID)[:7]), 16))
    mkDirs(outDir, commitID)
    inds = [ind for ind, l in lines if "diff --git" in l] + [len(lines)] #lines that start with diff --git
    shutil.copy(PatchFile, os.path.join(outDir, commitID, os.path.basename(PatchFile)))
    for i in range(len(inds)-1):
        OneClass(lines[inds[i]:inds[i+1]], os.path.join(outDir, commitID), commitID)


def mkdir(d):
    if not os.path.isdir(d):
        os.mkdir(d)


def buildPatchs(Path,outDir):
    mkdir(outDir)
    allComms = []
    for doc in glob.glob(os.path.join(Path, "*.patch")):
        allComms.extend(oneFile(doc, outDir))
    return allComms


def DbAdd(dbPath,allComms):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    c.execute('''CREATE TABLE commitedMethods (commitID INT, methodDir text, fileName text, methodName text, deletions INT , insertions INT , lines INT )''')
    for com in allComms:
        c.execute("INSERT INTO commitedMethods VALUES (?,?,?,?,?,?,?)",com)
    conn.commit()
    conn.close()

def RunCheckStyle(workingDir,outPath):
    os.system(  "java  -jar  C:\projs\checkstyle-6.8-SNAPSHOT-all.jar   -c  C:\projs\methodNameLines.xml javaFile -o " +outPath+"  "+workingDir)

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


def checkStyleCreateDict(lines):
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
            dataFile = file.replace("before\\", "")
            deleted, insertions = readDataFile(dataFile)
            inds = deleted
        if "after" in file:
            key = "insertions"
            dataFile = file.replace("after\\", "")
            deleted, insertions = readDataFile(dataFile)
            inds = insertions
        name, begin, end = data.split("@")
        rng = [str(x) for x in range(int(begin), int(end) + 2)]
        keyChange = len(set(rng) & set(inds))
        both=[x for x in inds if x in rng]
        keyChange = len(both)
        if keyChange==0:
            continue
        if "XWPFHyperlinkDecorator" in dataFile and "100517180" in dataFile:
            print key,keyChange,rng,inds, both, readDataFile(dataFile) , dataFile
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


def analyzeCheckStyle(checkOut):
    f=open(checkOut,"r")
    lines=f.readlines()
    f.close()
    lines=lines[1:-3]
    ans=[]
    methods=checkStyleCreateDict(lines)
    for methodDir  in methods:
        dels=0
        ins=0
        fileName=""
        methodName=""
        commitID=""
        if "deletions" in methods[methodDir]:
            dels=methods[methodDir]["deletions"]
        if "insertions" in methods[methodDir]:
            ins=methods[methodDir]["insertions"]
        if "fileName" in methods[methodDir]:
            fileName=methods[methodDir]["fileName"]
        if "methodName" in methods[methodDir]:
            methodName=methods[methodDir]["methodName"]
        if "commitID" in methods[methodDir]:
            commitID=methods[methodDir]["commitID"]
        row=[commitID,methodDir,fileName,methodName,str(dels),str(ins),str(dels+ins)]
        ans.append(row)
    return ans



def do_all(workingDir):
    patchD = os.path.join(workingDir, "patch")
    commitsFiles = os.path.join(workingDir, "commitsFiles")
    mkdir(patchD)
    mkdir(commitsFiles)
    run_commands = ["git", "format-patch", "--root", "-o", "patch", "--function-context", "--unified=9000"]
    p = subprocess.Popen(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=utilsConf.to_short_path(workingDir))
    p.communicate()
    buildPatchs(patchD, commitsFiles)
    checkOut = os.path.join(commitsFiles, "CheckStyle.txt")
    run_commands = ["java", "-jar", utilsConf.globalConfig()[3], "-c", utilsConf.globalConfig()[5], "javaFile", "-o", checkOut, commitsFiles]
    p = subprocess.Popen(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                         cwd=utilsConf.to_short_path(workingDir))
    p.communicate()
    allComms = analyzeCheckStyle(checkOut)
    return allComms



if __name__ == '__main__':
    #build("C:\GitHub\\try\org.eclipse.cdt")
    #build("C:\\tomcat\code\\try\\tomcat8","C:\\tomcat\code\\try\\tomcat8")
    #do_all("C:\projs\\antWorking\\antC")
    do_all("C:\Users\User\Downloads\poi")
    #mkDirs("C:\projs\\antWorking\\antC\CommitsFiles","amir")
    #oneFile("C:\projs\\antWorking\\antC\CommitsFiles\\282f346ca230a8dec8d1956af05fcc9d511ad672\\0007-Misc-doc-scoping-style-and-error-recovery-issues.patch","C:\projs\\antWorking\\antC\CommitsFiles\\amir")