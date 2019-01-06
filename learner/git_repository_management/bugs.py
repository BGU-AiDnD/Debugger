import feature_engineering.issuesExtract.csv_labels
import feature_engineering.issuesExtract.github_import
import feature_engineering.issuesExtract.google_code
import feature_engineering.issuesExtract.jira_import
import feature_engineering.issuesExtract.python_bugzilla
import feature_engineering.issuesExtract.sourceforge


class BugManager(object):
	"""Runs actions related to bugs issues."""

	ISSUE_TRACKERS_DICT = {
		"bugzilla": feature_engineering.issuesExtract.python_bugzilla.write_bugs_csv,
		"jira": feature_engineering.issuesExtract.jira_import.jiraIssues,
		"github": feature_engineering.issuesExtract.github_import.GithubIssues,
		"sourceforge": feature_engineering.issuesExtract.sourceforge.write_bugs_csv,
		"googlecode": feature_engineering.issuesExtract.google_code.write_bugs_csv,
		"csv_file": feature_engineering.issuesExtract.csv_labels.write_bugs_csv
	}

	def __init__(self, logger, configuration):
		self.logger = logger
		self.configuration = configuration

	def download_bugs(self):
		"""Download the bugs from the appropriate location."""
		self.logger.info("Downloading the bugs from the remote repository")
		self.ISSUE_TRACKERS_DICT[self.configuration.issue_tracker](
			self.configuration.bugsPath, self.configuration.issue_tracker_url,
			self.configuration.issue_tracker_product)
