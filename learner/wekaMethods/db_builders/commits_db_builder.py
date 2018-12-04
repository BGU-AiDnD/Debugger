"""Module to build and handle the commits DB tables"""
import unicodedata
from datetime import datetime


class Commit(object):
	TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

	def __init__(self, commit_raw_object):
		""""""
		self.id = int("".join(list(commit_raw_object.hexsha)[:7]), 16)
		self.committed_date = datetime.fromtimestamp(commit_raw_object.committed_date).strftime(
			self.TIME_FORMAT)
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

	def get_bug_fix_commit_fields(self, bug):
		return (self.id, bug, self.committed_date,
		        self.committer, self.author_date, self.author,
		        self.lines, self.deletions, self.insertions,
		        self.files, self.size, self.parent, self.reach, self.commit_message,
		        self.hex_sha)

	def get_commit_files_data(self, bug):
		commits_files_data = []
		for file_name in self.files:
			data = (file_name.replace("/", "\\"), self.id, self.committed_date, self.deletions,
			        self.insertions, bug, self.hex_sha)
			commits_files_data.append(data)

		return commits_files_data

	@staticmethod
	def get_fixed_bug_num_from_commit_text(commit_text, bugs_ids):
		"""Get the ID of the bug that was fixed in this issue out of the known
			bugs given as input.

		Args:
			commit_text (str): the text of the commit containing the bug fix.
			bugs_ids (list): the bugs that were previously mapped.

		Returns:
			str. The FIXED bug that was fixed in the current commit out of the known
				bugs list.
		"""
		s = commit_text.lower().replace(":", "") \
			.replace("#", "").replace("-", " ").replace("_", " ").split()

		for word in s:
			if word.isdigit() and word in bugs_ids:
				return word
		return "0"
