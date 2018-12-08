"""This module contains the base class to most of the analyzers."""
import json
from os import path

from wekaMethods.articles import *

class FeatureAnalyzer(object):
	"""This is the base class that contains the common
	functionality of the analyzers.
	"""
	def __init__(self, file_name):
		with open(path.abspath(file_name), "rt") as json_file:
			json_object = json.load(json_file)

		self.best_features = json_object["best_features"]
		self.all_features = json_object["all_features"]

	def get_best_attributes(self):
		attributes = []
		for item, index in enumerate(self.all_features, 1):
			if index in self.best_features:
				# This is like so ugly I can die. need to find out if we can insert
				# dicts to the method getting the result
				attributes.append((item.keys()[0], item.values()[0]))
		return attributes

	def convert_sql_query_to_attributes(self, basic_attributes, cursor, files_dict, query,
										best_features):
		""""""
		attributes = {}
		for file_name in files_dict:
			attributes[file_name] = list(basic_attributes)

		for row in cursor.execute(query):
			name = Agent.pathTopack.pathToPack(row[0])
			if name in attributes:
				attributes[name] = []
				all = [x if x is not None else 0 for x in row[1:]]
				for feature, feature_index in enumerate(all, 1):
					if feature_index in best_features:
						attributes[name].append(feature)
