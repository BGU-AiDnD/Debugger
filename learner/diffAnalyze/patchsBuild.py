__author__ = 'amir'


import sys
import os
import glob
import comments
import re

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

def OneClass(lines, outPath):
    fileName=lines[0].split()[2]
    fileName=fileName[2:]
    fileName=fileName.replace("/","_")
    if len(lines) >3:
        isNew="new file " in lines[1]
        isdeleted="deleted file " in lines[1]
        reducedFile=lines[3]
        addedFile=lines[4]
        lines=lines[6:]
        befLines=[]
        afterLines=[]
        deletedInds=[]
        addedInds=[]
        delind=0
        addind=0
        for l in lines:
            replaced=re.sub('@@(-|\+|,| |[0-9])*@@','',l)
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

        bef=open(outPath+"\\before\\"+fileName,"wb")
        bef.writelines(befLines)
        bef.close()
        af=open(outPath+"\\after\\"+fileName,"wb")
        af.writelines(afterLines)
        af.close()
        af=open(outPath+"\\"+fileName,"wb")
        af.writelines(["deleted\n",str(deletedInds)+"\n","added\n",str(addedInds)])
        af.close()




def oneFile(PatchFile, outDir):
    f=open(PatchFile,'r')
    lines=f.readlines()
    if len(lines)==0:
        return
    commitID=lines[0].split()[1] # line 0 word 1
    mkDirs(outDir,commitID)
    inds=[lines.index(l) for l in lines if "diff --git" in l]+[len(lines)] #lines that start with diff --git
    CopyStatement = "cmd /x /c \"c: & copy " + PatchFile+"  " + outDir+"\\"+commitID+"\\"+PatchFile.split("\\")[-1]+"\""
    os.system(CopyStatement)

    for i in range(len(inds)-1):
        OneClass(lines[inds[i]:inds[i+1]],outDir+"\\"+commitID)


#oneFile("C:\GitHub\\try\org.eclipse.cdt\\0244-Rename-DebugConfiguration-to-avoid-duplicate-names.patch","C:\GitHub\\try\org.eclipse.cdt\\p")

def build(Path):
    lst= glob.glob(Path+"/*.patch")
    i=0
    for doc in lst:
        print doc
        i=i+1
        oneFile(doc,Path+"\\patchReg")

#build("C:\GitHub\\try\org.eclipse.cdt")
#build("C:\\tomcat\code\\try\\tomcat8")