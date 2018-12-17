"""Module to handle all the cache directory actions."""


import os

from utils.filesystem import copy, create_directory_if_not_exists

CACHE_DIRS = ['weka', 'web_prediction_results', 'experiments', 'markers', 'configuration']

class DiskCache(object):
	"""Handle all the IO actions to the local folders containing the repositories caches."""

	def __init__(self, marker_handler):
		self.marker_handler = marker_handler

	def load_cache_directory_data(self):
		"""Loads the data from the cache directory in the local computer."""
		cache = self.marker_handler.caching_dir
		current_versions = self.marker_handler.versions
		config_dirs_data = map(lambda config_dir: os.path.join(
			cache, config_dir, "configuration"), os.listdir(cache))

		for configuration_file_path in config_dirs_data:
			if not os.path.exists(configuration_file_path):
				continue

			return configuration_file_path

	def copy_cache_directory_data(self):
		"""Copies the data to the local cache directory."""
		config = self.load_cache_directory_data()
		for folder in CACHE_DIRS:
			input_folder_path = os.path.join(os.path.dirname(config), folder)
			output_folder_path = os.path.join(self.marker_handler.workingDir, folder)
			if os.path.exists(input_folder_path):
				copy(input_folder_path, output_folder_path)

		return config


	def export_to_cache(self):
		"""Export the data to the local cache directory."""
		dir_name = os.path.join(self.marker_handler.caching_dir,
		                        self.marker_handler.issue_tracker_product)
		create_directory_if_not_exists(dir_name)
		for folder in CACHE_DIRS:
			copy(os.path.join(self.marker_handler.workingDir, folder),
			     os.path.join(dir_name, folder))
