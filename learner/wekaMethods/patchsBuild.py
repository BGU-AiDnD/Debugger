__author__ = 'amir'

import os
import glob
import re
import subprocess
import shutil
import utilsConf


# git format-patch --root origin

def mkDirs(outDir, commitID):
    o = outDir + "\\" + commitID
    if not (os.path.isdir(o)):
        os.mkdir(o)
    o = outDir + "\\" + commitID + "\\before"
    if not (os.path.isdir(o)):
        os.mkdir(o)
    o = outDir + "\\" + commitID + "\\after"
    if not (os.path.isdir(o)):
        os.mkdir(o)
    o = outDir + "\\" + commitID + "\\parser"
    if not (os.path.isdir(o)):
        os.mkdir(o)


def fixEnum(l):
    if "enum =" in l:
        l = l.replace("enum =", "enumAmir =")
    if "enum=" in l:
        l = l.replace("enum=", "enumAmir=")
    if "enum," in l:
        l = l.replace("enum,", "enumAmir,")
    if "enum." in l:
        l = l.replace("enum.", "enumAmir.")
    if "enum;" in l:
        l = l.replace("enum;", "enumAmir;")
    if "enum)" in l:
        l = l.replace("enum)", "enumAmir)")
    return l


def fixAssert(l):
    if "assert " in l:
        l = l.replace("assert ", "assertAmir ")
        if ":" in l:
            l = l.replace(":", ";//")
    if "assert(" in l:
        l = l.replace("assert(", "assertAmir(")
        if ":" in l:
            l = l.replace(":", ";//")
    return l


def OneClass(diff_lines, outPath, commitID, change):
    diff_files = diff_lines[0].split()
    if len(diff_files) < 3:
        assert False
    fileName = diff_lines[0].split()[3]
    fileName = fileName[2:]
    fileName = os.path.normpath(fileName).replace(os.path.sep, "_")
    if not fileName.endswith('.java'):
        return
    start_line = filter(lambda line: line[1].startswith('+++'), enumerate(diff_lines))
    if len(start_line) != 1:
        return  # no file
    diff_lines = diff_lines[start_line[0][0] + 1:]
    befLines = []
    afterLines = []
    deletedInds = []
    addedInds = []
    delind = 0
    addind = 0
    for l in diff_lines:
        if "\ No newline at end of file" in l:
            continue
        if "1.9.4.msysgit.2" in l:
            continue
        if "- \n" == l:
            continue
        if "-- \n" == l:
            continue
        l = fixEnum(l)
        l = fixAssert(l)
        replaced = re.sub('@@(-|\+|,| |[0-9])*@@', '', l)
        if replaced.startswith("*"):
            replaced = "\\" + replaced
        if replaced.startswith("+"):
            afterLines.append(replaced[1:])
            addedInds.append(addind)
            addind = addind + 1
        elif replaced.startswith("-"):
            befLines.append(replaced[1:])
            deletedInds.append(delind)
            delind = delind + 1
        else:
            afterLines.append(replaced)
            befLines.append(replaced)
            delind = delind + 1
            addind = addind + 1
    with open(os.path.join(outPath, "before", fileName), "wb") as bef:
        bef.writelines(befLines)
    with open(os.path.join(outPath, "after", fileName), "wb") as after:
        after.writelines(afterLines)
    with open(os.path.join(outPath, fileName + "_deletsIns.txt"), "wb") as f:
        f.writelines(["deleted\n", str(deletedInds) + "\n", "added\n", str(addedInds)])
    change.write(fileName + "@" + str(commitID) + "@" + str(deletedInds) + "@" + str(addedInds) + "\n")


def oneFile(PatchFile, outDir, change):
    with open(PatchFile, 'r') as f:
        lines = f.readlines()[:-3]
    if len(lines) == 0:
        return
    commitSha = lines[0].split()[1]  # line 0 word 1
    commitID = str(commitSha)
    mkDirs(outDir, commitID)
    inds = [lines.index(l) for l in lines if "diff --git" in l] + [len(lines)]  # lines that start with diff --git
    shutil.copyfile(PatchFile, os.path.join(outDir, commitID, os.path.basename(PatchFile)))
    for i in range(len(inds) - 1):
        diff_lines = lines[inds[i]:inds[i + 1]]
        if len(diff_lines) == 0:
            assert False
        OneClass(diff_lines, os.path.join(outDir, commitID), commitID, change)


def buildPatchs(Path, outDir, changedFile):
    with open(changedFile, "wb") as change:
        for patch in glob.glob(os.path.join(Path, "*.patch")):
            oneFile(patch, outDir, change)


def mkdir(d):
    if not os.path.isdir(d):
        os.mkdir(d)


def RunCheckStyle(workingDir, outPath, checkStyle68, methodNameLines):
    run_commands = ["java", "-jar", checkStyle68, "-c", methodNameLines, "javaFile", "-o", outPath, workingDir]
    utilsConf.open_subprocess(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()


def checkStyleCreateDict(checkOut, changesDict):
    methods = {}
    lines = []
    with open(checkOut, "r") as f:
        lines = f.readlines()[1:-3]
    for line in filter(lambda line: "@" in line and len(line.split()) == 2, lines):
        file, data = line.split(" ")
        file = file.split(".java")[0] + ".java"
        fileNameSplited = file.split(os.path.sep)
        fileName = fileNameSplited[-1].replace("_", os.path.sep)
        commitID = fileNameSplited[fileNameSplited.index("commitsFiles") + 1]
        if not (fileName, commitID) in changesDict.keys():
            continue
        key = ""
        inds = []
        deleted, insertions = changesDict[(fileName, commitID)]
        if "before" in file:
            key = "deletions"
            inds = deleted
        if "after" in file:
            key = "insertions"
            inds = insertions
        name, begin, end = data.split("@")
        both = set(map(str, inds)) & set(map(str, range(int(begin) - 1, int(end))))
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
            rows.append(map(str, [fileName, commitSha, len(dels), len(Ins), len(dels) + len(Ins)]))
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
        all_methods.append(map(str, [commitID, methodDir, fileName, methodName, dels, ins, dels + ins]))
    return all_methods, filesRows


@utilsConf.marker_decorator(utilsConf.PATCHS_FEATURES_MARKER)
def labeling():
    patchD = os.path.join(utilsConf.get_configuration().workingDir, "patch")
    commitsFiles = os.path.join(utilsConf.get_configuration().workingDir, "commitsFiles")
    mkdir(patchD)
    mkdir(commitsFiles)
    run_commands = "git format-patch --root -o ..\patch --function-context --unified=900000".split()
    proc = utilsConf.open_subprocess(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                     cwd=utilsConf.to_short_path(utilsConf.get_configuration().LocalGitPath))
    proc.communicate()
    buildPatchs(patchD, commitsFiles, utilsConf.get_configuration().changeFile)
    checkOut = utilsConf.get_configuration().MethodsParsed
    RunCheckStyle(commitsFiles, checkOut, utilsConf.get_configuration().checkStyle68,
                  utilsConf.get_configuration().methodsNamesXML)


if __name__ == "__main__":
    a, b = analyzeCheckStyle(r"C:\Temp\79f7a7ef529ae656a80f7e331f75e79999cef7ea\commitsFiles\CheckStyle.txt",
                             r"C:\Temp\79f7a7ef529ae656a80f7e331f75e79999cef7ea\commitsFiles\Ins_dels.txt")
    pass
