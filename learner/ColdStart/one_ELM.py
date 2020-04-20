import numpy as np
import arff
import os
import pandas as pd
from scipy.io.arff import loadarff
from sklearn.ensemble import RandomForestClassifier
# xgboost
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import check_random_state
from sklearn.utils.random import sample_without_replacement
from sklearn.model_selection import  KFold
import matplotlib.pyplot as plt
from imblearn.ensemble import BalancedRandomForestClassifier

from sklearn_extensions.extreme_learning_machines.elm import GenELMClassifier
from sklearn_extensions.extreme_learning_machines.random_layer import RBFRandomLayer, MLPRandomLayer


results_all_projects = pd.DataFrame(
        columns=['cold_start_project','model_source', 'precision_bug', 'recall_bug','F_bug', 'F2_bug','roc_area_bug', 'prc_area_bug', 'precision', 'recall',
                 'F1', 'F2', 'roc_area','prc_area','num_bugs_test','num_all_inst_test','percent_bugs_test','num_bugs_train','num_all_inst_train','percent_bugs_train'])

#features to change
def g2_attributes():
    return [("out_degree_public", "NUMERIC"),("katz_centrality(g2_public", "NUMERIC"),
("core_number(g2_public", "NUMERIC"),("closeness_centrality(g2_public", "NUMERIC"),("degree_centrality(g2_public", "NUMERIC"),("out_degree_centrality(g2_public", "NUMERIC"),
("out_degree_protected", "NUMERIC"),("katz_centrality(g2_protected", "NUMERIC"),
("core_number(g2_protected", "NUMERIC"),("closeness_centrality(g2_protected", "NUMERIC"),("degree_centrality(g2_protected", "NUMERIC"),("out_degree_centrality(g2_protected", "NUMERIC"),
("out_degree_private", "NUMERIC"),("katz_centrality(g2_private", "NUMERIC"),
("core_number(g2_private", "NUMERIC"),("closeness_centrality(g2_private", "NUMERIC"),("degree_centrality(g2_private", "NUMERIC"),("out_degree_centrality(g2_private", "NUMERIC"),
("out_degree_all", "NUMERIC"),("katz_centrality(g2_all", "NUMERIC"),
("core_number(g2_all", "NUMERIC"),("closeness_centrality(g2_all", "NUMERIC"),("degree_centrality(g2_all", "NUMERIC"),("out_degree_centrality(g2_all", "NUMERIC")]
def g3_attributes():
    return [("out_degreeG3_public", "NUMERIC"),("core_number(g3_public", "NUMERIC"),("closeness_centrality(g3_public", "NUMERIC"),("degree_centrality(g3_public", "NUMERIC"),("out_degree_centrality(g3_public", "NUMERIC"),
("out_degreeG3_protected", "NUMERIC"),("core_number(g3_protected", "NUMERIC"),("closeness_centrality(g3_protected", "NUMERIC"),("degree_centrality(g3_protected", "NUMERIC"),("out_degree_centrality(g3_protected", "NUMERIC"),
("out_degreeG3_private", "NUMERIC"),("core_number(g3_private", "NUMERIC"),("closeness_centrality(g3_private", "NUMERIC"),("degree_centrality(g3_private", "NUMERIC"),("out_degree_centrality(g3_private", "NUMERIC"),
("out_degreeG3_all", "NUMERIC"),("core_number(g3_all", "NUMERIC"),("closeness_centrality(g3_all", "NUMERIC"),("degree_centrality(g3_all", "NUMERIC"),("out_degree_centrality(g3_all", "NUMERIC")]
def process_attributes(bugs):
    bugs_features = [38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62,
                     63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87,
                     88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
                     110, 111, 112, 113, 114, 115, 116, 117, 118]
    all= [( "tot_changes", "NUMERIC"), ( "sum_insert", "NUMERIC"),
          ( "sum_delets", "NUMERIC"),( "count_insert", "NUMERIC"),
          ( "count_delets", "NUMERIC"),( "avg_insert", "NUMERIC"),
          ( "avg_delets", "NUMERIC"),( "avg_insert_nonzero", "NUMERIC"),
          ( "avg_delets_nonzero", "NUMERIC"), ( "tot_bugs", "NUMERIC"),( "tot_changes_last", "NUMERIC"), ( "sum_insert_last", "NUMERIC"),
          ( "sum_delet_lasts", "NUMERIC"),( "count_insert_last", "NUMERIC"),
          ( "count_delets_last", "NUMERIC"),( "avg_insert_last", "NUMERIC"),
          ( "avg_delets_last", "NUMERIC"),( "avg_insert_nonzero_last", "NUMERIC"),
          ( "avg_delets_nonzero_last", "NUMERIC"), ( "tot_bugs_last", "NUMERIC"), ( "tot_developers", "NUMERIC"),
          ( "lastVer_tot_developers", "NUMERIC"),( "last_commit", "NUMERIC"),( "last_bug", "NUMERIC"),( "last_bug_binary", "NUMERIC"),
          ( "change_set", "NUMERIC"), ( "age", "NUMERIC"),( "age2", "NUMERIC"),( "tot_changes_bugged", "NUMERIC"), ( "sum_insert_bugged", "NUMERIC"),
          ( "sum_delet_buggeds", "NUMERIC"),( "count_insert_bugged", "NUMERIC"),
          ( "count_delets_bugged", "NUMERIC"),( "avg_insert_bugged", "NUMERIC"),
          ( "avg_delets_bugged", "NUMERIC"),( "avg_insert_nonzero_bugged", "NUMERIC"),
          ( "avg_delets_nonzero_bugged", "NUMERIC"),

          ( "tot_changes_p3", "NUMERIC"), ( "sum_insert_p3", "NUMERIC"),
          ( "sum_delet_p3s", "NUMERIC"),( "count_insert_p3", "NUMERIC"),
          ( "count_delets_p3", "NUMERIC"),( "avg_insert_p3", "NUMERIC"),
          ( "avg_delets_p3", "NUMERIC"),( "avg_insert_nonzero_p3", "NUMERIC"),
          ( "avg_delets_nonzero_p3", "NUMERIC"),

          ( "tot_changes_normal", "NUMERIC"), ( "sum_insert_normal", "NUMERIC"),
          ( "sum_delet_normals", "NUMERIC"),( "count_insert_normal", "NUMERIC"),
          ( "count_delets_normal", "NUMERIC"),( "avg_insert_normal", "NUMERIC"),
          ( "avg_delets_normal", "NUMERIC"),( "avg_insert_nonzero_normal", "NUMERIC"),
          ( "avg_delets_nonzero_normal", "NUMERIC"),

          ( "tot_changes_enhancement", "NUMERIC"), ( "sum_insert_enhancement", "NUMERIC"),
          ( "sum_delet_enhancements", "NUMERIC"),( "count_insert_enhancement", "NUMERIC"),
          ( "count_delets_enhancement", "NUMERIC"),( "avg_insert_enhancement", "NUMERIC"),
          ( "avg_delets_enhancement", "NUMERIC"),( "avg_insert_nonzero_enhancement", "NUMERIC"),
          ( "avg_delets_nonzero_enhancement", "NUMERIC"),

          ( "tot_changes_major", "NUMERIC"), ( "sum_insert_major", "NUMERIC"),
          ( "sum_delet_majors", "NUMERIC"),( "count_insert_major", "NUMERIC"),
          ( "count_delets_major", "NUMERIC"),( "avg_insert_major", "NUMERIC"),
          ( "avg_delets_major", "NUMERIC"),( "avg_insert_nonzero_major", "NUMERIC"),
          ( "avg_delets_nonzero_major", "NUMERIC"),
          ( "tot_changes_Ranking", "NUMERIC"), ( "sum_insert_Ranking", "NUMERIC"),
          ( "sum_delet_Rankings", "NUMERIC"),( "count_insert_Ranking", "NUMERIC"),
          ( "count_delets_Ranking", "NUMERIC"),( "avg_insert_Ranking", "NUMERIC"),
          ( "avg_delets_Ranking", "NUMERIC"),( "avg_insert_nonzero_Ranking", "NUMERIC"),
          ( "avg_delets_nonzero_Ranking", "NUMERIC"),


          ( "avg_submit", "NUMERIC"),
          ( "avg_modify", "NUMERIC"),
          ( "distinct_OS", "NUMERIC"),
          ( "distinct_assignedTo", "NUMERIC"),
          ( "distinct_Hardware", "NUMERIC"),
          ( "distinct_Component", "NUMERIC"),
          ( "distinct_Version", "NUMERIC"),
          ( "count_Block", "NUMERIC"),
          ( "count_Depends", "NUMERIC"),

          ( "p1_count", "NUMERIC"), ( "p2_count", "NUMERIC"), ( "p3_count", "NUMERIC"), ( "p4_count", "NUMERIC"), ( "p5_count", "NUMERIC") ,
          ( "p1_count_perc", "NUMERIC"), ( "p2_count_perc", "NUMERIC"), ( "p3_count_perc", "NUMERIC"), ( "p4_count_perc", "NUMERIC"), ( "p5_count_perc", "NUMERIC") ,

          ( "minor_count", "NUMERIC"), ( "normal_count", "NUMERIC"), ( "major_count", "NUMERIC"), ( "enhancement_count", "NUMERIC"), ( "critical_count", "NUMERIC"), ( "blocker_count", "NUMERIC"), ( "trivial_count", "NUMERIC"),
          ( "minor_count_perc", "NUMERIC"), ( "normal_count_perc", "NUMERIC"), ( "major_count_perc", "NUMERIC"), ( "enhancement_count_perc", "NUMERIC"), ( "critical_count_perc", "NUMERIC"), ( "blocker_count_perc", "NUMERIC"), ( "trivial_count_perc", "NUMERIC"),

          ( "avg_commits_files", "NUMERIC"),
          ( "avg_commits_files_bugged", "NUMERIC"),
          ( "avg_commits_files_valid", "NUMERIC")
          ]
    ret=[]
    if bugs:
        for i in range(len(all)):
            if i+1 in bugs_features:
                ret.append(all[i])
    else:
        for i in range(len(all)):
            if i+1 not in bugs_features:
                ret.append(all[i])

    return ret


all_files ={
    "BOOKKEEPER": "D:\Debbuger\GAN\BOOKKEEPER\weka" ,
    "FOP": "D:\Debbuger\GAN\FOP\weka",
    "KAFKA": "D:\Debbuger\GAN\KAFKA\weka",
    "OOZIE": "D:\Debbuger\GAN\OOZIE\weka",
    "OPENNLP": "D:\Debbuger\GAN\OPENNLP\weka",
    "SENTRY": "D:\Debbuger\GAN\SENTRY\weka",
    "TAJO": "D:\Debbuger\GAN\TAJO\weka",
    "TILES": "D:\Debbuger\GAN\TILES\weka"
     }

pojects_training = {}
pojects_testing = {}

training_file = 'All_training_File.arff'
testing_file = "All_testing_File.arff"

#pre-processing to the data:
def selectFeatures(data,remove_bugs = True,remove_process= True):
    g2_f = g2_attributes()
    all2_att_names = [tup[0] for tup in g2_f]
    bugs_f = process_attributes(bugs=True)
    all_bugs_f_names = [tup[0] for tup in bugs_f]
    process_f = process_attributes(bugs=False)
    all_process_f_names = [tup[0] for tup in process_f]
    if all2_att_names[0] in data.columns:
        g3_f = g3_attributes()
        all3_att_names = [tup[0] for tup in g3_f]
        print (data.shape)
        new_data = data.drop(all2_att_names, axis=1)
        print (new_data.shape)
        new_data = new_data.drop(all3_att_names, axis=1)
        print (new_data.shape)
        data = new_data
    if remove_bugs and all_bugs_f_names[0] in data.columns:
        data = data.drop(all_bugs_f_names, axis=1)
    if remove_process and all_process_f_names[0] in data.columns:
        data = data.drop(all_process_f_names, axis=1)
    return data

def pre_processing(data):
    # data = selectFeatures(data)
    # print(data.isnull().sum())
    null_data = data[data.isnull().any(axis=1)]
    print(null_data.shape)
    num_of_rows = null_data.shape[0]
    tr_data_noNa = data.copy()
    if num_of_rows!= 0:
        for col in tr_data_noNa.columns[:-1]:
            if col != 'label' or col != 'hasBug':
                if tr_data_noNa[col].dtype == 'object':
                    #         col_mode = mode(tr_data[col].astype(str)).mode[0]
                    #         tr_data[col].fillna(col_mode,inplace=True)
                    tr_data_noNa[col].fillna("Unknown", inplace=True)
                else:
                    col_mean = data[col].mean()
                    tr_data_noNa[col].fillna(col_mean, inplace=True)
    tr_data_noNa = encode_categorial(tr_data_noNa)
    return tr_data_noNa

def encode_categorial(data):
    true_false_att = ["ONE_elem_params","exception","externalizable",'abstract','error','serializable','ONE_elem_params_constructors']
    for col in data:
        if col == 'IsInterface':
            data[col] = data[col].str.decode('utf-8')
            data[col] = data[col].map({'Interface': 0, 'class': 1})
        elif col == 'Parent':
            data[col] = data[col].str.decode('utf-8')
            data[col] = data[col].map({'Has_parent': 0, 'No_parent': 1})
        elif col == 'scope':
            data[col] = data[col].str.decode('utf-8')
            data[col] = data[col].map({'public': 0, 'protected': 1,'private':2,'default':3})
        elif col in true_false_att:
            data[col] = data[col].str.decode('utf-8')
            data[col] = data[col].map({'true': 1, 'false': 0, 'True': 1, 'False': 0})
    return data


#load arffs
def load_arff(data_arff):
    raw_data = loadarff(data_arff,)
    df_data = pd.DataFrame(raw_data[0])
    df_data = selectFeatures(df_data)
    df_data['hasBug'] = df_data['hasBug'].str.decode('utf-8')
    df_data['hasBug'] = df_data['hasBug'].map({'valid': 0, 'bugged': 1})
    df_data = pre_processing(df_data)
    return df_data

def dump_data(file_name,path,data):
    file_path = os.path.join(path, file_name)
    pickle.dump(data, open(file_path, 'wb'))


def load_arff_from_dir_into_dataFrames_dictionery():
    global pojects_training
    global pojects_testing
    pojects_training = {}
    pojects_testing = {}
    for key, val in all_files.items():
        print (key, "=>", val)
        # all_projects_data[key] = load_arff(val)
        pojects_training[key] = load_arff(os.path.join(val,training_file))
        dump_data(str(key)+"_training.df", val, pojects_training[key])
        pojects_testing[key] = load_arff(os.path.join(val,testing_file))
        dump_data(str(key)+"_testing.df", val, pojects_testing[key])
    return pojects_training,pojects_testing

def load_training_set_all_others(CS_project,training_dic):
    datasets = pd.DataFrame()
    for proj_name, df in training_dic.items():
        if CS_project != proj_name:
            data = df.copy()
            data.reset_index(drop=True, inplace=True)
            datasets = datasets.append(data, ignore_index=True)
    return datasets

#evaluate results - python
def calculateF2(precision, recall):
    if ((4 * precision) + recall) != 0:
        F2BUGS = (5 * ((precision * recall) / ((4 * precision) + recall)))
    else:
        F2BUGS = 0
    return F2BUGS
def create_all_eval_results(export,y_true, y_pred, key,num_of_bugs_test,num_of_all_instances_test,bugs_Precent_test,num_of_bugs_train,num_of_all_instances_train,bugs_Precent_train,from_model):

    un_true, _ = np.unique(y_true, return_counts=True)
    un_pred, _ = np.unique(y_pred, return_counts=True)
    #if len(un_true) == 1 or len(un_pred) == 1:
    y_true.append(0)
    y_true.append(1)
    y_pred.append(0)
    y_pred.append(1)
    y_true.append(0)
    y_true.append(1)
    y_pred.append(1)
    y_pred.append(0)
    #print("zero or ones")

    precision_bugged = metrics.precision_score(y_true, y_pred, pos_label=1, average='binary')
    recall_bugged = metrics.recall_score(y_true, y_pred, pos_label=1, average='binary')
    f_measure_bugged = metrics.f1_score(y_true, y_pred, pos_label=1, average='binary')
    f2_measure_bugged = calculateF2(precision_bugged, recall_bugged)

    try:
        roc_bugged = metrics.roc_auc_score(y_true, y_pred, average=None)
    except:
        print("exception_roc")
        roc_bugged = 0
    try:
        precision, recall, thresholds = metrics.precision_recall_curve(y_true, y_pred, pos_label=1)
        prc_bugged = metrics.auc(precision, recall)
    except:
        print("exception_prc")
        prc_bugged = 1

    precision_all = metrics.precision_score(y_true, y_pred, average='weighted')
    recall_all = metrics.recall_score(y_true, y_pred, average='weighted')
    f_measure_all = metrics.f1_score(y_true, y_pred, average='weighted')
    f2_measure_all = calculateF2(precision_all, recall_all)
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
        results_all_projects.loc[len(results_all_projects)] = [key, from_model, precision_bugged,
                                                           recall_bugged, f_measure_bugged,
                                                           f2_measure_bugged, roc_bugged, prc_bugged,
                                                           precision_all, recall_all, f_measure_all, f2_measure_all,
                                                           roc_all, prc_all, num_of_bugs_test, num_of_all_instances_test,
                                                           bugs_Precent_test, num_of_bugs_train, num_of_all_instances_train,
                                                           bugs_Precent_train]


    return np.array(list((precision_bugged,recall_bugged, f_measure_bugged,
                                            f2_measure_bugged, roc_bugged, prc_bugged,
                                            precision_all, recall_all, f_measure_all, f2_measure_all,
                                            roc_all, prc_all, num_of_bugs_test, num_of_all_instances_test,
                                            bugs_Precent_test, num_of_bugs_train, num_of_all_instances_train,
                                            bugs_Precent_train))) , f2_measure_bugged


def one_ELM(training_dic,testing_dic):
    for proj_name, df in training_dic.items():
        training_set = load_training_set_all_others(proj_name,training_dic)

        print("start process for: "+str(proj_name))
        tr_data_all = training_set.drop('hasBug', axis=1)

        nh = 10
        srhl_rbf = RBFRandomLayer(n_hidden=nh * 2, rbf_width=0.1, random_state=0)
        model = GenELMClassifier(hidden_layer=srhl_rbf)

        model = model.fit(tr_data_all.rename_axis('ID').values, training_set['hasBug'])
        all_x_test = testing_dic[proj_name].copy()
        all_x_test.reset_index(drop=True, inplace=True)
        x_test = all_x_test.copy()
        x_test = x_test.drop('hasBug', axis=1)

        pred = model.predict(x_test.rename_axis('ID').values)

        num_of_bugs_test = all_x_test['hasBug'].tolist().count(1)
        num_of_all_instances_test = len(all_x_test['hasBug'])
        try:
            bug_precent_test = float(num_of_bugs_test) / float(num_of_all_instances_test)
        except:
            bug_precent_test = 0

        num_of_bugs_train = training_set['hasBug'].tolist().count(1)
        num_of_all_instances_train = len(training_set['hasBug'])
        try:
            bug_precent_train = float(num_of_bugs_train) / float(num_of_all_instances_train)
        except:
            bug_precent_train = 0

        create_all_eval_results(True, all_x_test['hasBug'].tolist(),  pred.tolist(), proj_name, num_of_bugs_test, num_of_all_instances_test,
                                    bug_precent_test, num_of_bugs_train, num_of_all_instances_train,
                                    bug_precent_train, "one_ELM")



#load_arff_from_dir_into_dataFrames_dictionery()
#dump_data("all_trainning_dfs.dic",r'D:\Debbuger\ELM',pojects_training)

#dump_data("all_testing_dfs.dic",r'D:\Debbuger\ELM',pojects_testing)
pojects_training = pickle.load(open(r'D:\Debbuger\ELM\all_trainning_dfs.dic', "rb"))
pojects_testing = pickle.load(open(r'D:\Debbuger\ELM\all_testing_dfs.dic', "rb"))

one_ELM(pojects_training,pojects_testing)

results_all_projects.to_csv(r"D:\Debbuger\ELM\ALL_results.csv", index=False)

a = 3















