import os
import subprocess

from utils.filesystem import convert_to_long_path, convert_to_short_path
from utilsConf import open_subprocess


class GitCloningManager(object):
	"""Manages all the actions related to git cloning."""

	def __init__(self, logger, configuration):
		self.logger = logger
		self.configuration = configuration

	def checkout_local_git(self):
		"""Clone the git path to a local repository."""
		run_commands = ["git", "clone", convert_to_long_path(self.configuration.gitPath), 'repo']
		proc = open_subprocess(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
		                       shell=True, cwd=convert_to_long_path(self.configuration.workingDir))
		proc.communicate()

	@staticmethod
	def version_to_dir_name(version):
		return version.replace("\\", "_").replace("/", "_").replace("-", "_").replace(".", "_")

	def copy_directories(self):
		"""Copy the repositories directory trees to the disk for a faster access."""
		for version in self.configuration.vers:
			path = os.path.join(self.configuration.versPath,
			                    self.version_to_dir_name(version), "repo")

			if not os.path.exists(path):
				run_commands = ["git", "clone", convert_to_short_path(self.configuration.gitPath),
				                'repo']

				proc = open_subprocess(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
				                       shell=True, cwd=convert_to_short_path(
					                       os.path.join(self.configuration.versPath,
					                                    self.version_to_dir_name(version))))
				proc.communicate()

	def run_cmd(self, path, args):
		run_commands = ["git", "-C", path] + args
		self.logger.debug("running the command: {}".format(run_commands))

		proc = open_subprocess(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
		                       shell=True)
		proc.communicate()

	def run_git_revert(self):
		for version in self.configuration.vers:
			repo_path = os.path.join(self.configuration.versPath,
			                         self.version_to_dir_name(version), "repo")
			self.run_cmd(repo_path, ["clean", "-fd", version])
			self.run_cmd(repo_path, ["checkout", '-f', version])
			self.run_cmd(repo_path, ["clean", "-fd", version])
