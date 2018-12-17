import os
import shutil

import wekaMethods.articles
import wekaMethods.commsSpaces
from utils.monitors_manager import monitor, LEARNER_PHASE_FILE, VERSION_TEST_MARKER, FEATURES_MARKER, \
	ML_MODELS_MARKER
from wekaMethods import patchsBuild
from wekaMethods.db_builders import buildDB
from wekaMethods.features import complexity_features
from wekaMethods.features.features_extractor import extract_object_oriented_features_old


class FaultPredictorLearner(object):
	"""Handle all the Fault prediction related actions."""

	def __init__(self, logger, programming_language, configuration):
		self.logger = logger
		self.programming_language = programming_language
		self.configuration = configuration

	@monitor(ML_MODELS_MARKER)
	def create_build_machine_learning_model(self):
		for granularity in ['File', 'Method']:
			for buggedType in ["All", "Most"]:
				wekaMethods.articles.get_features(granularity, buggedType, self.configuration)

	@monitor(FEATURES_MARKER)
	def extract_features(self):
		"""Running the features extraction function."""
		self.logger.info("Extracting the complexity features from the versions.")
		complexity_features.extract_complexity_features(self.configuration)
		self.logger.info("extracting object oriented features")
		extract_object_oriented_features_old(self.configuration)
		wekaMethods.commsSpaces.create(self.configuration.vers_dirs,
		                               os.path.join(self.configuration.workingDir, "vers"))

	@monitor(VERSION_TEST_MARKER)
	def create_test_versions_tree(self):
		"""Creating the tested versions workdir directory tree"""
		src = os.path.join(self.configuration.workingDir, "vers",
		                   self.configuration.vers_dirs[-2], "repo")
		dst = os.path.join(self.configuration.workingDir, "testedVer", "repo")
		if not os.path.exists(dst):
			shutil.copytree(src, dst)

	@monitor(LEARNER_PHASE_FILE)
	def run_learner_algorithm(self):
		"""Run the fault prediction learning algorithm."""
		patchsBuild.PatchesBuilder(self.configuration, self.logger).labeling()
		buildDB.build_labels(self.configuration)
		self.create_test_versions_tree()
		self.extract_features()
		buildDB.buildOneTimeCommits(self.configuration)
		self.create_build_machine_learning_model()
