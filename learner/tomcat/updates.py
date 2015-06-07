__author__ = 'amir'

import glob
import os

def oneLevel(path):
    lst= glob.glob(path+"\\*")
    return lst

def pathToSvn(path):
    return "\\".join(path.split("\\")[5:])

def levels(path,level):
    ans=[]
    up=oneLevel(path)
    if level==0:
        ans=[pathToSvn(f) for f in up if os.path.isdir(f)]
        return ans
    for f in up:
        if os.path.isdir(f):
            ans.extend(levels(f,level-1))
        #else:
            #ans.append(pathToSvn(f))
    return ans

#f=open("C:\projs\git\svn\\22\levels0.txt","w")
#l=levels("C:\projs\git\svn\\22",0)
#f.writelines([x+"\n" for x in l])






