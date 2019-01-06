import datetime
import json
import logging
import os
import sqlite3
import subprocess
from contextlib import contextmanager
from datetime import datetime

import git
from attrdict import AttrDict

from utils.consts import GLOBAL_CONFIGURATION_FILE_PATH
from utils.filesystem import convert_to_long_path, create_directory_if_not_exists

current_dir = os.path.dirname(os.path.realpath(__file__))
utilsPath = os.path.realpath(os.path.join(current_dir, "../utils"))
docletPath = os.path.join(utilsPath, "xml-doclet-1.0.4-jar-with-dependencies.jar")
source_monitor_exe_path = os.path.join(utilsPath, "SourceMonitor.exe")
checkStyle57 = os.path.join(utilsPath, "checkstyle-5.7-all.jar")
checkStyle68 = os.path.join(utilsPath, "checkstyle-6.8-SNAPSHOT-all.jar")
all_checks_xml_path = os.path.join(utilsPath, "allChecks.xml")
methods_names_xml_path = os.path.join(utilsPath, "methodNameLines.xml")
wekaJar = os.path.join(utilsPath, "weka.jar")
RemoveBat = os.path.join(utilsPath, "../removeBat.bat")
caching_dir = os.path.realpath(os.path.join(current_dir, "../Debugger_cache"))
amir_tracer = os.path.join(utilsPath, "uber-tracer-1.0.1-SNAPSHOT.jar")
DEBUGGER_BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def versions_info(repository_path, versions):
	repo = git.Repo(repository_path)
	if len(versions) == 0:
		requested_commits = [x.commit for x in repo.tags]
		versions = repo.tags

	else:
		requested_commits = [x.commit for x in repo.tags if x.name in versions]
		if not requested_commits:
			requested_commits = filter(lambda c: c.hexsha in versions, repo.iter_commits())
	commits = [int("".join(list(x.hexsha)[:7]), 16) for x in requested_commits]
	dates = [datetime.fromtimestamp(x.committed_date).strftime('%Y-%m-%d %H:%M:%S') for x in
	         requested_commits]
	paths = [os.path.join(ver, "repo") for ver in versions]
	return AttrDict({
		"versions": versions,
		"paths": paths,
		"dates": dates,
		"commits": commits
	})


def git_file_path_to_java_name(file_path):
	directories = os.path.splitext(os.path.normpath(file_path))[0].split(os.path.sep)
	index = 0
	if 'java' in directories:
		index = directories.index('java') + 1
	elif 'src' in directories:
		index = directories.index('src') + 2
	return ".".join(directories[index:])


def create_global_configuration(configuration, prediction_files):
	"""Creates a global configuration file that the entire application would be able to use"""
	workdir = configuration.workdir
	version_info = versions_info(convert_to_long_path(configuration.git_repo_path),
	                             configuration.versions)

	version_dirs = map(version_to_dir_name, version_info.versions)
	committed_files_dir_name = os.path.join(workdir, "commitsFiles")
	local_git_path = convert_to_long_path(os.path.join(configuration.workdir, "repo"))
	create_directory_if_not_exists(local_git_path)
	versions_directory_path = os.path.join(workdir, "vers")

	return AttrDict({
		"versions_dir_path": versions_directory_path,
		"db_dir": os.path.join(workdir, "db_address"),
		"vers": version_info.versions,
		"paths": version_info.paths,
		"dates": version_info.dates,
		"commits": version_info.commits,
		"docletPath": docletPath,
		"source_monitor_exe_path": source_monitor_exe_path,
		"checkStyle57": checkStyle57,
		"checkStyle68": checkStyle68,
		"all_checks_xml_path": all_checks_xml_path,
		"methods_names_xml_path": methods_names_xml_path,
		"wekaJar": wekaJar,
		"RemoveBat": RemoveBat,
		"utilsPath": utilsPath,
		"versions": configuration.versions,
		"git_repo_path": configuration.git_repo_path,
		"issue_tracker": configuration.issue_tracker_name,
		"issue_tracker_url": configuration.issue_tracker_url,
		"issue_tracker_product": configuration.product_being_tracked,
		"workingDir": workdir,
		"bugsPath": os.path.join(workdir, "bugs.csv"),
		"vers_dirs": version_dirs,
		"vers_paths": map(lambda ver: os.path.join(versions_directory_path, ver), version_dirs),
		"LocalGitPath": local_git_path,
		"weka_path": convert_to_long_path(os.path.join(workdir, "weka")),
		"MethodsParsed": convert_to_long_path(os.path.join(committed_files_dir_name,
		                                                   "CheckStyle.txt")),
		"changeFile": convert_to_long_path(os.path.join(committed_files_dir_name, "Ins_dels.txt")),
		"debugger_base_path": DEBUGGER_BASE_PATH,
		"web_prediction_results": convert_to_long_path(os.path.join(workdir,
		                                                            "web_prediction_results")),
		"amir_tracer": amir_tracer,
		"configuration_path": convert_to_long_path(os.path.join(workdir, "configuration.json")),
		"caching_dir": caching_dir,
		"DebuggerTests": convert_to_long_path(os.path.join(workdir, "DebuggerTests")),
		"prediction_files": prediction_files,
		"experiments": convert_to_long_path(os.path.join(configuration.workdir, "experiments")),
		"monitors_dir": os.path.join(workdir, "markers")
	})


def configure(basic_config, logger):
	logger.info("Starting to configure the basic requirements to run the algorithm")

	create_directory_if_not_exists(basic_config.workdir)
	prediction_files = {
		'files': {'all': 'prediction_All_files.csv', 'most': 'prediction_Most_files.csv'},
		'methods': {'all': 'prediction_All_methods.csv', 'most': 'prediction_Most_methods.csv'}}

	logger.info("Creating the configuration object that the application uses.")
	configuration_object = create_global_configuration(basic_config, prediction_files)

	with open(GLOBAL_CONFIGURATION_FILE_PATH, 'wb') as configuration_file:
		json.dump(configuration_object, configuration_file)

	buggy_repo = git.Repo(convert_to_long_path(basic_config.git_repo_path))
	buggy_repo.close()
	try:
		repo = git.Repo(DEBUGGER_BASE_PATH)
		debugger_commit = str(repo.head.commit)
		logging.info('Debugger HEAD is on commit {0}'.format(debugger_commit))
		repo.close()

	except Exception as e:
		logger.error("An exception was raised.\n {}".format(e.message))

	create_working_directory_tree(configuration_object)


def version_to_dir_name(version):
	return version.replace("\\", "_").replace("/", "_").replace("-", "_").replace(".", "_")


def create_working_directory_tree(configuration):
	work_dir = configuration.workingDir
	create_directory_if_not_exists(work_dir)
	map(lambda dir_name: create_directory_if_not_exists(os.path.join(work_dir, dir_name)),
	    ["", "vers", "experiments", "experiments_known",
	     "db_address", "testedVer", "weka", "web_prediction_results", "markers", "DebuggerTests"])
	vers_path = os.path.join(work_dir, "vers")
	create_directory_if_not_exists(vers_path)

	check_all_dir_name = os.path.join(vers_path, "checkAll")
	create_directory_if_not_exists(check_all_dir_name)

	check_all_methods_data_dir_name = os.path.join(vers_path, "checkAllMethodsData")
	create_directory_if_not_exists(check_all_methods_data_dir_name)

	for version in configuration.vers:
		version = os.path.join(vers_path, version_to_dir_name(version))
		create_directory_if_not_exists(version)
		create_directory_if_not_exists(os.path.join(version, "blame"))
		create_directory_if_not_exists(os.path.join(version, "Jdoc2"))


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


@contextmanager
def use_sqllite(db_path):
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	yield conn
	conn.commit()
	conn.close()
