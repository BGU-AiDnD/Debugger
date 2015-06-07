__author__ = 'amir'

import requests
import ast
import re

r = requests.get('https://bugzilla.mozilla.org/rest/bug?product=Input')
#print r[0]
#print type(r)


#print r.text[0]
#print r.text[:200]

def bind(b):
    #print b
    ind=b.index(":")
    var=b[:ind]
    val=b[ind+1:]
    if val[0]=="{":
        val=DictToVals(val,"{","}")
    if val[0]=="[":
        val=ArrayToVals(val,"[","]")
    return var,val

def arrayElem(elem):
    val=elem
    if val[0]=="[":
        val=ArrayToVals(val,"[","]")
    if val[0]=="{":
        val=ArrayToVals(val,"{","}")
    return val


def valToDict(val):
    #print val
    binds=[]
    strat1="{"
    strat2="["
    end1="}"
    end2="]"
    delim=","
    count1=0
    count2=0
    startInd=0
    ind=0
    for c in val:
        if c==strat1:
            count1=count1+1
        if c==end1:
            count1=count1-1
        if c==strat2:
            count2=count2+1
        if c==end2:
            count2=count2-1
        if c==delim and count1==0 and count2==0:
            b=arrayElem(val[startInd:ind])
            binds.append(b)
            startInd=ind+1
        ind=ind+1
    return binds

def valToArray(val):
    print val
    binds={}
    strat1="{"
    strat2="["
    end1="}"
    end2="]"
    delim=","
    count1=0
    count2=0
    startInd=0
    ind=0
    for c in val:
        if c==strat1:
            count1=count1+1
        if c==end1:
            count1=count1-1
        if c==strat2:
            count2=count2+1
        if c==end2:
            count2=count2-1
        if c==delim and count1==0 and count2==0:
            a, b=bind(val[startInd:ind])
            binds[a]=b
            startInd=ind+1
        ind=ind+1
    return binds

def DictToVals(arr,starting,ending):
    tx=arr#[arr.index("["):]
    count=0
    startInd=-1
    ind=0
    vals=[]
    for c in tx:
        if c==starting:
            if count==0:
                startInd=ind+1
            count=count+1
        if c==ending:
            count=count-1
        if count==0 and startInd!=-1:
            vals.append(valToDict(tx[startInd:ind]))
        ind=ind+1
    return vals

def ArrayToVals(arr,starting,ending):
    tx=arr#[arr.index("["):]
    count=0
    startInd=-1
    ind=0
    vals=[]
    for c in tx:
        if c==starting:
            if count==0:
                startInd=ind+1
            count=count+1
        if c==ending:
            count=count-1
        if count==0 and startInd!=-1:
            vals.append(valToArray(tx[startInd:ind]))
        ind=ind+1
    return vals


tx=r.text[1:]
#print tx[:200]
#print tx.index("{")
#print tx[tx.index("{"):200]
print(DictToVals(tx[tx.index("["):],"{","}"))
tx=r.text[r.text.index("["):]

#print(tx[:200])
#outer = re.compile("\{{.+}\}")
#m = outer.search(tx)

#inner_str = m.group(1)
#print(inner_str)
#lit=ast.literal_eval(r.text)
#print lit

