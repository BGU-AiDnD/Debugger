__author__ = 'amir'

import comments
import os
import glob
import sqlite3
import checkStyle


# git format-patch --root origin
path="C:\GitHub\\try\org.eclipse.cdt\\patchReg\\"
path="C:\\tomcat\code\\try\\tomcat8\\patchReg\\"

i=0


def commentsDetect(befDir,i,d, ConfLine=1):
    lstBef = glob.glob(befDir + "/*.java")
    befComms = []
    for doc in lstBef:
        # print doc
        i = i + 1
        diffF = path + d + "\\" + doc.split("\\")[-1]
        f = open(diffF, "r")
        deleted = (f.readlines()[ConfLine])
        deleted = deleted.replace("[","").replace("]","").replace("\n","")
        deleted = deleted.split(",")
        if deleted == [''] :
            continue
        deleted = [int(x) for x in deleted]
        commentsLines = comments.commLines(doc)
        allComm = False not in [False for x in deleted if x not in commentsLines]
        if allComm == True:
            befComms.append(doc.split("\\")[-1])
        if i == -1:
            exit()
    return befComms

def commentsCreate(path):
    Toadd=[]
    for d in os.listdir(path):
        if os.path.isdir(path+d):
            hex=d
            commit_id=int("".join(list(hex)[:7]),16)
            befDir=path+d+"\\before\\"
            afDir=path+d+"\\after\\"
            befComms=commentsDetect(befDir,i,d,1)
            afComms=commentsDetect(afDir,i,d,3)
            comms=list(set(befComms) & set(afComms))
            if comms!=[]:
                #c.executemany("INSERT INTO comments VALUES (?,?)", [(x.replace("_","\\"),commit_id ) for x in  comms])
                #Toadd.extend([c.execute("INSERT INTO comments VALUES (?,?)", (x.replace("_","\\"),commit_id )) for x in  comms]
                Toadd.extend([(x.replace("_","\\"),commit_id ) for x in  comms])
    return Toadd
def commentsAdd(rows,c,commits) :
    Toadd=[]
    for r in rows:
        if r[1] not in commits:
                    continue
        Toadd.append(r)
    c.execute('''CREATE TABLE comments (name text, commitid INT)''')
    c.executemany("INSERT INTO comments VALUES (?,?)",Toadd)
    index_createD='  CREATE INDEX IF NOT EXISTS comments_name ON comments (name)'
    c.execute(index_createD)
    index_createD='  CREATE INDEX IF NOT EXISTS comments_commitid ON comments (commitid)'
    c.execute(index_createD)
    conn.commit()


def checkStyleCreate(path,CodeDir):
    Toadd=[]
    for d in os.listdir(path):
        if os.path.isdir(path+d):
            if os.path.isdir(path+d):
                commit_id=int("".join(list(d)[:7]),16)
                add=checkStyle.commitAnalyze(path+d,commit_id,CodeDir)
                for a in add:
                    if len(a)!=83:
                        print len(a),path+d
                Toadd.extend(add)
    return Toadd

def checkStyleAdd(rows,c,commits):
    Toadd=[]
    for r in rows:
        if r[0] not in commits:
                continue
        Toadd.append(r)
    c.execute('''CREATE TABLE checkStyleAnalyzeExtends (commitid INT,name text, NCSS INT,FileLen INT,sum_fors REAL,sum_ifs REAL,sum_tries REAL,
		len_mccab REAL,sum_mccab REAL,mean_mccab REAL,median_mccab REAL,var_mccab REAL,max_mccab REAL,min_mccab REAL, oneElement_mccab text,
		len_fanOut REAL,sum_fanOut REAL,mean_fanOut REAL,median_fanOut REAL,var_fanOut REAL,max_fanOut REAL,min_fanOut REAL, oneElement_fanOut text,
		len_NPath REAL,sum_NPath REAL,mean_NPath REAL,median_NPath REAL,var_NPath REAL,max_NPath REAL,min_NPath REAL, oneElement_NPath text,
		len_JavaNCSSmet REAL,sum_JavaNCSSmet REAL,mean_JavaNCSSmet REAL,median_JavaNCSSmet REAL,var_JavaNCSSmet REAL,max_JavaNCSSmet REAL,min_JavaNCSSmet REAL, oneElement_JavaNCSSmet text,
		len_thorwsSTM REAL,sum_thorwsSTM REAL,mean_thorwsSTM REAL,median_thorwsSTM REAL,var_thorwsSTM REAL,max_thorwsSTM REAL,min_thorwsSTM REAL, oneElement_thorwsSTM text,
		len_coupl REAL,sum_coupl REAL,mean_coupl REAL,median_coupl REAL,var_coupl REAL,max_coupl REAL,min_coupl REAL, oneElement_coupl text,
		len_executables REAL,sum_executables REAL,mean_executables REAL,median_executables REAL,var_executables REAL,max_executables REAL,min_executables REAL, oneElement_executables text,
		len_lens REAL,sum_lens REAL,mean_lens REAL,median_lens REAL,var_lens REAL,max_lens REAL,min_lens REAL, oneElement_lens text,
		publics REAL,protecteds REAL,privates REAL,totals REAL ,len_params REAL,sum_params REAL,mean_params REAL,median_params REAL,var_params REAL,max_params REAL,min_params REAL, oneElement_params text
		)''')
    c.executemany("INSERT INTO checkStyleAnalyzeExtends VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",Toadd)
    index_createD='  CREATE INDEX IF NOT EXISTS checkStyleAnalyzeE_name ON checkStyleAnalyzeExtends (name)'
    c.execute(index_createD)
    index_createD='  CREATE INDEX IF NOT EXISTS checkStyleAnalyzeE_commitid ON checkStyleAnalyzeExtends (commitid)'
    c.execute(index_createD)
    conn.commit()

#DBpath="C:\GitHub\\vers\\dbAdd\\done2"
DBpath="C:\\tomcat\code\\dbAdd"
#vers=('CDT_8_0_1','CDT_8_0_2','CDT_8_1_0','CDT_8_1_1','CDT_8_1_2' )
vers=("TOMCAT_8_0_4", "TOMCAT_8_0_5", "TOMCAT_8_0_6", "TOMCAT_8_0_7", "TOMCAT_8_0_8", "TOMCAT_8_0_9")
CodeDir="repo"
#rows=checkStyleCreate(path,CodeDir)
commentsRows=commentsCreate(path)
for ver in vers:
        print ver
        dbP=DBpath+"\\"+ver+".db"
        conn = sqlite3.connect(dbP)
        conn.text_factory = str
        c = conn.cursor()
        commits=[]
        commQ=" select distinct ID from commits"
        for row in c.execute(commQ):
            commits.append(row[0])
        commentsAdd(commentsRows,c,commits)
        #checkStyleAdd(rows,c,commits)
        conn.close()





