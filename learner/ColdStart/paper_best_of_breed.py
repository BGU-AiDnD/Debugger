import os
from collections import Counter
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
# xgboost
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split
import pickle
from sklearn.utils import check_random_state
from sklearn.model_selection import  KFold
from imblearn.ensemble import BalancedRandomForestClassifier
import from_weka_to_python
end_file_no_process="_no_process.sav"
end_file_no_bugs="_no_bugs.sav"
end_file_all="_all.sav"

all_projects_training_no_process= {}
all_projects_training_no_bugs= {}
all_projects_training_all= {}
all_projects_testing_no_process= {}
all_projects_testing_no_bugs= {}
all_projects_testing_all = {}

results_path = r'D:\Debbuger\GAN'

all_files ={
    "BOOKKEEPER": "D:\Debbuger\GAN\BOOKKEEPER\weka" ,
    "DERBY": "D:\Debbuger\GAN\DERBY\weka",
    "FOP": "D:\Debbuger\GAN\FOP\weka",
    "KAFKA": "D:\Debbuger\GAN\KAFKA\weka",
    "OOZIE": "D:\Debbuger\GAN\OOZIE\weka",
    "OPENNLP": "D:\Debbuger\GAN\OPENNLP\weka",
    "SENTRY": "D:\Debbuger\GAN\SENTRY\weka",
    "TAJO": "D:\Debbuger\GAN\TAJO\weka",
    "TILES": "D:\Debbuger\GAN\TILES\weka"
     }

export_result_by_host_model={
    "BOOKKEEPER": r"D:\Debbuger\GAN\bestOfBreed\BOOKKEEPER",
    "DERBY": r"D:\Debbuger\GAN\bestOfBreed\DERBY",
    "FOP": r"D:\Debbuger\GAN\bestOfBreed\FOP",
    "KAFKA": r"D:\Debbuger\GAN\bestOfBreed\KAFKA",
    "OOZIE": r"D:\Debbuger\GAN\bestOfBreed\OOZIE",
    "OPENNLP": r"D:\Debbuger\GAN\bestOfBreed\OPENNLP",
    "SENTRY": r"D:\Debbuger\GAN\bestOfBreed\SENTRY",
    "TAJO": r"D:\Debbuger\GAN\bestOfBreed\TAJO",
    "TILES": r"D:\Debbuger\GAN\bestOfBreed\TILES"
     }

results_all_projects = pd.DataFrame(
        columns=['cold_start_project','host_model','result_type','features_type','model_source', 'precision_bug', 'recall_bug','F_bug', 'F2_bug','roc_area_bug', 'prc_area_bug', 'precision', 'recall',
                 'F1', 'F2', 'roc_area','prc_area','num_bugs','num_all_inst','precent_bugs'])


def load_arff_from_dir_into_dataFrames_dictionery():
    for key, val in all_files.items():
        print key, "=>", val
        # all_projects_training_selected_features = from_weka_to_python.load_arff(os.path.join(val,from_weka_to_python.training_file))
        all_projects_testing_selected_features = from_weka_to_python.load_arff(os.path.join(val,from_weka_to_python.testing_file))

        # all_projects_training_selected_features = from_weka_to_python.pre_processing(all_projects_training_selected_features)
        all_projects_testing_selected_features['hasBug'] = all_projects_testing_selected_features['hasBug'].map({'valid': 0, 'bugged': 1})
        all_projects_testing_selected_features = from_weka_to_python.pre_processing(all_projects_testing_selected_features)

        # all_projects_training_selected_features = from_weka_to_python.selectFeatures(all_projects_training_selected_features, False, False)
        # all_projects_training_all[key] =all_projects_training_selected_features.copy()
        # all_projects_training_selected_features = from_weka_to_python.selectFeatures(all_projects_training_selected_features, True, False)
        # all_projects_training_no_bugs[key] = all_projects_training_selected_features.copy()
        # all_projects_training_selected_features = from_weka_to_python.selectFeatures(all_projects_training_selected_features, True, True)
        # all_projects_training_no_process[key] = all_projects_training_selected_features.copy()

        all_projects_testing_selected_features = from_weka_to_python.selectFeatures(all_projects_testing_selected_features, False, False)
        all_projects_testing_all[key] = all_projects_testing_selected_features.copy()
        all_projects_testing_selected_features = from_weka_to_python.selectFeatures(all_projects_testing_selected_features, True, False)
        all_projects_testing_no_bugs[key] = all_projects_testing_selected_features.copy()
        all_projects_testing_selected_features = from_weka_to_python.selectFeatures(all_projects_testing_selected_features, True, True)
        all_projects_testing_no_process[key] = all_projects_testing_selected_features.copy()


def find_best_of_breed(dic):
    index = max(dic, key=lambda i: dic[i])
    return index

def export_best_of_breed_result(best_of_breed_project_name,feature_type,feature_chosen):
    model_no_process = pickle.load(open(os.path.join(all_files[best_of_breed_project_name], best_of_breed_project_name + end_file_no_process), 'rb'))
    model_no_bugs = pickle.load(open(os.path.join(all_files[best_of_breed_project_name], best_of_breed_project_name + end_file_no_bugs), 'rb'))
    model_all = pickle.load(open(os.path.join(all_files[best_of_breed_project_name], best_of_breed_project_name + end_file_all), 'rb'))
    for cold_start_proj, files_path in all_files.items():
        num_of_bugs = all_projects_testing_all[cold_start_proj].loc[
            all_projects_testing_all[cold_start_proj]['hasBug'] == 1].shape[0]
        num_of_all_instances = all_projects_testing_all[cold_start_proj].shape[0]
        bug_precent = float(num_of_bugs) / float(num_of_all_instances)

        if feature_type == "all":
            x_test = all_projects_testing_all[cold_start_proj].drop('hasBug', axis=1)
            pred = model_all.predict(x_test)
            create_all_eval_results(True, all_projects_testing_all[cold_start_proj]['hasBug'], pred, cold_start_proj,
                                    best_of_breed_project_name, "testing",
                                    "all", num_of_bugs, num_of_all_instances, bug_precent, "best_of_breed"+feature_chosen)
        elif feature_type == "no_bugs":
            x_test = all_projects_testing_no_bugs[cold_start_proj].drop('hasBug', axis=1)
            pred = model_no_bugs.predict(x_test)
            create_all_eval_results(True, all_projects_testing_all[cold_start_proj]['hasBug'], pred, cold_start_proj,
                                    best_of_breed_project_name, "testing",
                                    "no_bugs", num_of_bugs, num_of_all_instances, bug_precent, "best_of_breed"+feature_chosen)
        elif feature_type == "no_process":
            x_test = all_projects_testing_no_process[cold_start_proj].drop('hasBug', axis=1)
            pred = model_no_process.predict(x_test)
            create_all_eval_results(True, all_projects_testing_all[cold_start_proj]['hasBug'], pred, cold_start_proj,
                                best_of_breed_project_name, "testing",
                                "no_process", num_of_bugs, num_of_all_instances, bug_precent, "best_of_breed"+feature_chosen)


#evaluate results - python
def calculateF2(precision, recall):
    if ((4 * precision) + recall) != 0:
        F2BUGS = (5 * ((precision * recall) / ((4 * precision) + recall)))
    else:
        F2BUGS = 0
    return F2BUGS
def create_all_eval_results(export,y_true, y_pred, key,host_model,result_type,features_type,num_of_bugs,num_of_all_instances,bugs_Precent,from_model):
    precision_bugged = metrics.precision_score(y_true,y_pred,pos_label=1,average='binary')
    recall_bugged = metrics.recall_score(y_true,y_pred,pos_label=1,average='binary')
    f_measure_bugged = metrics.f1_score(y_true,y_pred,pos_label=1,average='binary')
    f2_measure_bugged = calculateF2(precision_bugged,recall_bugged)

    un_true,_ = np.unique(y_true, return_counts=True)
    un_pred,_ = np.unique(y_pred, return_counts=True)
    if len(un_true) ==1 or len(un_pred)==1:
        roc_bugged = '?'
        prc_bugged = '?'
        print("zero")
    else:
        try:
            roc_bugged = metrics.roc_auc_score(y_true,y_pred,average=None)
        except:
            print("exception_roc")
            roc_bugged = '?'
        try:
            precision, recall, thresholds = metrics.precision_recall_curve(y_true, y_pred,pos_label=1)
            prc_bugged = metrics.auc(precision, recall)
        except:
            print("exception_prc")
            prc_bugged = '?'

    precision_all = metrics.precision_score(y_true, y_pred, average='weighted')
    recall_all = metrics.recall_score(y_true, y_pred, average='weighted')
    f_measure_all = metrics.f1_score(y_true, y_pred,average='weighted')
    f2_measure_all = calculateF2(precision_all, recall_all)
    if len(un_true) ==1 or len(un_pred)==1:
        roc_all = 0
        prc_all =  1
        print("zero")
    else:
        try:
            roc_all = metrics.roc_auc_score(y_true, y_pred, average='weighted')
        except:
            print("exception_roc")
            roc_all = 0
        try:
            precision, recall, thresholds = metrics.precision_recall_curve(y_true, y_pred)
            prc_all = metrics.auc(recall, precision)
        except:
            print("exception_prc")
            prc_all = 1


    if export:
        global results_all_projects
        results_all_projects.loc[len(results_all_projects)] = [key,host_model, result_type, features_type, from_model, precision_bugged,
                                                           recall_bugged, f_measure_bugged,
                                                           f2_measure_bugged, roc_bugged, prc_bugged,
                                                           precision_all, recall_all, f_measure_all, f2_measure_all,
                                                           roc_all, prc_all, num_of_bugs, num_of_all_instances,
                                                           bugs_Precent]
    else:
        return np.array(list((precision_bugged,recall_bugged, f_measure_bugged,
                                            f2_measure_bugged, roc_bugged, prc_bugged,
                                            precision_all, recall_all, f_measure_all, f2_measure_all,
                                            roc_all, prc_all, num_of_bugs, num_of_all_instances,
                                            bugs_Precent)))

def runOnAllBestModel(feature_chosen):
    outputDir= "D:\Debbuger\BestModel"
    directory = "D:\Debbuger\Try"
    best_of_breed_all ={}
    best_of_breed_no_bugs ={}
    best_of_breed_no_process ={}
    for host_model, weka_path in all_files.items():
        # first - load all three models
        model_no_process = pickle.load(open(os.path.join(weka_path,host_model+end_file_no_process), 'rb'))
        model_no_bugs = pickle.load(open(os.path.join(weka_path,host_model+end_file_no_bugs), 'rb'))
        model_all = pickle.load(open(os.path.join(weka_path,host_model+end_file_all), 'rb'))
        for cold_start_proj, files_path in all_files.items():
            num_of_bugs = all_projects_testing_all[cold_start_proj].loc[
                all_projects_testing_all[cold_start_proj]['hasBug'] == 1].shape[0]
            num_of_all_instances = all_projects_testing_all[cold_start_proj].shape[0]
            bug_precent = float(num_of_bugs) / float(num_of_all_instances)

            x_test = all_projects_testing_all[cold_start_proj].drop('hasBug', axis=1)
            pred = model_all.predict(x_test)
            create_all_eval_results(True, all_projects_testing_all[cold_start_proj]['hasBug'], pred,cold_start_proj,host_model, "testing",
                                    "all", num_of_bugs, num_of_all_instances, bug_precent, "best_of_breed"+feature_chosen)

            x_test = all_projects_testing_no_bugs[cold_start_proj].drop('hasBug', axis=1)
            pred = model_no_bugs.predict(x_test)
            create_all_eval_results(True, all_projects_testing_all[cold_start_proj]['hasBug'], pred, cold_start_proj,
                                    host_model, "testing",
                                    "no_bugs", num_of_bugs, num_of_all_instances, bug_precent, "best_of_breed"+feature_chosen)

            x_test = all_projects_testing_no_process[cold_start_proj].drop('hasBug', axis=1)
            pred = model_no_process.predict(x_test)
            create_all_eval_results(True, all_projects_testing_all[cold_start_proj]['hasBug'], pred, cold_start_proj,
                                    host_model, "testing",
                                    "no_process", num_of_bugs, num_of_all_instances, bug_precent, "best_of_breed"+feature_chosen)

        global results_all_projects
        results_all_projects.to_csv(os.path.join(export_result_by_host_model[host_model],"all_project.csv"), index=False)

        only_selected = results_all_projects.loc[results_all_projects["features_type"] == 'all']
        try:
            best_of_breed_all[host_model] = only_selected[feature_chosen].mean()
        except:
            print("lambda 1")
            best_of_breed_all[host_model] = only_selected[feature_chosen][lambda x: x != '?'].mean()

        only_selected = results_all_projects.loc[results_all_projects['features_type'] == "no_bugs"]
        try:
            best_of_breed_no_bugs[host_model] = only_selected[feature_chosen].mean()
        except:
            print("lambda 2")
            best_of_breed_no_bugs[host_model] = only_selected[feature_chosen][lambda x: x != '?'].mean()

        only_selected = results_all_projects.loc[results_all_projects['features_type'] == "no_process"]
        try:
            best_of_breed_no_process[host_model] = only_selected[feature_chosen].mean()
        except:
            print("lambda 3")
            best_of_breed_no_process[host_model] = only_selected[feature_chosen][lambda x: x != '?'].mean()

        results_all_projects = pd.DataFrame(
            columns=['cold_start_project', 'host_model', 'result_type', 'features_type', 'model_source',
                     'precision_bug', 'recall_bug', 'F_bug', 'F2_bug', 'roc_area_bug', 'prc_area_bug', 'precision',
                     'recall',
                     'F1', 'F2', 'roc_area', 'prc_area', 'num_bugs', 'num_all_inst', 'precent_bugs'])

    best_of_breed_project_name = find_best_of_breed(best_of_breed_all)
    export_best_of_breed_result(best_of_breed_project_name,"all",feature_chosen)
    best_of_breed_project_name = find_best_of_breed(best_of_breed_no_bugs)
    export_best_of_breed_result(best_of_breed_project_name,"no_bugs",feature_chosen)
    best_of_breed_project_name = find_best_of_breed(best_of_breed_no_process)
    export_best_of_breed_result(best_of_breed_project_name,"no_process",feature_chosen)
    global results_all_projects
    results_all_projects.to_csv(os.path.join(results_path, "best_of_breed_results"+feature_chosen+".csv"), index=False)


load_arff_from_dir_into_dataFrames_dictionery()
runOnAllBestModel("F2_bug")
runOnAllBestModel("roc_area_bug")
runOnAllBestModel("prc_area_bug")
