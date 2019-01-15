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


@utilsConf.marker_decorator(utilsConf.COMMENTS_SPACES_MARKER)
def create(vers, Path):
    for ver in vers:
        vPath = os.path.join(Path, ver)
        commsPath = os.path.join(vPath, "commentsSpaces")
        if not os.path.isdir(commsPath):
            os.mkdir(commsPath)
        java_files = []
        for root, _, files in os.walk(os.path.join(vPath,"repo")):
            java_files.extend(map(lambda file_name: utilsConf.to_short_path(os.path.join(root, file_name)),
                                  filter(lambda file_name: file_name.endswith('.java'), files)))
        for f in java_files:
            if not os.path.isfile(f):
                continue
            outPath = os.path.join(commsPath, os.path.basename(f) + ".txt")
            comm, spaces = commentsSpacesLines(f)
            with open(outPath, "w") as out:
                out.writelines(["comments\n", str(comm), "\nspaces\n", str(spaces)])


def read(file):
    if not os.path.isfile(file):
        return [], []
    with open(file) as f:
        lines=[x.split("\n")[0] for x in f.readlines()]
        comms = eval(lines[1])
        spaces = eval(lines[3])
        return comms,spaces