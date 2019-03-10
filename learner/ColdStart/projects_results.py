import os
import csv
import weka_parser
import json

base = r"C:\Users\amirelm\Documents\GitHub\Debugger\Debugger_cache"
experiments_base = os.path.join(base, r"{0}\experiments")
prediction_base = os.path.join(base, r"{0}\weka")

diagnosis_files_all = os.path.join(experiments_base, r"files_all")
diagnosis_files_most = os.path.join(experiments_base, r"files_most")
diagnosis_methods_all = os.path.join(experiments_base, r"methods_all")
diagnosis_methods_most = os.path.join(experiments_base, r"methods_most")
diagnoses_results = {"files_all": diagnosis_files_all, "files_most": diagnosis_files_most, "methods_all": diagnosis_methods_all, "methods_most": diagnosis_methods_most}
prediction_files_all = os.path.join(prediction_base, r"testingfiles_All.txt")
prediction_files_most = os.path.join(prediction_base, r"testingfiles_Most.txt")
prediction_methods_all = os.path.join(prediction_base, r"testingmethods_All.txt")
prediction_methods_most = os.path.join(prediction_base, r"testingmethods_Most.txt")
prediction_results = {"files_all": prediction_files_all, "files_most": prediction_files_most, "methods_all": prediction_methods_all, "methods_most": prediction_methods_most}


class Project(object):
    def __init__(self, project_name):
        self.project_name = project_name
        self.has_prediction = Project.has_prediction(self.project_name)
        self.has_diagnosis = Project.has_diagnosis(self.project_name)
        if self.has_prediction:
            self.prediction = self.read_prediction()
        if self.has_diagnosis:
            self.diagnosis = self.read_diagnosis()

    @staticmethod
    def has_files(project, files):
        return all(map(lambda res: os.path.exists(res.format(project)), files))

    @staticmethod
    def has_diagnosis(project):
        return Project.has_files(project, diagnoses_results.values())

    @staticmethod
    def has_prediction(project):
        return Project.has_files(project, prediction_results.values())

    @staticmethod
    def read_diagnosis_file(path):
        with open(path) as f:
            return json.loads(f.read())

    def read_diagnosis(self):
        results = dict.fromkeys(diagnoses_results.keys())
        for configuration in results:
            results[configuration] = Project.read_diagnosis_file(diagnoses_results[configuration].format(self.project_name))
        return results

    def read_prediction(self):
        results = dict.fromkeys(prediction_results.keys())
        for configuration in results:
            with open(prediction_results[configuration].format(self.project_name)) as f:
                results[configuration] = weka_parser.parse_WEKA_scores(f.read())
        return results


def write_diagnosis_results(projects, out_path):
    scores = []
    header = ['project', 'configuration']
    rows = []
    for project in projects:
        for configuration in project.diagnosis:
            for ind in project.diagnosis[configuration]:
                if len(scores) == 0:
                    scores = project.diagnosis[configuration][ind].keys()
                rows.append([project.project_name, configuration, ind] + map(lambda score: project.diagnosis[configuration][ind][score], scores))
    rows = [header + scores] + rows
    with open(out_path, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def write_prediction_results(projects, out_path):
    scores = ['PRC Area', 'ROC area', 'F-measure', 'FP rate', 'recall', 'MCC', 'TP rate', 'precision']
    header = ['project', 'configuration', 'class'] + scores
    rows = [header]
    for project in projects:
        for configuration in project.prediction:
            for test_class in project.prediction[configuration]['test']['accuracy by class']:
                rows.append([project.project_name, configuration, test_class] + map(lambda score: project.prediction[configuration]['test']['accuracy by class'][test_class][score], scores))
    with open(out_path, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def write_meta_data(projects, out_path):
    pass


def main():
    projects = map(Project, os.listdir(base))
    prediction = filter(lambda p: p.has_prediction and sum(p.prediction['files_all']['test']['confusion matrix']['bugged'].values()) > 0, projects)
    diagnosis = filter(lambda p: p.has_diagnosis, projects)
    write_meta_data(prediction + diagnosis, "meta_data.csv")
    write_prediction_results(prediction, "prediction.csv")
    write_diagnosis_results(diagnosis, "diagnosis.csv")
    pass


if __name__ == "__main__":
    main()