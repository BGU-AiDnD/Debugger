__author__ = 'amir'

import Planner.pomcp.main
import Planner.mcts.main
import Planner.lrtdp.main
import Planner.lrtdp.LRTDPModule
import Diagnoser.diagnoserUtils
import HP_Random


import glob
import os
import csv
import Planning_Results


def mkOneDir(dir):
    if not os.path.isdir(dir):
            os.mkdir(dir)

def runAll(instancesDir, outDir, planners):
    for name,alg in planners:
        outD=os.path.join(outDir,name)
        mkOneDir(outD)
        for f in glob.glob(os.path.join(instancesDir,"*.txt")):
            print f
            file=os.path.join(instancesDir,f)
            outfile=os.path.join(outD,f.split("\\")[-1]+".csv")
            outData=[["Algorithm","precision", "recall", "steps"]] # header
            ei = Diagnoser.diagnoserUtils.readPlanningFile(file)
            outData=outData+[[name]+list(alg(ei))]
            writer=csv.writer(open(outfile,"wb"))
            writer.writerows(outData)


def runAll_optimized(instancesDir, outDir, planners):
    outData=[["file_name","planner","learn_algorithm","pBug","pValid","tests","index","precision","recall","steps", "repr" ]]
    outfile=os.path.join(outDir,"planningMED.csv")
    for f in glob.glob(os.path.join(instancesDir,"*.txt")):
        print f
        learn_alg,pBug,pValid,tests,index=Planning_Results.instance_name_to_meta(os.path.basename(f))
        file=os.path.join(instancesDir,f)
        ei = Diagnoser.diagnoserUtils.readPlanningFile(file)
        for name,alg in planners:
            precision,recall,steps, rpr =alg(ei)
            outData.append([os.path.basename(f), name,learn_alg,pBug,pValid,tests,index,precision,recall,steps, rpr])
            writer=csv.writer(open(outfile,"wb"))
            writer.writerows(outData)

def check__pomcp():
    file="C:\projs\ptry\lrtdp\\30_uniform_1.txt"
    file="C:\projs\ptry\lrtdp\\10_0.6_0.0_0.txt"
    ei=Diagnoser.diagnoserUtils.readPlanningFile(file)
    print Planner.pomcp.main.main(ei)
    print HP_Random.main_HP(ei)


def one_lrtdp(file, epsilon, out_dir, stack, trials):
    ei = Diagnoser.diagnoserUtils.readPlanningFile(file)
    instance = str(epsilon) + "_" + str(stack) + "_" + str(trials)
    instance_file = os.path.join(out_dir, instance + ".csv")

    Planner.lrtdp.LRTDPModule.setVars(ei, epsilon, stack, 50, trials)
    Planner.lrtdp.LRTDPModule.lrtdp()
    precision, recall, steps = Planner.lrtdp.LRTDPModule.evaluatePolicy()
    outData = [["Algorithm", "epsilon", "stack", "trials", "precision", "recall", "steps"]]  # header
    outData += [[instance, str(epsilon), str(stack), str(trials)] + list((precision, recall, steps))]
    writer = csv.writer(open(instance_file, "wb"))
    writer.writerows(outData)


def check_lrtdp(file, out_dir):
    epsilon_start, epsilon_end, epsilon_step = 0.1, 0.51, 0.2
    stack_start, stack_end, stack_step = 10, 31, 10
    trials_start, trials_end, trials_step = 10, 21, 5

    epsilon = epsilon_start
    while epsilon <= epsilon_end:
        stack = stack_start
        while stack <= stack_end:
            trials = trials_start
            while trials <= trials_end:
                print file, epsilon, out_dir, stack, trials
                one_lrtdp(file, epsilon, out_dir, stack, trials)
                trials += trials_step
            stack += stack_step
        epsilon +=epsilon_step

def lrtdp_multi_check(instances_dir, out_dir):
    for f in glob.glob(os.path.join(instances_dir,"*.txt")):
        print f
        file = os.path.join(instances_dir,f)
        out_instance_dir = os.path.join(out_dir, f.split("\\")[-1])
        if not  os.path.isdir(out_instance_dir):
            os.mkdir(out_instance_dir)
        check_lrtdp(file, out_instance_dir)

def mcts_by_approach(approach, iterations):
    def approached_mcts(ei):
        return Planner.mcts.main.main_mcts(ei, approach, iterations)
    return approached_mcts

def lrtdp_by_approach(epsilonArg, iterations, approachArg):
    def approached_lrtdp(ei):
        Planner.lrtdp.LRTDPModule.setVars(ei, epsilonArg, iterations, approachArg)
        return Planner.lrtdp.LRTDPModule.lrtdp()
    return approached_lrtdp

def check_all_planners(instances_dir, out_dir):
    planners=[("mcts_hp",mcts_by_approach("hp", 100) ), ("mcts_entropy",mcts_by_approach("entropy", 100) ),
              ("lrtdp_hp",lrtdp_by_approach(0 , 20, 100,"hp")),("lrtdp_entropy",lrtdp_by_approach(0 , 20, 100,"entropy")),
              ("HP",HP_Random.main_HP), ("entropy", HP_Random.main_entropy),
          ("Random",HP_Random.main_Random), ("initials", HP_Random.only_initials), ("all_tests", HP_Random.all_tests)]
    runAll_optimized(instances_dir, out_dir, planners)

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
        planners = [("mcts_hp", mcts_by_approach("hp", 200)), ("mcts_entropy", mcts_by_approach("entropy", 200)),
                    ("lrtdp_hp", lrtdp_by_approach(0, 200, "hp")),
                    ("lrtdp_entropy", lrtdp_by_approach(0, 200, "entropy")),
                    ("HP", HP_Random.main_HP), ("entropy", HP_Random.main_entropy),
                    ("Random", HP_Random.main_Random), ("initials", HP_Random.only_initials),
                    ("all_tests", HP_Random.all_tests)]
        runAll_optimized(in_dir, out_dir, planners)



if __name__=="__main__":
    ei = Diagnoser.diagnoserUtils.readPlanningFile(r"C:\projs\planning\ant\files_All752\planner\180_uniform_5.txt")
    planners = [("mcts_hp", mcts_by_approach("hp", 200)), ("mcts_entropy", mcts_by_approach("entropy", 200)),
                ("lrtdp_hp", lrtdp_by_approach(0, 200, "hp")), ("lrtdp_entropy", lrtdp_by_approach(0, 200, "entropy")),
                ("HP", HP_Random.main_HP), ("entropy", HP_Random.main_entropy),
                ("Random", HP_Random.main_Random), ("initials", HP_Random.only_initials),
                ("all_tests", HP_Random.all_tests)]
    for name, alg in planners:
        print name
        print alg(ei)
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
