import git

from feature_engineering.db_builder import DBBuilder
from feature_engineering.db_builders.bugs_db_builder import parse_bugs_data


class CSharpDBBuilder(DBBuilder):
	"""Class to build all the tables related to C# applications."""

	def __init__(self, configuration):
		super(CSharpDBBuilder, self).__init__(configuration)

	def build_all_versions_db(self):
		"""Build the versions DB."""
		repo = git.Repo(self.configuration.git_repo_path)
		all_bugs, bugs_ids = parse_bugs_data(self.configuration.bugs_path)
