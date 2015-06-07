#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import git
import datetime
import buildDB
import commsSpaces
import unittest
import articles
import csv

"""
resources :
git
windows
xml-doclet-1.0.4-jar-with-dependencies.jar
checkStyle5.7
"""

"""
workingDir=C:\projs\antWorking
git=C:\projs\antC
vers=(ANT_13_B2,ANT_13_MAIN_MERGE4,ANT_MAIN_13_MERGE4)
"""

def configure(confFile):
    lines =[x.split("\n")[0] for x in open(confFile,"r").readlines()]
    vers, gitPath, workingDir="","",""
    for x in lines:
        if x.startswith("workingDir"):
            v=x.split("=")[1]
            workingDir=v
        if x.startswith("git"):
            v=x.split("=")[1]
            gitPath=v
        if x.startswith("vers"):
            v=x.split("=")[1]
            v=v.split("(")[1]
            v=v.split(")")[0]
            vers=v.split(",")
    return [v.lstrip() for v in vers], gitPath, workingDir

def mkOneDir(dir):
    if not os.path.isdir(dir):
            os.mkdir(dir)

def Mkdirs(workingDir,vers):
    mkOneDir(workingDir)
    coptSt = "copy C:\projs\\xml-doclet-1.0.4-jar-with-dependencies.jar "+workingDir + "\\xml-doclet-1.0.4-jar-with-dependencies.jar "
    print coptSt
    os.system(coptSt)
    coptSt = "copy C:\projs\\allChecks.xml "+workingDir + "\\allChecks.xml "
    os.system(coptSt)
    coptSt = "copy C:\projs\\checkstyle-5.7-all.jar "+workingDir + "\\checkstyle-5.7-all.jar "
    os.system(coptSt)

    versPath=os.path.join(workingDir,"vers")
    mkOneDir(versPath)
    ver=os.path.join(versPath,"checkAll")
    mkOneDir(ver)
    dbadd=os.path.join(workingDir,"dbAdd")
    mkOneDir(dbadd)
    weka=os.path.join(workingDir,"weka")
    mkOneDir(weka)
    for v in vers:
        ver=os.path.join(versPath,v)
        mkOneDir(ver)
        blame=os.path.join(ver,"blame")
        mkOneDir(blame)
        Jdoc2=os.path.join(ver,"Jdoc2")
        mkOneDir(Jdoc2)
    return versPath, dbadd

def CopyDirs(gitPath, versPath,vers):
    for x in vers:
        path=os.path.join(versPath,x)+"\\"
        path=os.path.join(path,"repo")#+"\\"
        coptSt = "xcopy " + gitPath + " " + path + " /C /e /i /h"
        os.system(coptSt)


def GitRevert(versPath,vers):
    for x in vers:
        path=os.path.join(versPath,x)
        path=os.path.join(path,"repo")+"\\"
        path_x = "c: & cd " + path + " & git reset -q " + x
        #path_x = "c: & cd " + path + " & git revert  " + x
        print path_x
        os.system(path_x)

def Extract_OO_features(versPath,vers):
    for x in vers:
        path=os.path.join(versPath,x)
        command = """c: & cd """ + path + " & for /R .\\repo %f in (*.java) do (call javadoc -doclet com.github.markusbernhardt.xmldoclet.XmlDoclet -docletpath ..\..\\xml-doclet-1.0.4-jar-with-dependencies.jar -filename %~nxf.xml -private -d .\Jdoc2 %f) "
        print command
        os.system(command)
# GENERATE Jdoc



def SourceMonitorXml(workingDir,ver):
    bat="\"C:\Program Files (x86)\SourceMonitor\SourceMonitor.exe\" /C sourceMonitor.xml "
    versParh=os.path.join(workingDir,"vers")
    verDir=os.path.join(versParh,ver)
    verREPO=os.path.join(verDir,"repo")
    verP=os.path.join(verDir,ver)
    xml="""
    <!--?xml version="1.0" encoding="UTF-8" ?-->
<sourcemonitor_commands>

   <write_log>true</write_log>

   <command>
       <project_file>verP.smp</project_file>
       <project_language>Java</project_language>
       <file_extensions>*.java</file_extensions>
       <source_directory>verREPO</source_directory>
       <include_subdirectories>true</include_subdirectories>
       <checkpoint_name>Baseline</checkpoint_name>

       <export>
           <export_file>verP.csv</export_file>
           <export_type>3 (Export project details in CSV)</export_type>
           <export_option>1 (do not use any of the options set in the Options dialog)</export_option>
       </export>
   </command>

   <command>
       <project_file>verP.smp</project_file>
       <project_language>Java</project_language>
       <file_extensions>*.java</file_extensions>
       <source_directory>verREPO</source_directory>
       <include_subdirectories>true</include_subdirectories>
       <checkpoint_name>Baseline</checkpoint_name>
       <export>
           <export_file>verP_methods.csv</export_file>
           <export_type>6 (Export method metrics in CSV)</export_type>
           <export_option>1 (do not use any of the options set in the Options dialog)</export_option>
       </export>
   </command>

</sourcemonitor_commands>"""
    xml=xml.replace("verREPO",verREPO)
    xml=xml.replace("verP",verP)
    xmlPath=os.path.join(verDir,"sourceMonitor.xml")
    f=open(xmlPath,"wb")
    f.write(xml)
    f.close()
    os.system("""c: & cd """ + verDir + " & " + bat)


def blameExecute(  path, pathRepo):
    blameWrite=" & dir /b /s *.java > ..\\javaFiles.txt"
    doBlame="for /F   %f in (../blame.txt) do (git blame --show-stats --score-debug -p --line-porcelain -l %f > ..\\blame\%~nxf)"
    blame_write = "c: & cd " + pathRepo + blameWrite
    os.system(blame_write)
    blameO3 = os.path.join(path, "javaFiles.txt")
    blameO1 = os.path.join(path, "blame.txt")
    open(blameO1, "wb").write("".join([x.replace(pathRepo + "\\", "") for x in open(blameO3, "r")]))
    blame = """c: & cd """ + pathRepo + " & " + doBlame
    os.system(blame)


def Extract_complexity_features(versPath,vers,workingDir):
    for x in vers:
        path=os.path.join(versPath,x)
        pathRepo=os.path.join(path,"repo")

        checkStyle="c: & cd "+workingDir+ " &  java -jar checkstyle-5.7-all.jar -c allChecks.xml -r "+pathRepo+" -f xml -o vers/checkAll/"+x+".xml "
        os.system(checkStyle)
        blameExecute(path, pathRepo)
        SourceMonitorXml(workingDir,x)



def GitVersInfo(basicPath,repoPath,vers):
    #repoPath="C:\\tomcat\\code\\tomcat8\\"
    r=git.Repo(repoPath)
    #vers=["TOMCAT_8_0_4", "TOMCAT_8_0_5", "TOMCAT_8_0_6", "TOMCAT_8_0_7", "TOMCAT_8_0_8", "TOMCAT_8_0_9"]
    if vers==[]:
        wanted=[ x.commit for x in r.tags ]
        vers=r.tags
    else:
        wanted=[ x.commit for x in r.tags if x.name in vers]
    commits=[int("".join(list(x.hexsha)[:7]),16) for x in wanted]
    dates=[datetime.datetime.fromtimestamp(x.committed_date).strftime('%Y-%m-%d %H:%M:%S') for x in wanted]
    paths=[os.path.join(basicPath, os.path.join(n, "repo")) for n in vers]
    return vers,paths,dates,commits


# blame
#checkStyle

def featuresExtract(vers, versPath, workingDir):
    Extract_OO_features(versPath, vers)
    Extract_complexity_features(versPath, vers, workingDir)
    commsSpaces.create(vers, os.path.join(workingDir, "vers"))


def versionsCreate(gitPath, vers, versPath):
    CopyDirs(gitPath, versPath, vers)
    GitRevert(versPath, vers)


def gitInfoToCsv(gitPath,outFile):
        #repoPath="C:\\tomcat\\code\\tomcat8\\"
    r=git.Repo(gitPath)
    #vers=["TOMCAT_8_0_4", "TOMCAT_8_0_5", "TOMCAT_8_0_6", "TOMCAT_8_0_7", "TOMCAT_8_0_8", "TOMCAT_8_0_9"]
    wanted=[ x.commit for x in r.tags ]
    vers=r.tags
    dates=[datetime.datetime.fromtimestamp(x.committed_date).strftime('%Y-%m-%d %H:%M:%S') for x in wanted]
    lines=[["ver","date"]]
    for v,d in zip(vers,dates):
        lines.append([v,d])
    f=open(outFile,"wb")
    writer=csv.writer(f)
    writer.writerows(lines)
    f.close()


def wrapper(confFile, csvPath="poiBugs.csv"):
    vers, gitPath, workingDir =configure(confFile)
    versPath, dbadd=Mkdirs(workingDir,vers)
    vers,paths,dates,commits=GitVersInfo("c:\\",gitPath,vers)
    versionsCreate(gitPath, vers, versPath)
    featuresExtract(vers, versPath, workingDir)
    bugsPath=os.path.join(workingDir, csvPath)
    buildDB.buildOneTimeCommits(versPath,dbadd,bugsPath,False,-1,vers,"repo")
    weka=os.path.join(workingDir,"weka")
    articles.articlesAllpacks(workingDir,gitPath,weka,vers)
    #DO extract all_one compare data
    #create packs file
    #build agent



if __name__ == '__main__':
    wrapper("C:\projs\\antConf.txt","antBugs.csv")
    #wrapper("C:\projs\\poiConf.txt","poiBugs.csv")
    #wrapper("C:\projs\\karafConf.txt","karafBugs.csv")
    #Mkdirs("C:\projs\\karafW",["s"])
    #gitInfoToCsv("C:\projs\\karaf","C:\projs\\karaf\\karaf.csv")
    #SourceMonitorXml("C:\projs\poiWorking","REL_3_10_1")