from collections import Counter
import numpy as np
import arff
import os
import learner.ColdStart.weka_parser
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


# mycomp:
wekaJar = 'C:\\Users\\USER\\Documents\\Debugger\\Debugger\\utils\\weka.jar'  # os.path.join(utilsPath, "weka.jar")

# server:
# wekaJar = 'C:\\Users\\inbalros\\PycharmProjects\\Debugger\\utils\\weka.jar'


results_path = r'D:\Debbuger\GAN'

arff_start_path_with_bugs = r'D:\Debbuger\GAN\arff_start_with_bugs.txt'
arff_start_path_no_bugs = r'D:\Debbuger\GAN\arff_start_no_bugs.txt'
arff_start_path_no_process = r'D:\Debbuger\GAN\arff_start_no_process.txt'

training_file = "All_training_File.arff"
testing_file = "All_testing_File.arff"


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

all_projects_training_selected_features = {}

all_projects_testing_selected_features = {}

results_all_projects = pd.DataFrame(
        columns=['cold_start_project','result_type','features_type','model_source', 'precision_bug', 'recall_bug','F_bug', 'F2_bug','roc_area_bug', 'prc_area_bug', 'precision', 'recall',
                 'F1', 'F2', 'roc_area','prc_area','num_bugs','num_all_inst','precent_bugs'])

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

###########
def encode_categorial(data):
    true_false_att = ["ONE_elem_params","exception","externalizable",'abstract','error','serializable','ONE_elem_params_constructors']
    for col in data:
        if col == 'IsInterface':
            data[col] = data[col].map({'Interface': 0, 'class': 1})
        elif col == 'Parent':
            data[col] = data[col].map({'Has_parent': 0, 'No_parent': 1})
        elif col == 'scope':
            data[col] = data[col].map({'public': 0, 'protected': 1,'private':2,'default':3})
        elif col in true_false_att:
            data[col] = data[col].map({'true': 1, 'false': 0, 'True': 1, 'False': 0})
    return data

def convert_data(attributes, data):
    new_attributes = []
    attributes_convert = []
    for name, values in attributes:
        if values == "NUMERIC":
            new_attributes.append([name, values])
            attributes_convert.append(values)
        else:
            new_attributes.append([name, [ind for ind, x in enumerate(values)]])
            attributes_convert.append(dict([(x, ind) for ind, x in enumerate(values)]))
    new_data = []
    for instance in data:
        if None in instance:
            continue
        new_instance = []
        for ind, x in enumerate(instance):
            if attributes_convert[ind] == "NUMERIC":
                new_instance.append(x)
            else:
                new_instance.append(attributes_convert[ind][x])
        new_data.append(new_instance)
    return new_data
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

#creating model and test it
def train_model(x_train, y_train):
    x_train = encode_categorial(x_train)
    model = RandomForestClassifier()
    model.fit(x_train, y_train)
    # pickle.dump(model, open("D:\Debbuger\GAN", 'wb'))
    return model
def predict_model(model, x_test):
    x_test = encode_categorial(x_test)
    pred = model.predict(x_test)
    return pred
def save_model_dump(name,path,model):
    file_path = os.path.join(path, name)
    pickle.dump(model, open(file_path, 'wb'))

#create arffs
def create_arff_from_dataframe(df,path):
    arff.dump(path
              , df.values
              , relation='relation name'
              , names=df.columns)
def change_start_of_arff_file(type,arff_path):
    start_lines = None
    with open(type) as start:
        start_lines = start.readlines()
        start_lines.append('\n')

    change = True
    lines_to_save = None
    with open(arff_path) as file_to_change:
        change_lines = file_to_change.readlines()
        if len(change_lines) > 1:
            if type == arff_start_path_with_bugs :
                lines_to_save = start_lines + change_lines[364:]
            elif type == arff_start_path_no_bugs:
                lines_to_save = start_lines + change_lines[283:]
            else:
                lines_to_save = start_lines + change_lines[246:]
        else:
            change = False

        if change:
            with open(arff_path, "w") as f:
                f.writelines(lines_to_save)


#pre-processing to the data:
def selectFeatures(data,remove_bugs,remove_process):
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
#weka
def prep_train_and_test_to_arff():
    for key, val in all_files.items():
        print (key, "=>", val)
        all_projects_training_selected_features[key] = selectFeatures(all_projects_training_selected_features[key],False,False)
        all_projects_testing_selected_features[key] = selectFeatures(all_projects_testing_selected_features[key],False,False)
        train_path = os.path.join(val, "All_training_files_with_bugs.arff")
        test_path = os.path.join(val, "All_testing_files_with_bugs.arff")
        create_arff_from_dataframe(all_projects_training_selected_features[key],train_path)
        create_arff_from_dataframe(all_projects_testing_selected_features[key],test_path)
        create_arff_from_dataframe(all_projects_testing_selected_features[key],test_path)
        change_start_of_arff_file(arff_start_path_with_bugs,train_path)
        change_start_of_arff_file(arff_start_path_with_bugs,test_path)

        all_projects_training_selected_features[key] = selectFeatures(all_projects_training_selected_features[key],True,False)
        all_projects_testing_selected_features[key] = selectFeatures(all_projects_testing_selected_features[key],True,False)
        train_path = os.path.join(val, "All_training_files_no_bugs.arff")
        test_path = os.path.join(val, "All_testing_files_no_bugs.arff")
        create_arff_from_dataframe(all_projects_training_selected_features[key], train_path)
        create_arff_from_dataframe(all_projects_testing_selected_features[key], test_path)
        change_start_of_arff_file(arff_start_path_no_bugs, train_path)
        change_start_of_arff_file(arff_start_path_no_bugs, test_path)

        all_projects_training_selected_features[key] = selectFeatures(all_projects_training_selected_features[key],True,True)
        all_projects_testing_selected_features[key] = selectFeatures(all_projects_testing_selected_features[key],True, True)
        train_path = os.path.join(val, "All_training_files_no_process.arff")
        test_path = os.path.join(val, "All_testing_files_no_process.arff")
        create_arff_from_dataframe(all_projects_training_selected_features[key], train_path)
        create_arff_from_dataframe(all_projects_testing_selected_features[key], test_path)
        change_start_of_arff_file(arff_start_path_no_process, train_path)
        change_start_of_arff_file(arff_start_path_no_process, test_path)
#python
def prep_train_and_test_to_sklearn():
    for key, val in all_files.items():
        print (key, "=>", val)
        all_projects_training_selected_features[key] = selectFeatures(all_projects_training_selected_features[key],False,False)
        all_projects_testing_selected_features[key] = selectFeatures(all_projects_testing_selected_features[key],False,False)
        all_projects_training_selected_features[key]['hasBug'] = all_projects_training_selected_features[key]['hasBug'].map({'valid': 0, 'bugged': 1})
        all_projects_testing_selected_features[key]['hasBug'] = all_projects_testing_selected_features[key]['hasBug'].map({'valid': 0, 'bugged': 1})
        all_projects_training_selected_features[key] = pre_processing(all_projects_training_selected_features[key])
        all_projects_testing_selected_features[key] = pre_processing(all_projects_testing_selected_features[key])
        model = predict_model_kfold(key,val,"all",'hasBug',all_projects_training_selected_features[key])
        x_test = all_projects_testing_selected_features[key].drop('hasBug', axis=1)
        pred = model.predict(x_test)
        num_of_bugs = all_projects_testing_selected_features[key].loc[all_projects_testing_selected_features[key]['hasBug'] == 1].shape[0]
        num_of_all_instances= all_projects_testing_selected_features[key].shape[0]
        bug_precent = float(num_of_bugs)/float(num_of_all_instances)
        create_all_eval_results(True,all_projects_testing_selected_features[key]['hasBug'],pred,key,"testing","all",num_of_bugs,num_of_all_instances,bug_precent,"sklearn - python")
        save_model_dump(key+"_all.sav",val,model)

        all_projects_training_selected_features[key] = selectFeatures(all_projects_training_selected_features[key],True,False)
        all_projects_testing_selected_features[key] = selectFeatures(all_projects_testing_selected_features[key],True,False)
        model = predict_model_kfold(key, val, "no_bugs", 'hasBug', all_projects_training_selected_features[key])
        x_test = all_projects_testing_selected_features[key].drop('hasBug', axis=1)
        pred = model.predict(x_test)
        create_all_eval_results(True, all_projects_testing_selected_features[key]['hasBug'], pred, key, "testing",
                                "no_bugs", num_of_bugs, num_of_all_instances, bug_precent, "sklearn - python")
        save_model_dump(key + "_no_bugs.sav", val, model)

        all_projects_training_selected_features[key] = selectFeatures(all_projects_training_selected_features[key],True,True)
        all_projects_testing_selected_features[key] = selectFeatures(all_projects_testing_selected_features[key],True, True)
        model = predict_model_kfold(key, val, "no_process", 'hasBug', all_projects_training_selected_features[key])
        x_test = all_projects_testing_selected_features[key].drop('hasBug', axis=1)
        pred = model.predict(x_test)
        create_all_eval_results(True, all_projects_testing_selected_features[key]['hasBug'], pred, key, "testing",
                                "no_process", num_of_bugs, num_of_all_instances, bug_precent, "sklearn - python")
        save_model_dump(key + "_no_process.sav", val, model)


def predict_model_kfold(name,path,features_type,label_name,data):
    kfold = KFold(10, True)
    #RandomForest -I 1000 -K 0 -S 1 -num-slots 1
    model = BalancedRandomForestClassifier(n_estimators=1000,max_depth=5)
    index = 0
    size = data.shape[0]
    all_predictions = 0
    x = data.drop('hasBug', axis=1)
    y = data['hasBug']
    num_of_bugs = data.loc[data['hasBug'] == 1].shape[0]
    num_of_all_instances = data.shape[0]
    bug_precent = float(num_of_bugs) / float(num_of_all_instances)
    for train, test in kfold.split(data):
        index += 1
        prediction_train = model.fit(x.iloc[train], y.iloc[train]).predict(x.iloc[test])
        all_predictions += create_all_eval_results(False,y.iloc[test],prediction_train,name,"training",features_type,num_of_bugs,num_of_all_instances,bug_precent,None)

    all_predictions /= index
    start_list = [name,"training",features_type,"sklearn - python"]
    result_list = start_list+ all_predictions.tolist()

    global results_all_projects
    results_all_projects.loc[len(results_all_projects)] = result_list

    model.fit(x,y)
    return model


#load arffs
def load_arff(data_arff):
    raw_data = loadarff(data_arff)
    df_data = pd.DataFrame(raw_data[0])
    return df_data
def load_arff_from_dir_into_dataFrames_dictionery():
    for key, val in all_files.items():
        print (key, "=>", val)
        # all_projects_data[key] = load_arff(val)
        all_projects_training_selected_features[key] = load_arff(os.path.join(val,training_file))
        all_projects_testing_selected_features[key] = load_arff(os.path.join(val,testing_file))


#evaluate results - python
def calculateF2(precision, recall):
    if ((4 * precision) + recall) != 0:
        F2BUGS = (5 * ((precision * recall) / ((4 * precision) + recall)))
    else:
        F2BUGS = 0
    return F2BUGS
def create_all_eval_results(export,y_true, y_pred, key,result_type,features_type,num_of_bugs,num_of_all_instances,bugs_Precent,from_model):
    precision_bugged = metrics.precision_score(y_true,y_pred,pos_label=1,average='binary')
    recall_bugged = metrics.recall_score(y_true,y_pred,pos_label=1,average='binary')
    f_measure_bugged = metrics.f1_score(y_true,y_pred,pos_label=1,average='binary')
    f2_measure_bugged = calculateF2(precision_bugged,recall_bugged)

    un_true,_ = np.unique(y_true, return_counts=True)
    un_pred,_ = np.unique(y_pred, return_counts=True)
    if len(un_true) ==1 or len(un_pred)==1:
        roc_bugged = '?'
        prc_bugged =  '?'
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
        results_all_projects.loc[len(results_all_projects)] = [key, result_type, features_type, from_model, precision_bugged,
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

#evaluate results - weka
def export_all_results_from_weka():
    for key, val in all_files.items():
        print (key, "=>", val)
        dict_all_files = []
        dict_all_files.append(("training","no_process",os.path.join(val, "trainingfiles_All_no_process.txt")))
        dict_all_files.append(("test","no_process",os.path.join(val, "testingfiles_All_no_process.txt")))
        dict_all_files.append(("training","no_bugs",os.path.join(val, "trainingfiles_All_no_bugs.txt")))
        dict_all_files.append(("test","no_bugs",os.path.join(val, "testingfiles_All_no_bugs.txt")))
        dict_all_files.append(("training","all",os.path.join(val, "trainingfiles_All_with_bugs.txt")))
        dict_all_files.append(("test","all",os.path.join(val, "testingfiles_All_with_bugs.txt")))

        for result_type,features_type,path in dict_all_files:
            txtFile = open(path, "r")
            parsedResult =weka_parser.parse_WEKA_scores(txtFile.read())

            if result_type == "training":
                goto = 'cross-validation'
            else:
                goto = 'test'

            num_of_bugs = parsedResult[goto]['confusion matrix']['bugged']['bugged'] + \
                              parsedResult[goto]['confusion matrix']['bugged']['valid']
            num_of_all_instances = parsedResult[goto]['confusion matrix']['bugged']['bugged'] + \
                                       parsedResult[goto]['confusion matrix']['bugged']['valid'] + \
                                       parsedResult[goto]['confusion matrix']['valid']['bugged'] + \
                                       parsedResult[goto]['confusion matrix']['valid']['valid']
            bugs_Precent = float(num_of_bugs) / float(num_of_all_instances)
            precision_bugged = parsedResult[goto]['accuracy by class']['bugged']['precision']
            recall_bugged = parsedResult[goto]['accuracy by class']['bugged']['recall']
            f_measure_bugged = parsedResult[goto]['accuracy by class']['bugged']['F-measure']
            f2_measure_bugged = calculateF2(precision_bugged,recall_bugged)
            roc_bugged = parsedResult[goto]['accuracy by class']['bugged']['ROC area']
            prc_bugged = parsedResult[goto]['accuracy by class']['bugged']['PRC Area']

            precision_all = parsedResult[goto]['accuracy by class']['weighted avg']['precision']
            recall_all = parsedResult[goto]['accuracy by class']['weighted avg']['recall']
            f_measure_all = parsedResult[goto]['accuracy by class']['weighted avg']['F-measure']
            f2_measure_all = calculateF2(precision_all, recall_all)
            roc_all = parsedResult[goto]['accuracy by class']['weighted avg']['ROC area']
            prc_all = parsedResult[goto]['accuracy by class']['weighted avg']['PRC Area']

            global results_all_projects
            results_all_projects.loc[len(results_all_projects)] = [key, result_type,features_type,'weka',precision_bugged, recall_bugged,f_measure_bugged,
                                                                   f2_measure_bugged, roc_bugged,prc_bugged,
                                                                   precision_all, recall_all,f_measure_all, f2_measure_all, roc_all,prc_all,num_of_bugs,num_of_all_instances,bugs_Precent]

            if goto == 'test':
                all_predictions = pd.read_csv(path.replace("txt", "csv"))
                all_predictions['actual'] = all_predictions['actual'].map({'2:valid': 0, '1:bugged': 1})
                all_predictions['predicted'] = all_predictions['predicted'].map({'2:valid': 0, '1:bugged': 1})
                y_true = all_predictions['actual']
                y_pred = all_predictions['predicted']
                create_all_eval_results(True,y_true, y_pred, key,result_type,features_type,num_of_bugs,num_of_all_instances,bugs_Precent,"weka - using python")


#create model from weka
def build_Models_from_weka():
    buggedType = "All"
    for key, val in all_files.items():
        print (key, "=>", val)
        trainingFile_with_bugs = os.path.join(val,'All_training_files_with_bugs.arff')
        trainingFile_no_bugs = os.path.join(val,'All_training_files_no_bugs.arff')
        trainingFile_no_process = os.path.join(val,'All_training_files_no_process.arff')

        testingFile_with_bugs = os.path.join(val, 'All_testing_files_with_bugs.arff')
        testingFile_no_bugs = os.path.join(val, 'All_testing_files_no_bugs.arff')
        testingFile_no_process = os.path.join(val,'All_testing_files_no_process.arff')

        BuildWekaModel(val,trainingFile_with_bugs,testingFile_with_bugs,"files_"+buggedType+"_with_bugs",wekaJar)
        BuildWekaModel(val,trainingFile_no_bugs,testingFile_no_bugs,"files_"+buggedType+"_no_bugs",wekaJar)
        BuildWekaModel(val,trainingFile_no_process,testingFile_no_process,"files_"+buggedType+"_no_process",wekaJar)
def BuildWekaModel(weka, training, testing, name, wekaJar):
    algorithm="weka.classifiers.trees.RandomForest -I 1000 -K 0 -S 1 -num-slots 1 "
    os.system("cd /d  "+ weka +" & java -Xmx2024m  -cp "+(wekaJar)+" weka.Run " +algorithm+ " -x 10 -d .\\model"+name+".model -t "+training+" > training"+name+".txt")
    algorithm="weka.classifiers.trees.RandomForest"
    os.system("cd /d  "+ (weka) +" & java -Xmx2024m  -cp "+ (wekaJar) +" weka.Run " +algorithm+ " -l .\\model"+name+".model -T "+testing+" -classifications \"weka.classifiers.evaluation.output.prediction.CSV -file testing"+name+".csv\" ")
    os.system("cd /d  "+ (weka) +" & java -Xmx2024m  -cp "+ (wekaJar) +" weka.Run " +algorithm+ " -l .\\model"+name+".model -T "+testing+" > testing"+name+".txt ")


#main:

# try:
    # load_arff_from_dir_into_dataFrames_dictionery()
    # prep_train_and_test_to_arff()
    # build_Models_from_weka()
    # export_all_results_from_weka()
    # load_arff_from_dir_into_dataFrames_dictionery()
    # prep_train_and_test_to_sklearn()
    # results_all_projects.to_csv(r"D:\Debbuger\GAN\all_results.csv", index=False)

# except:
    # results_all_projects.to_csv(r"D:\Debbuger\GAN\all_results.csv", index=False)
