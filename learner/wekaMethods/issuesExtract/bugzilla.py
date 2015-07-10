__author__ = 'amir'

import bzlib.bugzilla
import bzlib.bug
import csv
import unicodedata
import datetime


print 1
b= bzlib.bugzilla.Bugzilla("https://bugs.eclipse.org/bugs/")
print 2
bugs=bzlib.bug.Bug.search(b, **{'product': "CDT"})
print 3
print bugs
print bugs[0]
print bugs[0].__dict__


#ID	Product	Component	Assigned To	Status	Resolution	Reporter	Last Modified	Version	Milestone	Hardware	OS	Priority	Severity	Summary	Keywords	Submit Date	Blocks	Depends On	Duplicate Of	CC
def issueAnalyze(issue):
    dict=issue
    Id=str(dict["id"])
    Product=str(dict["product"])
    Component=str(dict["component"])
    Assigned_To=str(dict["assigned_to"])
    Status=str(dict["status"])
    Resolution=str(dict["resolution"])
    Reporter=str(dict["creator"])
    Last_Modified=str(dict["last_change_time"])
    print Last_Modified
    Last_Modified=datetime.datetime.strptime(Last_Modified,'%Y-%m-%d').date().strftime("%d/%m/%y")

    Version=str(dict["version"])
    Milestone=str(dict["target_milestone"])
    Hardware=str(dict["platform"])
    OS=str(dict["op_sys"])
    Priority=str(dict["priority"])
    Severity=str(dict["severity"])
    Summary=str(dict["summary"])
    Keywords=str(dict["keywords"])
    Submit_Date=str(dict["creation_time"])
    print Submit_Date
    Submit_Date=datetime.datetime.strptime(Submit_Date,'%Y-%m-%d').date().strftime("%d/%m/%y")
    Blocks=str(dict["blocks"])
    Depends_On=str(dict["depends_on"])
    Duplicate_Of=""#,".join([v.name for v in issue.fields.issuelinks])
    CC=str(dict["cc"])
    return [Id,Product,Component,Assigned_To,Status,Resolution,Reporter,Last_Modified,Version,Milestone,Hardware,OS,Priority,Severity,Summary,Keywords,Submit_Date,Blocks,Depends_On,Duplicate_Of,CC]


def BugzillaIssues(url,productName,outFile):
    b= bzlib.bugzilla.Bugzilla(url)
    lines=[["ID","Product","Component","Assigned To","Status","Resolution","Reporter","Last Modified","Version","Milestone","Hardware","OS","Priority","Severity","Summary","Keywords","Submit Date","Blocks","Depends On","Duplicate Of","CC"]]
    allIssues=bzlib.bug.Bug.search(b, **{'product': productName})
    print(len(allIssues))
    for issue in allIssues:
        analyze = issueAnalyze(issue.__dict__)
        lines.append(analyze)
    f=open(outFile,"wb")
    writer=csv.writer(f)
    writer.writerows(lines)
    f.close()



print 1
b= bzlib.bugzilla.Bugzilla("https://bugs.eclipse.org/bugs/")
print 2
bugs=bzlib.bug.Bug.search(b, **{'product': "CDT"})
print 3
print bugs
print bugs[0]
print bugs[0].__dict__
d=bugs[0].__dict__
issueAnalyze(d)
for x in d:
    print x ,d[x]
data=d["_data"]
print data.keys()
print data.values()
exit()

b= bzlib.bugzilla.Bugzilla("https://bugs.eclipse.org/bugs/")
bugs=bzlib.bug.Bug.search(b, **{'product': "CDT"})
print bugs
print bugs[0]
print bugs[0].__dict__
d=bugs[0].__dict__
print d.keys()
print d.values()
print [x for x in bugs[0]]
print bugs[0].keys()
print bugs[0].values()
print bugs[0].data()
print bugs[0].history()
print [b for b in bugs]
print [b.data() for b in bugs]
print [b.history() for b in bugs]

exit()
bugs=bzlib.bug.Bug.search(b, **{'component': "CDT"})
print bugs
prod=b.get_products()
p=[x for x in prod  if x["name"]=="CDT"]
p=p[0]
for x in p:
    print x
    print p[x]
fi= b.get_fields()
fi=fi[0]
print ""
print ""
print ""
for x in fi:
    print x
    print fi[x]
