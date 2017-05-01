
__author__ = 'amir'

import sqlite3
import glob
import os
import wekaMethods.pathPackCsv
from xml.dom import minidom
import utilsConf

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
    lst= glob.glob(tracesPath+"/*.txt")
    f=open(outFile,"wb")
    for fileName in lst:
        f.write(fileName+"\n")
        file=open(fileName,"r")
        for line in file:
            f.write(line)
        file.close()
    f.close()


def testsDBConcatinationMany(dbPath, tracesPath , tests,filesDict,methodsDict,packPath):
    concatFile = os.path.join(tracesPath, "tracesConcat.txt")
    concatenate(tracesPath,concatFile)
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    f=open(concatFile,"r")
    testsRows=[]
    testsMethodsRows=[]
    testsFilesRowsDict={}
    testName=""
    for line in f:
        if "\\Trace_" in line:
            testName=line.split("\\")
            testName=testName[len(testName)-1]
            testName=testName.split(".txt")[0]
            testsRows.append([testName,0])
            conn.commit()
            continue
        else:
            s=line.split(" ")
            if(len(s)==0):
                break
            if(len(s)!=3):
                continue

            s=s[2]
            trace=s.split("\n")[0]
            trace=trace.split("\r")[0]
            spl=trace.split("@")
            methodName=spl[1]
            fileName=spl[0]
            if "$" in fileName:
                fileName=fileName.split("$")[0]
            if fileName not in packPath:
                continue
            fileName=packPath[fileName]
            methodName=fileName+"$"+methodName
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
    c.executemany("INSERT INTO tests VALUES (?,?)", testsRows)
    conn.commit()
    c.executemany("INSERT INTO testsMethods VALUES (?,?,?,?)", testsMethodsRows)
    conn.commit()
    conn.close()
    return filesDict




def bugsDBFiles(dbPath,cdtDb,filesDict,startingDate,endDate):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    conn2 = sqlite3.connect(cdtDb)
    conn2.text_factory = str
    c2 = conn2.cursor()
    bug_id = 'select bugId,name from Commitedfiles where bugId<>0  and name like "%.java" and commiter_date>="'+startingDate+'"  and commiter_date<="'+endDate+'" order by bugId'
    rows=c2.execute(bug_id)
    for r in rows:
        name=r[1]
        if not (".java" in name):
            continue
        fileInd=-90
        if(name in filesDict ):
            fileInd=filesDict[name]
        else:
            filesDict[name]=len(filesDict)
            fileInd=filesDict[name]
        c.execute("INSERT INTO buggedFiles VALUES (?,?,?,?)",[r[0],name,fileInd,name])
    conn.commit()
    conn.close()
    return filesDict

def bugsDBFilesMostModified(dbPath,cdtDb,filesDict,startingDate,endDate):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    conn2 = sqlite3.connect(cdtDb)
    conn2.text_factory = str
    c2 = conn2.cursor()
    bug_id = 'select Commitedfiles.bugId,Commitedfiles.name  from Commitedfiles , (select max(lines) as l, bugId from Commitedfiles where name like "%.java" and commiter_date>="'+startingDate+'"  and commiter_date<="'+endDate+'" group by bugId) as T where Commitedfiles.lines=T.l and Commitedfiles.bugId=T.bugId'

    rows=c2.execute(bug_id)
    for r in rows:
        name=r[1]
        if not (".java" in name):
            continue
        fileInd=-90
        if(name in filesDict ):
            fileInd=filesDict[name]
        else:
            filesDict[name]=len(filesDict)
            fileInd=filesDict[name]
        c.execute("INSERT INTO buggedFilesMostModified VALUES (?,?,?,?)",[r[0],name,fileInd,name])
    conn.commit()
    conn.close()
    return filesDict



def bugsDBMethods(dbPath,cdtDb,filesDict,startingDate,endDate):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    conn2 = sqlite3.connect(cdtDb)
    conn2.text_factory = str
    c2 = conn2.cursor()
    bug_id = 'select bugId,methodDir from CommitedMethods where bugId<>0  and methodDir like "%.java%" and commiter_date>="'+startingDate+'"  and commiter_date<="'+endDate+'" order by bugId'
    rows=c2.execute(bug_id)
    for r in rows:
        name=r[1]
        if not (".java" in name):
            continue
        fileInd=-90
        c.execute("INSERT INTO buggedMethods VALUES (?,?,?,?)",[r[0],name,fileInd,name])
    conn.commit()
    conn.close()
    return filesDict

def bugsDBMethodsMostModified(dbPath,cdtDb,filesDict,startingDate,endDate):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    conn2 = sqlite3.connect(cdtDb)
    conn2.text_factory = str
    c2 = conn2.cursor()
    bug_id = 'select CommitedMethods.bugId,CommitedMethods.methodDir  from CommitedMethods , (select max(lines) as l, bugId from CommitedMethods where methodDir like "%.java%" and commiter_date>="'+startingDate+'"  and commiter_date<="'+endDate+'" group by bugId) as T where CommitedMethods.lines=T.l and CommitedMethods.bugId=T.bugId'

    rows=c2.execute(bug_id)
    for r in rows:
        name=r[1]
        if not (".java" in name):
            continue
        fileInd=-90
        c.execute("INSERT INTO buggedMethodsMostModified VALUES (?,?,?,?)",[r[0],name,fileInd,name])
    conn.commit()
    conn.close()
    return filesDict



def filesDB(cdtDb,out):
    conn2 = sqlite3.connect(cdtDb)
    conn2.text_factory = str
    c2 = conn2.cursor()
    names=[]
    filesDict={}
    ind=0
    for row in c2.execute(str('select distinct name from haelsTfiles order by name')):
        name=row[0]
        filesDict[name]=ind
        name=name+"\n"
        ind=ind+1
        names.append(name)
    f=open(out,"wb")
    f.writelines(names)
    f.close()
    return filesDict

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
    index_createA=' CREATE INDEX IF NOT EXISTS testsFiles_name ON testsFiles (fileName)'
    c.execute(index_createA)
    conn.commit()
    index_createA=' CREATE INDEX IF NOT EXISTS testsFiles_namename ON testsFiles (name)'
    c.execute(index_createA)
    conn.commit()
    index_createA=' CREATE INDEX IF NOT EXISTS buggedFiles_name ON buggedFiles (fileName)'
    c.execute(index_createA)
    conn.commit()
    index_createA=' CREATE INDEX IF NOT EXISTS buggedFilesMostModified_name ON buggedFilesMostModified (fileName)'
    c.execute(index_createA)
    conn.commit()
    index_createA=' CREATE INDEX IF NOT EXISTS buggedFiles_BugId ON buggedFiles (BugId)'
    c.execute(index_createA)
    conn.commit()
    index_createA=' CREATE INDEX IF NOT EXISTS buggedFiles_name ON buggedFiles (name)'
    c.execute(index_createA)
    conn.commit()
    index_createA=' CREATE INDEX IF NOT EXISTS buggedFilesMostModified_BugId ON buggedFilesMostModified (BugId)'
    c.execute(index_createA)
    conn.commit()
    index_createA=' CREATE INDEX IF NOT EXISTS buggedFilesMostModified_name ON buggedFilesMostModified (name)'
    c.execute(index_createA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS MethodsNames ON testsMethods (methodName)"
    c.execute(indexA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS MethodsNames_name ON testsMethods (name)"
    c.execute(indexA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS MethodsTests ON testsMethods (Test)"
    c.execute(indexA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS MethodsBugged ON buggedMethods (BugId)"
    c.execute(indexA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS Methods_methodDir ON buggedMethods (methodDir)"
    c.execute(indexA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS Methods_name ON buggedMethods (name)"
    c.execute(indexA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS Methods_buggedMethodsMostModified ON buggedMethodsMostModified (BugId)"
    c.execute(indexA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS buggedMethodsMostModified_methodDir ON buggedMethodsMostModified (methodDir)"
    c.execute(indexA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS buggedMethodsMostModified_name ON buggedMethodsMostModified (name)"
    c.execute(indexA)
    conn.commit()
    conn.close()


def createTables(dbPath):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    c.execute('''CREATE TABLE testsMethods (Test text, methodName text,  fileName text , name text   )''')
    c.execute('''CREATE TABLE tests (Test text, outcome INT )''')
    c.execute('''CREATE TABLE testsFiles (Test text, fileName text , name text )''')
    c.execute('''CREATE TABLE buggedFiles (BugId INT, fileName text, fileID INT, name text )''')
    c.execute('''CREATE TABLE buggedFilesMostModified (BugId INT, fileName text, fileID INT, name text )''')
    c.execute('''CREATE TABLE buggedMethods (BugId INT, methodDir text, MethodID INT, name text )''')
    c.execute('''CREATE TABLE buggedMethodsMostModified (BugId INT, methodDir text, MethodID INT, name text )''')
    c.execute('''CREATE TABLE AllFiles (fileName text, fileID INT )''')
    conn.commit()
    conn.close()


@utilsConf.marker_decorator(utilsConf.TEST_DB_MARKER)
def basicBuild(workingDir,ver,startDate,EndDate):
    testDb = os.path.join( workingDir , "testsBugsMethods.db")
    dbData =os.path.join( workingDir ,"dbAdd\\"+ver+".db")
    gitPath=os.path.join( workingDir , "vers\\"+ver+"\\repo")
    filesDict = filesDB(dbData, workingDir+"allFiles.txt")
    createTables(testDb)

    methodsDict={}
    packPath=wekaMethods.pathPackCsv.projectPathPacks(gitPath)
    filesDict = testsDBConcatinationMany(testDb, os.path.join(workingDir,"DebuggerTests\\"), "", filesDict,methodsDict,packPath)
    filesDict = bugsDBFiles(testDb, dbData, filesDict,startDate,EndDate)
    filesDict = bugsDBFilesMostModified(testDb, dbData, filesDict,startDate,EndDate)
    bugsDBMethods(testDb, dbData, filesDict,startDate,EndDate)
    bugsDBMethodsMostModified(testDb, dbData, filesDict,startDate,EndDate)

    FilesNamesIdsToDB(testDb, workingDir+"allFiles.txt")
    createIndexes(testDb)

    return testDb
