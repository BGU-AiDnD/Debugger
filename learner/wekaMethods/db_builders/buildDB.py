import csv
import datetime
import gc
import os
import sqlite3
import unicodedata
from functools import partial

import git
import git.objects.tree

import wekaMethods.blameParse
import wekaMethods.checkReport
import wekaMethods.commentedCodeDetector
import wekaMethods.docXml
import wekaMethods.patchsBuild
import wekaMethods.pathPackCsv
import wekaMethods.source_Monitor
import utilsConf
from wekaMethods.tables_creation_sql_commands import JAVA_TABLES_CREATION_COMMANDS, \
	CREATE_ALL_METHODS_SQL_TABLE
from wekaMethods.db_builders.commits_db_builder import Commit


def collect_commit_table_data(bugs, commits, max):
	""""""
	commits_items = commits.items()
	all_commits = []
	all_files = []
	commits_bugs_dict = {}

	for index, (_, commit_object) in enumerate(commits_items, 1):
		if index == max:
			break

		bug_id_fixed_by_commit = bugs[index - 1]
		commit_data = Commit(commit_object)
		fields = commit_data.get_bug_fix_commit_fields(bug_id_fixed_by_commit)

		commits_bugs_dict[commit_data.hex_sha] = (
			bug_id_fixed_by_commit, commit_data.committed_date, commit_data.hex_sha,
			str(commit_data.id))
		all_commits.append(fields)
		commit_files_data = commit_data.get_commit_files_data(bug_id_fixed_by_commit)
		all_files += commit_files_data

	return all_commits, all_files, commits_bugs_dict

def commTablelight(commits):
	all_commits = []
	commitsBugsDict = {}
	for commit in commits:
		git_commit = commit._git_commit
		commit_id = int("".join(list(git_commit.hexsha)[:7]), 16)
		if not hasattr(git_commit, 'committed_date'):
			continue
		commiter_date = datetime.datetime.fromtimestamp(git_commit.committed_date).strftime(
			'%Y-%m-%d %H:%M:%S')
		author_date = datetime.datetime.fromtimestamp(git_commit.authored_date).strftime(
			'%Y-%m-%d %H:%M:%S')
		name = unicodedata.normalize('NFKD', git_commit.committer.name).encode('ascii', 'ignore')
		committer = str(name)
		author = str(git_commit.author.name.encode('ascii', 'ignore'))
		parent = 0
		if (git_commit.parents != ()):
			parent = int("".join(list(git_commit.parents[0].hexsha)[:7]), 16)
		msg = git_commit.message
		size = git_commit.size
		fields = (
			commit_id, commit._bug_id, commiter_date, committer, author_date, author, size, parent,
			msg,
			str(git_commit.hexsha))
		all_commits.append(fields)
		commitsBugsDict[str(git_commit.hexsha)] = (
			commit._bug_id, commiter_date, str(git_commit.hexsha), str(commit_id))
	return (all_commits, commitsBugsDict)


def clean_commit_message(commit_message):
	if "git-svn-id" in commit_message:
		return commit_message.split("git-svn-id")[0]
	return commit_message


def commits_and_Bugs(repo, bugsIds):
	def get_bug_num_from_comit_text(commit_text, bugsIds):
		s = commit_text.lower().replace(":", "").replace("#", "").replace("-", " ").replace("_",
																							" ").split()
		for word in s:
			if word.isdigit():
				if word in bugsIds:
					return word
		return "0"

	commits = []
	for git_commit in repo.iter_commits():
		commit_text = clean_commit_message(git_commit.message)
		commits.append(Commit(git_commit, get_bug_num_from_comit_text(commit_text, bugsIds)))
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
		next(reader, None)  # skip header
		for row in reader:  # iterates the rows of the file in orders
			r = []
			for x in row:
				lst = x
				if len(lst) > 0 and lst[0] == "=":
					lst = lst[2:(len(lst) - 1)]
				r.append(str(lst))
			if len(r) < 16:
				continue
			r[7] = fix_date(r[7])
			r[16] = fix_date(r[16])
			bugsIds.append(r[0])
			all_bugs.append(r)
		return all_bugs, bugsIds


def allFiles(path):
	acc = []
	pathLen = len(path) + 1  # one for the \
	for root, dirs, files in os.walk(path):  # Walk directory tree
		for f in files:
			path_join = "".join(list(os.path.join(root, f))[pathLen:])
			acc.append(path_join)
	return acc


def BuildRepo(gitPath, bugsPath, MethodsParsed, changeFile):
	repo = git.Repo(gitPath)
	allBugs, bugsIds = bugsTable(bugsPath)
	allMethods, filesRows = wekaMethods.patchsBuild.analyzeCheckStyle(MethodsParsed, changeFile)
	allCommits, commitsBugsDict = commTablelight(commits_and_Bugs(repo, bugsIds))
	allMethodsCommits = []
	allFilesCommits = []
	i = 0
	for m in allMethods:
		if not m[0] in commitsBugsDict:
			i = i + 1
			print "not CommitID method", m[0], i
			continue
		bug, commiterDate, sha, CommitId = commitsBugsDict[m[0]]
		r = m + [bug, commiterDate, CommitId]
		allMethodsCommits.append(r)
	i = 0
	for m in filesRows:
		if not m[1] in commitsBugsDict:
			i = i + 1
			print "not CommitID file", m[1], i
			continue
		bug, commiterDate, sha, CommitId = commitsBugsDict[m[1]]
		r = [0] + m + [bug, commiterDate, CommitId]
		allFilesCommits.append(r)
	return (allCommits, allFilesCommits, allMethodsCommits, allBugs, allFilesCommits)


def create_tables(cursor, add, _is_java=True):
	cursor.execute(CREATE_ALL_METHODS_SQL_TABLE)
	if not add:
		for sql_command in JAVA_TABLES_CREATION_COMMANDS:
			cursor.execute(sql_command)


def insert_values_into_table(connection, table_name, values):
	def get_values_str(num):
		return "".join(["(", (",".join(['?'] * num)), ")"])

	c = connection.cursor()
	c.executemany("INSERT INTO {0} VALUES {1}".format(table_name, get_values_str(len(values[0]))),
				  values)
	connection.commit()
	gc.collect()


def basicBuildOneTimeCommits(dbPath, gitPath, commits, commitedFiles, allMethodsCommits, bugs):
	conn = sqlite3.connect(dbPath)
	conn.text_factory = str
	insert_values_into_table(conn, 'files', list(enumerate(allFiles(gitPath))))
	insert_values_into_table(conn, 'commits', commits)
	insert_values_into_table(conn, 'bugs', bugs)
	insert_values_into_table(conn, 'Commitedfiles', commitedFiles)
	insert_values_into_table(conn, 'commitedMethods', allMethodsCommits)
	conn.close()


def BuildAllOneTimeCommits(git_path, dbPath, JavaDocPath, sourceMonitorFiles, sourceMonitorMethods,
						   checkStyle, checkStyleMethods, blamePath, date, add, max, CodeDir):
	conn = sqlite3.connect(dbPath)
	conn.text_factory = str
	c = conn.cursor()
	create_tables(c, add)
	insert_values_into_table(conn, "AllMethods", wekaMethods.checkReport.analyzeCheckStyle(checkStyleMethods))
	if (not add):
		insert_values_into_table(conn, "haelsTfiles", wekaMethods.commentedCodeDetector.buildHael(git_path))
		insert_values_into_table(conn, "JAVAfiles", wekaMethods.source_Monitor.source_files(sourceMonitorFiles))
		insert_values_into_table(conn, "Sourcemethods",
		                         wekaMethods.source_Monitor.source_methods(sourceMonitorMethods))
		# can add all javadoc options
		classes_data = []
		methodData = []
		fieldData = []
		consData = []
		for doc in wekaMethods.docXml.build(JavaDocPath, wekaMethods.pathPackCsv.projectPathPacks(git_path)):
			for classes, all_methods, all_fields, all_cons in doc:
				classes_data.append(classes)
				methodData.extend(all_methods)
				fieldData.extend(all_fields)
				consData.extend(all_cons)
		insert_values_into_table(conn, "classes", classes_data)
		insert_values_into_table(conn, "methods", methodData)
		insert_values_into_table(conn, "fields", fieldData)
		insert_values_into_table(conn, "constructors", consData)
		insert_values_into_table(conn, "blameExtends", wekaMethods.blameParse.blameBuild(blamePath, date))
		insert_values_into_table(conn, "checkStyleExtends",
		                         wekaMethods.checkReport.fileRead(checkStyle, False, CodeDir))
		insert_values_into_table(conn, "JAVAfilesFix",
		                         wekaMethods.source_Monitor.source_files(sourceMonitorFiles))
		insert_values_into_table(conn, "SourcemethodsFix",
		                         wekaMethods.source_Monitor.source_methods(sourceMonitorMethods))
	conn.close()


def _create_index(cursor, connection, index_query):
	cursor.execute(index_query)
	connection.commit()

def createIndexes(dbPath):
	conn = sqlite3.connect(dbPath)
	conn.text_factory = str
	c = conn.cursor()

	execute_index_creation = partial(_create_index, cursor=c, connection=conn)
	
	execute_index_creation('CREATE INDEX IF NOT EXISTS commits_id ON commits (ID)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS commits_commiter_date ON commits (commiter_date)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS bugs_id ON bugs (ID)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS bugsFix_id ON bugsFix (ID)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS commitedFiles_Commitid ON commitedfiles (commitid)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commitedFiles_commiter_date ON commitedfiles (commiter_date)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS commitedFiles_bugId ON commitedfiles (bugId)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS commitedFiles_Name ON commitedfiles (name)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS JAVAfiles_Name ON JAVAfiles (name)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS Sourcemethods_fileName ON Sourcemethods (File_Name)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS JAVAfilesFix_Name ON JAVAfilesFix (name)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS SourcemethodsFix_fileName ON SourcemethodsFix (File_Name)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS classes_Name ON classes (name)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS constructors_className ON constructors (className)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS methods_className ON methods (className)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS fields_className ON fields (className)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS checkStyle_name ON checkStyle (name)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS checkStyleExtends_name ON checkStyleExtends (name)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS blameExtends_name ON blameExtends (name)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS AllMethods_methodDir ON AllMethods (methodDir)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commitedMethods_methodDir ON commitedMethods (methodDir)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commitedMethods_commitID ON commitedMethods (commitID)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS AllMethods_fileName ON AllMethods (fileName)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commitedMethods_fileName ON commitedMethods (fileName)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commitedMethods_methodName ON commitedMethods (methodName)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS commitedMethods_bugId ON commitedMethods (bugId)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commitedMethods_commiter_date ON commitedMethods (commiter_date)')
	conn.close()


def buildBasicAllVers(vers, dates, versPath, CodeDir, dbsPath, bugsPath, MethodsParsed, changeFile):
	gitPath = os.path.join(versPath, vers[-1], CodeDir)
	commits, commitedFiles, allMethodsCommits, bugs, allFilesCommitsPatch = BuildRepo(gitPath,
																					  bugsPath,
																					  MethodsParsed,
																					  changeFile)
	for ver, date in zip(vers, dates):
		gitPath = os.path.join(versPath, ver, CodeDir)
		dbPath = os.path.join(dbsPath, ver + ".db")
		basicBuildOneTimeCommits(dbPath, gitPath, commits, commitedFiles, allMethodsCommits, bugs)


@utilsConf.marker_decorator(utilsConf.DB_BUILD_MARKER)
def buildOneTimeCommits():
	versPath = utilsConf.get_configuration().versPath
	db_dir = utilsConf.get_configuration().db_dir
	vers = utilsConf.get_configuration().vers_dirs
	dates = utilsConf.get_configuration().dates
	add = False
	max = -1
	CodeDir = "repo"
	for version, date in zip(vers, dates):
		gc.collect()
		Path = os.path.join(versPath, version)
		dbPath = os.path.join(db_dir, version + ".db")
		JavaDocPath = os.path.join(Path, "Jdoc2")
		sourceMonitorFiles = os.path.join(Path, version + ".csv")
		sourceMonitorMethods = os.path.join(Path, version + "_methods.csv")
		checkStyle = os.path.join(versPath, "checkAll", version + ".xml")
		checkStyleMethods = os.path.join(versPath, "checkAllMethodsData", version + ".txt")
		blamePath = os.path.join(Path, "blame")
		BuildAllOneTimeCommits(utilsConf.get_configuration().gitPath, dbPath, JavaDocPath,
							   sourceMonitorFiles, sourceMonitorMethods, checkStyle,
							   checkStyleMethods,
							   blamePath, date, add, max, CodeDir)
		createIndexes(dbPath)
	buildBasicAllVers(vers, dates, versPath, CodeDir, db_dir,
					  utilsConf.get_configuration().bugsPath,
					  utilsConf.get_configuration().MethodsParsed,
					  utilsConf.get_configuration().changeFile)
