import json

from attrdict import AttrDict

from filesystem_utils import convert_to_long_path, copy

import datetime
import shutil
import git
import os
import subprocess
import traceback
import sys
import github3
import sqlite3
from datetime import datetime
import logging
import detect_renamed_files
from contextlib import contextmanager

# markers names:
VERSIONS_MARKER = "versions"
VERSION_TEST_MARKER = "test_version"
FEATURES_MARKER = "features"
DB_BUILD_MARKER = "db"
DB_LABELS_MARKER = "labels"
ML_MODELS_MARKER = "ml"
COMPLEXITY_FEATURES_MARKER = "complexity_features"
OO_OLD_FEATURES_MARKER = "old_oo_features"
OO_FEATURES_MARKER = "oo_features"
COMMENTS_SPACES_MARKER = "comments_spaces_features"
PATCHS_FEATURES_MARKER = "patchs_features"
SOURCE_MONITOR_FEATURES_MARKER = "source_monitor_features"
BLAME_FEATURES_MARKER = "blame_features"
TEST_DB_MARKER = "test_db_features"
PACKS_FILE_MARKER = "packs_file_features"
LEARNER_PHASE_FILE = "learner_phase_file"
DISTRIBUTION_FILE = "distribution_file"
ALL_DONE_FILE = "all_done"
EXECUTE_TESTS = "test_executed"
ISSUE_TRACKER_FILE = "issue_tracker_file"
ERROR_FILE = "error_file"

conf = None

USE_LONG_PATHS = True


def globalConfig():
	current_dir = os.path.dirname(os.path.realpath(__file__))
	utilsPath = os.path.realpath(os.path.join(current_dir, "../utils"))
	docletPath = os.path.join(utilsPath, "xml-doclet-1.0.4-jar-with-dependencies.jar")
	sourceMonitorEXE = os.path.join(utilsPath, "SourceMonitor.exe")
	checkStyle57 = os.path.join(utilsPath, "checkstyle-5.7-all.jar")
	checkStyle68 = os.path.join(utilsPath, "checkstyle-6.8-SNAPSHOT-all.jar")
	allchecks = os.path.join(utilsPath, "allChecks.xml")
	methodsNamesXML = os.path.join(utilsPath, "methodNameLines.xml")
	wekaJar = os.path.join(utilsPath, "weka.jar")
	RemoveBat = os.path.join(utilsPath, "../removeBat.bat")
	return docletPath, sourceMonitorEXE, checkStyle57, checkStyle68, allchecks, methodsNamesXML, wekaJar, RemoveBat, utilsPath


def versions_info(repository_path, versions=[]):
	repo = git.Repo(repository_path)
	if len(versions) == 0:
		requested_commits = [x.commit for x in repo.tags]
		versions = repo.tags

	else:
		requested_commits = [x.commit for x in repo.tags if x.name in versions]
		if not requested_commits:
			requested_commits = filter(lambda c: c.hexsha in versions, repo.iter_commits())
	commits = [int("".join(list(x.hexsha)[:7]), 16) for x in requested_commits]
	dates = [datetime.fromtimestamp(x.committed_date).strftime('%Y-%m-%d %H:%M:%S') for x in requested_commits]
	paths = [os.path.join(ver, "repo") for ver in versions]
	return versions, paths, dates, commits


def copy_directories(gitPath, versPath, versions):
	remote_url = list(git.Repo(convert_to_long_path(gitPath)).remote().urls)[0]
	for version in versions:
		path = os.path.join(versPath, version_to_dir_name(version), "repo")
		if not os.path.exists(path):
			run_commands = ["git", "clone", remote_url, 'repo']
			proc = open_subprocess(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
			                       shell=True,
			                       cwd=convert_to_long_path(
				                       os.path.join(versPath, version_to_dir_name(version))))
			(out, err) = proc.communicate()


def GitRevert(versPath, vers):
	def run_cmd(path, args):
		run_commands = ["git", "-C", path] + args
		proc = open_subprocess(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
		                       shell=True)
		(out, err) = proc.communicate()

	for version in vers:
		repo_path = os.path.join(versPath, version_to_dir_name(version), "repo")
		run_cmd(repo_path, ["clean", "-fd", version])
		run_cmd(repo_path, ["checkout", '-f', version])
		run_cmd(repo_path, ["clean", "-fd", version])


def checkout_local_git(gitPath, workingDir):
	run_commands = ["git", "clone", convert_to_long_path(gitPath), 'repo']
	proc = open_subprocess(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
	                       cwd=convert_to_long_path(workingDir))
	(out, err) = proc.communicate()


def versionsCreate(gitPath, vers, versPath):
	copy_directories(gitPath, versPath, vers)
	GitRevert(versPath, vers)


def git_file_path_to_java_name(file_path):
	directories = os.path.splitext(os.path.normpath(file_path))[0].split(os.path.sep)
	index = 0
	if 'java' in directories:
		index = directories.index('java') + 1
	elif 'src' in directories:
		index = directories.index('src') + 2
	return ".".join(directories[index:])


def download_bugs(bugs_path, issue_tracker_url, issue_tracker_product, issue_tracker):
	import wekaMethods.issuesExtract.github_import
	import wekaMethods.issuesExtract.google_code
	import wekaMethods.issuesExtract.jira_import
	import wekaMethods.issuesExtract.python_bugzilla
	import wekaMethods.issuesExtract.sourceforge
	import wekaMethods.issuesExtract.csv_labels
	if issue_tracker == "bugzilla":
		wekaMethods.issuesExtract.python_bugzilla.write_bugs_csv(bugs_path, issue_tracker_url,
		                                                         issue_tracker_product)
	elif issue_tracker == "jira":
		wekaMethods.issuesExtract.jira_import.jiraIssues(bugs_path, issue_tracker_url,
		                                                 issue_tracker_product)
	elif issue_tracker == "github":
		wekaMethods.issuesExtract.github_import.GithubIssues(bugs_path, issue_tracker_url,
		                                                     issue_tracker_product)
	elif issue_tracker == "sourceforge":
		wekaMethods.issuesExtract.sourceforge.write_bugs_csv(bugs_path, issue_tracker_url,
		                                                     issue_tracker_product)
	elif issue_tracker == "googlecode":
		wekaMethods.issuesExtract.google_code.write_bugs_csv(bugs_path, issue_tracker_url,
		                                                     issue_tracker_product)
	elif issue_tracker == "csv_file":
		wekaMethods.issuesExtract.csv_labels.write_bugs_csv(bugs_path, issue_tracker_url,
		                                                    issue_tracker_product)


def configure(configuration_file, logger):
	logger.info("Starting to configure the basic requirements to run the algorithm")
	configuration = read_configuration(configuration_file)
	init_configuration(configuration.workdir, configuration.versions, logger)

	maker_handler = get_configuration()
	db_dir = os.path.join(configuration.workdir, "dbAdd")
	distribution_report = os.path.join(configuration.workdir, "distribution_report.csv")
	distribution_per_version_report = os.path.join(configuration.workdir,
	                                               "distribution_per_version_report.csv")
	versPath = os.path.join(configuration.workdir, "vers")
	vers, paths, dates, commits = versions_info(convert_to_long_path(configuration.git_repo_path),
	                                            configuration.versions)
	docletPath, sourceMonitorEXE, checkStyle57, checkStyle68, allchecks, methodsNamesXML, wekaJar, RemoveBat, utilsPath = globalConfig()
	current_dir = os.path.dirname(os.path.realpath(__file__))
	utilsPath = os.path.realpath(os.path.join(current_dir, "../utils"))
	caching_dir = os.path.realpath(os.path.join(current_dir, "../Debugger_cache"))
	amir_tracer = os.path.join(utilsPath, "uber-tracer-1.0.1-SNAPSHOT.jar")
	bugsPath = os.path.join(configuration.workdir, "bugs.csv")
	vers_dirs = map(version_to_dir_name, vers)
	vers_paths = map(lambda ver: os.path.join(versPath, ver), vers_dirs)
	LocalGitPath = convert_to_long_path(os.path.join(configuration.workdir, "repo"))
	prediction_files = {
		'files': {'all': 'prediction_All_files.csv', 'most': 'prediction_Most_files.csv'},
		'methods': {'all': 'prediction_All_methods.csv', 'most': 'prediction_Most_methods.csv'}}
	create_directory_if_not_exists(LocalGitPath)
	weka_path = convert_to_long_path(os.path.join(configuration.workdir, "weka"))
	web_prediction_results = convert_to_long_path(
		os.path.join(configuration.workdir, "web_prediction_results"))
	configuration_path = convert_to_long_path(os.path.join(configuration.workdir, "configuration.json"))
	experiments = convert_to_long_path(os.path.join(configuration.workdir, "experiments"))
	DebuggerTests = convert_to_long_path(os.path.join(configuration.workdir, "DebuggerTests"))
	MethodsParsed = convert_to_long_path(
		os.path.join(os.path.join(configuration.workdir, "commitsFiles"), "CheckStyle.txt"))
	changeFile = convert_to_long_path(
		os.path.join(os.path.join(configuration.workdir, "commitsFiles"), "Ins_dels.txt"))
	debugger_base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	buggy_repo = git.Repo(convert_to_long_path(configuration.git_repo_path))
	renamed_mapping = {}  # detect_renamed_files.renamed_files_for_repo(buggy_repo)
	remotes_urls = reduce(list.__add__, map(lambda r: list(r.urls), buggy_repo.remotes))
	buggy_repo.close()
	try:
		repo = git.Repo(debugger_base_path)
		debugger_commit = str(repo.head.commit)
		logging.info('Debugger HEAD is on commit {0}'.format(debugger_commit))
		repo.close()

	except:
		pass

	names_values = [("versPath", versPath), ("db_dir", db_dir), ("vers", vers), ("paths", paths),
	                ("dates", dates),
	                ("commits", commits), ("docletPath", docletPath),
	                ("sourceMonitorEXE", sourceMonitorEXE),
	                ("checkStyle57", checkStyle57), ("checkStyle68", checkStyle68),
	                ("allchecks", allchecks),
	                ("methodsNamesXML", methodsNamesXML), ("wekaJar", wekaJar),
	                ("RemoveBat", RemoveBat),
	                ("utilsPath", utilsPath), ("versions", configuration.versions),
	                ("gitPath", configuration.git_repo_path), ("issue_tracker",
	                                                           configuration.issue_tracker_name),
	                ("issue_tracker_url", configuration.issue_tracker_url),
	                ("issue_tracker_product", configuration.product_being_tracked),
	                ("workingDir", configuration.workdir), ("bugsPath", bugsPath),
	                ("vers_dirs", vers_dirs), ("vers_paths", vers_paths),
	                ("LocalGitPath", LocalGitPath), ("weka_path", weka_path),
	                ("MethodsParsed", MethodsParsed),
	                ("changeFile", changeFile), ("debugger_base_path", debugger_base_path),
	                ("web_prediction_results", web_prediction_results),
	                ("amir_tracer", amir_tracer), ("configuration_path", configuration_path),
	                ("caching_dir", caching_dir),
	                ('DebuggerTests', DebuggerTests), ('prediction_files', prediction_files),
	                ('experiments', experiments),
	                ('renamed_mapping', renamed_mapping),
	                ("distribution_report", distribution_report)] + locals().items()
	map(lambda name_val: setattr(maker_handler, name_val[0], name_val[1]), names_values)

	Mkdirs(configuration.workdir)
	download_bugs(bugsPath, configuration.issue_tracker_url, configuration.product_being_tracked,
	              configuration.issue_tracker_name)
	checkout_local_git(configuration.git_repo_path, configuration.workdir)
	versionsCreate(configuration.git_repo_path, vers, versPath)


def fix_renamed_file(file_name):
	return detect_renamed_files.fix_renamed_file(file_name, get_configuration().renamed_files)


def read_configuration(configuration_file_path):
	"""Read the configuration file and returns the object parsed.

	Args:
		configuration_file_path (str): the path to the configuration file.

	Note:
		The algorithm expects the configuration file to look as follows:
		{
			"workdir": <path to the working directory>
			"git_repo_path": <path to the cloned epository>
			"product_being_tracked": <name of the project ot handle>
			"issue_tracker_url": <url of the issue tracker system>
			"issue_tracker_name": <name of the issue tracker>
			"versions": <what versions to check>
		}

	Returns:
		AttrDict. the dictionary representing the configuration file.
	"""
	with open(configuration_file_path, "r") as conf:
		configuration = AttrDict(json.load(conf))

	return configuration


def version_to_dir_name(version):
	return version.replace("\\", "_").replace("/", "_").replace("-", "_").replace(".", "_")


def create_directory_if_not_exists(dir):
	if not os.path.isdir(dir):
		os.mkdir(dir)


def Mkdirs(workingDir):
	create_directory_if_not_exists(workingDir)
	map(lambda dir_name: create_directory_if_not_exists(os.path.join(workingDir, dir_name)),
	    ["", "vers", "experiments", "experiments_known",
	     "dbAdd", "testedVer", "weka", "web_prediction_results", "markers", "DebuggerTests"])
	versPath = os.path.join(workingDir, "vers")
	create_directory_if_not_exists(versPath)
	checkAll = os.path.join(versPath, "checkAll")
	create_directory_if_not_exists(checkAll)
	checkAllMethodsData = os.path.join(versPath, "checkAllMethodsData")
	create_directory_if_not_exists(checkAllMethodsData)
	for v in get_configuration().vers:
		version = os.path.join(versPath, version_to_dir_name(v))
		create_directory_if_not_exists(version)
		blame = os.path.join(version, "blame")
		create_directory_if_not_exists(blame)
		Jdoc2 = os.path.join(version, "Jdoc2")
		create_directory_if_not_exists(Jdoc2)
	return versPath


class Marker(object):
	def __init__(self, path, logger):
		self.marker_path = path
		self.logger = logger

	def is_done(self):
		if os.path.isfile(self.marker_path):
			with open(self.marker_path) as f:
				if "finish" in f.read():
					return True
		return False

	def start(self):
		with open(self.marker_path, "wb") as f:
			log_line = "start time: " + str(datetime.now()) + "\n"
			f.write(log_line)
			self.logger.debug('writing to %s: %s', self.marker_path, log_line)

	def error(self, error_msg):
		with open(self.marker_path, "ab") as f:
			f.write("failed\n")
			f.write("error msg : {0}\n".format(error_msg))
			self.logger.error("error msg : {0}\n".format(error_msg))

	def finish(self):
		with open(self.marker_path, "ab") as f:
			log_line = "finish time: " + str(datetime.now()) + "\n"
			f.write(log_line)
			self.logger.info('writing to %s: %s', self.marker_path, log_line)


class MarkerHandler(object):
	def __init__(self, workdir, versions, logger):
		self.markers_dir = os.path.join(workdir, "markers")
		self.versions = versions
		create_directory_if_not_exists(workdir)
		log_file_path = os.path.join(convert_to_long_path(workdir), "log.log")
		if os.path.exists(log_file_path):
			os.remove(log_file_path)

		self.logger = logger

	def get_marker_path(self, marker):
		return os.path.join(self.markers_dir, marker)

	def get_marker(self, marker):
		return Marker(self.get_marker_path(marker), self.logger)


def open_subprocess(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None,
                    preexec_fn=None,
                    close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False,
                    startupinfo=None, creationflags=0):
	logging.info('running new process with cmdline {0}'.format(" ".join(args)))
	return subprocess.Popen(args, bufsize=bufsize, executable=executable, stdin=stdin,
	                        stdout=stdout, stderr=stderr,
	                        preexec_fn=preexec_fn, close_fds=close_fds, shell=shell, cwd=cwd,
	                        env=env,
	                        universal_newlines=universal_newlines, startupinfo=startupinfo,
	                        creationflags=creationflags)


def init_configuration(workdir, versions, logger):
	global conf
	assert (conf is None)
	conf = MarkerHandler(workdir, versions, logger)


def get_configuration():
	return conf


def post_bug_to_github(etype, value, tb):
	# try to post bug to github
	try:
		gh = github3.login('DebuggerIssuesReport',
		                   password='DebuggerIssuesReport1')  # DebuggerIssuesReport@mail.com
		repo = gh.repository('BGU-AiDnD', 'Debugger')
		issue_body = "\n".join(["An Exception occurred while running Debugger:\n",
		                        "command line is {0}\n\n".format(" ".join(sys.argv))]) \
		             + "".join(['Traceback (most recent call last):\n'] + traceback.format_tb(
			tb) + traceback.format_exception_only(etype, value))
		issue = repo.create_issue(title='An Exception occurred : {0}'.format(value.message),
		                          body=issue_body, assignee='amir9979')
		configuration = get_configuration()
		issue.create_comment(
			body="Configuration is : \n" + "\n".join(map(str, configuration.__dict__.items())))
		with open(logging.root.handlers[0].baseFilename) as logger:
			issue.create_comment(body=logger.read())
	except:
		pass


@contextmanager
def use_sqllite(db_path):
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	yield conn
	conn.commit()
	conn.close()


def marker_decorator(marker):
	"""Run function if marker doesn't exists"""

	def decorator(func):
		def f(*args, **kwargs):
			ans = None
			if not get_configuration().get_marker(marker).is_done():
				get_configuration().get_marker(marker).start()
				try:
					ans = func(*args, **kwargs)
					get_configuration().get_marker(marker).finish()
				except Exception as e:
					get_configuration().get_marker(marker).error(e.message)
					etype, value, tb = sys.exc_info()
					traceback.print_exc()
					post_bug_to_github(etype, value, tb)
					raise
			return ans

		return f

	return decorator


DIRS_CACHE = ['weka', 'web_prediction_results', 'experiments', 'markers', 'configuration']


def get_from_cache():
	cache = get_configuration().caching_dir
	current_versions = get_configuration().versions
	for configuration_file_path in map(lambda d: os.path.join(cache, d, "configuration"),
	                                   os.listdir(cache)):
		if not os.path.exists(configuration_file_path):
			continue

		import ipdb;
		ipdb.set_trace()
		configuration = read_configuration(configuration_file_path)
		if configuration.versions == current_versions:
			return configuration_file_path

	return None


def copy_from_cache():
	config = get_from_cache()
	if config is None:
		return None
	for folder in DIRS_CACHE:
		copy(os.path.join(os.path.dirname(config), folder),
		     os.path.join(get_configuration().workingDir, folder))
	return config


def export_to_cache():
	dir_name = os.path.join(get_configuration().caching_dir,
	                        get_configuration().issue_tracker_product)
	create_directory_if_not_exists(dir_name)
	for folder in DIRS_CACHE:
		copy(os.path.join(get_configuration().workingDir, folder), os.path.join(dir_name, folder))
