__author__ = 'amir'
import github3
import csv
import unicodedata
import datetime




#ID	Product	Component	Assigned To	Status	Resolution	Reporter	Last Modified	Version	Milestone	Hardware	OS	Priority	Severity	Summary	Keywords	Submit Date	Blocks	Depends On	Duplicate Of	CC
def issueAnalyze(issue,product,component):
    def nice_time(time):
        return datetime.datetime.strptime(time, '%Y-%m-%d').date().strftime('%d/%m/%Y %H:%M:%S')
    Id=str(issue.number)
    Product=str(product)
    Component=str(component)
    Assigned_To=str(issue.assignee)
    Status=str(issue.state)
    Resolution=""
    Reporter=str(issue.user)
    Last_Modified=str(issue.updated_at)
    Last_Modified=Last_Modified.split(" ")[0]
    Last_Modified=nice_time(Last_Modified)
    Version=""
    Milestone=str(issue.milestone)
    Hardware=""
    OS=""
    Priority=""
    Severity=""
    Summary=""
    if issue.body!=None:
		Summary=" ".join(str( unicodedata.normalize('NFKD', issue.body).encode('ascii','ignore')).split())
    Keywords=""#str(dict["keywords"])
    Submit_Date=str(issue.created_at)
    Submit_Date=Submit_Date.split(" ")[0]
    #print Submit_Date
    Submit_Date=nice_time(Submit_Date)
    Blocks=""
    Depends_On=""
    Duplicate_Of=""#,".join([v.name for v in issue.fields.issuelinks])
    CC=""#str(dict["cc"])
    return [Id,Product,Component,Assigned_To,Status,Resolution,Reporter,Last_Modified,Version,Milestone,Hardware,OS,Priority,Severity,Summary,Keywords,Submit_Date,Blocks,Depends_On,Duplicate_Of,CC]


def GithubIssues(outFile, owner, repo):
    gh = github3.login('DebuggerIssuesReport', password='DebuggerIssuesReport1')
    lines=[["ID","Product","Component","Assigned To","Status","Resolution","Reporter","Last Modified","Version","Milestone","Hardware","OS","Priority","Severity","Summary","Keywords","Submit Date","Blocks","Depends On","Duplicate Of","CC"]]
    reporepository = gh.repository(owner, repo)
    allIssues= reporepository.issues(state='all')
    for issue in allIssues:
        analyze = issueAnalyze(issue,repo,repo)
        lines.append(analyze)
    with  open(outFile,"wb") as f:
        writer=csv.writer(f)
        writer.writerows(lines)

if __name__ == "__main__":
    # GithubIssues(r"C:\temp\orientBugs.csv", "orientechnologies", "orientdb")
    GithubIssues(r"C:\temp\JodaOrg2.csv", "JodaOrg", "joda-time")

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