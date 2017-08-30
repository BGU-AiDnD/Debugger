from numpy.lib.function_base import average

__author__ = 'Amir-pc'

from xml.dom import minidom
import docXml
import numpy
from collections import Counter

# for %%f in (CDT_8_0_1,CDT_8_0_2,CDT_8_0_3,CDT_8_1_0,CDT_8_1_1,CDT_8_1_2 ) do  java -jar checkstyle-5.7-all.jar -c cycl.xml -r ../%%f/org.eclipse.cdt/ -f xml -o ../mccabe/%%f.xml

# VisibilityModifier
# Nested if-else depth is 1
def getVal(ind,msg):
    spl=msg.split(" ")
    if( len(spl)<=ind):
        return -1
    val=(spl[ind]).replace(",","")
    if (val!="-" ):
        return min([9999,int(val)])
    else:
        return 0

def getAposVal(ind, msg):
    spl=msg.split(" ")
    if( len(spl)<=ind):
        return -1
    val=(spl[ind]).replace(",","")
    val=val.replace("&apos;","")
    if (val!="-"):
        return val
    else:
        return 0

def mccabe():
    return (3,"Cyclomatic Complexity")

def MagicNumber():
    return (0," is a magic number.")

def FileLen():
    return (3,"File length is")

def RedundantImport():
    return (30,"Redundant import from the same package")

def UnusedImports():
    return (30,"Unused import ")

def NCSSComplexity():
    return (5,"NCSS for this file is")

def JavaNCSS():
    return (5,"NCSS for this method is ")

def RequireThis():
    return (50,"Method call to  ")

def RequireThisVar():
    return (50,"Reference to instance variable  ")

def Outer():
    return (4,"Outer types defined")

def AnonInnerLength():
    return (5,"Anonymous inner class length is ")

def AvoidNestedBlocks():
    return (50,"Avoid nested blocks.")

def publicMethods():
    return (5,"Number of public methods")

def protectedMethods():
    return (5,"Number of protected methods")

def privateMethods():
    return (5,"Number of private methods")

def TotalMethods():
    return (5,"Total number of methods")

def FanOutComplexity():
    return (4,"Class Fan-Out Complexity")

def BooleanExpressionComplexity():
    return (4,"Boolean expression complexity is")

def NPathComplexity():
    return (3, "NPath Complexity is")

def Throws():
    return (3,"Throws count is")

def coupling():
    return (5,"Class Data Abstraction Coupling is")

def execs():
    return (4,"Executable statement count is ")

def methodLen():
    return (3,"Method length is")

def Fordepth():
    return (4,"Nested for depth is")

def Ifdepth():
    return (4,"Nested if-else depth is")

def NestedTryDepth():
    return (4,"Nested try depth is")

def OneStatementPerLine():
    return (50,"Only one statement per line allowed.")

def ParameterNumber():
    return (5,"More than 0 parameters (found .")


def stat(lst):
    counts= Counter(lst)
    return len(lst),sum(lst),numpy.mean(lst),numpy.median(lst),numpy.var(lst),max(lst),min(lst), 1==len(counts)

#def fileRead(doc,max1,isAnalyze=False, CodePath='org.eclipse.cdt'):
def fileRead(doc,max1,isAnalyze, CodeDir):
    f=open(doc)
    couner=0
    lines=[]
    ans=[]
    x=0
    for line in f:
        x=x+1
        if(x<=2):
            continue
        lines.append(line)
        if line=="</file>\n":
            #print lines[28][72:]
            chars = docXml.removeBadChars("".join(lines))
            chars="".join([ch for ch in chars.split("\n") if "checks.coding.MultipleStringLiteralsCheck" not in ch])
            #print chars.split("\n")[28]
            xmldoc=minidom.parseString(chars)
            lines=[]
            files=xmldoc.getElementsByTagName("file")
            for i in range(len(files)):
                name= files[i].attributes["name"].value
                if(not ".java" in name):
                    continue
                s=name.split('\\')
                name='\\'.join(s[s.index(CodeDir)+1:])
                errors=files[i].getElementsByTagName("error")
                if couner==max1:
                    return ans
                couner=couner+1

                mccab=[]
                fanOut=[]
                NPath=[]
                JavaNCSSmet=[]
                magicNums=[]
                importStam=[]
                memberCall=[]
                varsCall=[]
                outr=[]
                inner=[]
                nested=[]
                boolComplex=[]
                thorwsSTM=[]
                coupl=[]
                executables=[]
                lens=[]
                fors=[]
                ifs=[]
                tries=[]
                onePerLine=[]

                NCSS=0
                FileL=0
                publics=0
                protecteds=0
                privates=0
                totals=0
                params=[]
                for j in range(len(errors)):
                    value__split = errors[j].attributes["message"].value
                    if("=/**"==value__split):
                        continue
                    mc=mccabe()
                    if(value__split.startswith(mc[1])):
                        mccab.append(getVal(mc[0],value__split))
                    mc=FanOutComplexity()
                    if(value__split.startswith(mc[1])):
                        fanOut.append(getVal(mc[0],value__split))
                    mc=NPathComplexity()
                    if(value__split.startswith(mc[1])):
                        NPath.append(getVal(mc[0],value__split))
                    mc=JavaNCSS()
                    if(value__split.startswith(mc[1])):
                        JavaNCSSmet.append(getVal(mc[0],value__split))
                    mc=MagicNumber()
                    if(value__split.startswith(mc[1])):
                        magicNums.append(getVal(mc[0],value__split))
                    mc=RedundantImport()
                    if(value__split.startswith(mc[1])):
                        importStam.append(getVal(mc[0],value__split))
                    mc=UnusedImports()
                    if(value__split.startswith(mc[1])):
                        importStam.append(getVal(mc[0],value__split))
                    mc=RequireThis()
                    if(value__split.startswith(mc[1])):
                        memberCall.append(getVal(mc[0],value__split))
                    mc=RequireThisVar()
                    if(value__split.startswith(mc[1])):
                        varsCall.append(getVal(mc[0],value__split))
                    mc=Outer()
                    if(value__split.startswith(mc[1])):
                        outr.append(getVal(mc[0],value__split))
                    mc=AnonInnerLength()
                    if(value__split.startswith(mc[1])):
                        inner.append(getVal(mc[0],value__split))
                    mc=AvoidNestedBlocks()
                    if(value__split.startswith(mc[1])):
                        nested.append(getVal(mc[0],value__split))
                    mc=BooleanExpressionComplexity()
                    if(value__split.startswith(mc[1])):
                        boolComplex.append(getVal(mc[0],value__split))
                    mc=Throws()
                    if(value__split.startswith(mc[1])):
                        thorwsSTM.append(getVal(mc[0],value__split))
                    mc=coupling()
                    if(value__split.startswith(mc[1])):
                        coupl.append(getVal(mc[0],value__split))
                    mc=execs()
                    if(value__split.startswith(mc[1])):
                        executables.append(getVal(mc[0],value__split))
                    mc=methodLen()
                    if(value__split.startswith(mc[1])):
                        l=getVal(mc[0],value__split)
                        lens.append(l)
                    mc=Fordepth()
                    if(value__split.startswith(mc[1])):
                        fors.append(getVal(mc[0],value__split))
                    mc=Ifdepth()
                    if(value__split.startswith(mc[1])):
                        ifs.append(getVal(mc[0],value__split))
                    mc=NestedTryDepth()
                    if(value__split.startswith(mc[1])):
                        tries.append(getVal(mc[0],value__split))
                    mc=OneStatementPerLine()
                    if(value__split.startswith(mc[1])):
                        onePerLine.append(getVal(mc[0],value__split))

                    mc=NCSSComplexity()
                    if(value__split.startswith(mc[1])):
                        NCSS=max(getVal(mc[0],value__split),NCSS)
                    mc=FileLen()
                    if(value__split.startswith(mc[1])):
                        FileL=max(getVal(mc[0],value__split),FileL)
                    mc=publicMethods()
                    if(value__split.startswith(mc[1])):
                        publics=max(getVal(mc[0],value__split),publics)
                    mc=protectedMethods()
                    if(value__split.startswith(mc[1])):
                        protecteds=max(getVal(mc[0],value__split),protecteds)
                    mc=privateMethods()
                    if(value__split.startswith(mc[1])):
                        privates=max(getVal(mc[0],value__split),privates)
                    mc=TotalMethods()
                    if(value__split.startswith(mc[1])):
                        totals=max(getVal(mc[0],value__split),totals)
                    mc=ParameterNumber()
                    if(value__split.startswith(mc[1])):
                        params.append(getVal(mc[0],value__split))
                if mccab==[]:
                    mccab=[-999]
                if fanOut==[]:
                    fanOut=[-999]
                if NPath==[]:
                    NPath=[-999]
                if JavaNCSSmet==[]:
                    JavaNCSSmet=[-999]
                if magicNums==[]:
                    magicNums =[-999]
                if importStam==[]:
                    importStam=[-999]
                if memberCall==[]:
                    memberCall =[-999]
                if varsCall==[]:
                    varsCall =[-999]
                if outr==[]:
                    outr =[-999]
                if inner==[]:
                    inner =[-999]
                if nested==[]:
                    nested =[-999]
                if boolComplex==[]:
                    boolComplex =[-999]
                if thorwsSTM==[]:
                    thorwsSTM =[-999]
                if coupl==[]:
                    coupl=[-999]
                if executables==[]:
                    executables=[-999]
                if lens==[]:
                    lens =[-999]
                if fors==[]:
                    fors=[0]
                if ifs==[]:
                    ifs=[0]
                if tries==[]:
                    tries =[0]
                if onePerLine==[]:
                    onePerLine =[-999]


                if params==[]:
                    params =[-999]
                fileP=[name,NCSS,FileL]
                fileP.append(sum(fors))
                fileP.append(sum(ifs))
                fileP.append(sum(tries))
                fileP.extend(list(stat(mccab)))
                fileP.extend(list(stat(fanOut)))
                fileP.extend(list(stat(NPath)))
                fileP.extend(list(stat(JavaNCSSmet)))
                fileP.extend(list(stat(thorwsSTM)))
                fileP.extend(list(stat(coupl)))
                fileP.extend(list(stat(executables)))
                fileP.extend(list(stat(lens)))
                if isAnalyze:
                    fileP.extend([publics,protecteds,privates,totals])
                    fileP.extend(list(stat(params)))
                #fileP.extend(list(stat(magicNums)))
                #fileP.extend(list(stat(importStam)))
                #fileP.extend(list(stat(memberCall)))
                #fileP.extend(list(stat(varsCall)))
                #fileP.extend(list(stat(outr)))
                #fileP.extend(list(stat(inner)))
                #fileP.extend(list(stat(nested)))
                #fileP.extend(list(stat(boolComplex)))
                ans=ans+[fileP]
        else:
            continue
    return ans

def checkStyleCreateDict(lines,repoPath):
    methods={}
    for o in lines:
        if o == "":
            continue
        if not "@" in o:
            continue
        file, data = o.split(" ")
        data=data.split("\n")[0]
        file=file.split(".java")[0]+".java"
        name, begin, end = data.split("@")
        fileName = file[len(repoPath)+1:]
        methodDir = fileName + "$" + name
        if not methodDir in methods:
            methods[methodDir] = {}
        if not "methodName" in methods[methodDir]:
            methods[methodDir]["methodName"] = name
        if not "fileName" in methods[methodDir]:
            methods[methodDir]["fileName"] = fileName
        if not "beginLine" in methods[methodDir]:
            methods[methodDir]["beginLine"] = begin
        if not "EndLine" in methods[methodDir]:
            methods[methodDir]["EndLine"] = end
    return methods


def analyzeCheckStyle(checkOut,repoPath):
    f=open(checkOut,"r")
    lines=f.readlines()
    f.close()
    lines=lines[1:-3]
    ans=[]
    methods=checkStyleCreateDict(lines,repoPath)
    for methodDir  in methods:
        begin=0
        end=0
        fileName=""
        methodName=""
        if "fileName" in methods[methodDir]:
            fileName=methods[methodDir]["fileName"]
        if "methodName" in methods[methodDir]:
            methodName=methods[methodDir]["methodName"]
        if "beginLine" in methods[methodDir]:
            begin=methods[methodDir]["beginLine"]
        if "EndLine" in methods[methodDir]:
            end=methods[methodDir]["EndLine"]
        row=[methodDir,fileName,methodName,str(begin),str(end)]
        ans.append(row)
    return ans



if __name__ == "__main__":
    ans= analyzeCheckStyle("C:\projs\poi2Working\\vers\checkAllMethodsData\\REL_3_7.txt","C:\projs\poi2Working\\vers\\REL_3_7\\repo")
    #fileRead("C:\projs\\antWorking\\vers\checkAll\\ANT_170.xml",-1,False,"repo")
