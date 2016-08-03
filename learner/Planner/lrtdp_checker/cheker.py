__author__ = 'amir'

import glob
import csv
import os

PATH = r"C:\projs\lrtdp\planners8"
OUT_CSV = os.path.join(PATH, "out.csv")
results = [["instance", "Algorithm", "epsilon", "stack", "trials", "precision", "recall", "steps"]]
for dir_name in glob.glob(os.path.join(PATH,"*")):
    d = os.path.join(PATH, dir_name)
    for experiment in glob.glob(os.path.join(d,"*.csv")):
        exp_file = os.path.join(d, experiment)
        results.append([dir_name[len(PATH) + 1 :]] + [x for x in csv.reader(open(exp_file))][1])
with open(OUT_CSV, "wb") as writer_csv:
    writer = csv.writer(writer_csv)
    writer.writerows(results)