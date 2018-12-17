import wekaMethods.issuesExtract.csv_labels
import wekaMethods.issuesExtract.github_import
import wekaMethods.issuesExtract.google_code
import wekaMethods.issuesExtract.jira_import
import wekaMethods.issuesExtract.python_bugzilla
import wekaMethods.issuesExtract.sourceforge


class BugManager(object):
	"""Runs actions related to bugs issues."""

	ISSUE_TRACKERS_DICT = {
		"bugzilla": wekaMethods.issuesExtract.python_bugzilla.write_bugs_csv,
		"jira": wekaMethods.issuesExtract.jira_import.jiraIssues,
		"github": wekaMethods.issuesExtract.github_import.GithubIssues,
		"sourceforge": wekaMethods.issuesExtract.sourceforge.write_bugs_csv,
		"googlecode": wekaMethods.issuesExtract.google_code.write_bugs_csv,
		"csv_file": wekaMethods.issuesExtract.csv_labels.write_bugs_csv
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
