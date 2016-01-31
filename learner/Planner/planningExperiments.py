__author__ = 'amir'

import Planner.pomcp.main
import Planner.lrtdp.main
import Diagnoser.diagnoserUtils
import HP_Random

import glob
import os
import csv


planners=[("pomcp",Planner.pomcp.main.main),("lrtdp",Planner.lrtdp.main.main),("HP",HP_Random.main_HP),("Random",HP_Random.main_Random)]
# planners=[("Random",HP_Random.main_Random)]





def runAll(instancesDir, outDir):
    for f in glob.glob(os.path.join(instancesDir,"*.txt")):
        print f
        file=os.path.join(instancesDir,f)
        outfile=os.path.join(outDir,f.split("\\")[-1]+".csv")
        outData=["Algorithm","precision", "recall", "steps"] # header
        ei = Diagnoser.diagnoserUtils.readPlanningFile(file)
        for name,alg in planners:
            outData=outData+[[name]+list(alg(ei.Copy()))]
        writer=csv.writer(open(outfile,"wb"))
        writer.writerows(outData)



if __name__=="__main__":
    inDir="C:\\projs\\planningTry\\in"
    outDir="C:\\projs\\planningTry\\out"
    runAll(inDir,outDir)