from utils.monitors_manager import monitor, COMMENTS_SPACES_MARKER
from utils.filesystem import convert_to_long_path

__author__ = 'amir'

import diffAnalyze.comments
import os


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


@monitor(COMMENTS_SPACES_MARKER)
def create(vers, Path):
    for ver in vers:
        vPath = os.path.join(Path, ver)
        commsPath = os.path.join(vPath, "commentsSpaces")
        if not os.path.isdir(commsPath):
            os.mkdir(commsPath)
        files = [convert_to_long_path(x.split("\n")[0]) for x in open(os.path.join(vPath, "javaFiles.txt"), "r").readlines()]
        for f in files:
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