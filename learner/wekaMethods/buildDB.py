
__author__ = 'Amir-pc'

import sqlite3
import git
import csv
import gc
import git.objects.tree
import os
import re
import datetime
import checkReport
import blameParse
import commentedCodeDetector
import pathPackCsv
import unicodedata
import patchsBuild
import docXml
import source_Monitor
import utilsConf
from Agent.pathTopack import get_renamed_files_for_commit

class Commit(object):
    def __init__(self, git_commit, bug_id):
        self._git_commit = git_commit
        self._bug_id = bug_id
        self._commit_id = self._git_commit.hexsha
        self._files = get_renamed_files_for_commit(self._git_commit).keys()
        # if self._git_commit.parents:
        #     self.commited_files = map(lambda d: (d.a_path, d.renamed, d.new_file, d.deleted_file),
        #                               self._git_commit.tree.diff(self._git_commit.parents[0].tree))

    def to_list(self):
        return [self._commit_id, str(self._bug_id), ";".join(self._files)]

    @staticmethod
    def clean_commit_message(commit_message):
        message = commit_message
        if "git-svn-id" in commit_message:
            message = commit_message.split("git-svn-id")[0]
        return message.lower().replace(":", "").replace("#", "").replace("-", " ").replace("_", " ")


def commTablelight(commits):
    all_commits=[]
    commitsBugsDict={}
    for commit in commits:
        git_commit = commit._git_commit
        commit_id=int("".join(list(git_commit.hexsha)[:7]),16)
        if not hasattr(git_commit, 'committed_date'):
            continue
        commiter_date = datetime.datetime.fromtimestamp(git_commit.committed_date).strftime('%Y-%m-%d %H:%M:%S')
        author_date = datetime.datetime.fromtimestamp(git_commit.authored_date).strftime('%Y-%m-%d %H:%M:%S')
        name = unicodedata.normalize('NFKD', git_commit.committer.name).encode('ascii','ignore')
        committer = str(name)
        author = str(git_commit.author.name.encode('ascii','ignore'))
        parent = 0
        if(git_commit.parents!=() ):
            parent =int("".join(list(git_commit.parents[0].hexsha)[:7]),16)
        msg = git_commit.message
        size = git_commit.size
        fields = (commit_id, commit._bug_id, commiter_date,committer,author_date,author,size,parent,msg ,str(git_commit.hexsha))
        all_commits.append(fields)
        commitsBugsDict[str(git_commit.hexsha)]=(commit._bug_id,commiter_date,str(git_commit.hexsha),str(commit_id))
    return all_commits, commitsBugsDict


def commits_and_Bugs(repo, bugsIds):
    def replace(chars_to_replace, replacement, s):
        temp_s = s
        for c in chars_to_replace:
            temp_s = temp_s.replace(c, replacement)
        return temp_s

    def get_bug_num_from_commit_text(git_commit, bugsIds):
        if str(git_commit.hexsha) in bugsIds:
            return str(git_commit.hexsha)
        commit_text = Commit.clean_commit_message(git_commit.summary)
        text = replace("[]?#,:", "", commit_text.lower())
        text = replace("-_", " ", text)
        for word in text.split():
            if word.isdigit():
                if word in bugsIds:
                    return word
        return "0"
    commits= []
    for git_commit in repo.iter_commits():
        commits.append(Commit(git_commit, get_bug_num_from_commit_text(git_commit, bugsIds)))
    return commits


def bugsTable(bugs_path):
    # Create table
    all_bugs = []
    bugsIds = []
    def fix_date(date):
        if len(date) == len('09/01/09'):
            return datetime.datetime.strptime(date, "%d/%m/%y")
        return datetime.datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
    with open(bugs_path, "rb") as BugsFile:
        # creates the reader object
        reader = csv.reader(BugsFile)
        next(reader, None) # skip header
        for row in reader:# iterates the rows of the file in orders
            r = []
            for x in row:
                lst = x
                if len(lst)>0 and lst[0]=="=" :
                    lst=lst[2:(len(lst)-1)]
                r.append(str(lst))
            if len(r) < 16:
                continue
            r[7] = fix_date(r[7])
            r[16] = fix_date(r[16])
            bugsIds.append(r[0])
            all_bugs.append(r)
        return all_bugs, bugsIds


def allFiles(path):
    acc=[]
    pathLen = len(path)+1 # one for the \
    for root, dirs, files in os.walk(path): # Walk directory tree
        for f in files:
            path_join = "".join(list(os.path.join(root, f))[pathLen:])
            acc.append(path_join)
    return acc


def BuildRepo(gitPath, bugsPath, MethodsParsed, changeFile):
    repo = git.Repo(gitPath)
    allBugs, bugsIds = bugsTable(bugsPath)
    allMethods, filesRows = patchsBuild.analyzeCheckStyle(MethodsParsed, changeFile)
    allCommits, commitsBugsDict = commTablelight(commits_and_Bugs(repo, bugsIds))
    allMethodsCommits = []
    allFilesCommits = []
    i=0
    for m in allMethods:
        if not m[0] in commitsBugsDict:
            i=i+1
            print "not CommitID method",m[0], i
            continue
        bug,commiterDate,sha,CommitId=commitsBugsDict[m[0]]
        r=m+[bug,commiterDate,CommitId]
        allMethodsCommits.append(r)
    i=0
    for m in filesRows:
        if not m[1] in commitsBugsDict:
            i=i+1
            print "not CommitID file",m[1], i
            continue
        bug,commiterDate,sha,CommitId=commitsBugsDict[m[1]]
        r=[0]+m+[bug,commiterDate,CommitId]
        allFilesCommits.append(r)
    return (allCommits,allFilesCommits,allMethodsCommits,allBugs,allFilesCommits)


def createTables(dbpath):
    with utilsConf.use_sqllite(dbpath) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS AllMethods (methodDir text, fileName text, methodName text, beginLine INT , endLine INT )''')
        c.execute('''CREATE TABLE IF NOT EXISTS commitedMethods (commit_sha text , methodDir text, fileName text, methodName text, deletions INT , insertions INT , lines INT, is_new_file INT, is_deleted_file INT, is_renamed_file INT, bugId INT, commiter_date DateTime,commitID INT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS bugsFix (ID INT,Product text,Component text,Assigned_To text,Status text,Resolution text,Reporter text,Last_Modified DateTime ,Version text,Milestone text,Hardware text,OS text,Priority text,Severity text,Summary text,Keywords text,Submit_Date DateTime ,Blocks text,Depends_On text,Duplicate_Of INT,CC text)''')
        #c.execute('''CREATE TABLE IF NOT EXISTS commits (ID INT, bugId INT, commiter_date DateTime , commiter text,author_date DateTime , author text  , lines INT,deletions INT,insertions INT,files INT,size INT, parentID INT,reachable_commits INT, message text,commit_sha text )''')
        c.execute('''CREATE TABLE IF NOT EXISTS commits (ID INT, bugId INT, commiter_date DateTime , commiter text,author_date DateTime , author text  , size INT, parentID INT, message text,commit_sha text )''')
        #c.execute(
         #   '''CREATE TABLE IF NOT EXISTS Commitedfiles (id INT,name text, commitid INT, commiter_date DateTime,lines INT,deletions INT,insertions INT, bugId INT,commit_sha text)''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS Commitedfiles (id INT,name text,commit_sha text,deletions INT,insertions INT, lines INT, is_new_file INT, is_deleted_file INT, is_renamed_file INT, bugId INT, commiter_date DateTime, commitid INT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS files (id INT,name text)''')
        c.execute('''CREATE TABLE IF NOT EXISTS Complexyfiles (name text, complex INT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS haelsTfiles (name text, Operators_count INT, Distinct_operators INT, Operands_count INT, Distinct_operands INT, Program_length INT, Program_vocabulary INT,Volume float, Difficulty INT, Effort float)''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS bugs (ID INT,Product text,Component text,Assigned_To text,Status text,Resolution text,Reporter text,Last_Modified DateTime ,Version text,Milestone text,Hardware text,OS text,Priority text,Severity text,Summary text,Keywords text,Submit_Date DateTime ,Blocks text,Depends_On text,Duplicate_Of INT,CC text)''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS JAVAfiles (name text,Lines INT,	Statements INT,	Percent_Branch_Statements INT,Method_Call_Statements INT,Percent_Lines_with_Comments INT,Classes_and_Interfaces INT,Methods_per_Class float,Average_Statements_per_Method float,Line_Number_of_Most_Complex_Method 	INT, Name_of_Most_Complex_Method 	text, Maximum_Complexity INT,Line_Number_of_Deepest_Block INT,Maximum_Block_Depth INT,Average_Block_Depth	float, Average_Complexity	float, Statements_at_block_level_0 INT,Statements_at_block_level_1 INT,Statements_at_block_level_2 INT,Statements_at_block_level_3 INT,Statements_at_block_level_4 INT,Statements_at_block_level_5 INT,Statements_at_block_level_6 INT,Statements_at_block_level_7 INT,Statements_at_block_level_8 INT,Statements_at_block_level_9 INT)''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS Sourcemethods (File_Name text, Method text ,Complexity	INT, Statements INT, 	Maximum_Depth	INT, Calls INT)''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS classes (Dirpath text,superClass text,exception text, name text,externalizable text ,abstract text ,path text ,error text   ,included text ,scope text   ,serializable text)''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS constructors (Dirpath text ,className text , name text , synchronized text, varArgs text,  classPath text ,static text, signature text, included text, scope text, final text,  native text,  Num_params text)''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS methods (Dirpath text,className text, name text , synchronized text, abstract text , varArgs text, classPath text , static text, signature text , included text , scope text  , final text  , native text   ,return text,Num_params text)''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS fields (Dirpath text,className text,static text, name text, classPath text, transient text,volatile text,scope text,    final text, type text)''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS checkStyle (name text,McCabe REAL,fanOut REAL,NPath REAL,FileLen INT, NCSS INT, outer INT, publicMethods INT, totalMethods INT,thorwsSTM INT,Coupling INT,Executables INT, depthFor INT,depthIf INT)''')
        #c.execute(
        #   '''CREATE TABLE IF NOT EXISTS blame (name text,diff_commits INT,diff_commits_lastver INT,groups INT ,committers INT,avg_date DateTime,median_date DateTime ,max_date DateTime,numBlobs INT, numPatchs INT,numCommits INT )''')
        c.execute('''CREATE TABLE IF NOT EXISTS comments (name text, commitid INT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS blameExtends (name text,diff_commits INT,diff_commits_lastver INT,diff_commitsApproved INT,diff_commits_lastverApproved INT,numBlobs INT, numPatchs INT,numCommits INT,
                    len_times INT,mean_times DateTime,median_times DateTime,var_times float,max_times DateTime,min_times DateTime,p01_times  float,p02_times  float,p05_times  float,mx1_times  float, max_min_times INT,
                    ones_times float, twos_times float,less5_times float,less10_times float,
                    len_difftimes INT,mean_difftimes DateTime,median_difftimes DateTime,var_difftimes float,max_difftimes DateTime,min_difftimes DateTime,p01_difftimes float,p02_difftimes float,p05_difftimes float,mx1_difftimes  float, max_min_difftimes INT,
                    ones_difftimes float, twos_difftimes float,less5_difftimes float,less10_difftimes float,
                    len_committers INT,p01_committers  float,p02_committers  float,p05_committers  float,mx1_committers  float,
                    len_timesApproved INT,mean_timesApproved DateTime,median_timesApproved DateTime,var_timesApproved float,max_timesApproved DateTime,min_timesApproved DateTime,p01_timesApproved  float,p02_timesApproved  float,p05_timesApproved  float,mx1_timesApproved  float, max_min_timesApproved INT,
                    ones_timesApproved float, twos_timesApproved float,less5_timesApproved float,less10_timesApproved float,
                    len_difftimesApproved INT,mean_difftimesApproved DateTime,median_difftimesApproved DateTime,var_difftimesApproved float,max_difftimesApproved DateTime,min_difftimesApproved DateTime,p01_difftimesApproved float,p02_difftimesApproved float,p05_difftimesApproved float,mx1__difftimesApproved  float, max_min_difftimesApproved INT,
                    ones_difftimesApproved float, twos_difftimesApproved float,less5_difftimesApproved float,less10_difftimesApproved float,
                    len_committersApproved INT,p01_committersApproved  float,p02_committersApproved  float,p05_committersApproved  float,mx1_committersApproved  float,
                    len_groups INT,mean_groups float,median_groups float,var_groups float,max_groups float,min_groups float,p01_groups  float,p02_groups  float,p05_groups  float,mx1_groups  float,
                    len_groupsApproved INT,mean_groupsApproved float,median_groupsApproved float,var_groupsApproved float,max_groupsApproved float,min_groupsApproved float,p01_groupsApproved  float,p02_groupsApproved  float,p05_groupsApproved  float,mx1_groupsApproved  float)'''    )
        c.execute(
            '''CREATE TABLE IF NOT EXISTS checkStyleExtends (name text, NCSS INT,FileLen INT,sum_fors REAL,sum_ifs REAL,sum_tries REAL,
                        len_mccab REAL,sum_mccab REAL,mean_mccab REAL,median_mccab REAL,var_mccab REAL,max_mccab REAL,min_mccab REAL, oneElement_mccab text,
                        len_fanOut REAL,sum_fanOut REAL,mean_fanOut REAL,median_fanOut REAL,var_fanOut REAL,max_fanOut REAL,min_fanOut REAL, oneElement_fanOut text,
                        len_NPath REAL,sum_NPath REAL,mean_NPath REAL,median_NPath REAL,var_NPath REAL,max_NPath REAL,min_NPath REAL, oneElement_NPath text,
                        len_JavaNCSSmet REAL,sum_JavaNCSSmet REAL,mean_JavaNCSSmet REAL,median_JavaNCSSmet REAL,var_JavaNCSSmet REAL,max_JavaNCSSmet REAL,min_JavaNCSSmet REAL, oneElement_JavaNCSSmet text,
                        len_thorwsSTM REAL,sum_thorwsSTM REAL,mean_thorwsSTM REAL,median_thorwsSTM REAL,var_thorwsSTM REAL,max_thorwsSTM REAL,min_thorwsSTM REAL, oneElement_thorwsSTM text,
                        len_coupl REAL,sum_coupl REAL,mean_coupl REAL,median_coupl REAL,var_coupl REAL,max_coupl REAL,min_coupl REAL, oneElement_coupl text,
                        len_executables REAL,sum_executables REAL,mean_executables REAL,median_executables REAL,var_executables REAL,max_executables REAL,min_executables REAL, oneElement_executables text,
                        len_lens REAL,sum_lens REAL,mean_lens REAL,median_lens REAL,var_lens REAL,max_lens REAL,min_lens REAL, oneElement_lens text
                        )''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS JAVAfilesFix (name text,Lines INT,	Statements INT,	Percent_Branch_Statements INT,Method_Call_Statements INT,Percent_Lines_with_Comments INT,Classes_and_Interfaces INT,Methods_per_Class float,Average_Statements_per_Method float,Line_Number_of_Most_Complex_Method 	INT, Name_of_Most_Complex_Method 	text, Maximum_Complexity INT,Line_Number_of_Deepest_Block INT,Maximum_Block_Depth INT,Average_Block_Depth	float, Average_Complexity	float, Statements_at_block_level_0 INT,Statements_at_block_level_1 INT,Statements_at_block_level_2 INT,Statements_at_block_level_3 INT,Statements_at_block_level_4 INT,Statements_at_block_level_5 INT,Statements_at_block_level_6 INT,Statements_at_block_level_7 INT,Statements_at_block_level_8 INT,Statements_at_block_level_9 INT)''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS SourcemethodsFix (File_Name text, Method text ,Complexity	INT, Statements INT, 	Maximum_Depth	INT, Calls INT)''')
    createIndexes(dbpath)


def insert_values_into_table(connection, table_name, values):
    def get_values_str(num):
        return "".join(["(", (",".join(['?'] * num)), ")"])
    if len(values) == 0:
        return
    c = connection.cursor()
    c.executemany("INSERT INTO {0} VALUES {1}".format(table_name, get_values_str(len(values[0]))), values)
    connection.commit()
    gc.collect()


def basicBuildOneTimeCommits(dbPath, commits, commitedFiles,allMethodsCommits, bugs):
    with utilsConf.use_sqllite(dbPath) as conn:
        createTables(dbPath)
        insert_values_into_table(conn, 'commits', commits)
        insert_values_into_table(conn, 'bugs', bugs)
        insert_values_into_table(conn, 'Commitedfiles', commitedFiles)
        insert_values_into_table(conn, 'commitedMethods', allMethodsCommits)


def BuildAllOneTimeCommits(git_path, dbPath, JavaDocPath, sourceMonitorFiles, sourceMonitorMethods, checkStyle, checkStyleMethods, blamePath, date, CodeDir):
    with utilsConf.use_sqllite(dbPath) as conn:
        createTables(dbPath)
        insert_values_into_table(conn, "AllMethods", checkReport.analyzeCheckStyle(checkStyleMethods))
        insert_values_into_table(conn, "haelsTfiles", commentedCodeDetector.buildHael(git_path))
        insert_values_into_table(conn, "JAVAfiles", source_Monitor.source_files(sourceMonitorFiles))
        insert_values_into_table(conn, "Sourcemethods", source_Monitor.source_methods(sourceMonitorMethods))
        insert_values_into_table(conn, 'files', list(enumerate(allFiles(git_path))))
        # can add all javadoc options
        classes_data = []
        methodData = []
        fieldData = []
        consData = []
        # for doc in docXml.build(JavaDocPath, pathPackCsv.projectPathPacks(git_path)):
        #     for classes, all_methods, all_fields, all_cons in doc:
        #         classes_data.append(classes)
        #         methodData.extend(all_methods)
        #         fieldData.extend(all_fields)
        #         consData.extend(all_cons)
        insert_values_into_table(conn, "classes", classes_data)
        insert_values_into_table(conn, "methods", methodData)
        insert_values_into_table(conn, "fields", fieldData)
        insert_values_into_table(conn, "constructors", consData)
        # insert_values_into_table(conn, "blameExtends", blameParse.blameBuild(blamePath, date))
        insert_values_into_table(conn, "checkStyleExtends", checkReport.fileRead(checkStyle, False, CodeDir))
        insert_values_into_table(conn, "JAVAfilesFix", source_Monitor.source_files(sourceMonitorFiles))
        insert_values_into_table(conn, "SourcemethodsFix", source_Monitor.source_methods(sourceMonitorMethods))


def createIndexes(dbPath):
    with utilsConf.use_sqllite(dbPath) as conn:
        c = conn.cursor()

        def create_index(index):
            c.execute(index)
            conn.commit()
        create_index('CREATE INDEX IF NOT EXISTS commits_id ON commits (ID)')
        create_index('CREATE INDEX IF NOT EXISTS commits_commiter_date ON commits (commiter_date)')
        create_index('CREATE INDEX IF NOT EXISTS bugs_id ON bugs (ID)')
        create_index('CREATE INDEX IF NOT EXISTS bugsFix_id ON bugsFix (ID)')
        create_index('CREATE INDEX IF NOT EXISTS commitedFiles_Commitid ON commitedfiles (commitid)')
        create_index('CREATE INDEX IF NOT EXISTS commitedFiles_commiter_date ON commitedfiles (commiter_date)')
        create_index('CREATE INDEX IF NOT EXISTS commitedFiles_bugId ON commitedfiles (bugId)')
        create_index('CREATE INDEX IF NOT EXISTS commitedFiles_Name ON commitedfiles (name)')
        create_index('CREATE INDEX IF NOT EXISTS JAVAfiles_Name ON JAVAfiles (name)')
        create_index('CREATE INDEX IF NOT EXISTS Sourcemethods_fileName ON Sourcemethods (File_Name)')
        create_index('CREATE INDEX IF NOT EXISTS JAVAfilesFix_Name ON JAVAfilesFix (name)')
        create_index('CREATE INDEX IF NOT EXISTS SourcemethodsFix_fileName ON SourcemethodsFix (File_Name)')
        create_index('CREATE INDEX IF NOT EXISTS classes_Name ON classes (name)')
        create_index('CREATE INDEX IF NOT EXISTS constructors_className ON constructors (className)')
        create_index('CREATE INDEX IF NOT EXISTS methods_className ON methods (className)')
        create_index('CREATE INDEX IF NOT EXISTS fields_className ON fields (className)')
        create_index('CREATE INDEX IF NOT EXISTS checkStyle_name ON checkStyle (name)')
        create_index('CREATE INDEX IF NOT EXISTS checkStyleExtends_name ON checkStyleExtends (name)')
        create_index('CREATE INDEX IF NOT EXISTS blameExtends_name ON blameExtends (name)')
        create_index('CREATE INDEX IF NOT EXISTS AllMethods_methodDir ON AllMethods (methodDir)')
        create_index('CREATE INDEX IF NOT EXISTS commitedMethods_methodDir ON commitedMethods (methodDir)')
        create_index('CREATE INDEX IF NOT EXISTS commitedMethods_commitID ON commitedMethods (commitID)')
        create_index('CREATE INDEX IF NOT EXISTS AllMethods_fileName ON AllMethods (fileName)')
        create_index('CREATE INDEX IF NOT EXISTS commitedMethods_fileName ON commitedMethods (fileName)')
        create_index('CREATE INDEX IF NOT EXISTS commitedMethods_methodName ON commitedMethods (methodName)')
        create_index('CREATE INDEX IF NOT EXISTS commitedMethods_bugId ON commitedMethods (bugId)')
        create_index('CREATE INDEX IF NOT EXISTS commitedMethods_commiter_date ON commitedMethods (commiter_date)')


def buildBasicAllVers(vers, dates, dbsPath, bugsPath, MethodsParsed, changeFile):
    gitPath = utilsConf.get_configuration().LocalGitPath
    commits, commitedFiles, allMethodsCommits, bugs, allFilesCommitsPatch = BuildRepo(gitPath, bugsPath, MethodsParsed, changeFile)
    for ver, date in zip(vers,dates):
        dbPath = os.path.join(dbsPath, ver+".db")
        basicBuildOneTimeCommits(dbPath, commits, commitedFiles, allMethodsCommits, bugs)


@utilsConf.marker_decorator(utilsConf.DB_LABELS_MARKER)
def build_labels():
    db_dir = utilsConf.get_configuration().db_dir
    vers = utilsConf.get_configuration().vers_dirs
    dates = utilsConf.get_configuration().dates
    buildBasicAllVers(vers, dates, db_dir, utilsConf.get_configuration().bugsPath,
                      utilsConf.get_configuration().MethodsParsed, utilsConf.get_configuration().changeFile)


@utilsConf.marker_decorator(utilsConf.DB_BUILD_MARKER)
def buildOneTimeCommits():
    versPath = utilsConf.get_configuration().versPath
    db_dir = utilsConf.get_configuration().db_dir
    vers = utilsConf.get_configuration().vers_dirs
    dates = utilsConf.get_configuration().dates
    CodeDir = "repo"
    build_labels()
    for version, date in zip(vers, dates):
        gc.collect()
        Path = os.path.join(versPath, version)
        dbPath = os.path.join(db_dir, version + ".db")
        JavaDocPath = os.path.join(Path, "Jdoc2")
        sourceMonitorFiles = os.path.join(Path, version+".csv")
        sourceMonitorMethods = os.path.join(Path, version+"_methods.csv")
        checkStyle = os.path.join(versPath, "checkAll", version+".xml")
        checkStyleMethods = os.path.join(versPath, "checkAllMethodsData", version+".txt")
        blamePath = os.path.join(Path, "blame")
        BuildAllOneTimeCommits(utilsConf.get_configuration().gitPath, dbPath, JavaDocPath,
                               sourceMonitorFiles, sourceMonitorMethods, checkStyle, checkStyleMethods,
                               blamePath, date, CodeDir)
