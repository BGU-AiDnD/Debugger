__author__ = 'Amir-pc'
import csv
import sqlite3


def source_files(sourceFilesReport):
    with open(sourceFilesReport) as f:
        reader = csv.reader(f)
        # creates the reader object
        files_metrics = []
        for row_ in list(reader)[1]:# iterates the rows of the file in orders
            name = str(row_[3]).replace("\\","/")
            r=[name]+[x.replace("*","") for x in  row_[4:]]
            files_metrics.append(r)
        return files_metrics

def source_methods(sourceMethodsReport):
    with open(sourceMethodsReport) as f:
        reader = csv.reader(f)
        methods = []
        for row_ in list(reader)[1:]:# iterates the rows of the file in orders
            try:
                name = str(row_[3]).replace("\\", "/")
                add = [name]+[x.replace("*", "") for x in row_[4:9]]
                methods.append(add)
            except:
                pass
        return methods


def build(sourceMonitorFiles, sourceMonitorMethods, max):
    files_metrics=source_files(sourceMonitorFiles)
    methods=source_methods(sourceMonitorMethods)
    return (files_metrics,methods)