__author__ = 'amir'

import Planner.pomcp.main
import Planner.lrtdp.main
import Diagnoser.diagnoserUtils
import HP_Random

import glob
import os
import csv


planners=[("pomcp",Planner.pomcp.main.main),("lrtdp",Planner.lrtdp.main.main),("HP",HP_Random.main_HP),("Random",HP_Random.main_Random)]
# planners=[("HP",HP_Random.main_HP),("Random",HP_Random.main_Random)]



def mkOneDir(dir):
    if not os.path.isdir(dir):
            os.mkdir(dir)

def runAll(instancesDir, outDir):
    for name,alg in planners:
        outD=os.path.join(outDir,name)
        mkOneDir(outD)
        for f in glob.glob(os.path.join(instancesDir,"*.txt")):
            print f
            file=os.path.join(instancesDir,f)
            outfile=os.path.join(outD,f.split("\\")[-1]+".csv")
            outData=[["Algorithm","precision", "recall", "steps"]] # header
            ei = Diagnoser.diagnoserUtils.readPlanningFile(file)
            outData=outData+[[name]+list(alg(ei.Copy()))]
            writer=csv.writer(open(outfile,"wb"))
            writer.writerows(outData)


def planning_for_project(dir):
    for d in os.listdir(dir):
        if "." in d:
            continue
        if d=="weka":
            continue
        experiment_dir=os.path.join(dir,d)
        in_dir=os.path.join(experiment_dir,"planner")
        out_dir=os.path.join(experiment_dir,"new_planners")
        mkOneDir(out_dir)
        runAll(in_dir, out_dir)


if __name__=="__main__":

    # inDir="C:\\projs\\planningTry\\in"
    # outDir="C:\\projs\\planningTry\\out"
    # runAll(inDir,outDir)

    path=""
    for x in ["cdt","orient","ant","poi"]:
        planning_for_project(os.path.join(path,x))
