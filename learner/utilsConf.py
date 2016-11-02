__author__ = 'amir'
import os

def globalConfig(confFile):
    lines =[x.split("\n")[0] for x in open(confFile,"r").readlines()]
    current_dir = os.path.dirname(os.path.realpath(__file__))
    utilsPath = os.path.realpath(os.path.join(current_dir, "../utils"))
    docletPath = os.path.join(utilsPath, "xml-doclet-1.0.4-jar-with-dependencies.jar")
    sourceMonitorEXE = "C:\Program Files (x86)\SourceMonitor\SourceMonitor.exe"
    checkStyle57 = os.path.join(utilsPath, "checkstyle-5.7-all.jar")
    checkStyle68 = os.path.join(utilsPath, "checkstyle-6.8-SNAPSHOT-all.jar")
    allchecks = os.path.join(utilsPath, "allChecks.xml")
    methodsNamesXML = os.path.join(utilsPath, "methodNameLines.xml")
    wekaJar = os.path.join(utilsPath, "weka.jar")
    RemoveBat = os.path.join(utilsPath, "../removeBat.bat")
    for x in lines:
        if x.startswith("sourceMonitorEXE"):
            v=x.split("=")[1]
            sourceMonitorEXE=v
    return docletPath,sourceMonitorEXE,checkStyle57,checkStyle68,allchecks,methodsNamesXML,wekaJar,RemoveBat,utilsPath


def configure(confFile):
    lines =[x.split("\n")[0] for x in open(confFile,"r").readlines()]
    vers, gitPath,bugs, workingDir="","","",""
    for x in lines:
        if x.startswith("workingDir"):
            v=x.split("=")[1]
            workingDir=v
        if x.startswith("git"):
            v=x.split("=")[1]
            gitPath=v
        if x.startswith("bugs"):
            v=x.split("=")[1]
            bugs=v
        if x.startswith("vers"):
            v=x.split("=")[1]
            v=v.split("(")[1]
            v=v.split(")")[0]
            vers=v.split(",")
    docletPath="C:\projs\\xml-doclet-1.0.4-jar-with-dependencies.jar"
    sourceMonitorEXE="C:\Program Files (x86)\SourceMonitor\SourceMonitor.exe"
    checkStyle57,checkStyle68,allchecks,methodsNamesXML="C:\projs\\checkstyle-5.7-all.jar","C:\projs\checkstyle-6.8-SNAPSHOT-all.jar","C:\projs\\allChecks.xml","C:\projs\methodNameLines.xml"
    return [v.lstrip() for v in vers], gitPath,bugs, workingDir#,docletPath,sourceMonitorEXE,checkStyle57,checkStyle68,allchecks,methodsNamesXML


def configureExperiments(confFile):
    lines =[x.split("\n")[0] for x in open(confFile,"r").readlines()]
    vers, gitPath,bugs, workingDir="","","",""
    for x in lines:
        if x.startswith("workingDir"):
            v=x.split("=")[1]
            workingDir=v
        if x.startswith("git"):
            v=x.split("=")[1]
            gitPath=v
        if x.startswith("bugs"):
            v=x.split("=")[1]
            bugs=v
        if x.startswith("vers"):
            v=x.split("=")[1]
            v=v.split("(")[1]
            v=v.split(")")[0]
            vers=v.split(",")
    return [v.lstrip() for v in vers], gitPath,bugs, workingDir