import os
import csv
import arff
from collections import Counter


def Parse(file):
    f = open(file, "r")
    lines = f.readlines()
    titles = ["TP Rate", "FP Rate", "Precision", "Recall", " F-Measure", "MCC", "ROC Area", "PRC Area"]
    classes = ['bugged', "valid", "both"]
    dict = {}
    if not '=== Detailed Accuracy By Class ===\n' in lines:
        for c in classes:
            dict[c] = {}
            for title in titles:
                dict[c][title] = 0
        return dict
    ind = [i for i, x in enumerate(lines) if x == "=== Detailed Accuracy By Class ===\n"][-1]
    details = [x.lstrip().replace("Weighted Avg.", "").split() for x in lines[ind + 3: ind + 6]]
    details[0] = details[0][:-1]
    details[1] = details[1][:-1]
    for c, p in zip(classes, details):
        dict[c] = {}
        for metric, title in zip(p, titles):
            dict[c][title] = metric
    return dict


def class_distribution(arff_file):
    with open(arff_file) as f:
        a = arff.load(f)
        return dict(Counter([instance[-1] for instance in a['data']]))


def parse_dir(project_dir, class_to_show):
    data = {}
    for bug_type in ["all", "most"]:
        for granularity in ["files", "methods"]:
            results_filename = os.path.join(project_dir, "{0}_{1}_.results".format(bug_type, granularity))
            arff_file = os.path.join(project_dir, "{0}_testing_{1}.arff".format(bug_type, granularity))
            d = Parse(results_filename)[class_to_show]
            d.update(class_distribution(arff_file))
            data["{0}: {1}_{2}".format(os.path.basename(project_dir), bug_type, granularity)] = d
    return data


metrics = ["TP Rate", "FP Rate", "Precision", "Recall", " F-Measure", "MCC", "ROC Area", "PRC Area", 'bugged', "valid"]
headers = ["configuration"] + metrics


def to_list(dir_dict):
    out = []
    for configuration in dir_dict:
        out.append([configuration] + [dir_dict[configuration][metric] for metric in metrics])
    return out


lines = [headers]
for project in ["poi", "ant", "cdt", "orient"]:
    lines.extend(to_list(parse_dir(r"C:\Temp\weka\final\{0}".format(project), "bugged")))
with open(r"C:\Temp\weka\final\data_bugged.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(lines)


