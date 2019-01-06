import os
import subprocess
from httplib import OK
from itertools import izip
from math import ceil

import requests
from attrdict import AttrDict


class SonarQube(object):
	"""Class to handle the functionality related to the sonarqube tool."""

	DEFAULT_PAGE_SIZE = 500.0
	CODE_SMELL_RULE_TYPE = "CODE_SMELL"

	INSPECTION_RESULT_ISSUES_URL = "http://localhost:9000/api/issues/search?ps=500&p={page}"
	INSPECTION_RESULT_LINE = ("{file_name},{issue_line_number},{issue_message},"
	                          "{issue_severity},{issue_type},{issue_start_offset},"
	                          "{issue_end_offset}")
	INSPECTION_FILE_TITLES = "FILE_NAME,LINE_NUMBER,MESSAGE,SEVERITY,ISSUE_TYPE,START_OFFSET," \
	                         "END_OFFSET"

	def __init__(self, configuration, logger):
		self.nuget = "D:\\School\\Thesis\\nuget\\nuget.exe"
		self.msbuild = "C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\MSBuild.exe"
		self.sonarqube_proc = "D:\\School\\Thesis\\sonar-scanner-msbuild-4.5.0.1761-net46" \
		                      "\\SonarScanner.MSBuild.exe"

		self.configuration = configuration
		self.logger = logger
		self.version_dir_path = None

	def build_project(self):
		"""Build the src project."""
		# Ensure msbuild exists
		if not os.path.isfile(self.msbuild):
			raise Exception('MsBuild.exe not found. path=' + self.msbuild)

		# restore nuget dependencies
		self.logger.debug("restoring NuGet dependencies")
		subprocess.call([self.nuget, "restore"], cwd=self.version_dir_path)
		# Clean the project
		self.logger.debug("Cleaning project directory")
		subprocess.call([self.msbuild, "/t:restore"], cwd=self.version_dir_path)
		# Build fresh after clean
		self.logger.debug("Building the project version")
		subprocess.call([self.msbuild, "/t:Rebuild"], cwd=self.version_dir_path)

	def create_inspection_requirements(self, version):
		"""Running the SonarSanner startup process."""
		subprocess.call([self.sonarqube_proc, "begin",
		                 "/k:project_analyze_{project_name}_{version_num}".format(
			                 project_name=self.configuration.issue_tracker_product,
			                 version_num=version),
		                 "/v:\"{version_num}\"".format(version_num=version)],
		                cwd=self.version_dir_path)

	def execute_version_inspection(self):
		"""Execute an inspection on a single version of the source code."""
		# End the inspection and create the output report
		self.logger.debug("Creating the report after the version build")
		subprocess.call([self.sonarqube_proc, "end"], cwd=self.version_dir_path)

	def parse_issue(self, analysis_result, issue):
		"""Parse single issue and appends it to the result list."""
		file_name = issue.component.split(":")[-1]
		issue_line_number = issue.line
		issue_message = issue.message
		issue_severity = issue.severity
		issue_type = issue.textRange.type
		issue_start_offset = issue.testRange.startOffset
		issue_end_offset = issue.testRange.endOffset
		analysis_result.append(
			self.INSPECTION_RESULT_ISSUES_URL.format(file_name=file_name,
			                                         issue_line_number=issue_line_number,
			                                         issue_message=issue_message,
			                                         issue_severity=issue_severity,
			                                         issue_type=issue_type,
			                                         issue_start_offset=issue_start_offset,
			                                         issue_end_offset=issue_end_offset))

	def parse_page(self, analysis_result, page_index):
		response = requests.get(self.INSPECTION_RESULT_ISSUES_URL.format(page=page_index))
		if response is not OK:
			raise ValueError("Cannot fetch inspection result from the server")
		inspection = AttrDict(response.json())
		for issue in inspection.issues:
			self.parse_issue(analysis_result, issue)

	def parse_inspection(self):
		"""Parses the inspection result"""
		response = requests.get(self.INSPECTION_RESULT_ISSUES_URL.format(page=1))
		if response is not OK:
			raise ValueError("Cannot fetch inspection result from the server")

		inspection = AttrDict(response.json())
		# The results are returned in pages, in order for the app to get all the issues,
		# need to go through the pages.
		file_name = "{}_analysis_result.csv".format(self.configuration.issue_tracker_product)
		analysis_file_path = os.path.join(self.configuration.workingDir, file_name)
		with open(analysis_file_path, "w") as analysis_result_file:
			analysis_result = []
			total_issues_num = inspection.total  # returns the number of issues
			total_pages = ceil(total_issues_num / self.DEFAULT_PAGE_SIZE)

			# parse the first page.
			self.parse_page(analysis_result, 1)

			for page_index in xrange(2, total_pages + 1):
				self.parse_page(analysis_result, page_index)

			analysis_result_file.write(self.INSPECTION_FILE_TITLES)
			analysis_result_file.writelines(analysis_result)

	def inspect_versions(self):
		"""Create the analysis report for every version tested in the project."""
		# Run on every version of the project and create an analysis
		for version_path, version_key in izip(self.configuration.vers_paths,
		                                      self.configuration.vers):
			self.version_dir_path = os.path.join(version_path, "repo")
			self.logger.info("Inspecting the version - %s", version_key)
			self.create_inspection_requirements(version_key)
			self.build_project()
			self.parse_inspection()
