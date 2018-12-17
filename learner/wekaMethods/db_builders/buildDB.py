import gc
import os
import sqlite3
from functools import partial

import git

import utilsConf
import wekaMethods.blameParse
from utils.monitors_manager import monitor, DB_BUILD_MARKER, DB_LABELS_MARKER
from wekaMethods import (patchsBuild,
                         source_Monitor,
                         commentedCodeDetector,
                         checkReport,
                         docXml,
                         pathPackCsv)
from wekaMethods.db_builders.bugs_db_builder import parse_bugs_data
from wekaMethods.db_builders.commits_db_builder import CommitTable
from wekaMethods.db_builders.tables_creation_sql_commands import (JAVA_TABLES_CREATION_COMMANDS,
                                                                  CREATE_ALL_METHODS_SQL_TABLE)
from wekaMethods.db_builders.tables_names import (FIELDS_TABLE_NAME,
                                                  COMMITS_TABLE_NAME,
                                                  BUGS_TABLE_NAME,
                                                  COMMITTED_FILES_TABLE_NAME,
                                                  COMMITTED_METHODS_TABLE_NAME,
                                                  ALL_METHOD_TABLE_NAME, HALSTEAD_TABLE_NAME,
                                                  JAVA_FILES_TABLE_NAME, SOURCE_METHODS_TABLE_NAME)


# import git.objects.tree


def collect_repository_data(git_path, bugs_path, parsed_methods, change_files):
	""""""
	repo = git.Repo(git_path)
	all_bugs, bugs_ids = parse_bugs_data(bugs_path)
	all_methods, files_rows = patchsBuild.analyzeCheckStyle(parsed_methods, change_files)
	all_commits, commits_bugs_dict = CommitTable(repository=repo, bug_ids=bugs_ids) \
		.collect_light_commit_table_data()

	all_methods_commits = extract_committed_id_method_data(all_methods, commits_bugs_dict, 0)
	all_files_commits = extract_committed_id_method_data(all_methods, commits_bugs_dict, 1)

	return all_commits, all_files_commits, all_methods_commits, all_bugs, all_files_commits


def extract_committed_id_method_data(all_methods, commits_bugs_dict, item_index):
	committed_items = []
	not_commit_id_counter = 1
	for method in all_methods:
		item_commit_id = method[item_index]
		if item_commit_id not in commits_bugs_dict:
			print "not CommitID item: {}, {}".format(item_commit_id, not_commit_id_counter)
			not_commit_id_counter += 1
			continue

		bug, committer_date, sha, commit_id = commits_bugs_dict[item_commit_id]
		committed_items.append(method + [bug, committer_date, commit_id])

	return committed_items


def create_tables(cursor, do_add=False, is_java=True):
	cursor.execute(CREATE_ALL_METHODS_SQL_TABLE)
	if do_add:
		return

	for sql_command in JAVA_TABLES_CREATION_COMMANDS:
		# print "Running the command: {}".format(sql_command)
		cursor.execute(sql_command)


def insert_values_into_table(connection, table_name, values):
	values_str = "".join(["(", (",".join(['?'] * len(values[0]))), ")"])
	cursor = connection.cursor()
	cursor.executemany("INSERT INTO {0} VALUES {1}".format(table_name, values_str), values)

	connection.commit()
	gc.collect()


def get_relative_files_paths(path):
	"""Get the relative paths of the files that belongs to the repositry.

	Args:
		path (str): path to the repository.

	Returns:
		list. All the files' relative paths and an added index to each path.
	"""
	relative_paths = []
	for root, _, files in os.walk(path):  # Walk directory tree
		for file_name in files:
			abs_path = os.path.join(root, file_name)
			file_relative_path = abs_path.split("{}/".format(path))[1]
			relative_paths.append(file_relative_path)

	return relative_paths


def insert_single_commit_data(db_path, git_path, commits, committed_files, all_methods_commits,
                              bugs):
	""""""
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	insert_values_into_table(conn, FIELDS_TABLE_NAME,
	                         list(enumerate(get_relative_files_paths(git_path))))
	insert_values_into_table(conn, COMMITS_TABLE_NAME, commits)
	insert_values_into_table(conn, BUGS_TABLE_NAME, bugs)
	insert_values_into_table(conn, COMMITTED_FILES_TABLE_NAME, committed_files)
	insert_values_into_table(conn, COMMITTED_METHODS_TABLE_NAME, all_methods_commits)
	conn.close()


def BuildAllOneTimeCommits(git_path, db_path, javadoc_path, source_monitor_files,
                           source_monitor_methods, checkstyle, checkstyle_methods, blame_path, date,
                           do_add, code_dir):
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	cursor = conn.cursor()
	# Creating all the relevant tables
	create_tables(cursor, do_add)

	# Inserting the collected values to the created tables.
	insert_values_into_table(conn, ALL_METHOD_TABLE_NAME,
	                         checkReport.analyzeCheckStyle(checkstyle_methods))
	if not do_add:
		insert_values_into_table(conn, HALSTEAD_TABLE_NAME,
		                         commentedCodeDetector.buildHael(git_path))
		insert_values_into_table(conn, JAVA_FILES_TABLE_NAME,
		                         source_Monitor.source_files(source_monitor_files))
		insert_values_into_table(conn, SOURCE_METHODS_TABLE_NAME,
		                         source_Monitor.source_methods(source_monitor_methods))
		# can add all javadoc options
		classes_data = []
		methodData = []
		fieldData = []
		consData = []
		for doc in docXml.build(javadoc_path, pathPackCsv.projectPathPacks(git_path)):
			for classes, all_methods, all_fields, all_cons in doc:
				classes_data.append(classes)
				methodData.extend(all_methods)
				fieldData.extend(all_fields)
				consData.extend(all_cons)
		insert_values_into_table(conn, "classes", classes_data)
		insert_values_into_table(conn, "methods", methodData)
		insert_values_into_table(conn, "fields", fieldData)
		insert_values_into_table(conn, "constructors", consData)
		insert_values_into_table(conn, "blameExtends",
		                         wekaMethods.blameParse.blameBuild(blame_path, date))
		insert_values_into_table(conn, "checkStyleExtends",
		                         wekaMethods.checkReport.fileRead(checkstyle, False, code_dir))
		insert_values_into_table(conn, "JAVAfilesFix",
		                         wekaMethods.source_Monitor.source_files(source_monitor_files))
		insert_values_into_table(conn, "SourcemethodsFix",
		                         wekaMethods.source_Monitor.source_methods(source_monitor_methods))
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
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commits_commiter_date ON commits (commiter_date)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS bugs_id ON bugs (ID)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS bugsFix_id ON bugsFix (ID)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commitedFiles_Commitid ON commitedfiles (commitid)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commitedFiles_commiter_date ON Commitedfiles (commiter_date)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commitedFiles_bugId ON Commitedfiles (bugId)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS commitedFiles_Name ON Commitedfiles (name)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS JAVAfiles_Name ON JAVAfiles (name)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS Sourcemethods_fileName ON Sourcemethods (File_Name)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS JAVAfilesFix_Name ON JAVAfilesFix (name)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS SourcemethodsFix_fileName ON SourcemethodsFix (File_Name)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS classes_Name ON classes (name)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS constructors_className ON constructors (className)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS methods_className ON methods (className)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS fields_className ON fields (className)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS checkStyle_name ON checkStyle (name)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS checkStyleExtends_name ON checkStyleExtends (name)')
	execute_index_creation('CREATE INDEX IF NOT EXISTS blameExtends_name ON blameExtends (name)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS AllMethods_methodDir ON AllMethods (methodDir)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commitedMethods_methodDir ON commitedMethods (methodDir)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commitedMethods_commitID ON commitedMethods (commitID)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS AllMethods_fileName ON AllMethods (fileName)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commitedMethods_fileName ON commitedMethods (fileName)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commitedMethods_methodName ON commitedMethods (methodName)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commitedMethods_bugId ON commitedMethods (bugId)')
	execute_index_creation(
		'CREATE INDEX IF NOT EXISTS commitedMethods_commiter_date ON commitedMethods (commiter_date)')
	conn.close()


def basicBuildOneTimeCommits(dbPath, commits, commitedFiles, allMethodsCommits, bugs):
	with utilsConf.use_sqllite(dbPath) as conn:
		createTables(dbPath)
		insert_values_into_table(conn, 'commits', commits)
		insert_values_into_table(conn, 'bugs', bugs)
		insert_values_into_table(conn, 'Commitedfiles', commitedFiles)
		insert_values_into_table(conn, 'commitedMethods', allMethodsCommits)


def buildBasicAllVers(vers, dates, dbsPath, bugsPath, MethodsParsed, changeFile, configuration):
	gitPath = configuration.LocalGitPath
	commits, commitedFiles, allMethodsCommits, bugs, allFilesCommitsPatch = \
		collect_repository_data(gitPath, bugsPath, MethodsParsed, changeFile)
	for ver, date in zip(vers, dates):
		dbPath = os.path.join(dbsPath, ver + ".db")
		basicBuildOneTimeCommits(dbPath, commits, commitedFiles, allMethodsCommits, bugs)


@monitor(DB_LABELS_MARKER)
def build_labels(configuration):
	buildBasicAllVers(configuration.vers_dirs, configuration.dates,
	                  configuration.db_dir, configuration.bugsPath,
	                  configuration.MethodsParsed, configuration.changeFile, configuration)


@monitor(DB_BUILD_MARKER)
def buildOneTimeCommits(configuration):
	versPath = configuration.versPath
	db_dir = configuration.db_dir
	vers = configuration.vers_dirs
	dates = configuration.dates
	CodeDir = "repo"
	build_labels()
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
		BuildAllOneTimeCommits(configuration.gitPath, dbPath, JavaDocPath,
		                       sourceMonitorFiles, sourceMonitorMethods, checkStyle,
		                       checkStyleMethods,
		                       blamePath, date, CodeDir)
