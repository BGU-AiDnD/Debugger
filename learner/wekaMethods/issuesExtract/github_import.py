__author__ = 'amir'
import github3
import csv
import unicodedata
import datetime




#ID	Product	Component	Assigned To	Status	Resolution	Reporter	Last Modified	Version	Milestone	Hardware	OS	Priority	Severity	Summary	Keywords	Submit Date	Blocks	Depends On	Duplicate Of	CC
def issueAnalyze(issue,product,component):
    Id=str(issue.id)
    Product=str(product)
    Component=str(component)
    Assigned_To=str(issue.assignee)
    Status=str(issue.state)
    Resolution=""
    Reporter=str(issue.user)
    Last_Modified=str(issue.updated_at)
    print Last_Modified
    Last_Modified=datetime.datetime.strptime(Last_Modified,'%Y-%m-%d').date().strftime("%d/%m/%y")
    Version=""
    Milestone=str(issue.milestone)
    Hardware=""
    OS=""
    Priority=""
    Severity=""
    Summary=str(issue.body)
    Keywords=str(dict["keywords"])
    Submit_Date=str(issue.created_at)
    print Submit_Date
    Submit_Date=datetime.datetime.strptime(Submit_Date,'%Y-%m-%d').date().strftime("%d/%m/%y")
    Blocks=""
    Depends_On=""
    Duplicate_Of=""#,".join([v.name for v in issue.fields.issuelinks])
    CC=str(dict["cc"])
    return [Id,Product,Component,Assigned_To,Status,Resolution,Reporter,Last_Modified,Version,Milestone,Hardware,OS,Priority,Severity,Summary,Keywords,Submit_Date,Blocks,Depends_On,Duplicate_Of,CC]


def GithubIssues(url,owner,repo,outFile):
    gh=github3.GitHub()
    lines=[["ID","Product","Component","Assigned To","Status","Resolution","Reporter","Last Modified","Version","Milestone","Hardware","OS","Priority","Severity","Summary","Keywords","Submit Date","Blocks","Depends On","Duplicate Of","CC"]]
    allIssues= gh.iter_repo_issues(owner,repo)
    print(len(allIssues))
    for issue in allIssues:
        analyze = issueAnalyze(issue,repo,repo)
        lines.append(analyze)
    f=open(outFile,"wb")
    writer=csv.writer(f)
    writer.writerows(lines)
    f.close()

"""

gh=github3.GitHub()
issues= gh.iter_repo_issues("PyGithub","PyGithub",state="all")
iss= [x for x in issues]
print len(iss)
isu=iss[6]
print isu.state
print isu.labels
print isu.body
print isu.repository
print isu.user
print [str(x.labels) for x in issues]
print isu.title
print isu.state
exit()
gh = login(user, pw)
issue = gh.issue(user, repo, num)
if issue.is_closed():
    issue.reopen()

issue.edit('New issue title', issue.body + '\n------\n**Update:** Text to append')
"""