__author__ = 'Amir-pc'

import glob
from xml.dom import minidom


def constructor(c,className):
    att =c.attributes
    keys=att.keys()
    vals=[]
    params=len(c.getElementsByTagName("parameter"))
    for a in att.values():
        vals=vals+[a.value]
    keys=["className"]+keys+["Num_params"]
    vals=[className]+vals+[params]
    sig=vals[keys.index(u'signature')]
    ret = className + "." + vals[keys.index(u'name')]+sig
    return ret


def method(c,className):
    att =c.attributes
    keys=att.keys()
    vals=[]
    for a in att.values():
        vals=vals+[a.value]
    keys=keys#+["return"]
    vals=vals#+[ret]
    keys=["className"]+keys#+["Num_params"]
    vals=[className]+vals#+[params]
    sig=vals[keys.index(u'signature')]
    ret = className + "." + vals[keys.index(u'name')]+sig
    return ret


def field(c,className):
    att =c.attributes
    keys=att.keys()
    vals=[]
    for a in att.values():
        vals=vals+[a.value]
    ret=c.getElementsByTagName("type")
    ret=ret.attributes.values()[0].value
    keys=["className"]+keys+["type"]
    vals=[className]+vals+[ret]
    return vals

def classRead(c):
    all_methods=[]
    all_cons=[]
    att =c.attributes
    keys=att.keys()
    vals=[]
    for a in att.values():
        vals=vals+[a.value]
    name=""
    if u'name' in keys:
        name=vals[keys.index(u'name')]
    constructors=c.getElementsByTagName("constructor")
    for obj in constructors:
        all_cons.append(constructor(obj,name))
    methods=c.getElementsByTagName("method")
    for obj in methods:
        all_methods.append(method(obj,name))
    ret = all_methods+all_cons
    return ret


def xmlRead(doc):
    all_classes=[]
    xmldoc=minidom.parse(doc)
    root=xmldoc.getElementsByTagName("root")[0]
    package=root.getElementsByTagName("package")[0]
    classes= package.getElementsByTagName("class")
    #for i in range(len(classes)):
    #    if(i%2==0):
    #        all_classes.append(classRead(classes[i]))
    #pack="stop in " +package.attributes["name"].value
    pack=package.attributes["name"].value
    all=[]
    #for c in all_classes:
     #   for m in c:
            #all=all+[pack]#+"."+m]
    all=all+[pack]#+"."+m]
    return all

def build(JavaDocPath,max):
    docs=[]
    lst= glob.glob(JavaDocPath+"/*.xml")
    i=0
    for doc in lst:
        if (i==max):
            break
        i=i+1
        print(doc)
        docs=docs +xmlRead(doc)
    return docs

if __name__ == '__main__':
    f=open("C:/Jmeter/testPacks.txt","wb")
    f.write( "\n".join(list(set(build("C:\\testJdoc" , -1)))))
    f.close()