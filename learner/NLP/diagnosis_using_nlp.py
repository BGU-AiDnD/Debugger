import os
import glob
import csv
from sklearn.metrics import precision_recall_fscore_support
import nlp_model
import numpy as np

METADATA_DIR = "bugs_files"
DIAGNOSER_OUTPUT_DIR = "out"
NAMED_DIAGNOSER_OUTPUT_DIR = "named2"

def diagnosis_file_to_named_file(diagnoses_file, named_diagnoses_file, files_ids):
    def line_to_named_line(line):
        probability_index = line.index("P")
        return map(lambda id: files_ids[id], line[:probability_index]) + line[probability_index:]

    with open(diagnoses_file) as diagnoses:
        with open(named_diagnoses_file, "wb") as named:
            csv.writer(named).writerows(map(line_to_named_line,list(csv.reader(diagnoses))))

def main():
    results_dir = r"C:\Users\User\Dropbox\For ori\ant\files_All867"
    for experiment_instance in glob.glob(os.path.join(results_dir, METADATA_DIR, "*")):
        used_files = []
        with open(experiment_instance) as experiment:
            lines = map(lambda line: line.replace("\n", ""), experiment.readlines())
            used_files = lines[lines.index("FileNames") + 1].split(",")
        files = dict(map(lambda a : (str(a[0]),a[1].replace("\\","/")), enumerate(used_files)))
        diagnoser, id = os.path.basename(experiment_instance).split(".")[0].split("_")
        diagnoses_file = os.path.join(results_dir, DIAGNOSER_OUTPUT_DIR, "DIFG_check_{0}_uniform_{1}.csv.csv".format(diagnoser, id))
        named_diagnoses_file = os.path.join(results_dir, NAMED_DIAGNOSER_OUTPUT_DIR, "{0}_uniform_{1}.csv".format(diagnoser, id))
        try:
            diagnosis_file_to_named_file(diagnoses_file, named_diagnoses_file, files)
        except:
            pass

def read_nlp_data(nlp_path):
    with open(nlp_path) as f:
        reader = csv.reader(f)
        similarities = {}
        for comp_a, comp_b, similarity in reader:
            similarities.setdefault(min(comp_a, comp_b), {})[max(comp_a, comp_b)] = similarity
        return similarities

class Diagnosis(object):
    def __init__(self, diagnosis, probability, bugs):
        self.diagnosis = diagnosis
        self.probability = probability
        self.bugs = bugs

    def get_precision(self):
        tp, fn, fp = self.get_confusion_matrix()
        return 0.0 if (tp + fp) == 0 else tp / (tp + fp)

    def get_recall(self):
        tp, fn, fp = self.get_confusion_matrix()
        return 0.0 if (tp + fn) == 0 else tp / (tp + fn)

    def get_confusion_matrix(self):
        tp = len([comp for comp in self.diagnosis if comp in self.bugs])
        fn = len([comp for comp in self.bugs if comp not in self.diagnosis])
        fp = len([comp for comp in self.diagnosis if comp not in self.bugs])
        return float(tp), float(fn), float(fp)

    def get_probability(self, alpha = 0.0):
        return self.probability

class NLP_Diagnosis(Diagnosis):
    def __init__(self, diagnosis, probability, bugs, nlp_data):
        super(NLP_Diagnosis, self).__init__(diagnosis, probability, bugs)
        self.nlp_data = nlp_data

    def get_diagnosis_similarities(self):
        similarity_factor = 1.0
        for ind, comp_a in enumerate(self.diagnosis):
            for comp_b in self.diagnosis[ind + 1:]:
                similarity_factor *= self.nlp_data.score(comp_a, comp_b)
        return similarity_factor

    def get_probability(self, alpha = 0.0):
        return alpha * self.get_diagnosis_similarities() + (1 - alpha) * super(NLP_Diagnosis, self).get_probability()

class Diagnosis_Results(object):
    def __init__(self, diagnosis_file, bugs, nlp_data = None):
        self.diagnoses = []
        self.bugs = bugs
        self.init_diagnoses(bugs, diagnosis_file, nlp_data)

    def init_diagnoses(self, bugs, diagnosis_file, nlp_data = None):
        with open(diagnosis_file) as f:
            for diagnosis_line in csv.reader(f):
                probability_index = diagnosis_line.index("P")
                self.diagnoses.append(Diagnosis(diagnosis_line[:probability_index],
                                                float(diagnosis_line[probability_index + 1]),
                                                bugs))

    def get_weighted_precision(self, alpha = 0.0):
        sum_probabilities = 0.0 + reduce(lambda d1,d2: d1 + d2, map(lambda d1: d1.get_probability(alpha), self.diagnoses))
        return reduce(lambda d1,d2: d1 + d2, map(lambda d1: (d1.get_probability(alpha)/ sum_probabilities) * d1.get_precision(), self.diagnoses))

    def get_weighted_recall(self, alpha = 0.0):
        sum_probabilities = 0.0 + reduce(lambda d1,d2: d1 + d2, map(lambda d1: d1.get_probability(alpha), self.diagnoses))
        return reduce(lambda d1,d2: d1 + d2, map(lambda d1: (d1.get_probability(alpha)/ sum_probabilities) * d1.get_recall(), self.diagnoses))


class NLP_Diagnosis_Results(Diagnosis_Results):
    def init_diagnoses(self, bugs, diagnosis_file, nlp_data):
        with open(diagnosis_file) as f:
            for diagnosis_line in csv.reader(f):
                probability_index = diagnosis_line.index("P")
                self.diagnoses.append(NLP_Diagnosis(diagnosis_line[:probability_index],
                                                float(diagnosis_line[probability_index + 1]),
                                                bugs, nlp_data))


similarities = read_nlp_data(r"C:\Users\User\Downloads\ANT_cosine_similarity.csv")
results_dir = r"C:\Users\User\Dropbox\For ori\ant\files_All867"
model = nlp_model.build_model(r"C:\Temp\Ant_for_NLP.csv")
model.save(r'C:\temp\temp_model')
out_file = r"C:\temp\nlp_diagnosis.csv"
out_lines = [["file", "alpha", "diagnosis_precision", "diagnosis_recall", "nlp_precision", "nlp_recall"]]
for experiment_instance in glob.glob(os.path.join(results_dir, METADATA_DIR, "*")):
    used_files = []
    with open(experiment_instance) as experiment:
        lines = map(lambda line: line.replace("\n", ""), experiment.readlines())
        used_files = lines[lines.index("FileNames") + 1].split(",")
        bugged_ids = lines[lines.index("Bugged") + 1].split(",")
    files = dict(map(lambda a : (str(a[0]),a[1].replace("\\","/")), enumerate(used_files)))
    bugged_files = map(lambda id: files[id], bugged_ids)
    try:
        diagnoser, id = os.path.basename(experiment_instance).split(".")[0].split("_")
        named_diagnoses_file = os.path.join(results_dir, NAMED_DIAGNOSER_OUTPUT_DIR, "{0}_uniform_{1}.csv".format(diagnoser, id))
        results = Diagnosis_Results(named_diagnoses_file, bugged_files)
        nlp_results = NLP_Diagnosis_Results(named_diagnoses_file, bugged_files, model)
        print named_diagnoses_file
        for alpha in [0, 0.1,0.2, 0.3, 0.4, 0.5, 0.6 , 0.7, 0.8, 0.9, 1]:
            out_lines.append([os.path.basename(named_diagnoses_file), str(alpha),
                          str(results.get_weighted_precision(alpha)), str(results.get_weighted_recall(alpha))
            , str(nlp_results.get_weighted_precision(alpha)), str(nlp_results.get_weighted_recall(alpha))])
    except:
        pass

with open(out_file, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(out_lines)