__author__ = 'amir'

import Planner.pomcp.main
import Planner.mcts.main
import Planner.lrtdp.main
import Planner.lrtdp.LRTDPModule
import Diagnoser.diagnoserUtils
import HP_Random
import similarity
import time
import timer


import glob
import gc
import os
import csv
import Planning_Results
from threading import Thread
import functools

def timeout(timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, timeout))]
            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception, e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(timeout)
            except Exception, je:
                print 'error starting thread'
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco

def mkOneDir(dir):
    if not os.path.isdir(dir):
            os.mkdir(dir)
@timeout(3600)
def get_results_from_mdp(ei, alg):
    gc.collect()
    start = time.time()
    precision, recall, steps, rpr = alg(ei)
    total_time = time.time() - start
    return precision, recall, steps, total_time, rpr


def runAll_optimized(instancesDir, outDir, planners):
    outData=[["file_name","planner","learn_algorithm","pBug","pValid","tests","index","precision","recall","steps", "time", "repr" ]]
    outfile=os.path.join(outDir,"planningMED.csv")
    for f in glob.glob(os.path.join(instancesDir,"*.txt")):
        print f
        learn_alg,pBug,pValid,tests,index=Planning_Results.instance_name_to_meta(os.path.basename(f))
        file=os.path.join(instancesDir,f)
        ei = Diagnoser.diagnoserUtils.readPlanningFile(file)
        for name,alg in planners:
            try:
                precision, recall, steps, total_time, rpr = get_results_from_mdp(ei, alg)
                outData.append([os.path.basename(f), name,learn_alg,pBug,pValid,tests,index,precision,recall,steps,total_time, rpr])
                writer=csv.writer(open(outfile,"wb"))
                writer.writerows(outData)
            except:
                pass

def mcts_by_approach(approach, iterations):
    def approached_mcts(ei):
        return Planner.mcts.main.main_mcts(ei, approach, iterations)
    return approached_mcts

def lrtdp_by_approach(epsilonArg, iterations, greedy_action_treshold, approachArg):
    def approached_lrtdp(ei):
        Planner.lrtdp.LRTDPModule.setVars(ei, epsilonArg, iterations, greedy_action_treshold, approachArg)
        return Planner.lrtdp.LRTDPModule.lrtdp()
    return approached_lrtdp

def entropy_by_threshold(threshold):
    return lambda ei: HP_Random.main_entropy(ei, threshold=threshold)

def entropy_by_batch(batch):
    return lambda ei: HP_Random.main_entropy(ei, batch=batch)

def planning_for_project(dir):
    for d in os.listdir(dir):
        if "." in d:
            continue
        if d=="weka":
            continue
        experiment_dir = os.path.join(dir,d)
        in_dir = os.path.join(experiment_dir,"planner")
        out_dir = os.path.join(experiment_dir,"all_planners")
        mkOneDir(out_dir)
        planners = [#("mcts_hp", mcts_by_approach("hp", 200)), ("mcts_entropy", mcts_by_approach("entropy", 200)),
                    # ("lrtdp_hp", lrtdp_by_approach(0, 200, "hp")),
                    ("mcts_hp_100", mcts_by_approach("hp", 100)),
                    ("mcts_hp_70", mcts_by_approach("hp", 70)),
                    ("mcts_hp_50", mcts_by_approach("hp", 50)),
                    ("mcts_hp_10", mcts_by_approach("hp", 10)),
                    ("mcts_hp_5", mcts_by_approach("hp", 5)),
                    # ("lrtdp_entropy", lrtdp_by_approach(0, 200, "entropy")),
                    # ("entropy_0.8", entropy_by_threshold(0.8)),
                    # ("entropy_0.6", entropy_by_threshold(0.6)),
                    # ("entropy_0.4", entropy_by_threshold(0.4)),
                    # ("entropy_0.2", entropy_by_threshold(0.2)),
                    # ("entropy_batch_2", entropy_by_batch(2)),
                    # ("entropy_batch_5", entropy_by_batch(5)),
                    ("HP", HP_Random.main_HP), ("entropy", HP_Random.main_entropy),
                    ("Random", HP_Random.main_Random), ("initials", HP_Random.only_initials),
                    ("all_tests", HP_Random.all_tests)]
        runAll_optimized(in_dir, out_dir, planners)

def test():
    ei = Diagnoser.diagnoserUtils.readPlanningFile(r"C:\Temp\ant_bug\100_uniform_0.txt")
    print ei.calc_precision_recall()
    planners = [ # ("lrtdp_hp_0.3", lrtdp_by_approach(1, 10, 0.3, "hp")),
                 # ("lrtdp_hp_0.7", lrtdp_by_approach(1, 10, 0.7, "hp")),
                 ("lrtdp_hp_0.1", lrtdp_by_approach(1, 10, 0.1, "hp")),
                 #("mcts_hp_50", mcts_by_approach("hp", 50)),
                # ("mcts_hp_10", mcts_by_approach("hp", 200)),
                #("mcts_hp_5", mcts_by_approach("hp", 5)),
                # ("mcts_entropy", mcts_by_approach("entropy", 5)),
                ("HP", HP_Random.main_HP),
                # ("entropy_0.6", entropy_by_threshold(0.6)),
                # ("entropy_0.4", entropy_by_threshold(0.4)),
                # ("entropy_0.2", entropy_by_threshold(0.2)),
                # ("entropy_batch_2", entropy_by_batch(2)),
                # ("entropy_batch_5", entropy_by_batch(5)),
                # ("entropy", HP_Random.main_entropy),
                # ("Random", HP_Random.main_Random), ("initials", HP_Random.only_initials),
                ("all_tests", HP_Random.all_tests)]
    for name, alg in reversed(planners):
        print name
        print get_results_from_mdp(ei,alg)


if __name__ == "__main__":
    pass
    # print a(ei.Copy())
    #check_lrtdp("","")
    #lrtdp_multi_check("C:\projs\lrtdp\instances2", "C:\projs\lrtdp\planners8")
    # check_all_planners("C:\projs\lrtdp\instances3", "C:\projs\planners_check")
    # ei = Diagnoser.diagnoserUtils.readPlanningFile(r"C:\projs\lrtdp\instances\40_uniform_8.txt")
    # for i in xrange(35):
    #     ei.addTest(i)
    # print ei.initial_tests
    # print ei.calc_precision_recall()
    # inDir="C:\\projs\\planningTry\\in"
    # outDir="C:\\projs\\planningTry\\out"
    # runAll(inDir,outDir)

    # path=""
    # for x in ["cdt","orient","ant","poi"]:
    #     planning_for_project(os.path.join(path,x))
