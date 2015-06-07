__author__ = 'Amir-pc'
from random import randint
import csv
import sqlite3
import os
import random
import arff_use

testImports={}

def testFiles(filePath,name,basePath,names,Fnames,ind):
    global testImports
    if(not os.path.isfile(filePath)):
        print(filePath)
        testImports[name]=[]
    for i in testImports:
        if i==name:
            return testImports[name]
    files=[]
    with open(filePath) as f:
        content = f.readlines()
        for c in content:
            if("import" in c.split()):
                file= c.split()[1]
                file=file.split(";")[0]
                spl=file.split(".")
                s = ".".join(spl[0:3])
                if(s =="org.eclipse.cdt"):
                    files.append(file)
        f.close()
    i_s=[a.split(".") for a in files]
    i_s=[a[len(a)-1] for a in i_s]
    recursive=[]
    if( ind !=0):
        for i in i_s:
            if(i in Fnames):
                n=names[Fnames.index(i)]
                filePath1=os.path.join(basePath,n)
                recursive.append(testFiles(filePath1,n,basePath,names,Fnames,ind-1))
    testImports[name]=i_s+recursive
    return testImports[name]

def testsRows(dbpath,basePath): # return a list of lists where each one refer to test and its files
    conn = sqlite3.connect(dbpath)
    conn.text_factory = str
    c = conn.cursor()
    rows=[]
    names=[]
    for row in c.execute(str('select distinct name from haelsTfiles order by name')):
        name=row[0]
        names.append(name)
        Fnames=[]
    for j in names:
            a=0
            fName=j.split("\\")
            fName=fName[len(fName)-1]
            fName=fName.split(".")
            fName=fName[0]
            Fnames.append(fName)

    for row in c.execute(str('select name from haelsTfiles where name like "%test%"')):
        name=row[0]
        filePath=os.path.join(basePath,name)
        rows=rows+[testFiles(filePath,name,basePath,names,Fnames,5)]

    conn.close()
    return rows

def wekaAns(filename):
    probs=[]
    yesMin=1
    noMax=0
    with open(filename) as f:
        content = f.readlines()
        content=content[content.index(" inst#     actual  predicted error prediction\n")+1:]
        content=content[:content.index("\n")-1]
        for i in content:
            s=i.split()
            if(len(s)==0):
                break
            #print(s)
            ind=3
            if(len(s)==5 or len(s)==6):
                ind=4
            p=s[ind]
            if(p[0] not in list("0123456789")):
                p=p[1:]
            x = float(p)
            if(s[2]=="2:no"):
                x=1-x
                noMax=max(noMax,x)
            else:
                yesMin=min(yesMin,x)
            probs.append(x)
    return probs

def testAns(arf):
    return [i[26] for i in arff_use.load_arff(arf)["data"]]


def tom(dbpath,basePath,arf,const=0.5):
    conn = sqlite3.connect(dbpath)
    conn.text_factory = str
    c = conn.cursor()
    names=[]
    testFile=testsRows(dbpath,basePath)
    for row in c.execute(str('select distinct name from haelsTfiles order by name')):
        name=row[0]
        names.append(name)
    conn.close()
    ans=testAns(arf)
    tests=[]
    Fnames=[]
    for j in names:
            a=0
            fName=j.split("\\")
            fName=fName[len(fName)-1]
            fName=fName.split(".")
            fName=fName[0]
            Fnames.append(fName)
    print "start test"
    for i in testFile:
        p=1
        if( len(i) == 0):
            continue
        test=[]
        for j in Fnames:
            a=0
            if(j in i):
                a=1
                if(Fnames.index(j)<len(ans)):
                    if(ans[Fnames.index(j)]=='yes'):
                        p=p*const
            if(len(ans)>Fnames.index(j)):
                test.append(a)
        pss=1
        if(not (1 in test)):
            continue
        if(p>random.uniform(0,1)):
            pss=0
        print(test)
        test.append(pss)
        tests.append(test)
    return tests






def checkExport():
        reader = csv.reader("C:\Users\Amir-pc\Documents\GitHub\\vers\\all_final2.csv")
        for r in reader:
            l=len(r)
            tests=r[0:l-1]
            p=r[l-1]
            if(p==0):
                if(1 not in tests):
                    print "error"

def checkWeka(dbpath, wekPath="C:\Users\Amir-pc\Documents\GitHub\\vers\\weka2.txt"):
    ans=wekaAns(wekPath)
    for n in range(10):
        num=n/10.0
        dum=(n+1)/10.0
        print [len([i for i in ans if i>=num and i<dum]),num,dum]
    conn = sqlite3.connect(dbpath)
    conn.text_factory = str
    c = conn.cursor()
    data=[]
    add=[]
    names=[]
    for row in c.execute(str('select distinct name from haelsTfiles order by name')):
        name=row[0]
        names.append(name)
    conn.close()
    ret=[]
    ind=0
    for i in ans:
        if i==1:
          ret.append(ind)
        ind=ind+1
    max=0
    for i in ans:
        if i <> 1 and i>max:
                max=i
    print(ans)
    ans1=[]
    for  i in ans:
        if(i==1):
            ans1.append(0.9)
        else:
            ans1.append(i)
    print(ans1)
    return  ret


def checkTom(Tom1,Tom2,inds,arf):
    tm=tom(Tom1,Tom2,arf)
    tests=tm
    parts=[]
    groups=[]
    cou=0
    testsOnly=[ i[:len(i)-1]   for i in tests ]
    ts=[len([t1 for t1 in t if t1==1]) for t in testsOnly]
    zeros=[]
    zeros1=[]
    count=0
    for i in ts:
        if i==0:
            zeros.append(count)
        if i==1:
            zeros1.append(count)
        count=count+1
    print(zeros)
    print(zeros1)
    return
    a9=0
    for t1 in ts:
        a9=a9+t1
    #print("avg")
    #print (0.0+a9)/len(ts)
    for i in tests:
        groups.append(cou)
        c=0
        part=[]
        for a in i:
            if a==1:
               part.append(c)
            c=c+1
        parts.append(part)
        cou=cou+1
    return
    print parts
    print(groups)
    for i in range(len(parts)):
        j=i
        while(j<len(parts)-1):
            j=j+1
            #list(set(parts[groups[i]]).intersection(set(parts[groups[j]] )))
            if([x for x in parts[groups[i]] if x in parts[groups[j]]] != []):
                parts[i].append(parts[j])
                groups[j]=groups[i]
    #print parts
    print(groups)
    s = set(groups)
    print s
    print len(s)
    for ind in inds:
        #print(ind)
        #print wek[ind]
        lens=[]
        count=0
        for i in tests:
            if(1== i[ind]):
                count=count+1
                lens.append(len([a for a in i if a==1]))
        #print(count)
        #print(lens)

def tom_from_file(len1=-1,file="C:\Users\Amir-pc\Documents\GitHub\\vers\\ML\\Tom_all_Fixed.csv"):
    print(file)
    reader = csv.reader(open(file, "r"))
    if (len1==-1):
        return  [j for j in reader]
    return [i[:len1]+[i[len(i)-1]] for i in reader if ("1" in i[:len1])]
def matrix_from_sen_num(db,base,arf,sen_num,len1):
    tm=tom_from_file(len1)
    #tm=tom(db,base,arf)
    return tm
    print len(tm)
    tests1=tm
    parts=[]
    groups=[]
    cou=0
    for i in tests1:
        groups.append(cou)
        c=0
        part=[]
        for a in i:
            if a=="1":
               part.append(c)
            c=c+1
        parts.append(part)
        cou=cou+1
    print(parts)

    for i in range(len(parts)):
        j=i
        while(j<len(parts)-1):
            j=j+1
            #list(set(parts[groups[i]]).intersection(set(parts[groups[j]] )))
            if([x for x in parts[groups[i]] if x in parts[groups[j]]] != []):
                parts[i].append(parts[j])
                groups[j]=groups[i]
    set_g=[int(s) for s in list(set(groups))]
    g_p=[]
    print set_g
    for i in set_g:
        s = set(parts[i])
        g_p=g_p+[list(s)]
    groups_parts=[list(set(parts[i])) for i in set_g]
    print(g_p)
    return
    sen=list(set(groups))[sen_num]
    #print str(len(tests1)) +"_end"
    #print(groups)
    sen_tests=[tests1[groups.index(g)] for g in groups if g==sen]
    return sen_tests

def used_elements(tm,O):
    new_tm=[i[:len(i)-1] for i in tm]
    inds=[]
    for i in range(len(new_tm[0])):
        for j in new_tm:
            if j[i]=='1':
                    inds=inds+[i]
    inds=list(set(inds))
    with open(O, 'wb') as f:
        f.write(str(inds))
    return inds



def yes_inds(arf):
    ans=testAns(arf)
    i=0
    inds=[]
    for j in ans:
        if(j=="yes"):
            inds=inds+[i]
        i=i+1
    return inds


def optimize(inds_bef, tm_bef, wek_bef):
    inds=[]
    wek = []
    tm = [[] for t in tm_bef]
    for i in range(len(tm_bef[0])-1):
        need = False
        for elem in tm_bef:
            if elem[i] == "1":
                if elem[len(elem) - 1] == "1":
                    need = True
                    break
        if need == True:
            wek = wek + [wek_bef[i]]
            inds = inds + [inds_bef[i]]
            for ind in range(len(tm)):
                tm[ind] = tm[ind] + [tm_bef[ind][i]]
    i = len(tm_bef[0]) - 1
    for ind in range(len(tm)):
        tm[ind] = tm[ind] + [tm_bef[ind][i]]
    newTm=[]
    last=len(tm[0])-1
    if(last==-1):
        newTm=[]
    else:
        for i in range(len(tm)):
            if ("1" in tm[i][:last]):
                newTm=newTm+[tm[i]]
    return inds, newTm, wek


def export(wekPath, Out, yes_Out,arf,tomFile):
    wek_bef=wekaAns(wekPath)
    inds_bef=range(len(wek_bef))
    #wek_bef=[1,2,3]
    tm_bef=tom_from_file(len(wek_bef),tomFile)
    #tm_bef=tom_from_file(len(wek_bef),"C:\Users\Amir-pc\Documents\GitHub\\vers\\ML\\try.csv")
    #tm=tom(db,base,arf)
    inds, tm, wek = optimize( inds_bef, tm_bef, wek_bef)
    yes_bef=yes_inds(arf)

    for i in [5*t for t in range(16) if t!=0]:
        for j in range(16):
            tm3=tm[j*i:(j+1)*i]
            Out2=Out+"OPT__i=_"+str(i)+"j=_"+str(j)+"_"
            if tm3==[]:
                continue
            tm_ij=[]
            inds_ij, tm_ij, wek_ij = optimize( inds, tm3, wek)
            if tm_ij==[]:
                continue

            rand=[random.uniform(0,1) for w in wek_ij]
            uniform=[0.01 for w in wek_ij]
            yes_ij=yes_Out+"i="+str(i)+"j="+str(j)+".csv"
            yes=[]
            for y in yes_bef:
             if y in inds_ij:
                 yes=yes+[inds_ij.index(y)]

            with open(yes_ij, 'wb') as f:
                writer = csv.writer(f)
                writer.writerows([yes])

            used_elements(tm_ij,Out2+".txt")
            wekMat=[wek_ij]+tm_ij
            uniMat=[uniform]+tm_ij
            randMat=[rand]+tm_ij
            mats=[wekMat,randMat,uniMat]
            for O,r in zip([Out2+"Wek.csv",Out2+"Rand.csv",Out2+"Uni.csv"],mats):
                with open(O, 'wb') as f:
                    writer = csv.writer(f)
                    writer.writerows(r)


def multipleOuts(arr):
    names_1 =[('CDT_1_2_1_M1', '15-12-2003 20:28:17'), ('CDT_2_0', '16-07-2004 21:34:07'), ('CDT_3_0', '13-08-2005 00:26:02'), ('CDT_4_0_0', '26-06-2007 19:43:38'), ('CDT_5_0_0', '17-06-2008 18:29:54'), ('CDT_6_0_0', '17-06-2009 00:38:18'), ('CDT_7_0_0', '14-06-2010 23:38:05'), ('CDT_8_0_0', '08-06-2011 17:41:28'), ('CDT_8_0_1', '15-09-2011 17:10:38'), ('CDT_8_0_2', '11-02-2012 20:41:28'), ('CDT_8_1_0', '10-06-2012 08:01:17'), ('CDT_8_1_1', '17-09-2012 10:00:18')]#, ('CDT_8_1_2', '14-02-2013 01:21:52')]#
    last='CDT_8_1_2'
    names=[i[0] for i in names_1]
    basicPath="C:\Users\Amir-pc\Documents\GitHub\\vers\\CDT_8_1_2\\org.eclipse.cdt"
    base="C:\Users\Amir-pc\Documents\GitHub\\vers\\"
    arf=os.path.join(os.path.join(base,"ML"), str("CDT_8_1_2ML_sec_alone"+".arff"))
    wekPath=os.path.join(os.path.join(base,"ML\\bench"), str("wek_11"+".txt"))
    db=os.path.join(os.path.join(base,"db2"),str(last+"4.db"))
    for i in [i+100 for i in range(100)]:
        #i="try"
        Out=os.path.join(os.path.join(os.path.join(base,"ML"),"."), str("CSV_11_NEW_"+str(i)+"_"))
        export(basicPath,arf,wekPath,db,Out,i)



def tom_all(db,base,arf,O,const):
    tm=tom(db,base,arf,const)
    with open(O, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(tm)


def names_inds(dbpath):
    conn = sqlite3.connect(dbpath)
    conn.text_factory = str
    c = conn.cursor()
    names=[]
    for row in c.execute(str('select distinct name from haelsTfiles order by name')):
        name=row[0]
        names.append(name)
    conn.close()
    return names






#    tom_all(db,basicPath,"C:\Users\Amir-pc\Documents\GitHub\\vers\\ML\\CDT_8_1_2ML_sec_alone.arff",base1+"_tom_"+str(con)+".csv",con)
#checkWeka("C:\Users\Amir-pc\Documents\GitHub\\vers\dbMaccAll\CDT_8_2_0.db")
#tom("C:\Users\Amir-pc\Documents\GitHub\\vers\dbMaccAll\CDT_8_2_0.db","C:\Users\Amir-pc\Documents\GitHub\\vers\\CDT_8_2_0\\org.eclipse.cdt",arf)
#checkTom("C:\Users\Amir-pc\Documents\GitHub\\vers\dbMaccAll\CDT_8_2_0.db","C:\Users\Amir-pc\Documents\GitHub\\vers\\CDT_8_2_0\\org.eclipse.cdt",[709,781,1039,1040,1477,1960,2321,2353,2368,3213,7910],"C:\Users\Amir-pc\Documents\GitHub\\vers\\ML\\CDT_8_1_2ML_sec_alone.arff")
#testFiles("C:\\Users\Amir-pc\Documents\\GitHub\\vers\\CDT_8_2_0\\org.eclipse.cdt\\xlc\org.eclipse.cdt.errorparsers.xlc.tests\\src\\org\\eclipse\\cdt\\errorparsers\\xlc\\tests\\XlcErrorParserTester.java")


def testOptimize():
    global last, basicPath, base, arf, db, base1, wek_bef, inds_bef, tm_bef, inds, tm, wek, i, j, tm3, inds_ij, tm_ij, wek_ij, yes_bef, yes, y, l, a, outs, tm_am, new_ou, t, ro, s, le, ind
    last = 'CDT_8_1_2'
    basicPath = "C:\Users\Amir-pc\Documents\GitHub\\vers\\CDT_8_1_2\\org.eclipse.cdt"
    base = "C:\Users\Amir-pc\Documents\GitHub\\vers\\"
    arf = os.path.join(os.path.join(base, "ML"), str("CDT_8_1_2ML_sec_alone" + ".arff"))
    db = os.path.join(os.path.join(base, "db2"), str(last + "4.db"))
    base1 = "C:\Users\Amir-pc\Documents\GitHub\\vers\\ML\\"
    wek_bef = wekaAns("C:\Users\Amir-pc\Documents\GitHub\\vers\\weka2.txt")
    inds_bef = range(len(wek_bef))
    tm_bef = tom_from_file(len(wek_bef), "C:\Users\Amir-pc\Documents\GitHub\\vers\\ML\\_tom_0.8.csv")
    inds, tm, wek = optimize(inds_bef, tm_bef, wek_bef)
    i = 35
    j = 2
    tm3 = tm[j * i:(j + 1) * i]
    inds_ij, tm_ij, wek_ij = optimize(inds, tm3, wek)
    yes_bef = yes_inds(arf)
    print("yes")
    yes = []
    for y in yes_bef:
        if y in inds_ij:
            yes = yes + [inds_ij.index(y)]
    l = len(tm_ij[0])
    outs = [a[l - 1] for a in tm_ij]
    tm_am = []
    new_ou = []
    for i in range(len(tm_ij)):
        t = tm_ij[i]
        ro = []
        for s in yes:
            ro = ro + [t[s]]
        tm_am = tm_am + [ro]
        new_ou = new_ou + [outs[i]]
    le = len(tm_am[0])
    for ind in range(le):
        t = tm_am[ind]
        if not ('1' in t):
            print(ind)
            print(t)
            print(new_ou[ind])

last = 'CDT_8_1_2'

basicPath = "C:\Users\Amir-pc\Documents\GitHub\\vers\\CDT_8_1_2\\org.eclipse.cdt"
base = "C:\Users\Amir-pc\Documents\GitHub\\vers\\"
arf = os.path.join(os.path.join(base, "ML"), str("CDT_8_1_2ML_sec_alone" + ".arff"))
db = os.path.join(os.path.join(base, "db2"), str(last + "4.db"))
base1 = "C:\Users\Amir-pc\Documents\GitHub\\vers\\ML\\"
dir="C:\Users\Amir-pc\Documents\GitHub\\tom\\"

export("C:\Users\Amir-pc\Documents\GitHub\\vers\\ML\\WEKA_07_09.txt",dir,dir+"yesInds","C:\Users\Amir-pc\Documents\GitHub\\vers\\ML\\CDT_8_1_2ML_sec_alone.arff","C:\Users\Amir-pc\Documents\GitHub\\tom\\mat\\mat.csv")



for const in range(10):
    con=0.1+const/10.0
    dir="C:\Users\Amir-pc\Documents\GitHub\\vers\\ML\\"+str(con)+"\\"
    if not (os.path.isdir(dir)):
        os.mkdir(dir)
   # export("C:\Users\Amir-pc\Documents\GitHub\\vers\\weka2.txt",dir,dir+"yesInds","C:\Users\Amir-pc\Documents\GitHub\\vers\\ML\\CDT_8_1_2ML_sec_alone.arff","C:\Users\Amir-pc\Documents\GitHub\\vers\\ML\\"+"_tom_"+str(con)+".csv")
    #tom_all(db,basicPath,"C:\Users\Amir-pc\Documents\GitHub\\vers\\ML\\CDT_8_1_2ML_sec_alone.arff",base1+"_tom_"+str(con)+".csv",con)







wek_bef = wekaAns("C:\Users\Amir-pc\Documents\GitHub\\vers\\ML\\WEKA_07_09.txt")
#tm_bef = tom_from_file(len(wek_bef), "C:\Users\Amir-pc\Documents\GitHub\\vers\\ML\\_tom_0.9.csv")
#l=len(tm_bef[0])
#outs=[a[l-1] for a in tm_bef]
print("amir")
print wek_bef
#print len([a for a in outs if a =="0"])
