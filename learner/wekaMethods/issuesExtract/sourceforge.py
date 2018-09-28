import utilsConf
import csv
import urllib2
import json
import datetime

QUERY = r"https://sourceforge.net/rest/p/{PRODUCT}/bugs/search/?q=status%3Aclosed-invalid+or+status%3Aclosed-later+or+status%3Aclosed-accepted+or+status%3Aclosed-duplicate+or+status%3Aclosed-out-of-date+or+status%3Aclosed-rejected+or+status%3Aclosed-works-for-me+or+status%3Aclosed+or+status%3Aclosed-wont-fix+or+status%3Aclosed-fixed&page={PAGE}"


def extract_bug_data(bug):
    return bug['ticket_num'], "", ",".join(bug['labels']), bug['assigned_to'], bug['status'], "", bug['reported_by'], \
           datetime.datetime.strptime(bug['mod_date'].split('.')[0], '%Y-%m-%d %H:%M:%S').date().strftime(
               '%d/%m/%Y %H:%M:%S'), \
           "", bug['custom_fields'].get('_milestone', ""), "", "", "P{0}".format(
        bug['custom_fields'].get('_priority', "")), \
           "", bug['summary'], "", datetime.datetime.strptime(bug['created_date'].split('.')[0],
                                                              '%Y-%m-%d %H:%M:%S').date().strftime('%d/%m/%Y %H:%M:%S') \
        , "", "", "", ""


def get_all_bugs(product):
    page = 0
    bugs = []
    while True:
        data = json.loads(urllib2.urlopen(QUERY.format(PRODUCT=product, PAGE=page)).read())
        if len(data['tickets']) == 0:
            break
        bugs.extend(map(extract_bug_data, data['tickets']))
        page += 1
    return bugs


@utilsConf.marker_decorator(utilsConf.ISSUE_TRACKER_FILE)
def write_bugs_csv(csv_bug_file, url, product):
    lines = [
        ["id", "product", "component", "assigned_to", "status", "resolution", "reporter", "last_change_time", "version",
         "target_milestone", "platform", "op_sys", "priority", "severity", "summary", "keywords", "creation_time",
         "blocks", "depends_on", "Duplicate Of", "cc"]]
    lines.extend(get_all_bugs(product))
    with open(csv_bug_file, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(lines)
