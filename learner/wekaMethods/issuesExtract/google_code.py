import csv
import urllib2
import json

from utils.monitors_manager import monitor, ISSUE_TRACKER_FILE

QUERY = r"https://storage.googleapis.com/google-code-archive/v2/code.google.com/{PRODUCT}/issues-page-{PAGE}.json"
PRIORITIES = {"Priority-Medium": 'P3', "Priority-Low": 'P1', 'Priority-High': 'P5'}

def extract_bug_data(bug):
    milestone = ''
    for label in bug['labels']:
        if label.startswith('Milestone'):
            milestone = label
    priority = 'P1'
    for label in bug['labels']:
        if label in PRIORITIES:
            priority = PRIORITIES[label]
    return bug['id'], "", bug['labels'][0], "", bug['status'], "", "", \
           "", \
           "", milestone, "", "", priority, \
           "", bug['summary'], "", ""\
        , "", "", "", ""


def get_all_bugs(product):
    page = 1
    bugs = []
    while True:
        data = json.loads(urllib2.urlopen(QUERY.format(PRODUCT=product, PAGE=page)).read())
        bugs.extend(map(extract_bug_data, data['issues']))
        page += 1
        if data["pageNumber"] == data["totalPages"]:
            break
    return bugs


@monitor(ISSUE_TRACKER_FILE)
def write_bugs_csv(csv_bug_file, url, product):
    lines=[["id", "product", "component", "assigned_to", "status", "resolution", "reporter", "last_change_time", "version", "target_milestone", "platform", "op_sys", "priority", "severity", "summary", "keywords", "creation_time", "blocks", "depends_on", "Duplicate Of", "cc"]]
    lines.extend(get_all_bugs(product))
    with open(csv_bug_file,"wb") as f:
        writer=csv.writer(f)
        writer.writerows(lines)
