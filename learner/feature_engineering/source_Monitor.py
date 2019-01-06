__author__ = 'Amir-pc'
import csv
import os

def parse_file(path, expected_line_size, name_ind=3, features_start_ind=4, features_end_ind=None):
    with open(path) as f:
        reader = csv.reader(f)
        # creates the reader object
        metrics = []
        for features_row in list(reader)[1:]:# iterates the rows of the file in orders
            if len(features_row) != expected_line_size:
                # known bugs of source monitor, comma exists in generic methods like Foo<T1, T1>
                continue
            try:
                name = os.path.normpath(str(features_row[name_ind]))
                r = [name]+[x.replace("*", "") for x in features_row[features_start_ind:features_end_ind]]
                metrics.append(r)
            except:
                pass
        return metrics


def source_files(sourceFilesReport):
    return parse_file(sourceFilesReport, 29)


def source_methods(sourceMethodsReport):
    return parse_file(sourceMethodsReport, 9, features_end_ind=9)


def build(sourceMonitorFiles, sourceMonitorMethods):
    files_metrics = source_files(sourceMonitorFiles)
    methods = source_methods(sourceMonitorMethods)
    return files_metrics, methods