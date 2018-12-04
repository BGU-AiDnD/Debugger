import datetime
import os
import sqlite3
import git
from wekaMethods.articles import load_arff, arff_build, write_to_arff, getPaths, Build88_GIT
from wekaMethods.db_builders.buildDB import names_dates

__author__ = 'amir'


def createAllArffs(basicPath):
    names=[i[0] for i in names_dates()]
    orginalPaths=[os.path.join(os.path.join(basicPath,"ML"), str(i+"ML_NEW_alone.arff")) for i in names]
    for n in range(len(names)):
        if n==0:
            continue
        training=os.path.join(os.path.join(basicPath,"ML"), str("TRAINING_"+str(n)+".arff"))
        test=os.path.join(os.path.join(basicPath,"ML"), str("TEST_"+str(n)+".arff"))
        testWild=os.path.join(os.path.join(basicPath,"ML"), str("TEST_WILD"+str(n)+".arff"))
        appendFiles(orginalPaths[:n],training)
        appendFiles(orginalPaths[n:],test)
        testFromFile(test,testWild)
    return  orginalPaths


def appendFiles(filePaths,path_join):
    data=[]
    print "start test"
    attr = [ ( "fileName", "NUMERIC"),( "tot_changes", "NUMERIC"), ( "sum_insert", "NUMERIC"),
            ( "sum_delets", "NUMERIC"), ( "tot_bugs", "NUMERIC"), ( "tot_developers", "NUMERIC"),
            ( "change_set", "NUMERIC"), ( "Operators_count", "NUMERIC"), ( "Operands_count", "NUMERIC"),
            ( "Distinct_operators", "NUMERIC"), ("Distinct_operands", "NUMERIC"), ("complexity", "NUMERIC"), ("avginsertions" , "NUMERIC" )  ,("suminsertions" , "NUMERIC" )  ,("countinsertions"  , "NUMERIC" ),
("avgdeletions" , "NUMERIC" )  ,("sumdeletions" , "NUMERIC" )  ,("countdeletions"  , "NUMERIC" )  ,("avglines" , "NUMERIC")  , ("sumlines" , "NUMERIC" ) , ("countlines" , "NUMERIC" ),
("sum(Commitedfiles.lines)/sum(commits.lines)" , "NUMERIC" ),
("sum(Commitedfiles.insertions)/sum(commits.insertions)" , "NUMERIC" ),
("sum(Commitedfiles.deletions)/ sum(commits.deletions)" , "NUMERIC" ),
("avg(lines)" , "NUMERIC" ),
("avg(insertions)" , "NUMERIC" ),
("avg(deletions)" , "NUMERIC" )#, ("packSet" , "NUMERIC" )
, ( "hasBug", ["yes", "no"])  ]
    for filePath in filePaths:
        data=data+load_arff(filePath)['data']
    print data[:3]
    arff_data = arff_build(attr, data, str(""), "appended")
    #path_join = os.path.join(os.path.join(basicPath,"ML"), str("Appended2.arff"))
    write_to_arff(arff_data, path_join)
    return data


def testFromFile(filePath,path_join):
    data=[]
    print "start test"
    attr = [ ( "fileName", "NUMERIC"),( "tot_changes", "NUMERIC"), ( "sum_insert", "NUMERIC"),
            ( "sum_delets", "NUMERIC"), ( "tot_bugs", "NUMERIC"), ( "tot_developers", "NUMERIC"),
            ( "change_set", "NUMERIC"), ( "Operators_count", "NUMERIC"), ( "Operands_count", "NUMERIC"),
            ( "Distinct_operators", "NUMERIC"), ("Distinct_operands", "NUMERIC"), ("complexity", "NUMERIC"), ("avginsertions" , "NUMERIC" )  ,("suminsertions" , "NUMERIC" )  ,("countinsertions"  , "NUMERIC" ),
("avgdeletions" , "NUMERIC" )  ,("sumdeletions" , "NUMERIC" )  ,("countdeletions"  , "NUMERIC" )  ,("avglines" , "NUMERIC")  , ("sumlines" , "NUMERIC" ) , ("countlines" , "NUMERIC" ),
("sum(Commitedfiles.lines)/sum(commits.lines)" , "NUMERIC" ),
("sum(Commitedfiles.insertions)/sum(commits.insertions)" , "NUMERIC" ),
("sum(Commitedfiles.deletions)/ sum(commits.deletions)" , "NUMERIC" ),
("avg(lines)" , "NUMERIC" ),
("avg(insertions)" , "NUMERIC" ),
("avg(deletions)" , "NUMERIC" )#, ("packSet" , "NUMERIC" )
, ( "hasBug", ["yes", "no"])  ]
    test_data=[d[:26]+["?"] for d in load_arff(filePath)['data']]
    print test_data[:3]
    arff_data = arff_build(attr, test_data, str(""), filePath)
    #path_join = os.path.join(os.path.join(basicPath,"ML"), str("testSuit_800.arff"))
    write_to_arff(arff_data, path_join)
    return data


def testAns(basicPath):
    names,paths=getPaths(basicPath)
    dates =[i[1] for i in names_dates()]
    i=0
    data=[]
    print "start test"
    attr = [ ( "fileName", "NUMERIC"),( "tot_changes", "NUMERIC"), ( "sum_insert", "NUMERIC"),
            ( "sum_delets", "NUMERIC"), ( "tot_bugs", "NUMERIC"), ( "tot_developers", "NUMERIC"),
            ( "change_set", "NUMERIC"), ( "Operators_count", "NUMERIC"), ( "Operands_count", "NUMERIC"),
            ( "Distinct_operators", "NUMERIC"), ("Distinct_operands", "NUMERIC"), ("complexity", "NUMERIC"), ("avginsertions" , "NUMERIC" )  ,("suminsertions" , "NUMERIC" )  ,("countinsertions"  , "NUMERIC" ),
("avgdeletions" , "NUMERIC" )  ,("sumdeletions" , "NUMERIC" )  ,("countdeletions"  , "NUMERIC" )  ,("avglines" , "NUMERIC")  , ("sumlines" , "NUMERIC" ) , ("countlines" , "NUMERIC" ),
("sum(Commitedfiles.lines)/sum(commits.lines)" , "NUMERIC" ),
("sum(Commitedfiles.insertions)/sum(commits.insertions)" , "NUMERIC" ),
("sum(Commitedfiles.deletions)/ sum(commits.deletions)" , "NUMERIC" ),
("avg(lines)" , "NUMERIC" ),
("avg(insertions)" , "NUMERIC" ),
("avg(deletions)" , "NUMERIC" )#, ("packSet" , "NUMERIC" )
, ( "hasBug", ["yes", "no"])  ]
    i=len(names)-2
    #i=i+1
    os_path_join = os.path.join(os.path.join(basicPath, "db2"), str(names[i] + "4.db"))
    print(os_path_join)
    test_data,n=arff88_for_tag(os_path_join, dates[i], False)
    arff_data = arff_build(attr, test_data, str(n), "testSuit3_Ans")
    path_join = os.path.join(os.path.join(basicPath,"ML"), str("testSuit_Ans_new2.arff"))
    write_to_arff(arff_data, path_join)
    return data


def test(basicPath):
    names,paths=getPaths(basicPath)
    dates =[i[1] for i in names_dates()]
    i=0
    data=[]
    print "start test"
    attr = [ ( "fileName", "NUMERIC"),( "tot_changes", "NUMERIC"), ( "sum_insert", "NUMERIC"),
            ( "sum_delets", "NUMERIC"), ( "tot_bugs", "NUMERIC"), ( "tot_developers", "NUMERIC"),
            ( "change_set", "NUMERIC"), ( "Operators_count", "NUMERIC"), ( "Operands_count", "NUMERIC"),
            ( "Distinct_operators", "NUMERIC"), ("Distinct_operands", "NUMERIC"), ("complexity", "NUMERIC"), ("avginsertions" , "NUMERIC" )  ,("suminsertions" , "NUMERIC" )  ,("countinsertions"  , "NUMERIC" ),
("avgdeletions" , "NUMERIC" )  ,("sumdeletions" , "NUMERIC" )  ,("countdeletions"  , "NUMERIC" )  ,("avglines" , "NUMERIC")  , ("sumlines" , "NUMERIC" ) , ("countlines" , "NUMERIC" ),
("sum(Commitedfiles.lines)/sum(commits.lines)" , "NUMERIC" ),
("sum(Commitedfiles.insertions)/sum(commits.insertions)" , "NUMERIC" ),
("sum(Commitedfiles.deletions)/ sum(commits.deletions)" , "NUMERIC" ),
("avg(lines)" , "NUMERIC" ),
("avg(insertions)" , "NUMERIC" ),
("avg(deletions)" , "NUMERIC" )#, ("packSet" , "NUMERIC" )
, ( "hasBug", ["yes", "no"])  ]
    i=len(names)-2
    #i=i+1
    os_path_join = os.path.join(os.path.join(basicPath, "db2"), str(names[i] + "4.db"))
    print(os_path_join)
    test_data,n=arff88_for_tag(os_path_join, dates[i], True)
    arff_data = arff_build(attr, test_data, str(n), "testSuit3")
    path_join = os.path.join(os.path.join(basicPath,"ML"), str("testSuit_new2.arff"))
    write_to_arff(arff_data, path_join)
    return data


def arff88_alone(basicPath,i=0):
    names,paths=getPaths(basicPath)
    dates =[l[1] for l in names_dates()]
    data=[]
    print "start"
    attr = [ ( "fileName", "NUMERIC"),( "tot_changes", "NUMERIC"), ( "sum_insert", "NUMERIC"),
            ( "sum_delets", "NUMERIC"), ( "tot_bugs", "NUMERIC"), ( "tot_developers", "NUMERIC"),
            ( "change_set", "NUMERIC"), ( "Operators_count", "NUMERIC"), ( "Operands_count", "NUMERIC"),
            ( "Distinct_operators", "NUMERIC"), ("Distinct_operands", "NUMERIC"), ("complexity", "NUMERIC"), ("avginsertions" , "NUMERIC" )  ,("suminsertions" , "NUMERIC" )  ,("countinsertions"  , "NUMERIC" ),
("avgdeletions" , "NUMERIC" )  ,("sumdeletions" , "NUMERIC" )  ,("countdeletions"  , "NUMERIC" )  ,("avglines" , "NUMERIC")  , ("sumlines" , "NUMERIC" ) , ("countlines" , "NUMERIC" ),
("sum(Commitedfiles.lines)/sum(commits.lines)" , "NUMERIC" ),
("sum(Commitedfiles.insertions)/sum(commits.insertions)" , "NUMERIC" ),
("sum(Commitedfiles.deletions)/ sum(commits.deletions)" , "NUMERIC" ),
("avg(lines)" , "NUMERIC" ),
("avg(insertions)" , "NUMERIC" ),
("avg(deletions)" , "NUMERIC" )#, ("packSet" , "NUMERIC" )
, ( "hasBug", ["yes", "no"])  ]
    allNames=[]
    print names[i]
    #while (i+2<len(names)):
    os_path_join = os.path.join(os.path.join(basicPath, "db2"), str(names[i] + "4.db"))
    tag,nam = arff88_for_tag(os_path_join, dates[i],i, False)
    data=data+ tag
	#allNames=allNames+nam
    arff_data = arff_build(attr, data,str(allNames) , "base")
    path_join = os.path.join(os.path.join(basicPath,"ML"), str(names[i]+"ML_sec_alone.arff"))
    write_to_arff(arff_data, path_join)
    print i
    i=i+1
    return data


def arff88_for_file(dbpath,filename,start_date,end_date):
        conn = sqlite3.connect(dbpath)
        conn.text_factory = str
        c = conn.cursor()
        tot_changes=0
        sum_insert=0
        sum_delets=0
        tot_bugs=0
        tot_developers=0
        change_set=0
        complexity=0
        Operators_count, Operands_count , Distinct_operators  , Distinct_operands= 0,0,0,0
        s = str(
            'select name,count(*),sum(insertions),sum(deletions) from commitedfiles WHERE name="' + filename + '"   and commitedfiles.commiter_date<="' + str(
                start_date) + '"' + '  and commitedfiles.commiter_date<="' + str(end_date) + '"')
        for row in c.execute(s):
            tot_changes=(row[1])
            sum_insert=(row[2])
            sum_delets=(row[3])
        sql = str(
            'select name,count(bugId) from commitedfiles where bugID<>0 AND commitedfiles.name="' + filename + '"   and commitedfiles.commiter_date<="' + str(
                start_date) + '"' + '  and commitedfiles.commiter_date<="' + str(end_date) + '"')
        for row in c.execute(sql):
            tot_bugs=row[1]
        for row in c.execute(str('select name,count(distinct author) from commitedfiles,commits where commits.ID=commitedfiles.commitid  AND name="'+filename+'"   and commitedfiles.commiter_date<="' + str(start_date)+ '"'+'  and commitedfiles.commiter_date<="' + str(end_date)+ '"')):
            tot_developers=row[1]
        for row in c.execute(str('select count(distinct Commitedfiles.name) from Commitedfiles where commitid in (select commitid from Commitedfiles where name="' +filename+'"  and commitedfiles.commiter_date<="' + str(start_date)+ '")')):
            change_set=row[0]
        for row in c.execute(str('select * from Complexyfiles  where name="' +filename+ '"')):
            complexity=row[1]
        for row in c.execute(str('select   Operators_count, Operands_count , Distinct_operators  , Distinct_operands from  haelsTfiles  where  name="'+filename+'"')):
            Operators_count, Operands_count , Distinct_operators  , Distinct_operands= row[0],row[1],row[2],row[3]
        add=[filename,tot_changes,sum_insert,sum_delets,tot_bugs,tot_developers,change_set,Operators_count, Operands_count , Distinct_operators  , Distinct_operands,complexity]
#my own metrics
        avg_insert=0
        avg_del=0
        avg_lines=0
        sum_lines=0
        sum_dels=0
        sum_ins=0
        count_ins=0
        count_del=0
        count_lines=0
        mets=[]
        where_clause=' WHERE name="'+filename+'"  and commitedfiles.commiter_date<="' + str(start_date)+'"'+'  and commitedfiles.commiter_date<="' + str(end_date)+'"'
        clause = str("select name,avg(insertions),sum(insertions),count(insertions),avg(deletions),sum(deletions),count(deletions), avg(lines),sum(lines),count(lines)from Commitedfiles" + where_clause)
        for row in c.execute(clause
        ):
            mets=row[1:]
        add=add+list(mets)
        for row in c.execute(
            """
select Commitedfiles.name,
cast(sum(Commitedfiles.lines) as float) / cast(sum(commits.lines) as float) ,
cast(sum(Commitedfiles.insertions) as float) / cast(sum(commits.insertions) as float) ,
cast(sum(Commitedfiles.deletions) as float) / cast(sum(commits.deletions) as float)
from Commitedfiles, commits
            """+where_clause+ " and Commitedfiles.commitid=commits.ID"
        ):
            mets=row[1:]
        add=add+list(mets)

        exe = """
select name,  avg(lines), avg(insertions), avg(deletions)
from (select Commitedfiles.name as name,
	cast((Commitedfiles.lines) as float) / cast((commits.lines) as float) as lines ,
	cast((Commitedfiles.insertions) as float) / cast((commits.insertions) as float) as insertions ,
	cast((Commitedfiles.deletions) as float) / cast((commits.deletions) as float) as deletions
	from Commitedfiles, commits
	where Commitedfiles.commitid=commits.ID and name=\"""" + filename + """" and  commitedfiles.commiter_date<=""""" + '"' + str(
            start_date) + '"' + """ and  commitedfiles.commiter_date<=""""" + '"' + str(end_date) + '"' + """)
            """
        for row in c.execute(
                exe
        ):
            mets=row[1:]
        add=add+list(mets)
        splitted=filename.split("\\")
        pack="\\".join(splitted[0:len(splitted)-1])
        date_ = """
select count(distinct Commitedfiles.name)
from Commitedfiles
where commitid in
	(select commitid
	from Commitedfiles
	where name like \"%""" + pack + """%\" and commitedfiles.commiter_date<="' """ + str(start_date) + """ '") """
       # print date_
        for row in c.execute(
                date_
        ):
            mets=row[1:]
        add=add+list(mets)


        #
        d=[]
        for i in add:
            put=0
            if i!=None:
                put=i
            d=d+[put]
        conn.close()
        return d


def article88_GIT(basicPath,bugsPat,max):
    names,paths=getPaths(basicPath)
    paths_db=[os.path.join(os.path.join(basicPath,"db2"),str(i+"4.db")) for i in names]
    i=len(names)-2
    Build88_GIT(paths[i+1] #git
            ,paths_db
            ,bugsPat
            ,max)


def Build88(gitPath,haelsPath, dbPath,mccabePath , max):
    conn = sqlite3.connect(dbPath)
    conn.text_factory = str
    c = conn.cursor()
    c.execute('''CREATE TABLE files (id INT,name text)''')
    c.execute('''CREATE TABLE haelsTfiles (name text, Operators_count INT, Distinct_operators INT, Operands_count INT, Distinct_operands INT, Program_length INT, Program_vocabulary INT,Volume float, Difficulty INT, Effort float)''')
    c.execute('''CREATE TABLE Complexyfiles (name text, complex INT)''')
    files=allFiles(gitPath,max)
    # add files to table files
    i=0
    for f in files:
        c.execute("INSERT INTO files VALUES (?,?)", (i,f))
        i=i+1
    conn.commit()
    # add files to table files
    hael=buildHael(haelsPath,max)
    for h in hael:
        c.execute("INSERT INTO haelsTfiles VALUES (?,?,?,?,?,?,?,?,?,?)", h[0])
    conn.commit()
    comp=fileRead(mccabePath)
    for h in comp:
        c.execute("INSERT INTO Complexyfiles VALUES (?,?)", h)
    conn.commit()
    conn.close()


def Build88_GIT(gitPath, dbPath_all,bugsPath, max):
    commits,commitedFiles,bugs=BuildRepo(gitPath,bugsPath,max)
    files=allFiles(gitPath,max)
    for dbPath in dbPath_all:
        conn = sqlite3.connect(dbPath)
        conn.text_factory = str
        c = conn.cursor()
        c.execute('''CREATE TABLE commits (ID INT, bugId INT, commiter_date DateTime , commiter text,author_date DateTime , author text  , lines INT,deletions INT,insertions INT,files INT,size INT, parentID INT,reachable_commits INT, message text )''')
        c.execute('''CREATE TABLE Commitedfiles (id INT,name text, commitid INT, commiter_date DateTime,lines INT,deletions INT,insertions INT, bugId INT)''')
        c.execute('''CREATE TABLE bugs (ID INT,Product text,Component text,Assigned_To text,Status text,Resolution text,Reporter text,Last_Modified text ,Version text,Milestone text,Hardware text,OS text,Priority text,Severity text,Summary text,Keywords text,Submit_Date text ,Blocks text,Depends_On text,Duplicate_Of INT,CC text)''')
        for com in commits:
            print com
            c.execute("INSERT INTO commits VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", com)
            #can add commits and bugs to table and commited
        conn.commit()
        for bug in bugs:
            c.execute("INSERT INTO bugs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", bug)
        conn.commit()
        commited=[]
        for file in commitedFiles:
            file_ = file[0]
            files_index=-1
            if (file_ in files):
                files_index = files.index(file_)
            t = files_index,
            commited.append(t +file)
        for comFile in commited:
            c.execute("INSERT INTO Commitedfiles VALUES (?,?,?,?,?,?,?,?)", comFile)
        conn.commit()
        conn.close()


def article88(basicPath,max,i=0):
    names,paths=getPaths(basicPath)
    while (i+1<len(names)):
        mccabePath="C:\Users\Amir-pc\Documents\GitHub\\vers\mccabe\\"+names[i]+".xml"
        Build88(paths[i+1] #git
            ,paths[i]  #hael   the differ is to assignee the bugs known until the i+1 tag to the i source code
            ,os.path.join(os.path.join(basicPath,"db2"),str(names[i]+"4.db"))
            ,mccabePath
            ,max)
        i=i+1


def names_dates_GIT():
    repo = git.Repo("C:\Users\Amir-pc\Documents\GitHub\org.eclipse.cdt")
    tar=repo.tags
    u = [0,6,27,48,53,56,59,62,63,64#,65
	,66,67,68
        ,69
		]
    specifiedTags = []
    for u1 in u:
        specifiedTags.append(tar[u1])
    dates= [datetime.datetime.fromtimestamp(i.commit.committed_date).strftime('%Y-%m-%d') for i in specifiedTags]
    t,d= ([str(i) for i in specifiedTags],dates)
    zip1 = zip(t, d)
    return sorted(zip1,cmp=lambda d1,d2: d1>d2)


def names_commits_GIT():
    repo = git.Repo("C:\\GitHub\\vers\CDT_8_2_0\org.eclipse.cdt")
    tar=repo.tags
    u = [0,6,27,48,53,56,59,62,63,64#,65
	,66,67,68
        ,69
		]
    specifiedTags = []
    for u1 in u:
        specifiedTags.append(tar[u1])
    commits= [str(int("".join(list(i.commit.hexsha)[:7]),16))  for i in specifiedTags]
    t,d= ([str(i) for i in specifiedTags],commits)
    zip1 = zip(t, d)
    return sorted(zip1,cmp=lambda d1,d2: d1>d2)


def arff88_for_tag(dbpath,dates,i, isTest,max):
    start_date=dates[i]
    end_date=dates[i+1]
    print dbpath
    conn = sqlite3.connect(dbpath)
    conn.text_factory = str
    c = conn.cursor()
    conn1 = sqlite3.connect(dbpath)
    conn1.text_factory = str
    c1 = conn1.cursor()
    data=[]
    add=[]
    names=[]
    count=0
    for row in c.execute(str('select distinct name from haelsTfiles order by name')):
        name=row[0]
        if (count==max):
            break
        count=count+1
        names.append(name)
        add=arff88_for_file(dbpath,name,start_date,end_date)
        bug="no"
        s = str('select bugid from commits where bugid<>0 and commiter_date>="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" and id in (select commitid from Commitedfiles where name= "' + name + '")')
        for r in c1.execute(s):
            if(r[0]!=0):
                bug="yes"
                break
        if(isTest):
           bug="?"
        add.append(str(bug))
        data=data+[add]
    conn.close()
    conn1.close()
    return data,names