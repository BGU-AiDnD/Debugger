__author__ = 'amir'

import jira
import csv
import unicodedata
import datetime
import utilsConf

#ID	Product	Component	Assigned To	Status	Resolution	Reporter	Last Modified	Version	Milestone	Hardware	OS	Priority	Severity	Summary	Keywords	Submit Date	Blocks	Depends On	Duplicate Of	CC
def issueAnalyze(issue):
    Id=issue.key.split("-")[1]
    Product=str(issue.fields.project)
    Component=",".join([x.name for x in issue.fields.components])
    Assigned_To="NONE"
    if issue.fields.assignee!=None:
        Assigned_To=str( unicodedata.normalize('NFKD', issue.fields.assignee.name).encode('ascii','ignore'))
    Status=str(issue.fields.status)
    Resolution=str(issue.fields.resolution)
    Reporter=str(issue.fields.reporter.name)
    Last_Modified=str(issue.fields.updated)[:10]
    Last_Modified=datetime.datetime.strptime(Last_Modified,'%Y-%m-%d').date().strftime('%d/%m/%Y %H:%M:%S')

    Version = ""
    if hasattr(issue.fields, 'versions'):
        Version=",".join([v.name for v in getattr(issue.fields, 'versions')])
    Milestone=",".join([v.name for v in issue.fields.fixVersions])
    Hardware=str("")
    OS=""
    if not None==issue.fields.environment:
        OS=str(unicodedata.normalize('NFKD', issue.fields.environment).encode('ascii','ignore'))
        OS=" ".join(OS.split())
    Priority=str("")
    if "priority" in  issue.raw:
        Priority=str("P"+issue.raw["priority"]["id"])
    Severity=str("")
    if "issuetype"  in  issue.raw:
        Severity=str(issue.raw["issuetype"]["name"])
    Summary=str(unicodedata.normalize('NFKD', issue.fields.summary).encode('ascii','ignore'))
    Summary=Summary.replace("\n"," ")
    Keywords=str(issue.fields.labels)
    Submit_Date=str(issue.fields.created)[:10]
    Submit_Date=datetime.datetime.strptime(Submit_Date,'%Y-%m-%d').date().strftime('%d/%m/%Y %H:%M:%S')
    Blocks=str("")
    Depends_On=str("")
    Duplicate_Of=""#,".join([v.name for v in issue.fields.issuelinks])
    CC=str("")
    return [Id,Product,Component,Assigned_To,Status,Resolution,Reporter,Last_Modified,Version,Milestone,Hardware,OS,Priority,Severity,Summary,Keywords,Submit_Date,Blocks,Depends_On,Duplicate_Of,CC]

@utilsConf.marker_decorator(utilsConf.ISSUE_TRACKER_FILE)
def jiraIssues(outFile , url, project_name, bunch = 100):
    jiraE = jira.JIRA(url)
    allIssues=[]
    extracted_issues = 0
    lines = [
        ["id", "product", "component", "assigned_to", "status", "resolution", "reporter", "last_change_time", "version",
         "target_milestone", "platform", "op_sys", "priority", "severity", "summary", "keywords", "creation_time",
         "blocks", "depends_on", "Duplicate Of", "cc"]]
    while True:
        issues = jiraE.search_issues("project={0}".format(project_name), maxResults=bunch, startAt=extracted_issues)
        allIssues.extend(issues)
        extracted_issues=extracted_issues+bunch
        if len(issues) < bunch :
            break
    for issue in allIssues:
        analyze = issueAnalyze(issue)
        lines.append(analyze)
    f=open(outFile,"wb")
    writer=csv.writer(f)
    writer.writerows(lines)
    f.close()

if __name__ == "__main__":
    jiraIssues("C:\\temp\\CASSANDRA2.csv", "https://issues.apache.org/jira",'CASSANDRA')
