"""Module to build and handle the commits DB tables"""
import unicodedata
from datetime import datetime


class Commit(object):
	"""Class that represents the content of a bug-fix commit and all it's relevant data."""
	TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

	def __init__(self, commit_raw_object, bug_id):
		"""Initialize the class.

		Args:
			commit_raw_object (object): the object containing the raw un-parsed data of the commit.
			bug_id (str): the id of the bug that was fixed in the commit.
		"""
		self.id = int("".join(list(commit_raw_object.hexsha)[:7]), 16)
		if hasattr(commit_raw_object, 'committed_date'):
			self.committed_date = datetime.fromtimestamp(
				commit_raw_object.committed_date).strftime(self.TIME_FORMAT)
		else:
			self.committed_date = None
		self.author_date = datetime.fromtimestamp(commit_raw_object.authored_date).strftime(
			self.TIME_FORMAT)
		commiter_name = unicodedata.normalize('NFKD', commit_raw_object.committer.name).encode(
			'ascii',
			'ignore')
		self.committer = str(commiter_name)
		self.author = str(commit_raw_object.author.name.encode('ascii', 'ignore'))
		if len(commit_raw_object.parents) != 0:
			self.parent = int("".join(list(commit_raw_object.parents[0].hexsha)[:7]), 16)

		self.commit_message = commit_raw_object.message
		self.commit_size = commit_raw_object.size
		self.reach = commit_raw_object.count()
		stats = commit_raw_object.stats
		all_stats = stats.total
		self.deletions = all_stats["deletions"]
		self.commit_lines = all_stats["lines"]
		self.insertions = all_stats["insertions"]
		self.files = all_stats["files"]
		self.hex_sha = str(commit_raw_object.hexsha)
		self.bug_id = bug_id

	def get_commit_to_bug_relation_data(self):
		"""Gets the minimal data needed to connect between a commit and a bug fix.

		Returns:
			tuple. The relevant data to connect  certain commit to it's relevant bug.
		"""
		return self.bug_id, self.committed_date, self.hex_sha, str(self.id)

	def get_bug_fix_commit_fields(self):
		""""""
		return (self.id, self.bug_id, self.committed_date, self.committer, self.author_date,
			self.author, self.commit_lines, self.deletions, self.insertions, self.files,
			self.commit_size, self.parent, self.reach, self.commit_message, self.hex_sha)

	def get_commit_files_data(self):
		commits_files_data = []
		for file_name in self.files:
			data = (file_name.replace("/", "\\"), self.id, self.committed_date, self.deletions,
					self.insertions, self.bug_id, self.hex_sha)
			commits_files_data.append(data)

		return commits_files_data


class CommitTable(object):
	"""Class to handle the collection of the data relevant to the commit table."""

	def __init__(self, repository, bug_ids):
		# NOTICE: this is currently working with Git only.
		self.commits = []
		for commit_object in repository.iter_commits():
			cleaned_commit_text = self._clean_commit_message(commit_object.message)
			self.commits.append(Commit(commit_object,
						self._get_fixed_bug_num_from_commit_text(cleaned_commit_text, bug_ids)))

		self.bug_ids = bug_ids

	@staticmethod
	def _clean_commit_message(commit_message):
		"""Clean the commit message from redundant information that appears in Git.

		Args:
			commit_message (str): the commit message fetched from Git.

		Returns:
			str. The filtered commit message.
		"""
		if "git-svn-id" in commit_message:
			return commit_message.split("git-svn-id")[0]

		return commit_message

	@staticmethod
	def _get_fixed_bug_num_from_commit_text(commit_text, bugs_ids):
		"""Get the ID of the bug that was fixed in this issue out of the known
			bugs given as input.

		Args:
			commit_text (str): the text of the commit containing the bug fix.
			bugs_ids (list): the bugs that were previously mapped.

		Returns:
			number. The FIXED bug that was fixed in the current commit out of the known
				bugs list.
		"""
		parsed_commit_text = commit_text.lower().replace(":", "") \
			.replace("#", "").replace("-", " ").replace("_", " ").split()

		for word in parsed_commit_text:
			if word.isdigit() and word in bugs_ids:
				return word

		return "0"

	def collect_commit_table_data(self, stop_iteration_index):
		"""Collect all the relevant data n order to create a Commits table.

		Args:
			stop_iteration_index (number): the index of the iteration to stop the
				run.

		Returns:
			tuple. All the data needed to create a commits table.
		"""
		all_commits = []
		all_files = []
		commits_bugs_dict = {}

		for index, commit_object in enumerate(self.commits, 1):
			if index == stop_iteration_index:
				break

			fields = commit_object.get_bug_fix_commit_fields()
			commits_bugs_dict[commit_object.hex_sha] = \
				commit_object.get_commit_to_bug_relation_data()
			all_commits.append(fields)
			commit_files_data = commit_object.get_commit_files_data()
			all_files += commit_files_data

		return all_commits, all_files, commits_bugs_dict

	def collect_light_commit_table_data(self):
		"""Collect all the relevant data n order to create a Commits table.

		Returns:
			tuple. A lighter data tuple for the table creation.
		"""
		all_commits = []
		commits_to_bugs_dict = {}
		for commit in self.commits:
			if commit.committed_date is None:
				continue

			all_commits.append(commit.get_bug_fix_commit_fields())
			commits_to_bugs_dict[commit.hex_sha] = commit.get_commit_to_bug_relation_data()
		return all_commits, commits_to_bugs_dict
