__author__ = 'Amir-pc'

import glob
import re
import string
from xml.dom import minidom
import pathPackCsv

# for /R C:\Users\Amir-pc\Documents\GitHub\org.eclipse.cdt %f in (*.java) do javadoc -doclet com.github.markusbernhardt.xmldoclet.XmlDoclet -docletpath xml-doclet-1.0.4-jar-with-dependencies.jar -filename %~nxf.xml -private -d .\Jdoc %f

def constructor(c,className,Dirpath):
    att =c.attributes
    keys=att.keys()
    vals=[]
    params=len(c.getElementsByTagName("parameter"))
    for a in att.values():
        vals=vals+[a.value]
    keys=["className"]+keys+["Num_params"]
    vals=[Dirpath]+[className]+vals+[params]
    return vals


def method(c,className,Dirpath):
    att =c.attributes
    keys=att.keys()
    vals=[]
    for a in att.values():
        vals=vals+[a.value]
    ret=c.getElementsByTagName("return")[0]
    params=len(c.getElementsByTagName("parameter"))
    ret_att=ret.attributes
    ret=ret_att.values()[0].value
    keys=keys+["return"]
    vals=vals+[ret]
    keys=["className"]+keys+["Num_params"]
    vals=[Dirpath]+[className]+vals+[params]
    return vals


def field(c,className,Dirpath):
    att =c.attributes
    keys=att.keys()
    vals=[]
    for a in att.values():
        vals=vals+[a.value]
    ret=c.getElementsByTagName("type")[0]
    ret=ret.attributes.values()[0].value
    keys=["className"]+keys+["type"]
    vals=[Dirpath]+[className]+vals+[ret]
    return vals

def classRead(c,packPath):
    all_methods=[]
    all_fields=[]
    all_cons=[]
    att =c.attributes
    keys=att.keys()
    vals=[]
    for a in att.values():
        vals=vals+[a.value]
    superClass=""
    name=""
    Dirpath=""
    if len(vals)>1:
        name=vals[1]
    else:
        return ()
    if len(vals)>4:
        if vals[4] not in packPath:
            return ()
        Dirpath=packPath[vals[4]]
    else:
        return ()
    extends=c.getElementsByTagName("class")
    if(len(extends)>0):
        extends=extends[0]
        superClass=extends.attributes.values()[0].value
    keys=["Dirpath"]+["superClass"]+keys
    vals=[Dirpath]+[superClass]+vals
    constructors=c.getElementsByTagName("constructor")
    for cons in constructors:
        all_cons.append(constructor(cons,name,Dirpath))
    methods=c.getElementsByTagName("method")
    for met in methods:
        all_methods.append(method(met,name,Dirpath))
    fields=c.getElementsByTagName("field")
    for f in fields:
        all_fields.append(field(f,name,Dirpath))
    for i in range(10-len(vals)):
        vals=vals+["NONE"]
    return (vals,all_methods,all_fields,all_cons)


def interfaceRead(c,packPath):
    all_methods=[]
    all_fields=[]
    all_cons=[]
    att =c.attributes
    keys=att.keys()
    vals=[]
    for a in att.values():
        vals=vals+[a.value]
    superClass="Interface"
    name=""
    Dirpath=""

    if len(vals)>1:
        name=vals[1]
    else:
        return ()
    if len(vals)>2:
        if vals[2] in packPath:
            Dirpath=packPath[vals[2]]
        else:
            return ()
    else:
        return ()
    extends=c.getElementsByTagName("class")
    if(len(extends)>0):
        extends=extends[0]
        superClass=extends.attributes.values()[0].value
    keys=["superClass"]+keys
    vals=[Dirpath]+[superClass]+vals
    constructors=c.getElementsByTagName("constructor")
    for cons in constructors:
        all_cons.append(constructor(cons,name,Dirpath))
    methods=c.getElementsByTagName("method")
    for met in methods:
        all_methods.append(method(met,name,Dirpath))
    fields=c.getElementsByTagName("field")
    for f in fields:
        all_fields.append(field(f,name,Dirpath))

    #reshape ['superClass', u'included', u'scope', u'qualified', u'name'] to desired shape : superClass exception name externalizable abstract path error included scope serializable
    Dirpath,superClass,included  ,scope,path,name  =vals
    exception,  externalizable, abstract ,error ,serializable=["false","false","true","false","false"]

    vals=[Dirpath,superClass ,exception ,name ,externalizable ,abstract ,path ,error ,included ,scope ,serializable]
    return (vals,all_methods,all_fields,all_cons)


def removeBadChars(x):
    RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
                 u'|' + \
                 u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
                  (unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                   unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                   unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff))
    x = re.sub(RE_XML_ILLEGAL, "?", x)
    stripped = (c for c in x if 0 < ord(c) < 127)
    x=''.join(stripped)
    x = filter(lambda x: x in string.printable, x)
    #x="".join([ch for ch in x if (ch >= 0x0020 and ch <= 0xD7FF)  or ( ch >= 0xE000 and ch <= 0xFFFD ) or ch == 0x0009 or ch == 0x000A or  ch == 0x000D ])
    x = re.sub(u"[^\x01-\x7f]+",u"",x)
    return x.encode("utf-8")



def xmlRead(doc,packPath):
    all_classes=[]
    f=open(doc,"r")
    all=removeBadChars("".join(f.readlines()))
    f.close()
    xmldoc=minidom.parseString(all)
    root=xmldoc.getElementsByTagName("root")[0]
    packs=root.getElementsByTagName("package")
    if len(packs)==0:
        return -1
    package=packs[0]
    classes= package.getElementsByTagName("class")
    for i in range(len(classes)):
        if(i%2==0):
            classAtt = classRead(classes[i],packPath)
            if classAtt!=():
                all_classes.append(classAtt)
    interfaces= package.getElementsByTagName("interface")
    for i in range(len(interfaces)):
            classAtt = interfaceRead(interfaces[i],packPath)
            if classAtt!=():
                all_classes.append(classAtt)
    return all_classes

def build(JavaDocPath,packPath,max):
    docs=[]
    lst= glob.glob(JavaDocPath+"/*.xml")
    i=0
    for doc in lst:
        if (i==max):
            break
        i=i+1
        print(doc)
        r=xmlRead(doc,packPath)
        if r!=-1:
            docs.append(r)
    return docs


if __name__ == "__main__":

    packs = pathPackCsv.projectPathPacks("C:\projs\\antWorking\\vers\ANT_182\\repo")
    print packs.keys()
    a=build("C:\projs\\antWorking\\vers\ANT_170\Jdoc2", packs,-1)
    print a
    print a[0]
#print "\n".join(build("C:\GitHub\\vers\\CDT_8_0_2\Jdoc2",-1))
#build("C:\\tomcat\code\TOMCAT_8_0_4\Jdoc2",-1)