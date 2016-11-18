__author__ = 'amir'

import diffAnalyze.comments
import os
import utilsConf

def commentsSpacesLines(doc):
        comm=diffAnalyze.comments.commLines(doc)
        lines=[x for x in open(doc,"r").readlines()]
        spaces=[]
        ind=0
        for l in lines:
            stp=l.lstrip()
            if stp=="":
                spaces.append(ind)
            ind=ind+1
        return comm,spaces



#print commentsSpacesLines("C:\\GitHub\\vers\\CDT_8_1_2\\org.eclipse.cdt\\memory\\org.eclipse.cdt.debug.ui.memory.traditional\\src\\org\\eclipse\\cdt\\debug\\ui\\memory\\traditional\\IMemoryByte.java","")
@utilsConf.marker_decorator(utilsConf.COMMENTS_SPACES_MARKER)
def create(vers,Path):
    for ver in vers:
        vPath = Path +"\\"+ ver
        commsPath = vPath + "\\commentsSpaces"
        if not os.path.isdir(commsPath):
            os.mkdir(commsPath)
        files = [x.split("\n")[0] for x in open(vPath + "\\javaFiles.txt", "r").readlines()]
        for f in files:
            outPath = commsPath + "\\" + f.split("\\")[-1] + ".txt"
            #print f, outPath
            comm, spaces = commentsSpacesLines(f)
            o = open(outPath, "w")
            o.writelines(["comments\n", str(comm), "\nspaces\n", str(spaces)])


#create(('CDT_8_0_1', 'CDT_8_0_2', 'CDT_8_1_0', 'CDT_8_1_1', 'CDT_8_1_2' ),"C:\\GitHub\\vers\\" )

def read(file):
    spaces=[]
    comms=[]
    if not os.path.isfile(file):
		return [],[]
    lines=[x.split("\n")[0] for x in open(file,"r").readlines()]
    if lines[1]!='[]':
        comms=[int(x) for x in lines[1][1:-1].split(",")]
    if lines[3]!='[]':
        spaces=[int(x) for x in lines[3][1:-1].split(",")]
    return  comms,spaces

#print read("C:\GitHub\\vers\CDT_8_0_1\commentsSpaces\CaseBreakQuickFixTest.java.txt")