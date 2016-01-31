from Planner.pomcp import MCTSPARAMS, KNOWLEDGE, EXPERIMENTPARAMS, EXPERIMENT, DIAGNOSER

__author__ = 'amir'

import Diagnoser.diagnoserUtils

def main():
    searchParams= MCTSPARAMS.MCTSPARAMS()#MCTS::PARAMS
    expParams= EXPERIMENTPARAMS.EXPERIMENTPARAMS()# EXPERIMENT::PARAMS
    knowledge= KNOWLEDGE.KNOWLEDGE()# SIMULATOR::KNOWLEDGE
    problem=""
    outputfile=""
    policy=""#
    size=0
    number=0
    treeknowledge = 1
    rolloutknowledge = 1
    smarttreecount = 10# int
    smarttreevalue = 1.0#


    #real =NETWORK.NETWORK(size, number)#
    #simulator =NETWORK.NETWORK(size, number)#
    #
    file="C:\projs\\40_weka_randomForest9.txt"
    ei=Diagnoser.diagnoserUtils.readPlanningFile(file)

    real = DIAGNOSER.DIAGNOSER(ei,0.7)#
    simulator = DIAGNOSER.DIAGNOSER(ei.Copy(),0.7)#

    simulator.SetKnowledge(knowledge)#
    experiment = EXPERIMENT.EXPERIMENT(real, simulator, outputfile, expParams, searchParams)#EXPERIMENT
    experiment.DiscountedReturn()#

    return 0#


if __name__=="__main__":
    main()