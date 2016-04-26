__author__ = 'amir'

import Diagnoser.diagnoserUtils
import Diagnoser.ExperimentInstance
import LRTDP
import LRTDPModule

#### main get experiment instance, return planning report

def main(ei):
    instance = LRTDP.LRTDP(ei,0.7,200,200)
    instance.lrtdp()
    return instance.evaluatePolicy()


def mainModule(ei):
    LRTDPModule.clean()
    LRTDPModule.setVars(ei,0.7,300,200)
    LRTDPModule.lrtdp()
    return LRTDPModule.evaluatePolicy()
    #return LRTDPModule.multiLrtdp()

def run_file(f):
    instance = Diagnoser.diagnoserUtils.readPlanningFile(f)
    return mainModule(instance)

if __name__=="__main__":

    file="C:\projs\ptry\lrtdp\\10_0.6_0.0_15_all.txt"
    instance = Diagnoser.diagnoserUtils.readPlanningFile(file)
    print instance.calc_precision_recall() ,len(instance.initial_tests)


    file="C:\projs\ptry\lrtdp\\10_uniform_15_all.txt"
    instance = Diagnoser.diagnoserUtils.readPlanningFile(file)
    print instance.calc_precision_recall() ,len(instance.initial_tests)

    file="C:\projs\ptry\lrtdp\\10_uniform_15.txt"
    print run_file(file)
    file="C:\projs\ptry\lrtdp\\10_0.6_0.0_15.txt"
    print run_file(file)

