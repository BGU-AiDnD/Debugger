__author__ = 'Amir-pc'
import csv
import sqlite3


def source_files(sourceFilesReport,max):
    reader = csv.reader(sourceFilesReport)
    # creates the reader object
    files_metrics=[]
    index=0
    i=0
    for row_ in reader:# iterates the rows of the file in orders
        if(i==0):
            i=1
            continue
        name=str(row_[3]).replace("\\","/")
        r=[name]+[x.replace("*","") for x in  row_[4:]]
        files_metrics.append(r)
        #tot_changes=0
        #sum_insert=0
        #sum_delets=0
        #tot_bugs=0
        #tot_developers=0
        #number_of_methods=0
        #for row in db.execute(str('select name,count(*),sum(insertions),sum(deletions) from files WHERE name="'+name+"\"")):
         #   tot_changes=(row[1])
          #  sum_insert=(row[2])
           # sum_delets=(row[3])
        #for row in db.execute(str('select name,count(bugId) from files where bugID<>0 AND files.name="'+name+"\"")):
         #   tot_bugs=row[1]
        #for row in db.execute(str('select name,count(distinct author) from files,commits where commits.ID=files.commitid  AND name="'+name+"\"")):
         #   tot_developers=row[1]
        #add=[name,tot_changes,sum_insert,sum_delets,tot_bugs,tot_developers]+row_[4:]
        #metrics.execute("INSERT INTO files VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", add)
        index=index+1
        #print(str("files iter "+str(index)))
        if(index==max):
            break
    #connect.commit()
    return files_metrics

def source_methods(sourceMethodsReport,max):
    reader = csv.reader(sourceMethodsReport)
    index=0
    i=0
    methods=[]
    for row_ in reader:# iterates the rows of the file in orders
        if(i==0):
            i=1
            continue
        name=str(row_[3]).replace("\\","/")
        add=[name]+[x.replace("*","") for x in  row_[4:9]]
        methods.append(add)
        #print(str("method iter "+str(index)))
        index=index+1
        if(index==max):
            break
    return  methods


def build(sourceMonitorFiles,sourceMonitorMethods,max):
    sourceFilesReport = open(sourceMonitorFiles, "r")
    sourceMethodsReport = open(sourceMonitorMethods, "r")
    files_metrics=source_files(sourceFilesReport,max)
    methods=source_methods(sourceMethodsReport,max)
    #for add in methods:
     #   metrics.execute("INSERT INTO methods VALUES (?,?,?,?,?,?)", add)
    #connect.commit()
    return (files_metrics,methods)