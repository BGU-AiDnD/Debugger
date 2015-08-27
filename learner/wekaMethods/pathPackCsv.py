__author__ = 'amir'


import os
import fnmatch


def getPack(path):
    Jclass=path.split(".java")[0]
    if "\\" in Jclass:
        Jclass=Jclass.split("\\")[-1]
    if "/" in Jclass:
        Jclass=Jclass.split("/")[-1]

    f=open(path,"r")
    lines=f.readlines()
    l=[x for x in lines if "package " in x and ";" in x]
    if len(l)==0:
        return  "",""+Jclass
    line=l[0].lstrip()
	
    pack=line.split(";")[0].split("package ")[1]
    return pack, pack+"."+Jclass

#print(getPack("C:\projs\poiWorking\\vers\REL_3_6\\repo\src\java\org\\apache\poi\\dev\\RecordGenerator.java"))
#print(getPack("C:\projs\poiWorking\\vers\REL_3_6\\repo\src\java\org\\apache\poi\\dev\\RecordGenerator.java"))

def projectPathPacks(path):
    matches = {}
    for dirName, subdirList, fileList in os.walk(path):
        for filename in fnmatch.filter(fileList, '*.java'):
            pathToJava=os.path.join(dirName, filename)
            pack, classpath= getPack(pathToJava)
            #print pack,pathToJava[len(path)+1:], classpath
            matches[classpath]=pathToJava[len(path)+1:]
    return matches


if __name__ == "__main__":
    exit()
    #print(projectPathPacks("C:\projs\\antWorking\\vers\ANT_170\\repo"))

