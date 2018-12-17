import datetime
import json
import os
import sys
import traceback

from attrdict import AttrDict

from utils.consts import GLOBAL_CONFIGURATION_FILE_PATH
from utils.post_bug_report import post_bug_to_github

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


def monitor(monitor_name):
	"""Decorator that runs the monitoring class on the monitored method."""

	def decorator(func):
		def decorated_method(*args, **kwargs):
			result = None
			# Here we assume that this instance was already initialized.
			monitor_manager = MonitorsManager()
			function_monitor = monitor_manager.get_monitor("{}_{}".format(monitor_name,
			                                                              func.__name__))

			if not function_monitor.is_done():
				function_monitor.start()
				try:
					result = func(*args, **kwargs)
					function_monitor.finish()

				except Exception as e:
					function_monitor.error(e.message)
					etype, value, tb = sys.exc_info()
					traceback.print_exc()
					post_bug_to_github(etype, value, tb, monitor_manager)
					raise

			return result
		return decorated_method
	return decorator


class Monitor(object):
	"""Monitor to follow and run a certain function. in any case the results of the
	run are being monitored and logged.

	The monitor file looks as follows:
		{
			"start_time": <start time>,
			"end_time": <end time>,
			"finished": True / False,
			"success": True / False,
			"error": <error message>
		}
	"""
	TIME_FORMAT = "%m/%d/%Y-%H:%M:%S"

	def __init__(self, path, logger):
		self.monitor_file_path = path
		self.logger = logger

	def is_done(self):
		if os.path.isfile(self.monitor_file_path):
			with open(self.monitor_file_path, 'rb') as monitor_file:
				monitor_data = AttrDict(json.load(monitor_file))
				return monitor_data.finished

	def start(self):
		"""Start the function monitoring."""
		with open(self.monitor_file_path, "wb") as monitor_file:
			start_time = datetime.datetime.now()
			self.logger.debug("Started monitoring at {}".format(start_time))
			monitor_data = {
				"start_time": start_time.strftime(self.TIME_FORMAT),
				"end_time": None,
				"finished": False,
				"success": False,
				"error": ""
			}
			json.dump(monitor_data, monitor_file)
			self.logger.debug('Done writing to %s', self.monitor_file_path)

	def _fetch_monitor_data(self):
		"""Get the data from the monitor file."""
		with open(self.monitor_file_path, "r") as monitor_file:
			monitor_data = AttrDict(json.load(monitor_file))
		return monitor_data

	def error(self, error_msg):
		"""Log the error to the monitor file and to the log."""
		monitor_data = self._fetch_monitor_data()

		with open(self.monitor_file_path, "wb") as monitor_file:
			end_time = datetime.datetime.now()
			monitor_data.end_time = end_time.strftime(self.TIME_FORMAT)
			monitor_data.finished = True
			monitor_data.success = False
			monitor_data.error = error_msg
			json.dump(monitor_data, monitor_file)
			self.logger.error("an error was raised.\n {0}\n".format(error_msg))

	def finish(self):
		"""Notify the monitor file that the function run had finished"""
		monitor_data = self._fetch_monitor_data()

		with open(self.monitor_file_path, "wb") as monitor_file:
			end_time = datetime.datetime.now().strftime(self.TIME_FORMAT)
			monitor_data.end_time = end_time
			monitor_data.finished = True
			monitor_data.success = True
			monitor_data.error = ""
			json.dump(monitor_data, monitor_file)
			self.logger.info('Done function run %s. Writing to %s', end_time,
			                 self.monitor_file_path)


class Singleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]


class MonitorsManager(object):
	"""Singelton class that """

	__metaclass__ = Singleton

	def __init__(self, logger=None):
		"""Initialize the class.

		Notice:
			This __new__ enables the calling without params. you should ONLY do
			this AFTER the first initialization!
		"""
		self.logger = logger

	def get_monitor(self, monitor_name):
		with open(GLOBAL_CONFIGURATION_FILE_PATH, 'rb') as configuration_file:
			configurations = json.load(configuration_file)
			monitors_dir = configurations["monitors_dir"]

		return Monitor(os.path.join(monitors_dir, monitor_name), self.logger)
