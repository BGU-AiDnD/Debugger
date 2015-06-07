
__author__ = 'amir'

import sqlite3
import glob
import weka.pathPackCsv
from xml.dom import minidom

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

def testsDB(dbPath, tracesPath , tests,filesDict,packPath):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    c.execute('''CREATE TABLE testsFiles (Test text, fileName text, fileID INT )''')
    c.execute('''CREATE TABLE tests (Test text, outcome INT )''')
    files= glob.glob(tracesPath+"*")
    for f in files:
        testName=f.split("\\")
        testName=testName[len(testName)-1]
        testName=testName.split(".txt")[0]
        testName=testName.split("_")[1]
        lines=open(f,"rb").readlines()
        #if(not(testName in tests)):
         #   continue
        out="0"#tests[testName]
        lines=lines[:len(lines)-2]
        c.execute("INSERT INTO tests VALUES (?,?)", [testName,out] )
        for l in lines:
            s=l.split(" ")
            if(len(s)==0):
                break
            s=s[2]
            fileName=s.split("\n")[0]
            fileName=fileName.split("\r")[0]
            if "$" in fileName:
                fileName=fileName.split("$")[0]
            fileInd=-90
            if fileName not in packPath:
                continue
            fileName=packPath[fileName]
            if(fileName in filesDict ):
                fileInd=filesDict[fileName]
            else:
                filesDict[fileName]=len(filesDict)
                fileInd=filesDict[fileName]
                print(fileInd)
            c.execute("INSERT INTO testsFiles VALUES (?,?,?)", [testName,fileName,fileInd])
            conn.commit()
    conn.close()
    return filesDict



def bugsDB(dbPath,cdtDb,filesDict,startingDate,endDate):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    conn2 = sqlite3.connect(cdtDb)
    conn2.text_factory = str
    c2 = conn2.cursor()
    c.execute('''CREATE TABLE buggedFiles (BugId INT, fileName text, fileID INT )''')
    bug_id = 'select bugId,name from Commitedfiles where bugId<>0  and name like "%.java" and commiter_date>="'+startingDate+'"  and commiter_date<="'+endDate+'" order by bugId'
    print bug_id
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
            print(fileInd)
        c.execute("INSERT INTO buggedFiles VALUES (?,?,?)",[r[0],name,fileInd])
    conn.commit()
    conn.close()
    return filesDict


def OnebugsDB(dbPath,cdtDb):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    conn2 = sqlite3.connect(cdtDb)
    conn2.text_factory = str
    c2 = conn2.cursor()
    c.execute('''CREATE TABLE buggedFilesOne (BugId INT, fileName text, fileID INT )''')
    filesDict={}
    for r in c.execute('''select fileName,fileID from buggedFiles '''):
        name=r[0]
        id=r[1]
        filesDict[name]=id
    print filesDict

    bug_id = 'select Commitedfiles.bugId,Commitedfiles.name  from Commitedfiles , (select max(lines) as l, bugId from Commitedfiles where name like "%.java" and commiter_date>="2013-02-14"  and commiter_date<="2013-06-12" group by bugId) as T where Commitedfiles.lines=T.l and Commitedfiles.bugId=T.bugId'
    print bug_id
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
            print(fileInd)
        c.execute("INSERT INTO buggedFilesOne VALUES (?,?,?)",[r[0],name,fileInd])
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
    c.execute('''CREATE TABLE AllFiles (fileName text, fileID INT )''')
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
    index_createA=' CREATE INDEX IF NOT EXISTS buggedFiles_name ON buggedFiles (fileName)'
    c.execute(index_createA)
    conn.commit()
    index_createA=' CREATE INDEX IF NOT EXISTS testsFiles_id ON testsFiles (fileID)'
    c.execute(index_createA)
    conn.commit()
    index_createA=' CREATE INDEX IF NOT EXISTS buggedFiles_Fid ON buggedFiles (fileID)'
    c.execute(index_createA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS FilesNames ON testsFiles (fileName)"
    c.execute(indexA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS FilesTests ON testsFiles (Test)"
    c.execute(indexA)
    conn.commit()
    indexA="CREATE INDEX IF NOT EXISTS FilesBugged ON buggedFiles (BugId)"
    c.execute(indexA)
    conn.commit()



def basicBuild(workingDir,ver,startDate,EndDate):
    #workingDir="C:\projs\\antWorking\\"
    testDb = workingDir + "testsBugs.db"
    dbData = workingDir + "dbAdd\\"+ver+".db"
    gitPath=workingDir + "vers\\"+ver+"\\repo"
    filesDict = filesDB(dbData, workingDir+"allFiles.txt")
    print(len(filesDict))
    # reportsAppend("C:\\GitHub\\agent\\reports","C:\\GitHub\\agent\\reports\\all.xml")
    #filesDict = testsDB("C:\\GitHub\\agent\\testsBugs.db", "C:\\GitHub\\agent\\traces\\", xmlReadTest("C:\\GitHub\\agent\\reports\\all.xml"), filesDict)
    packPath=weka.pathPackCsv.projectPathPacks(gitPath)
    filesDict = testsDB(testDb, workingDir+"traces\\", "", filesDict,packPath)
    print(len(filesDict))
    filesDict = bugsDB(testDb, dbData, filesDict,startDate,EndDate)
    print(len(filesDict))
    new = sorted(filesDict.items(), key=lambda tup: tup[1])
    new = [n[0] + "\n" for n in new]
    f = open("C:\\GitHub\\agent\\allFiles.txt", "wb")
    f.writelines(new)
    f.close()
    FilesNamesIdsToDB(testDb, workingDir+"allFiles.txt")
    createIndexes(testDb)

#OnebugsDB("C:\\GitHub\\agent\\testsBugs.db", "C:\\GitHub\\vers\\db2\\CDT_8_1_24.db")
#filesDict = bugsDB("C:\\GitHub\\agent\\testsBugs.db", "C:\\GitHub\\vers\\dbAdd\\done\\CDT_8_1_2.db", filesDict)
basicBuild("C:\projs\\antWorking\\","ANT_182",'20/12/2010 20:59', '25/02/2012 21:19')
#basicBuild("C:\projs\\poi2Working\\","REL_3_9",'2013-11-28 22:56:20', '2014-08-14 02:51:40')
