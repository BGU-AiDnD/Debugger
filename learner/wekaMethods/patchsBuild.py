__author__ = 'amir'


import os
import glob
import re
import subprocess
import shutil
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


def OneClass(diff_lines, outPath, commitID, change):
    REMOVED = '---'
    ADDED = '+++'
    DEV_NULL = '/dev/null'
    diff_files = diff_lines[0].split()
    if len(diff_files) < 3:
        assert False
    if len(filter(lambda x: x.startswith(REMOVED), diff_lines)) != 1:
        return
    removed_file_name = filter(lambda x: x.startswith(REMOVED), diff_lines)[0].split()[1]
    added_file_name = filter(lambda x: x.startswith(ADDED), diff_lines)[0].split()[1]
    is_new_file = 1 if removed_file_name == DEV_NULL else 0
    is_deleted_file = 1 if added_file_name == DEV_NULL else 0
    is_renamed_file = 1 if not is_deleted_file and not is_new_file and added_file_name[2:] != removed_file_name[2:] else 0
    is_removed_file = 1 if is_renamed_file or is_deleted_file else 0
    file_names = [(added_file_name, 0)] + ([(removed_file_name, 1)] if is_removed_file else [])
    for name, removed in file_names:
        fileName = os.path.normpath(name[2:]).replace(os.path.sep, "_")
        if not fileName.endswith('.java'):
            continue
        start_line = filter(lambda line: line[1].startswith('+++'), enumerate(diff_lines))
        if len(start_line) != 1:
            return # no file
        diff_lines = diff_lines[start_line[0][0] + 1:]
        befLines=[]
        afterLines=[]
        deletedInds=[]
        addedInds=[]
        delind=0
        addind=0
        for l in diff_lines:
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
            f.writelines('\n'.join(map(str, ["deleted", deletedInds, "added", addedInds, is_new_file, removed, is_renamed_file])))
        change.write("@".join(map(str, [fileName, commitID, deletedInds, addedInds, is_new_file, removed, is_renamed_file])) + "\n")


def oneFile(PatchFile, outDir, change):
    with open(PatchFile,'r') as f:
        lines = f.readlines()[:-3]
    if len(lines) == 0:
        return
    commitID = str(lines[0].split()[1]) # line 0 word 1
    mkDirs(outDir, commitID)
    diffs = map(lambda x: x[0], filter(lambda x: x[1].startswith("diff --git"), enumerate(lines))) + [len(lines)]
    diff_lines = map(lambda diff: lines[diff[0]: diff[1]],zip(diffs, diffs[1:]))
    shutil.copyfile(PatchFile, os.path.join(outDir, commitID, os.path.basename(PatchFile)))
    for diff in diff_lines:
        if len(diff) == 0:
            assert False
        OneClass(diff, os.path.join(outDir, commitID), commitID, change)


def buildPatchs(Path,outDir,changedFile):
    with open(changedFile, "wb") as change:
        for patch in glob.glob(os.path.join(Path,"*.patch")):
            oneFile(patch, outDir, change)

def mkdir(d):
    if not os.path.isdir(d):
        os.mkdir(d)

def RunCheckStyle(workingDir, outPath, checkStyle68, methodNameLines):
    run_commands = ["java" ,"-jar" ,checkStyle68 ,"-c" ,methodNameLines ,"javaFile" ,"-o",outPath,workingDir]
    utilsConf.open_subprocess(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()


def checkStyleCreateDict(checkOut, changesDict):
    methods = {}
    lines = []
    with open(checkOut, "r") as f:
        lines = f.readlines()[1:-3]
    for line in filter(lambda line: "@" in line and len(line.split()) == 2, lines):
        file, data = line.split(" ")
        file = file.split(".java")[0]+".java"
        fileNameSplited = file.split(os.path.sep)
        fileName = fileNameSplited[-1].replace("_", os.path.sep)
        commitID = fileNameSplited[fileNameSplited.index("commitsFiles") + 1]
        if not (fileName, commitID) in changesDict.keys():
            continue
        key = ""
        inds = []
        deleted, insertions, is_new_file, is_deleted_file, is_renamed_file = changesDict[(fileName, commitID)]
        if "before" in file:
            key = "deletions"
            inds = deleted
        if "after" in file:
            key = "insertions"
            inds = insertions
        name, begin, end = data.split("@")
        both = set(map(str, inds)) & set(map(str, range(int(begin)-1, int(end))))
        keyChange = len(both)
        if keyChange == 0:
            continue
        methodDir = fileName + "$" + name
        tup = (methodDir, commitID)
        if not tup in methods:
            methods[tup] = {}
        methods[tup][key] = keyChange
        methods[tup].setdefault("methodName", name)
        methods[tup].setdefault("fileName", fileName)
        methods[tup].setdefault("commitID", commitID)
        methods[tup].setdefault("is_new_file", is_new_file)
        methods[tup].setdefault("is_deleted_file", is_deleted_file)
        methods[tup].setdefault("is_renamed_file", is_renamed_file)
    return methods


def readChangesFile(change):
    dict = {}
    rows = []
    with open(change, "r") as f:
        for line in f:
            fileName, commitSha, dels, Ins, is_new_file, is_deleted_file, is_renamed_file = line.strip().split("@")
            fileName = fileName.replace("_", os.path.sep)
            dict[(fileName, commitSha)] = map(eval, [dels, Ins, is_new_file, is_deleted_file, is_renamed_file])
            rows.append(map(str, [fileName,commitSha, len(dels), len(Ins), len(dels)+len(Ins), is_new_file, is_deleted_file, is_renamed_file]))
    return dict, rows


def analyzeCheckStyle(checkOut, changeFile):
    changesDict, filesRows = readChangesFile(changeFile)
    methods = checkStyleCreateDict(checkOut, changesDict)
    all_methods = []
    for tup in methods:
        methodDir = tup[0]
        dels = methods[tup].setdefault("deletions", 0)
        ins = methods[tup].setdefault("insertions", 0)
        fileName = methods[tup].setdefault("fileName", "")
        methodName = methods[tup].setdefault("methodName", "")
        commitID = methods[tup].setdefault("commitID", "")
        is_new_file = methods[tup].setdefault("is_new_file", 0)
        is_deleted_file = methods[tup].setdefault("is_deleted_file", 0)
        is_renamed_file = methods[tup].setdefault("is_renamed_file", 0)
        all_methods.append(map(str, [commitID, methodDir, fileName, methodName, dels, ins, dels+ins, is_new_file, is_deleted_file, is_renamed_file]))
    return all_methods, filesRows


@utilsConf.marker_decorator(utilsConf.PATCHS_FEATURES_MARKER)
def labeling():
    patchD = os.path.join(utilsConf.get_configuration().workingDir, "patch")
    commitsFiles = os.path.join(utilsConf.get_configuration().workingDir, "commitsFiles")
    mkdir(patchD)
    mkdir(commitsFiles)
    run_commands = "git format-patch --root -o ..\patch --function-context --unified=900000".split()
    proc = utilsConf.open_subprocess(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=utilsConf.to_short_path(utilsConf.get_configuration().LocalGitPath))
    proc.communicate()
    buildPatchs(patchD, commitsFiles, utilsConf.get_configuration().changeFile)
    checkOut = utilsConf.get_configuration().MethodsParsed
    RunCheckStyle(commitsFiles, checkOut, utilsConf.get_configuration().checkStyle68, utilsConf.get_configuration().methodsNamesXML)

if __name__ == "__main__":
    # with open(r"C:\Temp\amir.txt", "wb") as change:
    #     for patch in glob.glob(os.path.join(r"C:\Users\eranhe\Fault_Predicition_Defect4J\rss\math_3_amir1\patch","*.patch")):
    #         oneFile(patch, r"C:\Temp\79f7a7e", change)
    dict, rows = readChangesFile(r"C:\Users\eranhe\Fault_Predicition_Defect4J\rss\math_3_amir3\commitsFiles\Ins_dels.txt")
    pass