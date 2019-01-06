"""Module to get all the blames for each of the issues found in the code."""


class Blame(object):
	"""Manage the acquisition of the blame data and its usage."""

	GITHUB_QUERY_DICT = {
		'query': '{ repository(name: "{repo_na,e}", owner: "{owner}") {'
		         ' ref(qualifiedName:"{branch_name}") {'
		         'target { ... on Commit { blame(path:"{file_path}") {'
		         'ranges { commit { author { name } }'
              'startingLine\n endingLine\n age } } } } } } }'
	}

	# This will run git blame only on the requested line
	GIT_BLAME_COMMAND = ["git", "blame", "-L"]

	def __init__(self, configuration, api_token_path=None):
		self.configuration = configuration
		if api_token_path is None:
			self.api_token_path = "D:\\School\\Thesis\\github_token.txt"

		else:
			self.api_token_path = api_token_path

	def request_issue_blame_data(self, issue_path, branch_name, line_num):
		"""Get the blame data of a single issue found in the scan.

		Args:
			issue_path (str): path to the issued source file.
			branch_name (str): the name of the branch to search the issue in.
			line_num (number): the line to search for blame data in the results.

		Returns:
			str. The name of the user that committed the issue.
		"""
