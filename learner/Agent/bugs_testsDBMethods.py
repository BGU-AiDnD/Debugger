__author__ = 'amir'

import sqlite3
import glob
import os
import wekaMethods.pathPackCsv
from xml.dom import minidom
from junitparser import JUnitXml, junitparser
from junitparser.junitparser import Error, Failure
import utilsConf

ALL_FILES_BUGS_QUERY = 'select bugId,name from Commitedfiles where bugId<>0  and name like "%.java" and commiter_date>="{START_DATE}" and commiter_date<="{END_DATE}" order by bugId'
ALL_METHODS_BUGS_QUERY = 'select bugId,methodDir from CommitedMethods where bugId<>0  and methodDir like "%.java%" and commiter_date>="{START_DATE}" and commiter_date<="{END_DATE}" order by bugId'
MOST_MODIFIED_FILES_BUGS_QUERY = 'select Commitedfiles.bugId,Commitedfiles.name  from Commitedfiles , (select max(lines) as l, bugId from Commitedfiles where name like "%.java" and commiter_date>="{START_DATE}" and commiter_date<="{END_DATE}" group by bugId) as T where Commitedfiles.lines=T.l and Commitedfiles.bugId=T.bugId'
MOST_MODIFIED_METHODS_BUGS_QUERY = 'select CommitedMethods.bugId,CommitedMethods.methodDir  from CommitedMethods , (select max(lines) as l, bugId from CommitedMethods where methodDir like "%.java%" and commiter_date>="{START_DATE}" and commiter_date<="{END_DATE}" group by bugId) as T where CommitedMethods.lines=T.l and CommitedMethods.bugId=T.bugId'
SURFIRE_DIR_NAME = 'surefire-reports'

# dir /b /s /O:d >f.txt
#for /f %a in (f.txt) do ( type %a >com.txt)


def test(c):
    fail=c.getElementsByTagName("failure")
    out=len(fail)
    err=c.getElementsByTagName("error")
    if out==0:
        out=len(err)
    return (c.attributes["classname"].value+"."+c.attributes["name"].value,out)


def xmlReadTest(doc):
    outs={}
    xmldoc=minidom.parse(open(doc,"r"))
    suite=xmldoc.getElementsByTagName("testsuite")[0]
    tests= suite.getElementsByTagName("testcase")
    for i in range(len(tests)):
        name,out= test(tests[i])
        outs[name]=out
    return outs


def concatenate(tracesPath, outFile):
    lst = glob.glob(tracesPath+"/*.txt")
    with open(outFile,"wb") as f:
        for fileName in lst:
            f.write(fileName+"\n")
            with open(fileName,"r") as file:
                for line in file:
                    f.write(line)


def testsDBConcatinationMany(dbPath, tracesPath, filesDict, packPath):
    concatFile = os.path.join(tracesPath, "tracesConcat.txt")
    concatenate(tracesPath,concatFile)
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    testsRows=[]
    testsMethodsRows=[]
    testsFilesRowsDict={}
    testName = ""
    with open(concatFile) as f:
        for line in f:
            if "\\Trace_" in line:
                 # here is the test name
                testName = line.split('\\Trace_')[1].split('.txt')[0].split('_')[0]
                testsRows.append([testName])
                conn.commit()
            else:
                # just another trace
                splitted_line = line.split()
                if(len(splitted_line)==0):
                    break
                if(len(splitted_line)!=3):
                    continue
                trace=splitted_line[2].strip()
                fileName, methodName = trace.split("@")
                if "$" in fileName:
                    fileName = fileName.split("$")[0]
                if fileName not in packPath:
                    continue
                fileName = packPath[fileName]
                methodName = fileName+"$"+methodName
                testsMethodsRows.append([testName,methodName,fileName,methodName])
                if not testName in testsFilesRowsDict:
                    testsFilesRowsDict[testName]=set()
                testsFilesRowsDict[testName].add(fileName)
    testsFilesRows=[]
    for testName in testsFilesRowsDict:
        for fileName in testsFilesRowsDict[testName]:
            testsFilesRows.append([testName,fileName,fileName])
    c.executemany("INSERT INTO testsFiles VALUES (?,?,?)", testsFilesRows)
    conn.commit()
    c.executemany("INSERT INTO tests VALUES (?)", testsRows)
    conn.commit()
    c.executemany("INSERT INTO testsMethods VALUES (?,?,?,?)", testsMethodsRows)
    conn.commit()
    conn.close()
    return filesDict


def bugsDBFiles(dbPath, cdtDb, filesDict, startingDate, endDate, bugs_query=ALL_FILES_BUGS_QUERY, bugs_table='buggedFiles'):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    conn2 = sqlite3.connect(cdtDb)
    conn2.text_factory = str
    c2 = conn2.cursor()
    bug_id = bugs_query.format(START_DATE=startingDate, END_DATE=endDate)
    rows=c2.execute(bug_id)
    for r in rows:
        name=r[1]
        if not (".java" in name):
            continue
        fileInd = -1
        if(name in filesDict ):
            fileInd=filesDict[name]
        else:
            filesDict[name]=len(filesDict)
            fileInd=filesDict[name]
        c.execute("INSERT INTO {BUGS_TABLE} VALUES (?,?,?,?)".format(BUGS_TABLE=bugs_table),[r[0],name,fileInd,name])
    conn.commit()
    conn.close()
    return filesDict

def filesDB(gitPath,out):
    pathLen = len(gitPath) + 1  # one for the \
    files_list = []
    for root, dirs, files in os.walk(gitPath): # Walk directory tree
        for f in files:
            full_path = os.path.join(root, f)
            if( os.path.splitext(full_path)[1]=="java"):
                files_list.append("".join(list(full_path)[pathLen:]))
    with open(out,"wb") as f:
        f.writelines(files_list)
    return dict(map(reversed, enumerate(sorted(files_list))))

def FilesNamesIdsToDB(dbPath,allFilesPath):
    f=open(allFilesPath,"r")
    lines=f.readlines()
    lines=[l.split("\n")[0] for l in lines]
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    ind=0
    for l in lines:
        c.execute("INSERT INTO AllFiles VALUES (?,?)",[l,ind])
        ind=ind+1
    conn.commit()
    conn.close()


def createIndexes(dbPath):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    def execute_index(index):
        c.execute(index)
        conn.commit()
    execute_index(' CREATE INDEX IF NOT EXISTS testsFiles_name ON testsFiles (fileName)')
    execute_index(' CREATE INDEX IF NOT EXISTS testsFiles_namename ON testsFiles (name)')
    execute_index(' CREATE INDEX IF NOT EXISTS buggedFiles_name ON buggedFiles (fileName)')
    execute_index(' CREATE INDEX IF NOT EXISTS buggedFilesMostModified_name ON buggedFilesMostModified (fileName)')
    execute_index(' CREATE INDEX IF NOT EXISTS buggedFiles_BugId ON buggedFiles (BugId)')
    execute_index(' CREATE INDEX IF NOT EXISTS buggedFiles_name ON buggedFiles (name)')
    execute_index(' CREATE INDEX IF NOT EXISTS buggedFilesMostModified_BugId ON buggedFilesMostModified (BugId)')
    execute_index(' CREATE INDEX IF NOT EXISTS buggedFilesMostModified_name ON buggedFilesMostModified (name)')
    execute_index("CREATE INDEX IF NOT EXISTS MethodsNames ON testsMethods (methodName)")
    execute_index("CREATE INDEX IF NOT EXISTS MethodsNames_name ON testsMethods (name)")
    execute_index("CREATE INDEX IF NOT EXISTS MethodsTests ON testsMethods (Test)")
    execute_index("CREATE INDEX IF NOT EXISTS MethodsBugged ON buggedMethods (BugId)")
    execute_index("CREATE INDEX IF NOT EXISTS Methods_methodDir ON buggedMethods (methodDir)")
    execute_index("CREATE INDEX IF NOT EXISTS Methods_name ON buggedMethods (name)")
    execute_index("CREATE INDEX IF NOT EXISTS Methods_buggedMethodsMostModified ON buggedMethodsMostModified (BugId)")
    execute_index("CREATE INDEX IF NOT EXISTS buggedMethodsMostModified_methodDir ON buggedMethodsMostModified (methodDir)")
    execute_index("CREATE INDEX IF NOT EXISTS buggedMethodsMostModified_name ON buggedMethodsMostModified (name)")
    conn.close()


def createTables(dbPath):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    c.execute('''CREATE TABLE testsMethods (Test text, methodName text,  fileName text , name text   )''')
    c.execute('''CREATE TABLE tests (Test text)''')
    c.execute('''CREATE TABLE testsOutcomes (Test text, outcome text )''')
    c.execute('''CREATE TABLE testsFiles (Test text, fileName text , name text )''')
    c.execute('''CREATE TABLE buggedFiles (BugId INT, fileName text, fileID INT, name text )''')
    c.execute('''CREATE TABLE buggedFilesMostModified (BugId INT, fileName text, fileID INT, name text )''')
    c.execute('''CREATE TABLE buggedMethods (BugId INT, methodDir text, MethodID INT, name text )''')
    c.execute('''CREATE TABLE buggedMethodsMostModified (BugId INT, methodDir text, MethodID INT, name text )''')
    c.execute('''CREATE TABLE AllFiles (fileName text, fileID INT )''')
    conn.commit()
    conn.close()


def get_tests_results(repo_dir):
    surefire_reports = get_surefire_files(repo_dir)
    outcomes = {}
    for report in surefire_reports:
        for case in JUnitXml.fromfile(report):
            result = 'pass'
            if type(case.result) is Error:
                result = 'error'
            if type(case.result) is Failure:
                result = 'failure'
            outcomes["{classname}@{name}".format(classname=case.classname, name=case.name)] = result
    return outcomes


def get_surefire_files(repo_dir):
    surefire_files = []
    for root, _, files in os.walk(repo_dir):
        for name in files:
            if name.endswith('.xml') and os.path.basename(root) == SURFIRE_DIR_NAME:
                surefire_files.append(os.path.join(root, name))
    return surefire_files

def add_tests_outcome_to_db(testDb, repo_dir):
    conn = sqlite3.connect(testDb)
    conn.text_factory = str
    c = conn.cursor()
    c.executemany("INSERT INTO testsOutcomes VALUES (?, ?)", get_tests_results(repo_dir).items())
    conn.commit()
    conn.close()

@utilsConf.marker_decorator(utilsConf.TEST_DB_MARKER)
def basicBuild(workingDir, ver, startDate, EndDate):
    testDb = os.path.join(workingDir, "testsBugsMethods.db")
    dbData = os.path.join(workingDir,"dbAdd", ver + ".db")
    gitPath = os.path.join(workingDir, "vers", ver, "repo")
    filesDict = filesDB(gitPath, os.path.join(workingDir, "allFiles.txt"))
    createTables(testDb)
    createIndexes(testDb)
    add_tests_outcome_to_db(testDb, os.path.join( workingDir, "testedVer", "repo"))
    packPath = wekaMethods.pathPackCsv.projectPathPacks(gitPath)
    filesDict = testsDBConcatinationMany(testDb, os.path.join(workingDir, "DebuggerTests"),filesDict, packPath)
    filesDict = bugsDBFiles(testDb, dbData, filesDict, startDate, EndDate, ALL_FILES_BUGS_QUERY, 'buggedFiles')
    filesDict = bugsDBFiles(testDb, dbData, filesDict, startDate, EndDate, MOST_MODIFIED_FILES_BUGS_QUERY, 'buggedFilesMostModified')
    filesDict = bugsDBFiles(testDb, dbData, filesDict, startDate, EndDate, ALL_METHODS_BUGS_QUERY, 'buggedMethods')
    filesDict = bugsDBFiles(testDb, dbData, filesDict, startDate, EndDate, MOST_MODIFIED_METHODS_BUGS_QUERY, 'buggedMethodsMostModified')
    FilesNamesIdsToDB(testDb, os.path.join(workingDir, "allFiles.txt"))
    return testDb
