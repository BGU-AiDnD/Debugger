__author__ = 'Amir-pc'

import arff

from wekaMethods.buildDB import *
from wekaMethods.commentedCodeDetector import *
import features.process as process
import features.haelstead as haelstead
import features.OO as OO
import features.OOFamilies as OOFamilies
import features.sourceMonitor as sourceMonitor
import features.checkStyle as checkStyle
import features.blame as blame
import features.processFamilies as processFamilies
import features.analyzeComms as analyzeComms
import features.analyzeLast as analyzeLast
import featuresMethods.processMethods as processMethods
import featuresMethods.haelsteadMethods as haelsteadMethods
import featuresMethods.OOMethods as OOMethods
import featuresMethods.OOFamiliesMethods as OOFamiliesMethods
import featuresMethods.sourceMonitorMethods as sourceMonitorMethods
import featuresMethods.checkStyleMethods as checkStyleMethods
import featuresMethods.blameMethods as blameMethods
import featuresMethods.analyzeCommsMethods as analyzeCommsMethods
import featuresMethods.analyzeLastMethods as analyzeLastMethods
import featuresMethods.processMethodsFamilies as processMethodsFamilies
import Agent.pathTopack


#for %%l in (1,2,3,4,5,6,7,8,9,10,11,12) do (
#java -classpath ../weka/weka.jar weka.classifiers.trees.J48  -t TRAINING_%%l.arff -x 10 -d MOEDL_%%l.model
#java -classpath ../weka/weka.jar weka.classifiers.trees.J48  -l MOEDL_%%l.model -T TEST_WILD%%l.arff -p 0 > WEKA_%%l.txt  )


def arff_build(attributes, data,desc,relation):
    dict={}
    dict['attributes']=attributes
    dict['data']=data
    dict['description']=desc
    dict['relation']=relation
    return dict


def write_to_arff(data,filename):
    f = open(filename, 'w')
    f.write(arff.dumps(data))
    f.close()

def load_arff(filename):
    f = open(filename, 'r')
    arf= arff.loads(f.read())
    f.close()
    return arf

def names_commits():
    return [('CDT_1_2_1_M1', '196802131'), ('CDT_2_0', '93917497'), ('CDT_3_0', '175441672'), ('CDT_4_0_0', '149351409'), ('CDT_5_0_0', '17941490'), ('CDT_6_0_0', '82248927'), ('CDT_7_0_0', '175959399'), ('CDT_8_0_0', '89147757'), ('CDT_8_0_1', '142873029'), ('CDT_8_0_2', '221902410'), ('CDT_8_1_0', '84025691'), ('CDT_8_1_1', '61881040'), ('CDT_8_1_2', '107737174'), ('CDT_8_2_0', '138165869')]


def names_dates():
    return [('CDT_8_0_1', '2011-09-15'), ('CDT_8_0_2', '2012-02-11'), ('CDT_8_1_0', '2012-06-10'), ('CDT_8_1_1', '2012-09-17'), ('CDT_8_1_2', '2013-02-14'), ('CDT_8_2_0', '2013-06-12')]

def getPaths(basicPath):
    lst =[i[0] for i in names_dates()]
    return (lst, [os.path.join(basicPath, os.path.join(n, "org.eclipse.cdt")) for n in lst])

def EclipseInfo(basicPath):
    names,paths=getPaths(basicPath)
    dates =[i1[1] for i1 in names_dates()]
    commits =[i1[1] for i1 in names_commits()]
    return names,paths,dates,commits


def GitVersInfo(basicPath,repoPath,vers):
    r=git.Repo(repoPath)
    wanted=[ x.commit for x in r.tags if x.name in vers]
    commits=[int("".join(list(x.hexsha)[:7]),16) for x in wanted]
    dates=[datetime.datetime.fromtimestamp(x.committed_date).strftime('%Y-%m-%d %H:%M:%S') for x in wanted]
    paths=[os.path.join(basicPath, os.path.join(n, "repo")) for n in vers]
    return vers,paths,dates,commits




def createIndex(c, conn):
    index_createA = ' CREATE INDEX IF NOT EXISTS commits_id ON commits (ID)'
    c.execute(index_createA)
    conn.commit()
    index_createB = ' CREATE INDEX IF NOT EXISTS commitedFiles_Commitid ON commitedfiles (commitid)'
    c.execute(index_createB)
    conn.commit()
    index_createC = '  CREATE INDEX IF NOT EXISTS commitedFiles_Name ON commitedfiles (name)'
    c.execute(index_createC)
    conn.commit()
    index_createC = '  CREATE INDEX IF NOT EXISTS Commitedfiles_bugId ON Commitedfiles (bugId)'
    c.execute(index_createC)
    conn.commit()


def sqlToAttributes(basicAtt, c, files_dict, first):
    Att_dict = {}
    for f in files_dict.keys():
        Att_dict[f] = list(basicAtt)
    for row in c.execute(first):
        name = Agent.pathTopack.pathToPack(row[0])
        if (name in Att_dict):
            Att_dict[name] = list(row[1:])
    for f in Att_dict:
        files_dict[f] = files_dict[f] + Att_dict[f]

def sqlToAttributesBest(basicAtt, c, files_dict, first,best):
        Att_dict = {}
        for f in files_dict.keys():
            Att_dict[f] = list(basicAtt)
        for row in c.execute(first):
            name = Agent.pathTopack.pathToPack(row[0])
            if (name in Att_dict):
                ret=[]
                all=list(row[1:])
                for i in range(len(all)):
                    if i+1 in best:
                        ret.append(all[i])
                Att_dict[name] = ret
        for f in Att_dict:
            files_dict[f] = files_dict[f] + Att_dict[f]


def arff88_ByTag_Past(dbpath,dates,commits,i, isTest,max,buggedType):
    prev_date=dates[i-1]
    start_date=dates[i]
    end_date=dates[i+1]

    print dbpath
    conn = sqlite3.connect(dbpath)
    conn.text_factory = str
    c = conn.cursor()

    files_dict={}
    createIndex(c, conn)

    wanted_files='select distinct name from commitedfiles order by name'
    wanted_files='select distinct name from haelsTfiles  where Difficulty>5 order by name'
    for row in c.execute(wanted_files):
        name=Agent.pathTopack.pathToPack(row[0])
        files_dict[name]=[]

    first='select name, count(*),  sum(insertions),sum(deletions),count(distinct bugId)-1  from commitedfiles where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by name'
    sqlToAttributes(["0", "0", "0", "0"], c, files_dict, first)

    first_last='select name, count(*),  sum(insertions),sum(deletions),count(distinct bugId)-1  from commitedfiles where commiter_date>="' + str(prev_date)+ '"' + '  and commiter_date<="' + str(start_date) + '" group by name'
    sqlToAttributes(["0", "0", "0", "0"], c, files_dict, first_last)

    disAuthors='select name,count(distinct author) from commitedfiles,commits where commits.ID=commitedfiles.commitid  and commits.commiter_date<="' + str(start_date)+ '"' + '  and commits.commiter_date<="' + str(end_date) + '" group by Commitedfiles.name'
    sqlToAttributes(["0"], c, files_dict, disAuthors)

    disAuthors_last='select name,count(distinct author) from commitedfiles,commits where commits.ID=commitedfiles.commitid  and commits.commiter_date>="' + str(prev_date)+ '"' + '  and commits.commiter_date<="' + str(start_date) + '" group by Commitedfiles.name'
    sqlToAttributes(["0"], c, files_dict, disAuthors_last)

    last_commit='select name,julianday("'+ str(start_date)+'")-julianday(max(commiter_date)) from commitedfiles  where commitedfiles.commiter_date<="' + str(start_date)+ '"' + '  and commitedfiles.commiter_date<="' + str(end_date) + '" group by Commitedfiles.name'
    sqlToAttributes(["0"], c, files_dict, last_commit)

    last_bug='select name,julianday("'+ str(start_date)+'")-julianday(max(commiter_date)) from commitedfiles  where bugId<>0 and commitedfiles.commiter_date<="' + str(start_date)+ '"' + '  and commitedfiles.commiter_date<="' + str(end_date) + '" group by Commitedfiles.name'
    sqlToAttributes(["0"], c, files_dict, last_bug)

    last_ver_bug='select name,julianday("'+ str(start_date)+'")-julianday(max(commiter_date)) from commitedfiles  where bugId<>0 and commitedfiles.commiter_date>="' + str(prev_date)+ '"' + '  and commitedfiles.commiter_date<="' + str(start_date) + '" group by Commitedfiles.name'
    sqlToAttributes(["0"], c, files_dict, last_ver_bug)

    changeSet='select A.name,count(distinct B.name) from Commitedfiles as A, Commitedfiles as B where A.commitid=B.commitid and A.commiter_date<="' + str(start_date)+ '"' + '  and A.commiter_date<="' + str(end_date) + '" and B.commiter_date<="' + str(start_date)+ '"' + '  and B.commiter_date<="' + str(end_date) + '" group by A.name'
    sqlToAttributes(["0"], c, files_dict, changeSet)

    age='select name, sum( julianday(commiter_date)*insertions ) -sum( julianday(commiter_date)*deletions ) from Commitedfiles  where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) +'" group by name'
    sqlToAttributes(["0"], c, files_dict, age)

    age='select name, julianday("'+ str(start_date)+'")*(sum(insertions)-sum(deletions))-sum( julianday(commiter_date)*insertions ) -sum( julianday(commiter_date)*deletions ) from Commitedfiles  where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) +'" group by name'
    sqlToAttributes(["0"], c, files_dict, age)

    hael='select   name,Operators_count, Operands_count , Distinct_operators  , Distinct_operands,Program_length , Program_vocabulary ,Volume , Difficulty , Effort from  haelsTfiles group by name'
    sqlToAttributes(["0", "0", "0", "0","0","0", "0", "0", "0"], c, files_dict, hael)

    complex='select * from Complexyfiles group by name'
    sqlToAttributes(["0"], c, files_dict, complex)

    javaDocClassess='select path,exception,abstract,serializable  from classes '
    sqlToAttributes([ "false", "false", "false"], c, files_dict, javaDocClassess)

    countMethds="select classes.path,count(*) from classes,methods where classes.name=methods.className group by classes.path"
    sqlToAttributes(["0"], c, files_dict, countMethds)

    countMethds="select classes.path,cast(count(distinct methods.name) as real)/count(methods.name) from classes,methods where classes.name=methods.className group by classes.path"
    sqlToAttributes(["0"], c, files_dict, countMethds)

    countPrivatesMethds="select classes.path,count(*) from classes,methods where classes.name=methods.className and methods.scope=\"private\" group by classes.path"
    sqlToAttributes(["0"], c, files_dict, countPrivatesMethds)

    avgMethodsParams="select classes.path,avg(methods.Num_params) from classes,methods where classes.name=methods.className group by classes.path"
    sqlToAttributes(["0"], c, files_dict, avgMethodsParams)

    countFields="select classes.path,count(*) from classes,fields where classes.name=fields.className group by classes.path"
    sqlToAttributes(["0"], c, files_dict, countFields)

    countPrivateFields="select classes.path,count(*) from classes,fields where classes.name=fields.className and fields.scope=\"private\" group by classes.path"
    sqlToAttributes(["0"], c, files_dict, countPrivateFields)

    objectFields="select classes.path,count(*) from classes,fields where classes.name=fields.className and fields.type in (select distinct name from classes) group by classes.path"
    sqlToAttributes(["0"], c, files_dict, objectFields)

    countConst="select classes.path,count(*) from classes,constructors where classes.name=constructors.className group by classes.path"
    sqlToAttributes(["0"], c, files_dict, countConst)

    UsedThis="select classes.path,count(*) from classes,fields where classes.name=fields.type group by classes.path"
    sqlToAttributes(["0"], c, files_dict, UsedThis)

    sourceMethodsFiles='''select  name ,Lines ,	Statements ,	Percent_Branch_Statements ,Method_Call_Statements ,Percent_Lines_with_Comments
 ,Classes_and_interfaces ,Methods_per_Class ,
 Average_Statements_per_Method  ,
 Maximum_Complexity
   ,Average_Block_Depth	, Average_Complexity	,
 Statements_at_block_level_0 ,Statements_at_block_level_1 ,Statements_at_block_level_2 ,Statements_at_block_level_3 ,Statements_at_block_level_4 ,
 Statements_at_block_level_5 ,Statements_at_block_level_6 ,Statements_at_block_level_7 ,Statements_at_block_level_8 ,Statements_at_block_level_9  from JAVAfiles'''
    sqlToAttributes(["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"], c, files_dict, sourceMethodsFiles)

    style='select * from checkStyle group by name'
    sqlToAttributes(["0","0","0","0","0","0","0","0","0"], c, files_dict, style)

    blame='select name ,diff_commits  ,diff_commits_lastver  ,groups   ,committers  ,julianday("'+ str(start_date)+'")-julianday(avg_date)  ,julianday("'+ str(start_date)+'")-julianday(median_date)   ,julianday("'+ str(start_date)+'")-julianday(max_date)  ,numBlobs  , numPatchs  ,numCommits    from blame group by name'
    sqlToAttributes(["0","0","0","0","0","0","0","0","0","0"], c, files_dict, blame)

    styleAnalyze='select name ,sum(McCabe) ,sum(fanOut) ,sum(NPath) ,sum(FileLen) , sum(NCSS) , sum(outer) , sum(publicMethods) , sum(totalMethods) ,sum(thorwsSTM) ,sum(Coupling) ,sum(Executables) , sum(depthFor) ,sum(depthIf) from checkStyleAnalyze,commits where  checkStyleAnalyze.commitid=commits.ID and commits.commiter_date<="' + str(start_date)+ '"' + '  and commits.commiter_date<="' + str(end_date)+'" group by checkStyleAnalyze.name'
    sqlToAttributes(["0","0","0","0","0","0","0","0","0","0","0","0","0"], c, files_dict, styleAnalyze)

    styleAnalyzeLast='select name ,sum(McCabe) ,sum(fanOut) ,sum(NPath) ,sum(FileLen) , sum(NCSS) , sum(outer) , sum(publicMethods) , sum(totalMethods) ,sum(thorwsSTM) ,sum(Coupling) ,sum(Executables) , sum(depthFor) ,sum(depthIf) from checkStyleAnalyze,commits where  checkStyleAnalyze.commitid=commits.ID and commits.commiter_date>="' + str(prev_date)+ '"' + '  and commits.commiter_date<="' + str(start_date)+'" group by checkStyleAnalyze.name'
    sqlToAttributes(["0","0","0","0","0","0","0","0","0","0","0","0","0"], c, files_dict, styleAnalyzeLast)


    bugQ=""
    if (buggedType=="All"):
        bugQ='select distinct name,"bugged"  from commitedfiles where bugId<>0  and name like "%.java" and name not like "%test%" and commiter_date>="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date)+ "and not exists (select comments.commitid,comments.name from comments where comments.commitid=Commitedfiles.commitid and comments.name=Commitedfiles.name) " + '" group by name'
    if (buggedType=="Most"):
        bugQ='select distinct name,"bugged"  from (select Commitedfiles.bugId as bugId,Commitedfiles.name as name  from Commitedfiles , (select max(lines) as l, Commitedfiles.bugId as bugId from Commitedfiles where Commitedfiles.name like "%.java" and name not like "%test%" and commiter_date>="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) +"and not exists (select comments.commitid,comments.name from comments where comments.commitid=Commitedfiles.commitid and comments.name=Commitedfiles.name) " + '" group by bugId) as T where Commitedfiles.lines=T.l and Commitedfiles.bugId=T.bugId) where bugId<>0  group by name'
    files_hasBug={}
    for f in files_dict.keys():
        files_hasBug[f]=["valid"]
    for row in c.execute(bugQ):
        name=Agent.pathTopack.pathToPack(row[0])
        if(name in files_hasBug):
            bug="bugged"
            files_hasBug[name]=[bug]
    for f in files_hasBug:
        files_dict[f]=files_dict[f]+files_hasBug[f]

    conn.close()

    return files_dict.values(),files_dict.keys()


def arff88_ByTag_Objects(dbpath,dates,commits,i, isTest,max,buggedType,objects):
    prev_date=dates[i-1]
    start_date=dates[i]
    end_date=dates[i+1]

    print dbpath
    conn = sqlite3.connect(dbpath)
    conn.text_factory = str
    c = conn.cursor()
    files_dict={}
    createIndex(c, conn)
    wanted_files='select distinct name from haelsTfiles   order by name'
    for row in c.execute(wanted_files):
        name=Agent.pathTopack.pathToPack(row[0])
        files_dict[name]=[]
    #print(files_dict.keys())
    #exit()
    for o in objects:
        o.get_features(c, files_dict,prev_date,start_date,end_date)
        #a=0

    bugQ=""
    if (buggedType=="All"):
        bugQ='select distinct name,"bugged"  from commitedfiles where bugId<>0  and name like "%.java" and name not like "%test%" and commiter_date>="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date)+ '" and not exists (select comments.commitid,comments.name from comments where comments.commitid=Commitedfiles.commitid and comments.name=Commitedfiles.name) ' + ' group by name'
    if (buggedType=="Most"):
        bugQ='select distinct name,"bugged"  from (select Commitedfiles.bugId as bugId,Commitedfiles.name as name  from Commitedfiles , (select max(lines) as l, Commitedfiles.bugId as bugId from Commitedfiles where Commitedfiles.name like "%.java" and name not like "%test%" and commiter_date>="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) +"and not exists (select comments.commitid,comments.name from comments where comments.commitid=Commitedfiles.commitid and comments.name=Commitedfiles.name) " + '" group by bugId) as T where Commitedfiles.lines=T.l and Commitedfiles.bugId=T.bugId) where bugId<>0  group by name'
    files_hasBug={}
    for f in files_dict.keys():
        files_hasBug[f]=["valid"]
    print bugQ
    for row in c.execute(bugQ):
        name=Agent.pathTopack.pathToPack(row[0])
        if(name in files_hasBug):
            bug="bugged"
            files_hasBug[name]=[bug]
    for f in files_hasBug:
        #print files_hasBug[f]
        files_dict[f]=files_dict[f]+files_hasBug[f]

    conn.close()

    return files_dict.values(),files_dict.keys()

def arff88_ByTag_ObjectsMethods(dbpath,dates,commits,i, isTest,max,buggedType,objects):
    prev_date=dates[i-1]
    start_date=dates[i]
    end_date=dates[i+1]
    print dbpath
    conn = sqlite3.connect(dbpath)
    conn.text_factory = str
    c = conn.cursor()
    files_dict={}
    createIndex(c, conn)
    wanted_files='select distinct methodDir from AllMethods'
    for row in c.execute(wanted_files):
        name=Agent.pathTopack.pathToPack(row[0])
        files_dict[name]=[]
    #print(files_dict.keys())
    #exit()
    for o in objects:
        o.get_features(c, files_dict,prev_date,start_date,end_date)
        #a=0
    bugQ=""
    if (buggedType=="Most"):
        bugQ = 'select CommitedMethods.methodDir,"bugged"  from CommitedMethods , (select max(lines) as l, bugId from CommitedMethods where methodDir like "%.java%" and commiter_date>="'+str(start_date)+'"  and commiter_date<="'+str(end_date)+'" and bugId<>0 group by bugId) as T where CommitedMethods.lines=T.l and CommitedMethods.bugId=T.bugId group by methodDir'
    if (buggedType=="All"):
        bugQ='select distinct methodDir,"bugged"  from commitedMethods where bugId<>0  and methodDir like "%.java%" and methodDir not like "%test%" and commiter_date>="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date)+ '" ' + ' group by methodDir'
    files_hasBug={}
    for f in files_dict.keys():
        files_hasBug[f]=["valid"]
    print bugQ
    for row in c.execute(bugQ):
        name=Agent.pathTopack.pathToPack(row[0])
        if(name in files_hasBug):
            bug="bugged"
            files_hasBug[name]=[bug]
    for f in files_hasBug:
        #print files_hasBug[f]
        files_dict[f]=files_dict[f]+files_hasBug[f]
    conn.close()
    return files_dict.values(),files_dict.keys()


def arffCreateForTag(dbpath,dates,i, objects,bugQuery,wanted):
    print dates,i,dbpath
    print dates,i,dbpath
    prev_date=dates[i-1]
    start_date=dates[i]
    end_date=dates[i+1]
    print dbpath
    conn = sqlite3.connect(dbpath)
    conn.text_factory = str
    c = conn.cursor()
    files_dict={}
    createIndex(c, conn)
    #wanted_files='select distinct methodDir from AllMethods'
    for row in c.execute(wanted):
        name=Agent.pathTopack.pathToPack(row[0])
        files_dict[name]=[]
    #print(files_dict.keys())
    #exit()
    for o in objects:
        o.get_features(c, files_dict,prev_date,start_date,end_date)
        #a=0
    bugQ=bugQuery.replace("STARTDATE",str(start_date))
    bugQ=bugQ.replace("ENDDATE",str(end_date))
   # if (buggedType=="Most"):
  #      bugQ = 'select CommitedMethods.methodDir,"bugged"  from CommitedMethods , (select max(lines) as l, bugId from CommitedMethods where methodDir like "%.java%" and commiter_date>="'+str(start_date)+'"  and commiter_date<="'+str(end_date)+'" and bugId<>0 group by bugId) as T where CommitedMethods.lines=T.l and CommitedMethods.bugId=T.bugId group by methodDir'
 #   if (buggedType=="All"):
#        bugQ='select distinct methodDir,"bugged"  from commitedMethods where bugId<>0  and methodDir like "%.java%" and methodDir not like "%test%" and commiter_date>="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date)+ '" ' + ' group by methodDir'
    files_hasBug={}
    for f in files_dict.keys():
        files_hasBug[f]=["valid"]
    print bugQ
    for row in c.execute(bugQ):
        name=Agent.pathTopack.pathToPack(row[0])
        if(name in files_hasBug):
            bug="bugged"
            files_hasBug[name]=[bug]
    for f in files_hasBug:
        #print files_hasBug[f]
        files_dict[f]=files_dict[f]+files_hasBug[f]
    conn.close()
    return files_dict.values(),files_dict.keys()


def past_att():
    attr = [ #( "fileName", "string"),
             ( "tot_changes", "NUMERIC"), ( "sum_insert", "NUMERIC"),
            ( "sum_delets", "NUMERIC"), ( "tot_bugs", "NUMERIC"), ( "tot_developers", "NUMERIC"),
             ( "lastVer_tot_changes", "NUMERIC"), ( "lastVer_sum_insert", "NUMERIC"),
            ( "lastVer_sum_delets", "NUMERIC"), ( "lastVer_tot_bugs", "NUMERIC"), ( "lastVer_tot_developers", "NUMERIC"),( "last_commit", "NUMERIC"),( "last_bug", "NUMERIC"),( "last_bug_binary", "NUMERIC"),
            ( "change_set", "NUMERIC"), ( "age", "NUMERIC"),( "age2", "NUMERIC"), ( "Operators_count", "NUMERIC"), ( "Operands_count", "NUMERIC"),
            ( "Distinct_operators", "NUMERIC"), ("Distinct_operands", "NUMERIC"), ("Program_length", "NUMERIC"),
            ("Program_vocabulary", "NUMERIC"),("Volume", "NUMERIC"), ("Difficulty", "NUMERIC"), ("Effort", "NUMERIC"),
            ("complexity", "NUMERIC"),
            ('exception',['true','false']) ,('abstract',['true','false']) ,('serializable',['true','false']) ,
            ( "methods_Count", "NUMERIC"),( "methods_override", "NUMERIC"),( "methods_private_Count", "NUMERIC"),
            ( "methods_avg_params", "NUMERIC"),( "fields_Count", "NUMERIC"),( "fields_private_Count", "NUMERIC"),( "fields_Objects_Count", "NUMERIC"),
            ( "constructors_Count", "NUMERIC"),( "uses_Count", "NUMERIC"),("Lines" ,"NUMERIC"),
("Statements" ,"NUMERIC"),
("Percent_Branch_Statements" ,"NUMERIC"),
("Method_Call_Statements" ,"NUMERIC"),
("Percent_Lines_with_Comments" ,"NUMERIC"),
("Classes_and_interfaces" ,"NUMERIC"),
("Methods_per_Class" ,"NUMERIC"),
("Average_Statements_per_Method" ,"NUMERIC"),
("Maximum_Complexity" ,"NUMERIC"),
#("Maximum_Block_Depth" ,"NUMERIC"),
("Average_Block_Depth" ,"NUMERIC"),
("Average_Complexity" ,"NUMERIC"),
("Statements_at_block_level_0" ,"NUMERIC"),
("Statements_at_block_level_1" ,"NUMERIC"),
("Statements_at_block_level_2" ,"NUMERIC"),
("Statements_at_block_level_3" ,"NUMERIC"),
("Statements_at_block_level_4" ,"NUMERIC"),
("Statements_at_block_level_5" ,"NUMERIC"),
("Statements_at_block_level_6" ,"NUMERIC"),
("Statements_at_block_level_7" ,"NUMERIC"),
("Statements_at_block_level_8" ,"NUMERIC"),
("Statements_at_block_level_9" ,"NUMERIC"),
("McCabe" , "NUMERIC"),
("fanOut" , "NUMERIC"),
("NPath" , "NUMERIC"),
("FileLen" , "NUMERIC"),("NCSS" , "NUMERIC"),("outer" , "NUMERIC"),("publicMethods" , "NUMERIC"),("totalMethods" , "NUMERIC"),("thorwsSTM" , "NUMERIC"),
("diff_commits" , "NUMERIC") ,("diff_commits_lastver" , "NUMERIC") ,("groups" , "NUMERIC") ,("committers" , "NUMERIC") ,
("avg_date" , "NUMERIC") ,("median_date" , "NUMERIC" ) ,("max_date" , "NUMERIC") ,("numBlobs" , "NUMERIC") ,("numPatchs" , "NUMERIC") ,("numCommits" , "NUMERIC" ),
( "McCabe_Analyze" , "NUMERIC") ,("fanOut_Analyze" , "NUMERIC") ,("NPath_Analyze" , "NUMERIC") ,("FileLen_Analyze" , "NUMERIC") ,("NCSS_Analyze" , "NUMERIC") ,("outer_Analyze" , "NUMERIC") ,("publicMethods_Analyze" , "NUMERIC") ,
("totalMethods_Analyze" , "NUMERIC") ,("thorwsSTM_Analyze" , "NUMERIC") ,("Coupling_Analyze" , "NUMERIC") ,("Executables_Analyze" , "NUMERIC") ,("depthFor_Analyze" , "NUMERIC") ,("depthIf_Analyze" , "NUMERIC"),
( "McCabe_LastVer" , "NUMERIC") ,("fanOut_LastVer" , "NUMERIC") ,("NPath_LastVer" , "NUMERIC") ,("FileLen_LastVer" , "NUMERIC") ,("NCSS_LastVer" , "NUMERIC") ,
("outer_LastVer" , "NUMERIC") ,("publicMethods_LastVer" , "NUMERIC") ,("totalMethods_LastVer" , "NUMERIC") ,("thorwsSTM_LastVer" , "NUMERIC") ,("Coupling_LastVer" , "NUMERIC") ,("Executables_LastVer" , "NUMERIC") ,("depthFor_LastVer" , "NUMERIC") ,("depthIf_LastVer" , "NUMERIC"),
 ( "hasBug", ["bugged", "valid"])  ]

    return attr

def objectsAttr(objects):
    attr=[]
    lens=[0]
    for o in objects:
        a = o.get_attributes()
        attr.extend(a)
        lens.append(len(attr))
    attr.append(( "hasBug", ["bugged", "valid"]))
    return attr,lens

def writeFile(allNames, arffExtension,namesFile, attr, data, name, outPath):
    arff_data = arff_build(attr, data, str([]), "base")
    path_join = os.path.join(outPath, str(name + arffExtension))
    write_to_arff(arff_data, path_join)
    if namesFile!="":
        path_join = os.path.join(outPath, str(name + namesFile))
        f=open(path_join,"wb")
        writer=csv.writer(f)
        writer.writerows([[a] for a in allNames])
        f.close()
    #f.writelines(allNames)


def writeArff(allNames, arffName,namesFile, attr, data):
    arff_data = arff_build(attr, data, str([]), "base")
    write_to_arff(arff_data, arffName)
    if namesFile!="":
        f=open(namesFile,"wb")
        writer=csv.writer(f)
        writer.writerows([[a] for a in allNames])
        f.close()
    #f.writelines(allNames)


def arff88(basicPath,i,max,outPath,name,buggedType):
    names,paths=getPaths(basicPath)
    dates =[i1[1] for i1 in names_dates()]
    commits =[i1[1] for i1 in names_commits()]
    data=[]
    print "start"
    allNames=[]
    i=len(names)-6
    attr=past_att()
    #i=len(names)-12
    while (i+1<len(names)):
        os_path_join = os.path.join(basicPath, str(names[i] + ".db"))
        print(os_path_join)
        #tag,nam = arff88_for_tag(os_path_join, dates[i], dates[i+1], False,max)
        tag,nam = arff88_ByTag_Past(os_path_join, dates,commits, i, False,max,buggedType)
        data=data+ tag
        #allNames=allNames+nam
        if( i==len(names)-2):
            arffExtension = name+"_Only.arff"
            NamesFile = name+"_OnlyNames.csv"
            print "aattr", len(attr), attr
            writeFile(nam, arffExtension,NamesFile, attr, tag, names[i], outPath)
        if( i==len(names)-3):
            arffExtension = name+"_Appended.arff"
            NamesAppendFile = name+"_AppendedNames.csv"
            NamesAppendFile = ""
            print "aattr", len(attr), attr
            writeFile(allNames, arffExtension,NamesAppendFile, attr, data, names[i], outPath)
        print i
        i=i+1
    return data

def arff88Packs(basicPath,i,max,outPath,name,buggedType, packs,names,paths,dates,commits):
    print packs
    objects=featuresPacksToClasses(packs)
    data=[]
    print "start"
    i=0
    attr,lens=objectsAttr(objects)
    print attr
    #i=len(names)-12
    while (i+1<len(names)):
        os_path_join = os.path.join(basicPath, str(names[i] + ".db"))
        print(os_path_join)
        tag,nam = arff88_ByTag_Objects(os_path_join, dates,commits, i, False,max,buggedType,objects)
        data=data+ tag
        if( i==len(names)-2):
            arffExtension = name+"_Only.arff"
            NamesFile = name+"_OnlyNames.csv"
            writeFile(nam, arffExtension,NamesFile, attr, tag, names[i], outPath)
        if( i==len(names)-3):
            arffExtension = name+"_Appended.arff"
            NamesAppendFile = ""
            writeFile([], arffExtension,NamesAppendFile, attr, data, names[i], outPath)
        print i
        i=i+1
    return data

def arff88PacksMethods(basicPath,i,max,outPath,name,buggedType, packs,names,paths,dates,commits):
    print packs
    objects=featuresMethodsPacksToClasses(packs)
    data=[]
    print "start"
    i=0
    attr=objectsAttr(objects)
    print attr
    #i=len(names)-12
    while (i+1<len(names)):
        os_path_join = os.path.join(basicPath, str(names[i] + ".db"))
        print(os_path_join)
        #tag,nam = arff88_ByTag_Objects(os_path_join, dates,commits, i, False,max,buggedType,objects)
        tag,nam = arff88_ByTag_ObjectsMethods(os_path_join, dates,commits, i, False,max,buggedType,objects)
        data=data+ tag
        if( i==len(names)-2):
            arffExtension = name+"_OnlyMethods.arff"
            NamesFile = name+"_OnlyNamesMethods.csv"
            writeFile(nam, arffExtension,NamesFile, attr, tag, names[i], outPath)
        if( i==len(names)-3):
            arffExtension = name+"_AppendedMethods.arff"
            NamesAppendFile = ""
            writeFile([], arffExtension,NamesAppendFile, attr, data, names[i], outPath)
        print i
        i=i+1
    return data


def arffCreate(basicPath, objects, names, dates, bugQ, wanted, trainingFile, testingFile, NamesFile):
    data=[]
    print "start"
    i=0
    attr,lens=objectsAttr(objects)
    print "attr",len(attr),attr
    while (i+1<len(names)):
        dbpath = os.path.join(basicPath, str(names[i] + ".db"))
        print(dbpath)
        tag, allNames = arffCreateForTag(dbpath, dates, i, objects, bugQ, wanted)
        data = data+ tag
        if( i==len(names)-3):
            writeArff([], trainingFile, "", attr, data)
        if( i==len(names)-2):
            writeArff(allNames, testingFile, NamesFile, attr, tag)
        i=i+1
    return data


def attributeSelect(sourceFile, outFile,inds):
    source=load_arff(sourceFile)
    attributes=[]
    ind=0
    last=len(source['attributes'])-1
    for x in source['attributes']:
        if ind in inds or ind==last:
            attributes.append(x)
        ind=ind+1
    data=[]
    for x in source['data']:
        ind=0
        d=[]
        for y in x:
            if ind in inds or ind==last:
                d.append(y)
            ind=ind+1
        if(d!=[]):
            data.append(d)
    arff_data=arff_build(attributes, data,str([]),"selected")
    write_to_arff(arff_data, outFile)

def featuresMethodsPacksToClasses(packs):
    l=[]
    names=[]
    if "bugsMethods" in packs:
        l.append(processMethodsFamilies.processMethodsFamilies("bugsMethods"))
        names.append("bugsMethods")
        print "bugsMethods"
    if "processMethods" in packs:
        l.append(processMethods.processMethods())
        names.append("processMethods")
        print "processMethods"
    if "haelsteadMethods" in packs:
        l.append(haelsteadMethods.haelsteadMethods())
        names.append("haelsteadMethods")
        print "haelsteadMethods"
    if "OOMethods" in packs:
        l.append(OOMethods.OOMethods())
        names.append("OOMethods")
        print "OOMethods"
    if "g2Methods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("g2Methods"))
        names.append("g2Methods")
        print "g2Methods"
    if "g3Methods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("g3Methods"))
        names.append("g3Methods")
        print "g3Methods"
    if "g4Methods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("g4Methods"))
        names.append("g4Methods")
        print "g4Methods"
    if "methodsMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("methodsMethods"))
        names.append("methodsMethods")
        print "methodsMethods"
    if "methodsArticlesMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("methodsArticlesMethods"))
        names.append("methodsArticlesMethods")
        print "methodsArticlesMethods"
    if "methodsAddedMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("methodsAddedMethods"))
        names.append("methodsAddedMethods")
        print "methodsAddedMethods"
    if "hirarcyMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("hirarcyMethods"))
        names.append("hirarcyMethods")
        print "hirarcyMethods"
    if "fieldsMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("fieldsMethods"))
        names.append("fieldsMethods")
        print "fieldsMethods"
    if "fieldsArticlesMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("fieldsArticlesMethods"))
        names.append("fieldsArticlesMethods")
        print "fieldsArticlesMethods"
    if "fieldsAddedMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("fieldsAddedMethods"))
        names.append("fieldsAddedMethods")
        print "fieldsAddedMethods"
    if "constructorsMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("constructorsMethods"))
        names.append("constructorsMethods")
        print "constructorsMethods"
    if "constructorsArticlesMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("constructorsArticlesMethods"))
        names.append("constructorsArticlesMethods")
        print "constructorsArticlesMethods"
    if "constructorsAddedMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("constructorsAddedMethods"))
        names.append("constructorsAddedMethods")
        print "constructorsAddedMethods"
    if "lastProcessMethods" in packs:
        l.append(processMethodsFamilies.processMethodsFamilies("lastProcessMethods"))
        names.append("lastProcessMethods")
        print "lastProcessMethods"
    if "simpleProcessArticlesMethods" in packs:
        l.append(processMethodsFamilies.processMethodsFamilies("simpleProcessArticlesMethods"))
        names.append("simpleProcessArticlesMethods")
        print "simpleProcessArticlesMethods"
    if "simpleProcessAddedMethods" in packs:
        l.append(processMethodsFamilies.processMethodsFamilies("simpleProcessAddedMethods"))
        names.append("simpleProcessAddedMethods")
        print "simpleProcessAddedMethods"
    if "sourceMonitorMethods" in packs:
        l.append(sourceMonitorMethods.sourceMonitorMethods())
        names.append("sourceMonitorMethods")
        print "sourceMonitorMethods"
    if "checkStyleMethods" in packs:
        l.append(checkStyleMethods.checkStyleMethods())
        names.append("checkStyleMethods")
        print "checkStyleMethods"
    if "blameMethods" in packs:
        l.append(blameMethods.blameMethods())
        names.append("blameMethods")
        print "blameMethods"
    if "analyzeCommsMethods" in packs:
        l.append(analyzeCommsMethods.analyzeCommsMethods())
        names.append("analyzeCommsMethods")
        print "analyzeCommsMethods"
    if "analyzeLastMethods" in packs:
        l.append(analyzeLastMethods.analyzeLastMethods())
        names.append("analyzeLastMethods")
        print "analyzeLastMethods"
    attr=[]
    for o in l:
        attr.extend(o.get_attributes())
        print len(attr)
    return l,names


def featuresPacksToClasses(packs):
    l=[]
    names=[]
    if "process" in packs:
        l.append(process.process())
        names.append("process")
        print "process"
    if "haelstead" in packs:
        l.append(haelstead.haelstead())
        names.append("haelstead")
        print "haelstead"
    if "OO" in packs:
        l.append(OO.OO())
        names.append("OO")
        print "OO"
    if "g2" in packs:
        l.append(OOFamilies.OOFamilies("g2"))
        names.append("g2")
        print "g2"
    if "g3" in packs:
        l.append(OOFamilies.OOFamilies("g3"))
        names.append("g3")
        print "g3"
    if "g4" in packs:
        l.append(OOFamilies.OOFamilies("g4"))
        names.append("g4")
        print "g4"
    if "methods" in packs:
        l.append(OOFamilies.OOFamilies("methods"))
        names.append("methods")
        print "methods"
    if "methodsArticles" in packs:
        l.append(OOFamilies.OOFamilies("methodsArticles"))
        names.append("methodsArticles")
        print "methodsArticles"
    if "methodsAdded" in packs:
        l.append(OOFamilies.OOFamilies("methodsAdded"))
        names.append("methodsAdded")
        print "methodsAdded"
    if "hirarcy" in packs:
        l.append(OOFamilies.OOFamilies("hirarcy"))
        names.append("hirarcy")
        print "hirarcy"
    if "fields" in packs:
        l.append(OOFamilies.OOFamilies("fields"))
        names.append("fields")
        print "fields"
    if "fieldsArticles" in packs:
        l.append(OOFamilies.OOFamilies("fieldsArticles"))
        names.append("fieldsArticles")
        print "fieldsArticles"
    if "fieldsAdded" in packs:
        l.append(OOFamilies.OOFamilies("fieldsAdded"))
        names.append("fieldsAdded")
        print "fieldsAdded"
    if "constructors" in packs:
        l.append(OOFamilies.OOFamilies("constructors"))
        names.append("constructors")
        print "constructors"
    if "constructorsArticles" in packs:
        l.append(OOFamilies.OOFamilies("constructorsArticles"))
        names.append("constructorsArticles")
        print "constructorsArticles"
    if "constructorsAdded" in packs:
        l.append(OOFamilies.OOFamilies("constructorsAdded"))
        names.append("constructorsAdded")
        print "constructorsAdded"
    if "lastProcess" in packs:
        l.append(processFamilies.processFamilies("lastProcess"))
        names.append("lastProcess")
        print "lastProcess"
    if "simpleProcessArticles" in packs:
        l.append(processFamilies.processFamilies("simpleProcessArticles"))
        names.append("simpleProcessArticles")
        print "simpleProcessArticles"
    if "simpleProcessAdded" in packs:
        l.append(processFamilies.processFamilies("simpleProcessAdded"))
        names.append("simpleProcessAdded")
        print "simpleProcessAdded"
    if "bugs" in packs:
        l.append(processFamilies.processFamilies("bugs"))
        names.append("bugs")
        print "bugs"
    if "sourceMonitor" in packs:
        l.append(sourceMonitor.sourceMonitor())
        names.append("sourceMonitor")
        print "sourceMonitor"
    if "checkStyle" in packs:
        l.append(checkStyle.checkStyle())
        names.append("checkStyle")
        print "checkStyle"
    if "blame" in packs:
        l.append(blame.blame())
        names.append("blame")
        print "blame"
    if "analyzeComms" in packs:
        l.append(analyzeComms.analyzeComms())
        names.append("analyzeComms")
        print "analyzeComms"
    if "analyzeLast" in packs:
        l.append(analyzeLast.analyzeLast())
        names.append("analyzeLast")
        print "analyzeLast"
    return l,names

#print(createAllArffs("C:\Users\Amir-pc\Documents\GitHub\\vers"))


#print names_dates_GIT()
#arff88_alone("C:\Users\Amir-pc\Documents\GitHub\\vers",12)
#testFromFile("C:\Users\Amir-pc\Documents\GitHub\\vers",os.path.join(os.path.join("C:\Users\Amir-pc\Documents\GitHub\\vers","ML"), str("CDT_8_0_0ML_NEW_alone.arff")))
#p=[]
#names,paths=getPaths("C:\Users\Amir-pc\Documents\GitHub\\vers")
#for i in names:
#	path_join = os.path.join(os.path.join("C:\Users\Amir-pc\Documents\GitHub\\vers","ML"), str(str(i)+"ML_sec_alone.arff"))
#	p=p+[path_join]

#print(p[12])
#path_join = os.path.join(os.path.join("C:\Users\Amir-pc\Documents\GitHub\\vers","ML"), str(names[12]+"_WILD_12.arff"))
#testFromFile(p[12],path_join)
#appendFiles(p[:12],path_join = os.path.join(os.path.join("C:\Users\Amir-pc\Documents\GitHub\\vers","ML"), str("Append_To_11.arff")))
#appendFiles("C:\Users\Amir-pc\Documents\GitHub\\vers", p)
#arff88("C:\GitHub\\vers",0,-1,"C:\GitHub\\weka","All")
#print names_commits_GIT()



def All_one(sourcePathTrain,sourcePathTest,oned,alld,packsInds):
    red=list(set(reduce(lambda x, y: x+y, packsInds)))
    if not os.path.isdir(oned):
            os.mkdir(oned)
    if not os.path.isdir(alld):
            os.mkdir(alld)
    for ind in range(len(packsInds)):
        p=packsInds[ind]
        lst=list(red)
        for x in p:
            lst.remove(x)
        reduce1=lst
        print len(reduce1),len(p),len(reduce1)+len(p)
        outPathTrain=oned+"\\CDT_8_1_1_AllFiles_"+str(ind)+"_Appended.arff"
        outPathTest=oned+"\\CDT_8_1_2_AllFiles_"+str(ind)+"_Only.arff"
        attributeSelect(sourcePathTrain,outPathTrain,p)
        attributeSelect(sourcePathTest,outPathTest,p)
        outPathTrain=alld+"\\CDT_8_1_1_AllFiles_"+str(ind)+"_Appended.arff"
        outPathTest=alld+"\\CDT_8_1_2_AllFiles_"+str(ind)+"_Only.arff"
        attributeSelect(sourcePathTrain,outPathTrain, reduce1)
        attributeSelect(sourcePathTest,outPathTest,reduce1)


def articlesAllpacks(basicPath,repoPath,outDir,vers, vers_dirs,buggedType,dbPath):
    packs=["haelstead","g2","g3","methodsArticles","methodsAdded","hirarcy","fieldsArticles","fieldsAdded","constructorsArticles","constructorsAdded","lastProcess","simpleProcessArticles","simpleProcessAdded","bugs","sourceMonitor","checkStyle","blame"]#,"analyzeComms"]
    #packs=["bugsMethods"]
    bugQ=""
    wanted='select distinct name from haelsTfiles   order by name'
    if (buggedType=="All"):
        bugQ='select distinct name,"bugged"  from commitedfiles where bugId<>0  and name like "%.java" and name not like "%test%" and commiter_date>="' + str("STARTDATE")+ '"' + '  and commiter_date<="' + str("ENDDATE")+ '" and not exists (select comments.commitid,comments.name from comments where comments.commitid=Commitedfiles.commitid and comments.name=Commitedfiles.name) ' + ' group by name'
    if (buggedType=="Most"):
        bugQ='select distinct name,"bugged"  from (select Commitedfiles.bugId as bugId,Commitedfiles.name as name  from Commitedfiles , (select max(lines) as l, Commitedfiles.bugId as bugId from Commitedfiles where Commitedfiles.name like "%.java" and name not like "%test%" and commiter_date>="' + str("STARTDATE")+ '"' + '  and commiter_date<="' + str("ENDDATE") +"and not exists (select comments.commitid,comments.name from comments where comments.commitid=Commitedfiles.commitid and comments.name=Commitedfiles.name) " + '" group by bugId) as T where Commitedfiles.lines=T.l and Commitedfiles.bugId=T.bugId) where bugId<>0  group by name'
    print "bugQ", bugQ
    names,paths,dates,commits=GitVersInfo(basicPath,repoPath,vers)
    trainingFile=os.path.join(outDir,buggedType+"_training_files.arff")
    testingFile=os.path.join(outDir,buggedType+"_testing_files.arff")
    NamesFile=os.path.join(outDir,buggedType+"_names_files.csv")
    FeaturesClasses, Featuresnames=featuresPacksToClasses(packs)
    attr, lensAttr = objectsAttr(FeaturesClasses)
    arffCreate(dbPath, FeaturesClasses, vers_dirs, dates, bugQ, wanted, trainingFile, testingFile, NamesFile)
    return trainingFile, testingFile, NamesFile, Featuresnames, lensAttr

def articlesAllpacksMethods(basicPath,repoPath,outDir,vers, vers_dirs,buggedType,dbPath):
    packs=["lastProcessMethods","simpleProcessArticlesMethods","simpleProcessAddedMethods","bugsMethods"]#,"analyzeComms"]
    bugQ=""
    wanted='select distinct methodDir from AllMethods order by methodDir'
    if (buggedType=="Most"):
        bugQ = 'select CommitedMethods.methodDir,"bugged"  from CommitedMethods , (select max(lines) as l, bugId from CommitedMethods where methodDir like "%.java%" and commiter_date>="'+str("STARTDATE")+'"  and commiter_date<="'+str("ENDDATE")+'" and bugId<>0 group by bugId) as T where CommitedMethods.lines=T.l and CommitedMethods.bugId=T.bugId group by methodDir'
    if (buggedType=="All"):
        bugQ='select distinct methodDir,"bugged"  from commitedMethods where bugId<>0  and methodDir like "%.java%" and methodDir not like "%test%" and commiter_date>="' + str("STARTDATE")+ '"' + '  and commiter_date<="' + str("ENDDATE")+ '" ' + ' group by methodDir'
    names,paths,dates,commits=GitVersInfo(basicPath,repoPath,vers)
    trainingFile=os.path.join(outDir,buggedType+"_training_methods.arff")
    testingFile=os.path.join(outDir,buggedType+"_testing_methods.arff")
    NamesFile=os.path.join(outDir,buggedType+"_names_methods.csv")
    FeaturesClasses,Featuresnames=featuresMethodsPacksToClasses(packs)
    attr,lensAttr=objectsAttr(FeaturesClasses)
    arffCreate(dbPath, FeaturesClasses,vers_dirs,dates,bugQ,wanted,trainingFile,testingFile,NamesFile)
    return trainingFile,testingFile,NamesFile,Featuresnames,lensAttr



if __name__ == "__main__":
    buggedTypes=[]
    buggedTypes.append("All")
    d="C:\GitHub\\weka\\"+"m30"
    if not os.path.isdir(d):
        os.mkdir(d)
    #for b in buggedTypes:
        #arff88Packs("C:\GitHub\\vers\dbAdd\done2",0,100,d,"_"+b+"_bugsMore",b,["bugs"])
    #exit()
    packs=["haelstead","g2","g3","methodsArticles","methodsAdded","hirarcy","fieldsArticles","fieldsAdded","constructorsArticles","constructorsAdded","lastProcess","simpleProcessArticles","simpleProcessAdded","bugs","sourceMonitor","checkStyle","blame","analyzeComms"]
    packs=["haelstead","g2","g3","methodsArticles","methodsAdded","hirarcy","fieldsArticles","fieldsAdded","constructorsArticles","constructorsAdded","lastProcess","simpleProcessArticles","simpleProcessAdded","bugs","sourceMonitor","checkStyle","blame"]#,"analyzeComms"]
    for b in buggedTypes:
        basicPath="C:\GitHub\\vers\dbAdd\done2"
        names,paths,dates,commits=EclipseInfo(basicPath)
        #arff88Packs(basicPath,0,100,d,"_"+b+"_bugs",b,packs,names,paths,dates,commits)
        basicPath="C:\projs\poiWorking"
        repoPath="C:\projs\poi"
        Agent.pathTopack.project="poi"
        vers=["REL_3_0","REL_3_2_FINAL","REL_3_6","REL_3_7","REL_3_8_FINAL","REL_3_9","REL_3_10_1"]
        names,paths,dates,commits=GitVersInfo(basicPath,repoPath,vers)
        arff88Packs(basicPath+"\dbAdd",0,100,d,"_"+b+"_bugsPOI",b,packs,names,paths,dates,commits)

    exit()

    l=featuresPacksToClasses(packs)
    att=[]
    packsSizes=[0]
    for x in l:
        att.extend(x.get_attributes())
        packsSizes.append(len(att))
        print len(att)
    #exit()
    packsSizes=[0,10,34,54,68,92,104,111,133,138,162,176,190,199,280,333,369,405,650]
    packsInds=[]
    for i in range(len(packsSizes)-1):
        packsInds.append([x+packsSizes[i] for x in range(packsSizes[i+1]-packsSizes[i])])
    print packsInds
    Ronipack=["OC" ,"OC_OOO" ,"OC_OOO_OP" ,"OC_OOO_DFA" ,"OC_OOO_IBW" ,"OC_OOO_IBW_PWCOO"]
    Roni=[[10,11,8],[10,11,6,7,5,8,9],[10,11,6,7,5,8,9,0,1],[10,11,6,7,5,8,9,0,1,3,4],[10,11,6,7,5,8,9,0,1,3,4,2],[10,11,6,7,5,8,9,0,1,3,4,2,12,13]]
    RonipacksInds=[]
    for p in Roni:
        lst=[packsInds[x] for x in p]
        RonipacksInds.append(reduce(lambda x, y: x + y, lst))
    print len(RonipacksInds[-1])
    sourcePathTrain=d+"\\CDT_8_1_1_AllFiles_bugs_Appended.arff"
    sourcePathTest=d+"\\CDT_8_1_2_AllFiles_bugs_Only.arff"

    if not os.path.isdir(d):
        os.mkdir(d)
    #All_one(sourcePathTrain,sourcePathTest,d+"\\oneR",d+"\\allR",[RonipacksInds[0]])
    #exit()
    #All_one(sourcePathTrain,sourcePathTest,d+"\\one",d+"\\all",packsInds)
    #exit()
    for b in buggedTypes:
        arff88Packs("C:\GitHub\\vers\dbAdd\done2",0,100,d,"_"+b+"_bugs",b,packs)

    if 1==0:
        buggedTypes=[]
        buggedTypes.append("All")
        buggedTypes.append("Most")
        d="C:\GitHub\\weka\\"+"m4"
        if not os.path.isdir(d):
            os.mkdir(d)
        for b in buggedTypes:
            arff88("C:\GitHub\\vers\dbAdd\done2",0,100,d,"_"+b+"_blameP",b)
    if 0==2:
        sourcePathTrain="C:\GitHub\\weka\\m4\\CDT_8_1_1_AllFiles_blameP_Appended.arff"
        sourcePathTest="C:\GitHub\\weka\\m4\\CDT_8_1_2_AllFiles_blameP_Only.arff"
        cuts=[0,16,26,38,59,68,78,94,104]
        all=range(105)
        for i in range(len(cuts)-1):
            x,y=cuts[i],cuts[i+1]
            print x,y
            outPathTrain="C:\GitHub\\weka\\m5\\CDT_8_1_1_AllFiles_blameP_Appended_"+str(y)+".arff"
            outPathTest="C:\GitHub\\weka\\m5\\CDT_8_1_2_AllFiles_blameP_Only_"+str(y)+".arff"
            l=[i for i in all if i==104 or (i>=x and i<y) ]
            attributeSelect(sourcePathTrain,outPathTrain,l)
            attributeSelect(sourcePathTest,outPathTest,l)
            #testAns("C:\Users\Amir-pc\Documents\GitHub\\vers")

            #print( names_dates_GIT())