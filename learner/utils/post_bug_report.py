import logging
import sys
import traceback

import github3


ERROR_HEADLINE = ("An Exception occurred while running Debugger:\n"
                  "The input typed to the CMD is: {cmd_input}\n"
                  "Raised the traceback:\n {traceback}")

def post_bug_to_github(error_type, value, input_traceback, monitor_manager):
	"""Post a bug report to Github when an exception is raised.

	Args:
		error_type (str):
		value (str):
		input_traceback (str):
		monitor_manager (MarkerHandler):
	"""
	# try to post bug to github
	try:
		# DebuggerIssuesReport@mail.com - login to github
		github_session = github3.login('DebuggerIssuesReport',
		                               password='DebuggerIssuesReport1')
		repo = github_session.repository('BGU-AiDnD', 'Debugger')

		command_line_args = " ".join(sys.argv)
		error_raised = traceback.format_tb(input_traceback) + \
		               traceback.format_exception_only(error_type, value)
		issue_body = ERROR_HEADLINE.format(cmd_input=command_line_args,
		                                   traceback=error_raised)

		issue = repo.create_issue(title='An Exception occurred: {}'.format(value.message),
		                          body=issue_body, assignee='amir9979')
		issue.create_comment(
			body="Configuration is : \n" + "\n".join(map(str,
			                                             monitor_manager.__dict__.items())))

		with open(logging.root.handlers[0].baseFilename) as logger:
			issue.create_comment(body=logger.read())

	except Exception:
		pass    # TODO: add a log line to mention that the action failed.
