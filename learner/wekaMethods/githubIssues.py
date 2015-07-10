__author__ = 'amir'

from github import Github

g = Github()

from github3 import login
import github3

gh = login()
g = github3.GitHub('foo', 'bar')
print g
issues = [x for x in gh.iter_issues()]
print issues



