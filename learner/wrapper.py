"""Wrapper for the LDP algorithm.

Usage:
    wrapper.py <config_path> <language>
    wrapper.py <config_path> <language> learn
    wrapper.py <config_path> experiments

This is an algorithm to enhance the process of troubleshooting by learning the source code and then
predicting where bugs might occur.

The process learns the code, then runs a diagnosis on the code based on the previous versions of the
project. It learns where bugs had happened and thus creates an analysis of where they might occur
in the newer versions.

The third part is that the code suggests the user to create more tests if the diagnosis is not
accurate enough.

Options:
    -h --help
"""
import csv
import json
import logging
import shutil
import sys

import coloredlogs
from attrdict import AttrDict
from docopt import docopt

import utilsConf
from diagnosis_runner import DiagnosisRunner
from fault_prediction import FaultPredictorLearner
from git_repository_management.bugs import BugManager
from git_repository_management.git_repository import GitCloningManager
from utils.monitors_manager import monitor, ALL_DONE_FILE, MonitorsManager
from utils.consts import GLOBAL_CONFIGURATION_FILE_PATH
from utils.local_cache import DiskCache


class LearnerDiagnoserRunner(object):
	"""Class to manage the run of the application's algorithm."""

	def __init__(self, programming_language, logger):
		self.configuration = None
		self.cache = None
		self.logger = logger
		self.programing_language = programming_language
		self.learner = None
		self.diagnosis_runner = None

	@monitor(ALL_DONE_FILE)
	def run_all(self):
		""""""
		self.learner.run_learner_algorithm()
		self.diagnosis_runner.create_experiment(self.diagnosis_runner.execute_tests())

	def clean(self):
		"""Cleans the working directory once the run finishes"""
		self.logger.info("Cleaning the created paths to clean your computer")
		shutil.rmtree(self.configuration.versPath, ignore_errors=True)
		shutil.rmtree(self.configuration.LocalGitPath, ignore_errors=True)

	@staticmethod
	def parse_configuration_file(configuration_file_path):
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
		with open(configuration_file_path, "r") as conf_file:
			configuration = AttrDict(json.load(conf_file))

		return configuration

	def start_nlp_run(self, is_learning, is_experimenting):
		"""Parse the user's input and runs the appropriate algorithm."""
		if not is_experimenting and not is_learning:
			self.logger.info("Running both learning & experimenting")
			self.run_all()
			self.cache.export_to_cache()

		elif is_learning:
			self.logger.info("Running the **learning** algorithm")
			self.learner.run_learner_algorithm()

		elif is_experimenting:
			print "Feature not completed yet."

	def setup_running_configurations(self, config_file_path):
		"""Set up the relevant configurations for the running of the algorithm."""
		MonitorsManager(logger)
		utilsConf.configure(self.parse_configuration_file(config_file_path), logger)
		with open(GLOBAL_CONFIGURATION_FILE_PATH, 'rb') as configuration_file:
			configurations_json = json.load(configuration_file)

		self.configuration = AttrDict(configurations_json)
		self.learner = FaultPredictorLearner(self.logger, self.programing_language,
		                                     self.configuration)
		self.diagnosis_runner = DiagnosisRunner(self.logger, self.configuration)
		BugManager(self.logger, self.configuration).download_bugs()

		git_manager = GitCloningManager(self.logger, self.configuration)
		git_manager.checkout_local_git()
		git_manager.copy_directories()
		git_manager.run_git_revert()

		self.cache = DiskCache(self.configuration)


if __name__ == '__main__':
	csv.field_size_limit(sys.maxint)
	arguments = docopt(__doc__)
	config_file_path = arguments['<config_path>']
	programing_language = arguments['<language>']
	is_learning = arguments['learn']
	is_experimenting = arguments['experiments']

	logger = logging.getLogger("nlp_logger")
	coloredlogs.install(level='DEBUG')
	coloredlogs.install(level='DEBUG', logger=logger)

	ldp_algorithm_object = LearnerDiagnoserRunner(programing_language, logger)
	ldp_algorithm_object.setup_running_configurations(config_file_path)
	ldp_algorithm_object.start_nlp_run(is_learning, is_experimenting)
	ldp_algorithm_object.clean()
