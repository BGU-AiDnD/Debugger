__author__ = 'amir'

import sqlite3

dbPath="C:\\GitHub\\agent\\testsBugs.db"
packsFile="C:\\GitHub\\agent\\PacksBigger.txt"
conn = sqlite3.connect(dbPath)
conn.text_factory = str
c = conn.cursor()
s="select * from testsFiles"
lst =[str(w)+"\n" for w in set([".".join(x[0].split(".")[:4]) for x in c.execute(s)])]
f=open(packsFile,"wb")
f.writelines(lst)
f.close()
#print lst



