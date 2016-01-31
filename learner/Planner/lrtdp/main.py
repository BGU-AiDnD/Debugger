__author__ = 'amir'

import Diagnoser.diagnoserUtils
import Diagnoser.ExperimentInstance
import LRTDP
import LRTDPModule


#### main get experiment instance, return planning report

def main(ei):

    instance=LRTDP.LRTDP(ei,0.8,200,200)
    instance.lrtdp()
    return instance.evaluatePolicy()


def mainModule(ei):
    LRTDPModule.setVars(ei,0.5,300,200)
    LRTDPModule.lrtdp()
    return LRTDPModule.evaluatePolicy()
    #return LRTDPModule.multiLrtdp()

if __name__=="__main__":
    file="C:\projs\\40_uniform_9.txt"
    instance = Diagnoser.diagnoserUtils.readPlanningFile(file)
    #main(instance)
    print mainModule(instance)