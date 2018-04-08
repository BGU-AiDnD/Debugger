#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import subprocess
import datetime
import shutil
import csv
import tempfile
from random import randint
import git

import utilsConf
import wekaMethods.buildDB
import wekaMethods.commsSpaces
import wekaMethods.articles
import wekaMethods.patchsBuild
import wekaMethods.wekaAccuracy
import wekaMethods.issuesExtract.github_import
import wekaMethods.issuesExtract.jira_import
import wekaMethods.issuesExtract.python_bugzilla
import Agent.bugs_testsDBMethods
import Agent.experimentsMethods
import report
import All_One_create
import wekaMethods.ParseWekaOutput
import Planner.planningExperiments
import Planner.Planning_Results
import NLP.commits

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


def mkOneDir(dir):
    if not os.path.isdir(dir):
            os.mkdir(dir)

def version_to_dir_name(version):
    return version.replace("\\", "_").replace("/", "_").replace("-", "_").replace(".", "_")

def Mkdirs(workingDir,vers):
    mkOneDir(workingDir)
    #shutil.copyfile("C:\projs\\xml-doclet-1.0.4-jar-with-dependencies.jar", workingDir + "\\xml-doclet-1.0.4-jar-with-dependencies.jar")
    #shutil.copyfile("C:\projs\\allChecks.xml", workingDir + "\\allChecks.xml")
    #shutil.copyfile("C:\projs\\checkstyle-5.7-all.jar", workingDir + "\\checkstyle-5.7-all.jar")
    versPath=os.path.join(workingDir,"vers")
    mkOneDir(versPath)
    experiments=os.path.join(workingDir,"experiments")
    mkOneDir(experiments)
    experiments=os.path.join(workingDir,"experiments_known")
    mkOneDir(experiments)
    checkAll=os.path.join(versPath,"checkAll")
    mkOneDir(checkAll)
    checkAllMethodsData=os.path.join(versPath,"checkAllMethodsData")
    mkOneDir(checkAllMethodsData)
    dbadd=os.path.join(workingDir,"dbAdd")
    mkOneDir(dbadd)
    testedVer=os.path.join(workingDir,"testedVer")
    mkOneDir(testedVer)
    weka=os.path.join(workingDir,"weka")
    mkOneDir(weka)
    markers=os.path.join(workingDir,"markers")
    mkOneDir(markers)
    for v in vers:
        version=os.path.join(versPath,version_to_dir_name(v))
        mkOneDir(version)
        blame=os.path.join(version,"blame")
        mkOneDir(blame)
        Jdoc2=os.path.join(version,"Jdoc2")
        mkOneDir(Jdoc2)
    return versPath, dbadd

def CopyDirs(gitPath, versPath, versions):
    for version in versions:
        path=os.path.join(versPath,version_to_dir_name(version), "repo")
        if not os.path.exists(path):
            shutil.copytree(gitPath, path)


def GitRevert(versPath,vers):
    def run_cmd(path, args):
        proc = subprocess.Popen(["git", "-C", path] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

    for version in vers:
        repo_path = os.path.join(versPath, version_to_dir_name(version), "repo")
        run_cmd(repo_path, ["clean", "-fd", version])
        run_cmd(repo_path, ["checkout", '-f', version])
        run_cmd(repo_path, ["clean", "-fd", version])

def OO_features_error_analyze(err):
    # get all corrupted java files in err
    lines=err.split("\n")
    wantedLines=[]
    i=0
    for l in lines:
        if "symbol:   variable " in l:
            wantedLines.append(lines[i-3])
        i=i+1
    knownP=["static import only from classes and interfaces","unmappable character for encoding"]
    knownP=[""]
    dontMatter=["does not exist","cannot find symbol"]
    wantedLines=wantedLines+[x for x in lines if ".java:" in x]
    lines=wantedLines
    for d in dontMatter:
        lines=[x for x in lines if d not   in x]
    ans=[]
    for p in knownP:
        ans=ans+[x.split(".java")[0]+".java" for x in lines if p in x]
    return ans


@utilsConf.marker_decorator(utilsConf.OO_OLD_FEATURES_MARKER)
def Extract_OO_features_OLD(versPath, vers, docletPath):
    for version in vers:
        verPath=os.path.join(versPath,version_to_dir_name(version))
        command = """cd /d  """ + utilsConf.to_short_path(verPath) + " & for /R .\\repo %f in (*.java) do (call javadoc -doclet com.github.markusbernhardt.xmldoclet.XmlDoclet -docletpath "+utilsConf.to_short_path(docletPath)+" -filename %~nxf.xml -private -d .\Jdoc2 %f) "
        os.system(command)
# GENERATE Jdoc


@utilsConf.marker_decorator(utilsConf.OO_FEATURES_MARKER)
def Extract_OO_features(versPath,vers,docletPath="..\..\\xml-doclet-1.0.4-jar-with-dependencies.jar"):
    for x in vers:
        verPath=os.path.join(versPath,x)
        outPath=os.path.join(verPath,"Jdoc")
        outPath=os.path.join(outPath,"javadoc.xml")
        err=""
        open(os.path.join(verPath,"JdocFunc.txt"),"wt").writelines([x for x in open(os.path.join(verPath,"javaFiles.txt"),"r").readlines()])
        run_commands = ["javadoc", "-doclet", "com.github.markusbernhardt.xmldoclet.XmlDoclet","-docletpath ", docletPath, "-private","-d",".\Jdoc","@JdocFunc.txt"]
        bads=[]
        if (not os.path.exists(outPath)):
            bads=bads+OO_features_error_analyze(err)
            open(os.path.join(verPath,"JdocFunc.txt"),"wb").writelines([x for x in open(os.path.join(verPath,"javaFiles.txt"),"r").readlines() if x not in bads ])
            proc = subprocess.Popen(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,cwd=utilsConf.to_short_path(verPath))
            (out, err) = proc.communicate()
            bads=bads+OO_features_error_analyze(err)
            open(os.path.join(verPath,"JdocFunc.txt"),"wb").writelines([x for x in open(os.path.join(verPath,"javaFiles.txt"),"r").readlines() if x not in bads ])
            proc = subprocess.Popen(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,cwd=utilsConf.to_short_path(verPath))
            (out, err) = proc.communicate()
# GENERATE Jdoc


#@utilsConf.marker_decorator(utilsConf.SOURCE_MONITOR_FEATURES_MARKER)
def SourceMonitorXml(workingDir, ver, sourceMonitorEXE):
    verDir=os.path.join(utilsConf.to_short_path(workingDir), "vers", ver)
    verREPO=os.path.join(verDir, "repo")
    verP=os.path.join(verDir, ver)
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

</sourcemonitor_commands>""".replace("verP", verP).replace("verREPO", verREPO)
    xmlPath = os.path.join(verDir, "sourceMonitor.xml")
    with open(xmlPath, "wb") as f:
        f.write(xml)
    run_commands = [sourceMonitorEXE, "/C", xmlPath]
    proc = subprocess.Popen(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()


def blameExecute(path, pathRepo, ver):
    for root, dirs, files in os.walk(pathRepo):
        for name in files:
            if not os.path.splitext(name)[1].endswith("java"):
                continue
            git_file_path = os.path.join(root, name).replace(pathRepo + "\\", "")
            blame_file_path = os.path.abspath(os.path.join(path, 'blame', name))
            blame_commands = ['git', 'blame', '--show-stats', '--score-debug', '-p', '--line-porcelain', '-l', ver, git_file_path]
            proc = subprocess.Popen(blame_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=utilsConf.to_short_path(pathRepo))
            (out, err) = proc.communicate()
            with open(blame_file_path, "w") as f:
                f.writelines(out)
    run_commands = ["dir", "/b", "/s", "*.java"]
    proc = subprocess.Popen(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=utilsConf.to_short_path(pathRepo))
    (out, err) = proc.communicate()
    with open(os.path.join(path, "javaFiles.txt"), "wb") as f:
        f.writelines(out)


@utilsConf.marker_decorator(utilsConf.COMPLEXITY_FEATURES_MARKER)
def Extract_complexity_features(versPath,vers_dirs, vers,workingDir,sourceMonitorEXE,checkStyle57,checkStyle68,allchecks,methodsNamesXML):
    for version_path, version_name in zip(vers_dirs, vers):
        path=os.path.join(versPath,version_to_dir_name(version_path))
        pathRepo=os.path.join(path,"repo")
        SourceMonitorXml(workingDir,version_to_dir_name(version_path),sourceMonitorEXE)
        run_commands = ["java", "-jar", checkStyle68, "-c", methodsNamesXML,"javaFile","-o","vers/checkAllMethodsData/"+version_path+".txt",pathRepo]
        proc = subprocess.Popen(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=utilsConf.to_short_path(workingDir))
        (out, err) = proc.communicate()

        run_commands = ["java", "-jar", checkStyle57, "-c", allchecks,"-r",pathRepo,"-f","xml","-o","vers/checkAll/"+version_path+".xml"]
        proc = subprocess.Popen(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=utilsConf.to_short_path(workingDir))
        (out, err) = proc.communicate()

        blameExecute(path, pathRepo, version_name)

def GitVersInfo(basicPath,repoPath,vers):
    r=git.Repo(repoPath)
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
@utilsConf.marker_decorator(utilsConf.FEATURES_MARKER)
def featuresExtract(vers_dirs, vers, versPath, workingDir,LocalGitPath,logfile,docletPath,sourceMonitorEXE,checkStyle57,checkStyle68,allchecks,methodsNamesXML):
    Extract_complexity_features(versPath, vers_dirs, vers, workingDir,sourceMonitorEXE,checkStyle57,checkStyle68,allchecks,methodsNamesXML)
    logfile.write("after Extract_complexity_features "+ str(datetime.datetime.now())+"\n")
    logfile.flush()

    Extract_OO_features_OLD(versPath, vers,docletPath)
    logfile.write("after Extract_OO_features "+ str(datetime.datetime.now())+"\n")
    logfile.flush()

    wekaMethods.commsSpaces.create(vers_dirs, os.path.join(workingDir, "vers"))
    logfile.write("after commsSpaces "+ str(datetime.datetime.now())+"\n")
    logfile.flush()

    wekaMethods.patchsBuild.do_all(LocalGitPath, checkStyle68, methodsNamesXML)


@utilsConf.marker_decorator(utilsConf.VERSIONS_MARKER)
def versionsCreate(gitPath, vers, versPath,LocalGitPath):
    CopyDirs(gitPath, versPath, vers)
    GitRevert(versPath, vers)
    if not os.path.exists(LocalGitPath):
        shutil.copytree(gitPath, LocalGitPath)



def gitInfoToCsv(gitPath,outFile):
    r=git.Repo(gitPath)
    wanted=[ x.commit for x in r.tags ]
    dates=[datetime.datetime.fromtimestamp(x.committed_date).strftime('%Y-%m-%d %H:%M:%S') for x in wanted if type(x)==git.Commit]
    lines=[["ver","date"]]
    for v,d in zip(r.tags,dates):
        lines.append([v,d])
    with open(outFile,"wb") as f:
        writer=csv.writer(f)
        writer.writerows(lines)


def BuildWekaModel(weka, training, testing, namesCsv, outCsv, name, wekaJar):
    algorithm="weka.classifiers.trees.RandomForest -I 1000 -K 0 -S 1 -num-slots 1 "
    #os.system("cd /d  "+weka +" & java -Xmx2024m  -cp \"C:\\Program Files\\Weka-3-7\\weka.jar\" weka.Run " +algorithm+ " -x 10 -d .\\model.model -t "+training+" > training"+name+".txt")
    os.system("cd /d  "+ utilsConf.to_short_path(weka) +" & java -Xmx2024m  -cp "+utilsConf.to_short_path(wekaJar)+" weka.Run " +algorithm+ " -x 10 -d .\\model.model -t "+training+" > training"+name+".txt")
    # run_commands = ['java', '-Xmx2024m',  '-cp', wekaJar, 'weka.Run', algorithm, '-x', '10', '-d', '.\\model.model', 't']
    # proc = subprocess.Popen(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=utilsConf.to_short_path(weka))
    # proc.communicate()
    algorithm="weka.classifiers.trees.RandomForest "
    os.system("cd /d  "+ utilsConf.to_short_path(weka) +" & java -Xmx2024m  -cp "+ utilsConf.to_short_path(wekaJar) +" weka.Run " +algorithm+ " -l .\\model.model -T "+testing+" -classifications \"weka.classifiers.evaluation.output.prediction.CSV -file testing"+name+".csv\" ")
    os.system("cd /d  "+ utilsConf.to_short_path(weka) +" & java -Xmx2024m  -cp "+ utilsConf.to_short_path(wekaJar) +" weka.Run " +algorithm+ " -l .\\model.model -T "+testing+" > testing"+name+".txt ")
    wekaCsv = os.path.join(utilsConf.to_short_path(weka), "testing"+name+".csv")
    wekaMethods.wekaAccuracy.priorsCreation(namesCsv, wekaCsv, outCsv, "")


def testing(repoPath,antOrPom):
    shutil.copyfile("C:\GitHub\\agent\my-app\\agent.jar", repoPath + "\\agent.jar")
    if antOrPom=="ant":
        ant = "cd /d  " + repoPath + "  & ant test -keep-going -Dhalt.on.test.failure=\"false\" -Dtest.junit.vmargs=\"-javaagent:agent.jar\""
        #ant = "cd /d  " + repoPath + "  & ant test -keep-going -Dhalt.on.test.failure=\"false\" -Dpoi.test.locale =\"-Duser.language=en -Duser.country=US -javaagent:agent.jar\""
        os.system(ant)
    if antOrPom=="pom":
        runMvn = "cd /d  " + repoPath + "  & mvn clean install -Dmaven.test.failure.ignore=true -DargLine=\"-javaagent:agent.jar\""
        exit()
        os.system(runMvn)


    #adjust agent
    #check mvn or ant
    #run tests


def ExcelReport(csvData,excel,sheet):
    shutil.copyfile("C:\projs\\"+sheet+".xlsx", excel)
    os.system("java -jar ExcelChanger.jar "+excel+" "+csvData+" "+sheet)


def BuildMLFiles(outDir, buggedType, component):
    trainingFile=os.path.join(outDir,buggedType+"_training_"+component+".arff")
    testingFile=os.path.join(outDir,buggedType+"_testing_"+component+".arff")
    NamesFile=os.path.join(outDir,buggedType+"_names_"+component+".csv")
    outCsv=os.path.join(outDir,buggedType+"_out_"+component+".csv")
    return trainingFile, testingFile, NamesFile, outCsv


@utilsConf.marker_decorator(utilsConf.ML_MODELS_MARKER)
def createBuildMLModels(workingDir, gitPath, weka, vers, vers_dirs, db_dir, wekaJar, RemoveBat):
    for buggedType in ["All", "Most"]:
        Bpath=os.path.join(workingDir, buggedType)
        mkOneDir(Bpath)
        FilesPath=os.path.join(Bpath, "Files")
        methodsPath=os.path.join(Bpath, "Methods")
        mkOneDir(FilesPath)
        mkOneDir(methodsPath)
        trainingFile,testingFile,NamesFile,Featuresnames,lensAttr=wekaMethods.articles.articlesAllpacks(FilesPath, gitPath, weka, vers, vers_dirs, buggedType, db_dir)
        trainingFile, testingFile, NamesFile, outCsv=BuildMLFiles(utilsConf.to_short_path(weka),buggedType,"files")
        BuildWekaModel(weka,trainingFile,testingFile,NamesFile,outCsv,"files_"+buggedType,wekaJar)
        # All_One_create.allFamilies(FilesPath,Featuresnames,lensAttr,trainingFile, testingFile,RemoveBat)
        trainingFile,testingFile,NamesFile,Featuresnames,lensAttr=wekaMethods.articles.articlesAllpacksMethods(methodsPath, gitPath, weka, vers, vers_dirs, buggedType, db_dir)
        trainingFile, testingFile, NamesFile, outCsv=BuildMLFiles(utilsConf.to_short_path(weka),buggedType,"methods")
        BuildWekaModel(weka,trainingFile,testingFile,NamesFile,outCsv,"methods_"+buggedType,wekaJar)
        # All_One_create.allFamilies(methodsPath,Featuresnames,lensAttr,trainingFile, testingFile,RemoveBat)


def mergeArffs(merge,arffFile,tempFile):
    os.system('java -Xmx2024m  -cp "C:\Program Files\Weka-3-7\weka.jar" weka.filters.unsupervised.attribute.RemoveByName -E hasBug -i '+ merge+' > '+ tempFile)
    os.system('java -Xmx2024m  -cp "C:\Program Files\Weka-3-7\weka.jar" weka.core.Instances merge '+ tempFile+' '+ arffFile+'  > '+ merge)


def indsFamilies(packsInds,Wanted):
    outpacksInds=[]
    for p in Wanted:
        lst = [packsInds[x] for x in p]
        outpacksInds.append(reduce(lambda x, y: x + y, lst))
    return outpacksInds


def merge_multiple_arff_file(path,outArff,tempFile,indices):
        shutil.copyfile(os.path.join(path,str(indices[0])),outArff)
        for ind in indices[1:]:
            arffFile=os.path.join(path,str(ind))
            mergeArffs(outArff,arffFile,tempFile)


def ArticleFeaturesMostFiles(workingDir,outArffTrain,outArffTest,tempFile,outCsv,wekaJar,indices):
    weka=os.path.join(workingDir,"weka")
    Bpath=os.path.join(workingDir,"Most")
    FilesPath=os.path.join(Bpath,"Files")
    FilesPath=os.path.join(FilesPath,"Fam_one")
    for train,name in zip([outArffTrain,outArffTest],["_Appended.arff","_Only.arff"]):
        shutil.copyfile(os.path.join(FilesPath,str(0)+name),train)
        for ind in indices[1:]:
            arffFile=os.path.join(FilesPath,str(ind)+name)
            mergeArffs(train,arffFile,tempFile)
    trainingFile,testingFile,NamesFile=BuildMLFiles(weka,"Most","files")
    BuildWekaModel(weka,outArffTrain,outArffTest,NamesFile,outCsv,"methods_"+"Most",wekaJar)

def append_families_indices(workingDir,wekaJar, fam_one_path, buggedType,component,indices):
    weka=os.path.join(workingDir,"weka")
    instance_name = component+"_"+buggedType
    outArffTrain = os.path.join(weka, instance_name + "_Appended.arff")
    outArffTest = os.path.join(weka, instance_name + "_Only.arff")
    tempFile= os.path.join(weka, instance_name + "_TMP.arff")
    for train,name in zip([outArffTrain,outArffTest],["_Appended.arff","_Only.arff"]):
        shutil.copyfile(os.path.join(fam_one_path,str(0)+name),train)
        for ind in indices[1:]:
            arffFile=os.path.join(fam_one_path,str(ind)+name)
            mergeArffs(train,arffFile,tempFile)
    trainingFile,testingFile,NamesFile, outCsv=BuildMLFiles(weka,buggedType,component)
    BuildWekaModel(weka,outArffTrain,outArffTest,NamesFile,outCsv,instance_name,wekaJar)



def filesExperiments(workingDir,weka,packsPath,utilsPath, randNum):
    for buggedType in ["All","Most"]:
        outPath = os.path.join(workingDir, "experiments\\files_" + buggedType+randNum)
        outCsv=os.path.join(weka,buggedType+"_out_files.csv")
        Agent.experimentsMethods.RunExperiments(os.path.join(workingDir,"testsBugsMethods.db"), outPath,packsPath,outCsv,"File",buggedType,utilsPath)


def methodsExperiments(workingDir,weka,packsPath,utilsPath,randNum):
    for buggedType in ["All","Most"]:
        outPath = os.path.join(workingDir, "experiments\\methods" + buggedType+randNum)
        outCsv=os.path.join(weka,buggedType+"_out_methods.csv")
        Agent.experimentsMethods.RunExperiments(os.path.join(workingDir,"testsBugsMethods.db"), outPath,packsPath,outCsv,"method",buggedType,utilsPath)

def Experiments(workingDir,weka,packsPath,utilsPath,randNum):
    for buggedType, granularity in zip(["All", "Most"], ["File", "Method"]):
        outPath = os.path.join(workingDir, "experiments\\files_" + buggedType + randNum)
        outCsv = os.path.join(weka, buggedType + "_out_{GRANULARITY}.csv".format(GRANULARITY=granularity))
        Agent.experimentsMethods.RunExperiments(os.path.join(workingDir, "testsBugsMethods.db"), outPath, packsPath,
                                                outCsv, granularity, buggedType, utilsPath)

@utilsConf.marker_decorator(utilsConf.VERSION_TEST_MARKER)
def testVerConfig(workingDir,ver,antOrPom,startDate,endDate):
    testedVer=os.path.join(workingDir,"testedVer")
    testedVer=os.path.join(testedVer,"repo")
    tested=os.path.join(workingDir,"vers")
    tested=os.path.join(tested,ver)
    tested=os.path.join(tested,"repo")
    if not os.path.exists(testedVer):
        shutil.copytree(tested, testedVer)
    #testing(testedVer,antOrPom)
    #Agent.bugs_testsDBMethods.basicBuild(workingDir,ver,startDate,endDate)


def clean(versPath,LocalGitPath):
    shutil.rmtree(versPath, ignore_errors=True)
    shutil.rmtree(LocalGitPath, ignore_errors=True)


def download_bugs(issue_tracker, issue_tracker_url, issue_tracker_product):
    bugsPath = tempfile.mktemp(suffix=".csv")
    if issue_tracker == "bugzilla":
        wekaMethods.issuesExtract.python_bugzilla.write_bugs_csv(bugsPath, issue_tracker_url, issue_tracker_product)
    elif issue_tracker == "jira":
        wekaMethods.issuesExtract.jira_import.jiraIssues(bugsPath, issue_tracker_url, issue_tracker_product)
    elif issue_tracker == "github":
        wekaMethods.issuesExtract.github_import.GithubIssues(bugsPath, issue_tracker_url, issue_tracker_product)
    return bugsPath


def wrapperLearner(confFile):
    vers, gitPath,issue_tracker, issue_tracker_url, issue_tracker_product , workingDir = utilsConf.configure(confFile)
    docletPath, sourceMonitorEXE, checkStyle57, checkStyle68, allchecks, methodsNamesXML, wekaJar, RemoveBat, utilsPath = utilsConf.globalConfig()
    versPath, db_dir = Mkdirs(workingDir, vers)
    bugsPath = download_bugs(issue_tracker, issue_tracker_url, issue_tracker_product)
    vers_dirs = map(version_to_dir_name, vers)
    logfile=open(os.path.join(workingDir,"timeLog2.txt"),"wb")
    logfile.write("start "+ str(datetime.datetime.now())+"\n")
    logfile.flush()
    vers,paths,dates,commits=GitVersInfo("c:\\",gitPath,vers)
    LocalGitPath=os.path.join(workingDir,"repo")
    versionsCreate(gitPath, vers, versPath,LocalGitPath)
    testVerConfig(workingDir,vers_dirs[-2],"ant",dates[-2],dates[-1])
    # NLP.commits.data_to_csv(os.path.join(workingDir, "NLP_data.csv"), gitPath, bugsPath)
    mkOneDir(LocalGitPath)
    featuresExtract(vers_dirs, vers, versPath, workingDir,LocalGitPath,logfile,docletPath,sourceMonitorEXE,checkStyle57,checkStyle68,allchecks,methodsNamesXML)
    logfile.write("after featuresExtract "+ str(datetime.datetime.now())+"\n")
    logfile.flush()
    MethodsParsed=os.path.join(os.path.join(LocalGitPath,"commitsFiles"),"CheckStyle.txt")
    changeFile=os.path.join(os.path.join(LocalGitPath,"commitsFiles"),"Ins_dels.txt")
    wekaMethods.buildDB.buildOneTimeCommits(versPath,db_dir,bugsPath,False,-1,vers_dirs,"repo",MethodsParsed,changeFile,logfile,dates, gitPath)
    logfile.write("after buildDB "+ str(datetime.datetime.now())+"\n")
    logfile.flush()
    weka=utilsConf.to_short_path(os.path.join(workingDir,"weka"))
    createBuildMLModels(workingDir, gitPath, weka, vers, vers_dirs, db_dir, wekaJar, RemoveBat)
    utilsConf.get_configuration().get_marker(utilsConf.LEARNER_PHASE_FILE).finish()

    # FilesIndices=[[0,14,15],[1,2,3,4,5,6,7,8,9],[10,11,12,16],[13]] #Traditional , OO, process ,Bugs
    # FilesIndices_all=[indsFamilies(FilesIndices,[[x for x in range(len(FilesIndices)) if x != ind]])[0]  for ind in range(len(FilesIndices))] #Traditional , OO, process ,Bugs
    # MethodsIndices=[[0],[1],[2,3]]
    # MethodsIndices_all=[indsFamilies(MethodsIndices,[[x for x in range(len(MethodsIndices)) if x != ind]])[0]  for ind in range(len(MethodsIndices))] #Traditional , OO, process ,Bugs
    #
    # for granularity,indicesList_one,indicesList_all in [["Files",FilesIndices ,FilesIndices_all ], ["Methods",MethodsIndices ,MethodsIndices_all]]:
    #     for Bug_Type in ["All","Most"]:
    #         baseDir=os.path.join(workingDir,Bug_Type)
    #         baseDir=os.path.join(baseDir,granularity)
    #         #for One_or_all,indicesList in [("Fam_one",indicesList_one),("Fam_all",indicesList_all)]:
    #         for One_or_all,indicesList in [("Fam_all",indicesList_all)]:
    #             One_or_allDir=os.path.join(baseDir,"Fam_one")
    #             outDir=os.path.join(baseDir,"ThreeFam_"+One_or_all)
    #             mkOneDir(outDir)
    #             shutil.copyfile(os.path.join("D:\\Amir_Almishali\\projs","BuildEval.bat"),os.path.join(outDir,"BuildEval.bat"))
    #             for ind,indices in enumerate(indicesList):
    #                 outArffTrain=os.path.join(outDir,str(ind)+"_Appended.arff")
    #                 TraintempFile=os.path.join(baseDir,str(ind)+"_tempTrain.arff")
    #                 merge_multiple_arff_file(One_or_allDir,outArffTrain,TraintempFile,[str(x)+"_Appended.arff" for x in indices])
    #                 #print [str(x)+"_Appended.arff" for x in indices]
    #                 outArffTest=os.path.join(outDir,str(ind)+"_Only.arff")
    #                 TesttempFile=os.path.join(baseDir,str(ind)+"_tempTest.arff")
    #                 #print [str(y)+"_Only.arff" for y in indsFamilies(indicesList,[[x for x in range(len(indicesList)) if x != ind]])[0]]
    #                 #merge_multiple_arff_file(One_or_allDir,outArffTest,TesttempFile,[str(y)+"_Only.arff" for y in indices])
    #             #os.system("start /b cmd /x /c \"D: & cd  " + outDir +" &  " + outDir + "\\BuildEval.bat\"")
    #
    #
    # known_indices_files = [0, 3, 5, 6, 8, 11, 14]
    # known_indices_methods = [0, 2]
    # for granularity,indices in [["Files",known_indices_files ], ["Methods",known_indices_methods]]:
    #     for Bug_Type  in ["All","Most"]:
    #         baseDir=os.path.join(workingDir,Bug_Type)
    #         baseDir=os.path.join(baseDir,granularity)
    #         fam_one_path=os.path.join(baseDir,"Fam_one")
    #         append_families_indices(workingDir,wekaJar, fam_one_path, Bug_Type,granularity,indices)
    #ArticleFeaturesMostFiles(workingDir,outArffTrain,outArffTest,tempFile,outCsv,wekaJar,[0,3,5,6,8,11,14])

    #allOne types

def comprasionAll(confFile,globalConfFile):
    vers, gitPath,bugsPath, workingDir = utilsConf.configure(confFile)
    for buggedType in ["All","Most"]:
        Bpath=os.path.join(workingDir,buggedType)
        FilesPath=os.path.join(Bpath,"Files")
        methodsPath=os.path.join(Bpath,"Methods")
        packs=["haelstead","g2","g3","methodsArticles","methodsAdded","hirarcy","fieldsArticles","fieldsAdded","constructorsArticles","constructorsAdded","lastProcess","simpleProcessArticles","simpleProcessAdded","bugs","sourceMonitor","checkStyle","blame"]#,"analyzeComms"]
        FeaturesClasses,Featuresnames=wekaMethods.articles.featuresPacksToClasses(packs)
        wekaMethods.ParseWekaOutput.comprasion(os.path.join(FilesPath,"Fam_one\\out"),os.path.join(FilesPath,"Fam_all\\out"), os.path.join(workingDir,buggedType+"_"+"Files")+".csv",Featuresnames)
        packs=["lastProcessMethods","simpleProcessArticlesMethods","simpleProcessAddedMethods","bugsMethods"]#,"analyzeComms"]
        FeaturesClasses,Featuresnames=wekaMethods.articles.featuresMethodsPacksToClasses(packs)
        wekaMethods.ParseWekaOutput.comprasion(os.path.join(methodsPath,"Fam_one\\out"),os.path.join(methodsPath,"Fam_all\\out"), os.path.join(workingDir,buggedType+"_"+"Methods")+".csv",Featuresnames)


def comprasionThreeFam(confFile,globalConfFile):
    vers, gitPath,bugsPath, workingDir = utilsConf.configure(confFile)
    for buggedType in ["All","Most"]:
        Bpath=os.path.join(workingDir,buggedType)
        FilesPath=os.path.join(Bpath,"Files")
        methodsPath=os.path.join(Bpath,"Methods")
        packs=["Traditional" , "OO", "process" ,"Fault_History"]#,"analyzeComms"]
        wekaMethods.ParseWekaOutput.comprasion(os.path.join(FilesPath,"ThreeFam_Fam_one\\out"),os.path.join(FilesPath,"ThreeFam_Fam_all\\out"), os.path.join(workingDir,"ThreeFam_"+buggedType+"_"+"Files")+".csv",packs)
        packs=["Fault_History","process_version1","process_version2"]#,"analyzeComms"]
        wekaMethods.ParseWekaOutput.comprasion(os.path.join(methodsPath,"ThreeFam_Fam_one\\out"),os.path.join(methodsPath,"ThreeFam_Fam_all\\out"), os.path.join(workingDir,"ThreeFam_"+buggedType+"_"+"Methods")+".csv",packs)


def dictToList(dict,lst):
    ans=[]
    for l in lst:
        ans.append(dict[l])
    return ans

def comprasionTypes(confFile,globalConfFile):
    vers, gitPath,bugsPath, workingDir = utilsConf.configure(confFile)
    learnerOutFile=os.path.join(workingDir,"learner.csv")
    wekaD=os.path.join(workingDir,"weka")
    keys=["TP Rate","FP Rate","Precision","Recall"," F-Measure","MCC","ROC Area","PRC Area"]
    titles=["type","class","TP Rate","FP Rate","Precision","Recall"," F-Measure","MCC","ROC Area","PRC Area"]
    classes=['bugged',"valid","both"]
    filesNames=["testingAll_files.txt", "testingAll_methods.txt", "testingMost_files.txt", "testingMost_methods.txt"]
    lines=[titles]
    for f in filesNames:
        file=os.path.join(wekaD,f)
        Exptype=f.replace(".txt","").replace(".testing","")
        parsedDict=wekaMethods.ParseWekaOutput.Parse(file)
        for d in parsedDict:
          lines.append([Exptype,d]+list(dictToList(parsedDict[d],keys)))
    f=open(learnerOutFile,"wb")
    writer=csv.writer(f)
    writer.writerows(lines)
    f.close()



    #clean(versPath,LocalGitPath)


def reportProjectData(confFile,globalConfFile):
#java -Xmx2024m  -cp "C:\Program Files\Weka-3-7\weka.jar" weka.core.Instances 13_Appended.arff
    vers, gitPath,bugsPath, workingDir = utilsConf.configure(confFile)
    versPath, dbadd=Mkdirs(workingDir,vers)
    LocalGitPath=os.path.join(workingDir,"repo")
    reportCsv=os.path.join(workingDir,"report.csv")
    lastVer=os.path.join(dbadd,vers[-1]+".db")
    testsDB=os.path.join(workingDir,"testsBugsMethods.db")
    report.report(reportCsv,LocalGitPath,lastVer,testsDB)


def wrapperExperiments(confFile):
    vers, gitPath, issue_tracker, issue_tracker_url, issue_tracker_product, workingDir = utilsConf.configure(confFile)
    docletPath,sourceMonitorEXE,checkStyle57,checkStyle68,allchecks,methodsNamesXML,wekaJar,RemoveBat,utilsPath = utilsConf.globalConfig()
    vers_dirs = map(version_to_dir_name, vers)
    weka=os.path.join(workingDir,"weka")
    vers,paths,dates,commits=GitVersInfo("c:\\",gitPath,vers)
    testDb=Agent.bugs_testsDBMethods.basicBuild(workingDir,vers_dirs[-2],dates[-2],dates[-1])
    packsPath = os.path.join(workingDir, "packs.txt")
    Agent.experimentsMethods.packFileCreate(testDb,1,-1, packsPath)
    rnd = str(randint(0,900))
    print rnd
    Experiments(workingDir,weka,packsPath,utilsPath,rnd)

def wrapper_planning(confFile,globalConfFile):
    pass


def wrapper(confFile):
    vers, gitPath,bugsPath, workingDir = utilsConf.configure(confFile)
    versPath, dbadd=Mkdirs(workingDir,vers)
    logfile=open(os.path.join(workingDir,"timeLog.txt"),"wb")
    logfile.write("start "+ str(datetime.datetime.now())+"\n")
    logfile.flush()

    vers,paths,dates,commits=GitVersInfo("c:\\",gitPath,vers)
    LocalGitPath=os.path.join(workingDir,"repo")
    versionsCreate(gitPath, vers, versPath,LocalGitPath)
    mkOneDir(LocalGitPath)

    featuresExtract(vers, versPath, workingDir,LocalGitPath,logfile)
    logfile.write("after featuresExtract "+ str(datetime.datetime.now())+"\n")
    logfile.flush()


    MethodsParsed=os.path.join(os.path.join(LocalGitPath,"commitsFiles"),"CheckStyle.txt")
    changeFile=os.path.join(os.path.join(LocalGitPath,"commitsFiles"),"Ins_dels.txt")
    wekaMethods.buildDB.buildOneTimeCommits(versPath,dbadd,bugsPath,False,-1,vers,"repo",MethodsParsed,changeFile,logfile,dates)
    logfile.write("after buildDB "+ str(datetime.datetime.now())+"\n")
    logfile.flush()


    testVerConfig(workingDir,vers[-2],"ant",dates[-2],dates[-1])
    logfile.write("after testVerConfig "+ str(datetime.datetime.now())+"\n")
    logfile.flush()

    testDb = os.path.join( workingDir , "testsBugsMethods.db")
    packsPath = os.path.join(workingDir, "packs.txt")
    Agent.experimentsMethods.packFileCreate(testDb,1,-1, packsPath)

    weka=os.path.join(workingDir,"weka")
    createBuildMLModels(workingDir,gitPath,weka,vers,dbadd)
    filesExperiments(workingDir,weka,packsPath)
    logfile.write("after filesExperiments "+ str(datetime.datetime.now())+"\n")
    logfile.flush()
    exit()
    methodsExperiments(workingDir,weka,packsPath)
    logfile.write("after methodsExperiments "+ str(datetime.datetime.now())+"\n")
    logfile.flush()

    logfile.close()
    clean(versPath,LocalGitPath)

if __name__ == '__main__':
    # try:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        globalConf = os.path.realpath(os.path.join(current_dir, "../globalConf.txt"))
        csv.field_size_limit(sys.maxint)
        if len(sys.argv) == 1:
            # Planner.planningExperiments.test()
            wekaMethods.buildDB.bugs_test(r"C:\Temp\AntBugs.csv")
            # import Diagnoser.Barinel
            # Diagnoser.Barinel.test()
        else:
            print(sys.argv[1], globalConf)
            if sys.argv[2]=="learn":
                wrapperLearner(sys.argv[1])
            elif sys.argv[2]=="experiments":
                wrapperExperiments(sys.argv[1])
            elif sys.argv[2]=="planning":
                wrapper_planning(sys.argv[1], globalConf)
            elif sys.argv[2]=="all_planning":
                Planner.planningExperiments.planning_for_project(sys.argv[1])
    # except Exception as e:
    #     import traceback
    #     utilsConf.get_configuration().get_marker(utilsConf.ERROR_FILE).error(e.message + "\n")
    #     traceback.print_stack()

