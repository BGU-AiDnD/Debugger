import os
import glob
import csv

METADATA_DIR = "bugs_files"
DIAGNOSER_OUTPUT_DIR = "out"
NAMED_DIAGNOSER_OUTPUT_DIR = "named2"


def diagnosis_file_to_named_file(diagnoses_file, named_diagnoses_file, files_ids):
    def line_to_named_line(line):
        probability_index = line.index("P")
        return map(lambda id: files_ids[id], line[:probability_index]) + line[probability_index:]

    with open(diagnoses_file) as diagnoses:
        with open(named_diagnoses_file, "wb") as named:
            csv.writer(named).writerows(map(line_to_named_line, list(csv.reader(diagnoses))))


results_dir = r"C:\Users\User\Dropbox\For ori\ant\files_All867"
for experiment_instance in glob.glob(os.path.join(results_dir, METADATA_DIR, "*")):
    used_files = []
    with open(experiment_instance) as experiment:
        lines = map(lambda line: line.replace("\n", ""), experiment.readlines())
        used_files = lines[lines.index("FileNames") + 1].split(",")
    files = dict(map(lambda a: (str(a[0]), a[1].replace("\\", "/")), enumerate(used_files)))
    diagnoser, id = os.path.basename(experiment_instance).split(".")[0].split("_")
    diagnoses_file = os.path.join(results_dir, DIAGNOSER_OUTPUT_DIR,
                                  "DIFG_check_{0}_uniform_{1}.csv.csv".format(diagnoser, id))
    named_diagnoses_file = os.path.join(results_dir, NAMED_DIAGNOSER_OUTPUT_DIR,
                                        "{0}_uniform_{1}.csv".format(diagnoser, id))
    try:
        diagnosis_file_to_named_file(diagnoses_file, named_diagnoses_file, files)
    except:
        pass
