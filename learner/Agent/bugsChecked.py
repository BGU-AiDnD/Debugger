__author__ = 'amir'


import sqlite3
import csv

f=open("C:\\GitHub\\bugsChecked.csv","r")
reader=csv.reader(f)
lines=[r for r in reader]
lines=lines[1:]
dbPath="C:\\GitHub\\agent\\testsBugs.db"
conn = sqlite3.connect(dbPath)
conn.text_factory = str
c = conn.cursor()
#c.execute("CREATE TABLE IF NOT EXISTS buggedFilesChecked (BugId INT, fileName text, fileID INT )")
for l in lines:
    bugId=l[0]
    files=l[2]
    bugged=int(l[3])
    all=l[5:]
    all1=[]
    for a in all:
        if (a!= ''):
          all1.extend(a.split(" "))
    all1=" "+" ".join(["or fileName like '%"+str(a)+"'" for a in all1])
    s= "select * from buggedFiles where BugId="+str(bugId)+" and ("+ str(files)+"="+str(bugged)+all1+   " )"
    for r in c.execute(s):
        c.execute("INSERT INTO buggedFilesChecked VALUES (?,?,?)",list(r))
conn.commit()


