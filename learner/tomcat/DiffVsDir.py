__author__ = 'amir'


diffFile="C:\projs\git\svn\\22\\watchAdd.txt"
dirFile="C:\projs\git\svn\\22\\dirSumm2.txt"
outF=open("C:\projs\git\svn\\22\\watchREM.txt","w")

diffLines=[x.split("/\n")[0].split("\n")[0] for x in open(diffFile,"r").readlines()]
dirLines=[x.split("\n")[0] for x in open(dirFile,"r").readlines()]


#toUp=[x for x in diffLines if x not in dirLines]
for x in list( set(diffLines) - set(dirLines)):
        outF.write(x+"\n")