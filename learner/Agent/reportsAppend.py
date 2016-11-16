__author__ = 'amir'
from xml.dom import minidom
import glob

def reportsAppend(Path, out):
    lst= glob.glob(Path+"\\*.xml")
    childs=[]
    for doc in lst:
        xmldoc=minidom.parse(open(doc,"r"))
        suite=xmldoc.getElementsByTagName("testsuite")[0]
        tests= suite.getElementsByTagName("testcase")
        for i in range(len(tests)):
            childs.append(tests[i].toprettyxml())

    header="""<?xml version="1.0" ?>\n<testsuite>\n"""
    footer="</testsuite>"
    f=open(out, 'w')
    f.writelines([header])
    f.writelines(childs)
    f.writelines([footer])
    f.close()

def test(c):
    fail=c.getElementsByTagName("failure")
    out=len(fail)
    err=c.getElementsByTagName("error")
    if out==0:
        out=len(err)
    return (c.attributes["classname"].value+"."+c.attributes["name"].value,out)


def xmlReadTest(doc):
    outs=[]
    xmldoc=minidom.parse(open(doc,"r"))
    suite=xmldoc.getElementsByTagName("testsuite")[0]
    tests= suite.getElementsByTagName("testcase")
    for i in range(len(tests)):
        outs.append(test(tests[i]))
    return outs


def testsClasses(doc):
    outs=[]
    xmldoc=minidom.parse(open(doc,"r"))
    suite=xmldoc.getElementsByTagName("testsuite")[0]
    tests= suite.getElementsByTagName("testcase")
    for i in range(len(tests)):
        outs.append(tests[i].attributes["classname"].value)
    return outs
