"""Module to handle the the relevant actions related to the creation of the BUGS table."""
import csv
from datetime import datetime

BUG_ID_COL_NUM = 0
CREATION_TIME_COL_NUM = 16
LAST_CHANGE_TIME_COL_NUM = 7
SUFFICIENT_COLUMNS_DATA_AMOUNT = 16


def parse_bug_date(date):
	"""Parse the date into the appripriate format.

	Args:
		date (str): the date of the bug to parse and format.

	Returns:
		str. The formatted date.
	"""
	try:
		return datetime.strptime(date, "%d/%m/%y")
	except ValueError:
		return datetime.datetime.strptime(date, "%d/%m/%Y %H:%M:%S")


def parse_bugs_data(bugs_file_path):
	"""Parse the data from the bugs file path in orde to later place in the DB.

	Args:
		bugs_file_path (str): the path to the file containing all the bugs.

	Returns:
		tuple. The bugs extracted data, the bugs IDs.
	"""
	bugs_data = []
	bugs_ids = []
	with open(bugs_file_path, 'rb') as bugs_file:
		reader = csv.reader(bugs_file)
		next(reader, None)  # skip header
		for row in reader:  # iterates the rows of the file in order
			row_data = []
			for bug_data_column in row:
				cleaned_bug_data_column = bug_data_column
				if len(bug_data_column) > 0 and bug_data_column.startswith('='):
					cleaned_bug_data_column = bug_data_column[2:len(bug_data_column) - 1]

				row_data.append(cleaned_bug_data_column)

			if len(row_data) < SUFFICIENT_COLUMNS_DATA_AMOUNT:
				continue

			row_data[LAST_CHANGE_TIME_COL_NUM] = parse_bug_date(row_data[LAST_CHANGE_TIME_COL_NUM])
			row_data[CREATION_TIME_COL_NUM] = parse_bug_date(row_data[CREATION_TIME_COL_NUM])
			bugs_ids.append(row_data[BUG_ID_COL_NUM])
			bugs_data.append(row_data)

	return bugs_data, bugs_ids
