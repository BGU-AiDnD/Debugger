__author__ = 'amir'

import jira
import csv
import unicodedata
import datetime


#ID	Product	Component	Assigned To	Status	Resolution	Reporter	Last Modified	Version	Milestone	Hardware	OS	Priority	Severity	Summary	Keywords	Submit Date	Blocks	Depends On	Duplicate Of	CC
def issueAnalyze(issue):
    Id=issue.id
    Product=str(issue.fields.project)
    Component=",".join([x.name for x in issue.fields.components])
    Assigned_To="NONE"
    if issue.fields.assignee!=None:
        Assigned_To=str( unicodedata.normalize('NFKD', issue.fields.assignee.name).encode('ascii','ignore'))
    Status=str(issue.fields.status)
    Resolution=str(issue.fields.resolution)
    Reporter=str(issue.fields.reporter.name)
    Last_Modified=str(issue.fields.updated)[:10]
    Last_Modified=datetime.datetime.strptime(Last_Modified,'%Y-%m-%d').date().strftime("%d/%m/%y")

    Version=",".join([v.name for v in issue.fields.versions])
    Milestone=",".join([v.name for v in issue.fields.fixVersions])
    Hardware=str("")
    OS=""
    if not None==issue.fields.environment:
        OS=str(unicodedata.normalize('NFKD', issue.fields.environment).encode('ascii','ignore'))
    Priority=str("")
    if "priority" in  issue.raw:
        Priority=str("P"+issue.raw["priority"]["id"])
    Severity=str("")
    if "issuetype"  in  issue.raw:
        Severity=str(issue.raw["issuetype"]["name"])
    Summary=str(unicodedata.normalize('NFKD', issue.fields.summary).encode('ascii','ignore'))
    Keywords=str(issue.fields.labels)
    Submit_Date=str(issue.fields.created)[:10]
    Submit_Date=datetime.datetime.strptime(Submit_Date,'%Y-%m-%d').date().strftime("%d/%m/%y")
    Blocks=str("")
    Depends_On=str("")
    Duplicate_Of=""#,".join([v.name for v in issue.fields.issuelinks])
    CC=str("")
    return [Id,Product,Component,Assigned_To,Status,Resolution,Reporter,Last_Modified,Version,Milestone,Hardware,OS,Priority,Severity,Summary,Keywords,Submit_Date,Blocks,Depends_On,Duplicate_Of,CC]


def jiraIssues(url,query,maxResults,outFile):
    jiraE = jira.JIRA(url)
    allIssues=[]
    counter=0
    lines=[["ID","Product","Component","Assigned To","Status","Resolution","Reporter","Last Modified","Version","Milestone","Hardware","OS","Priority","Severity","Summary","Keywords","Submit Date","Blocks","Depends On","Duplicate Of","CC"]]
    while counter<maxResults:
        issues = jiraE.search_issues(query, maxResults=100,startAt=counter)
        allIssues.extend(issues)
        counter=counter+100
    print(len(allIssues))
    for issue in allIssues:
        analyze = issueAnalyze(issue)
        lines.append(analyze)
    f=open(outFile,"wb")
    #f.writelines([",".join(x) for x in lines])

    writer=csv.writer(f)
    writer.writerows(lines)
    f.close()


jiraIssues("https://java.net/jira",'project=JERSEY',2900,"C:\projs\\jerseyBugs.csv")
exit()
jiraIssues('https://issues.apache.org/jira','project=KARAF',3800,"C:\projs\\karaf\\karafBugs.csv")
exit()

jiraE = jira.JIRA('https://issues.apache.org/jira')

issues = jiraE.search_issues('project=KARAF')
print issues[0].fields


issue = jiraE.issue('JRA-9')
print issue.fields.project.key             # 'JRA'
print issue.fields.issuetype.name          # 'New Feature'
print issue.fields.reporter.displayName    # 'Mike Cannon-Brookes [Atlassian]'

