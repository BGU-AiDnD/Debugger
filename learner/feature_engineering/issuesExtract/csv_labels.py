import csv
import datetime

from utils.monitors_manager import monitor, ISSUE_TRACKER_FILE

HEADER = ["id", "product", "component", "assigned_to", "status", "resolution", "reporter",
          "last_change_time", "version", "target_milestone", "platform", "op_sys", "priority",
          "severity", "summary", "keywords", "creation_time", "blocks", "depends_on",
          "Duplicate Of", "cc"]
BLANKS = ['' for x in HEADER][1:]


def get_datetime(date):
	return datetime.datetime.strptime(date.strip()[:-6], "%a %b %d %H:%M:%S %Y").strftime(
		'%d/%m/%Y %H:%M:%S')


def get_all_bugs(csv_file):
	bugs = []
	with open(csv_file) as f:
		reader = csv.reader(f)
		bugs = map(
			lambda row: [row[4]] + ['' for _ in range(1, 7)] + [get_datetime(row[2])] + ['' for _ in
			                                                                             range(8,
			                                                                                   16)] + [
				            get_datetime(row[2])] + ['' for _ in range(17, 21)],
			filter(lambda row: int(row[5]), list(reader)[1:]))
	return bugs


@monitor(ISSUE_TRACKER_FILE)
def write_bugs_csv(csv_bug_file, url, csv_file):
	lines = [HEADER]
	lines.extend(get_all_bugs(csv_file))
	with open(csv_bug_file, "wb") as f:
		writer = csv.writer(f)
		writer.writerows(lines)
