__author__ = 'amir'

"""
reporting:
# versions-tags
# commits
# age = first commit date
# bugs reported
# bugs fixed
# files
# methods
# tests
"""

import git
import datetime
import sqlite3
import csv




def report(out,repoPath,learningDB,testsDB):
    r=git.Repo(repoPath)
    commits= [x for x in r.iter_commits()]
    tags=[ x.commit for x in r.tags ]
    firstDate=datetime.datetime.fromtimestamp(commits[-1].committed_date).strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(learningDB)
    conn.text_factory = str
    c = conn.cursor()
    bugsR=0
    for row in c.execute("select count(*) from bugs"):
        bugsR=row[0]
    bugsF=0
    for row in c.execute("select count(*) from commits where commits.bugId<>0"):
        bugsF=row[0]
    files=0
    for row in c.execute("select count(*) from haelsTfiles"):
        files=row[0]
    methods=0
    for row in c.execute("select count(*) from methods"):
        methods=row[0]
    conn.close()

    tests=-1
    if testsDB!="":
        conn = sqlite3.connect(testsDB)
        conn.text_factory = str
        c = conn.cursor()
        for row in c.execute("select count(*) from tests"):
            tests=row[0]
        conn.close()

    lines=[["versions","commits","startDate","bugs reported","bugs fixed","java files","methods","tests"],[len(tags),len(commits),firstDate,bugsR,bugsF,files,methods,tests]]
    with open(out, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(lines)


if __name__ == '__main__':
    report("C:\\projs\\poi7Working\\report.csv","C:\\projs\\poi7Working\\repo","C:\\projs\\poi7Working\\dbAdd\\REL_3_10_1.db","C:\\projs\\poi7Working\\testsBugsMethods.db")




