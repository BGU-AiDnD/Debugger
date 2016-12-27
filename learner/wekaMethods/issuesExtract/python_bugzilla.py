__author__ = 'amir'
import bugzilla
import csv

def get_bug_data(bug):
    return bug.id, bug.product, bug.component, bug.assigned_to, bug.status, bug.resolution, bug.reporter, bug.last_change_time, bug.version, bug.target_milestone, bug.platform, bug.op_sys, bug.priority, bug.severity, bug.summary, bug.keywords, bug.creation_time, bug.blocks, bug.depends_on, "", bug.cc

def get_all_bugs(url, product):
    bzapi = bugzilla.Bugzilla(url)
    q = bzapi.build_query(product=product)
    bugs = bzapi.query(q)
    return map(get_bug_data, bugs)

def write_bugs_csv(csv_bug_file, url, product):
    bugs = get_all_bugs(url, product)
    lines=[["id", "product", "component", "assigned_to", "status", "resolution", "reporter", "last_change_time", "version", "target_milestone", "platform", "op_sys", "priority", "severity", "summary", "keywords", "creation_time", "blocks", "depends_on", "Duplicate Of", "cc"]]
    lines.extend(bugs)
    f=open(csv_bug_file,"wb")
    writer=csv.writer(f)
    writer.writerows(lines)
    f.close()

if __name__ == "__main__":
    write_bugs_csv("C:\Temp\\bugs", "partner-bugzilla.redhat.com", "Fedora")