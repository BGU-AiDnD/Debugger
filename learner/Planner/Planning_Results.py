__author__ = 'amir'

import os
import csv
import glob
import shutil
import numpy as np



def instance_name_to_meta(name):
    vals=name.replace(".txt","").replace(".csv","").split("_")
    tests=vals[0]
    learn_alg="Sanity"
    pBug,pValid="0","0"
    if "randomForest" in name:
        learn_alg="randomForest"
    elif "uniform" in name:
        learn_alg="uniform"
    else:
        pBug=vals[1]
        pValid=vals[2]
        learn_alg=pValid

    index="".join([x for x in vals[-1] if x in "0123456789"])
    return learn_alg,pBug,pValid,tests,index

def get_results_from_csv(csvFile):
    results=[x for x in csv.reader(open(csvFile,"r"))][1]
    alg,precision,recall,steps=results
    return float(precision),float(recall),int(steps)



def result_planner(plannerDir,plannerName):
    all_results=[]
    merged_results=[]
    merged_dict={}
    for f in glob.glob(os.path.join(plannerDir,"*.csv")):
        file=f
        learn_alg,pBug,pValid,tests,index=instance_name_to_meta(f.split("\\")[-1])
        precision,recall,steps=get_results_from_csv(file)
        all_results.append([plannerName,learn_alg,pBug,pValid,tests,index,precision,recall,steps])
        key="_".join([learn_alg,pBug,pValid,tests])
        if key not in merged_dict:
            merged_dict[key]=[]
        merged_dict[key].append([precision,recall,steps])

    for key in merged_dict:
        learn_alg,pBug,pValid,tests=key.split("_")
        lst=merged_dict[key]
        precision,recall,steps=np.mean([x[0] for x in lst]),np.mean([x[1] for x in lst]),np.mean([x[2] for x in lst])
        merged_results.append([plannerName,learn_alg,pBug,pValid,tests,precision,recall,steps])
    return merged_results,all_results





def results_all_planners(planners_dir,outFile,out_med_file):
    planners=["pomcp","lrtdp","HP","Random"]
    outLInes=[["planner","learn_algorithm","pBug","pValid","tests","precision_avg","recall_avg","steps_avg" ]]
    all_results_LInes=[["planner","learn_algorithm","pBug","pValid","tests","index","precision","recall","steps" ]]
    for p in planners:
        merged_results,all_results=result_planner(os.path.join(planners_dir,p),p)
        outLInes=outLInes+merged_results
        all_results_LInes=all_results_LInes+all_results
    writer=csv.writer(open(out_med_file,"wb"))
    writer.writerows(all_results_LInes)
    writer=csv.writer(open(outFile,"wb"))
    writer.writerows(outLInes)


def project_results(projectDir,outName,out_med_name):
    for config_dir in glob.glob(os.path.join(projectDir,"*")):
        if not os.path.isdir(config_dir):
            continue
        results_all_planners(os.path.join(config_dir,"new_planners"),os.path.join(config_dir,outName+".csv"),os.path.join(config_dir,out_med_name+".csv"))


def multiProject(dir,projects):
    for p in projects:
        project_results(os.path.join(dir,p),"out_new_planners","med_new_planners")

# print results_all_planners("E:\\new_planners\\cdt\\new_planners","E:\\new_planners\\cdt\\new_planners\out.csv","E:\\new_planners\\cdt\\new_planners\outMed.csv")

def copy_planners_res(sourceD,destD):
    for root, dirs, files in os.walk(sourceD):
        for name in files:
            if "_new_planners.csv" in name:
                path=os.path.join(root, name)
                new_path=path.replace(sourceD,destD)
                dirs="\\".join(new_path.split("\\")[:-1])
                os.makedirs(dirs)
                shutil.copyfile(path,new_path)

