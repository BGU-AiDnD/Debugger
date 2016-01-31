__author__ = 'amir'


def globalConfig(confFile):
    lines =[x.split("\n")[0] for x in open(confFile,"r").readlines()]
    docletPath,sourceMonitorEXE,checkStyle57,checkStyle68,allchecks,methodsNamesXML,wekaJar="","","","","","",""
    RemoveBat=""
    utilsPath=""
    for x in lines:
        if x.startswith("docletPath"):
            v=x.split("=")[1]
            docletPath=v
        if x.startswith("sourceMonitorEXE"):
            v=x.split("=")[1]
            sourceMonitorEXE=v
        if x.startswith("checkStyle57"):
            v=x.split("=")[1]
            checkStyle57=v
        if x.startswith("checkStyle68"):
            v=x.split("=")[1]
            checkStyle68=v
        if x.startswith("allchecks"):
            v=x.split("=")[1]
            allchecks=v
        if x.startswith("methodsNamesXML"):
            v=x.split("=")[1]
            methodsNamesXML=v
        if x.startswith("wekaJar"):
            v=x.split("=")[1]
            wekaJar=v
        if x.startswith("RemoveBat"):
            v=x.split("=")[1]
            RemoveBat=v
        if x.startswith("utilsPath"):
            v=x.split("=")[1]
            utilsPath=v
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