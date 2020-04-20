import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

##sklearn for machine learning
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor,GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb
from xgboost.sklearn import XGBClassifier, XGBRegressor
from scipy.stats import mode
from sklearn.model_selection import StratifiedKFold,GridSearchCV

## imbalnce learn library to deal with unbalnced data
from imblearn.over_sampling import SMOTE, SMOTENC
from imblearn.combine import SMOTEENN

from scipy.io.arff import loadarff
from sklearn.ensemble import RandomForestClassifier
# xgboost
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import check_random_state
from sklearn.utils.random import sample_without_replacement
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
from imblearn.ensemble import BalancedRandomForestClassifier
import os
from imblearn.ensemble import BalancedRandomForestClassifier
#adding extreme learning
from sklearn_extensions.extreme_learning_machines.elm import GenELMClassifier
from sklearn_extensions.extreme_learning_machines.random_layer import RBFRandomLayer, MLPRandomLayer

results_all_projects = pd.DataFrame(
        columns=['cold_start_project','model_source', 'precision_bug', 'recall_bug','F_bug', 'F2_bug','roc_area_bug', 'prc_area_bug', 'precision', 'recall',
                 'F1', 'F2', 'roc_area','prc_area','num_bugs_test','num_all_inst_test','percent_bugs_test','num_bugs_train','num_all_inst_train','percent_bugs_train'])

def create_all_data_with_models_sav(directory,data_file):
    data = pickle.load(open( data_file, "rb" ))
    #del data['ckjm1.8']
    for filename in os.listdir(directory):
        if filename.endswith(".sav"):
            print(os.path.join(directory, filename))
            current_model = pickle.load(open( os.path.join(directory, filename) , "rb" ))
            data[filename[:-4]] = (current_model,data[filename[:-4]])
            print(os.path.join(directory, filename))

    file_path = os.path.join(directory, 'all_data_with_models.sav')
    pickle.dump(data, open(file_path, 'wb'))

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

def  predict_model(cur_proj_name,data,proj_name_host,model_host,testing_set_host,within_model):
    x = data.drop('bugs', axis=1)
    y = data['bugs']
    num_of_bugs_test = data['bugs'].tolist().count(1)
    num_of_all_instances_test = data.shape[0]
    bug_precent_test = float(num_of_bugs_test) / float(num_of_all_instances_test)

    num_of_bugs_train = testing_set_host['bugs'].tolist().count(1)
    num_of_all_instances_train  = testing_set_host.shape[0]
    bug_precent_train = float(num_of_bugs_train) / float(num_of_all_instances_train)

    if (within_model == "ELM"):
        prediction_test = model_host.predict(x.rename_axis('ID').values)
    else:
        prediction_test = model_host.predict(x)

    new_pred, new_f2 = create_all_eval_results(False,y.tolist(),prediction_test.tolist(),cur_proj_name,num_of_bugs_test,num_of_all_instances_test,bug_precent_test,num_of_bugs_train,num_of_all_instances_train,bug_precent_train,proj_name_host+"_within_"+within_model)
    start_list = [cur_proj_name,proj_name_host]
    result_list = start_list+ new_pred.tolist()

    global results_all_projects
    results_all_projects.loc[len(results_all_projects)] = result_list

    return new_f2

def best_of_breed(data,within_model):
    all_projects_bob = {}
    for proj_name_host, ( model_host,testing_set_host ) in data.items():
        f2_score = 0
        num_of_projects = 0

        for cur_proj_name, (cur_model,cur_testing_set) in data.items():

            if proj_name_host[:-3] != cur_proj_name[:-3]:
                num_of_projects +=1
                f2_score += predict_model(cur_proj_name,cur_testing_set,"bob("+proj_name_host+")",model_host,testing_set_host,within_model)

        f2_score /= num_of_projects
        all_projects_bob[proj_name_host] = f2_score

    index = max(all_projects_bob, key=lambda i: all_projects_bob[i])
    print("max is: " + str(index) + " - " + str(all_projects_bob[index]))
    for proj, f2 in all_projects_bob.items():
        print(str(proj)+ "  :  " + str(f2))

##############################################################
promise_projects_to_number = {
"xalan2.6"  : 1,
"xalan2.7" :  2,
"xalan2.4"  :  3,
"xalan2.5"  :  4,
"jEdit3.2"  :  5,
"log4j1.2"  :  6,
"log4j1.1"  :  7,
"log4j1.0"  :  8,
"camel1.0"  :  9,
"camel1.2"  :  10,
"camel1.4"  :  11,
"camel1.6"  :  12,
"lucene2.2"  :  13,
"lucene2.0"  :  14,
"synapse1.2"  :  15,
"synapse1.0"  :  16,
"lucene2.4"  :  17,
"poi1.5"  :  18,
"xerces1.4"  : 19 ,
"xerces1.2"  :  20,
"xerces1.3"  :  21,
"poi2.0"  :  22,
"jEdit4.0"  :  23,
"jEdit4.1"  :  24,
"jEdit4.2"  :  25,
"jEdit4.3"  :  26,
"poi2.5"  :  27,
"ant1.4"  :28,
"ant1.5"  :  29,
"ant1.6"  :  30,
"ant1.7"  :  31,
"ant1.3"  :  32,
"Tomcat6.0":  33,
"velocity1.6":  34,
"velocity1.5":  35,
"velocity1.4" :  36,
"synapse1.1" : 37,
"ivy2.0"  :  38,
"ivy1.1"  :39,
"poi3.0"  : 40,
"ivy1.4"  :  41
}
promise_number_to_project = {
 1 : "xalan2.6",
 2 : "xalan2.7",
 3 : "xalan2.4",
 4 : "xalan2.5",
 5 : "jEdit3.2",
 6 : "log4j1.2",
 7 : "log4j1.1",
 8 : "log4j1.0",
 9 : "camel1.0",
10 : "camel1.2",
11 : "camel1.4",
12 : "camel1.6",
13: "lucene2.2" ,
14: "lucene2.0" ,
15: "synapse1.2" ,
16: "synapse1.0" ,
17: "lucene2.4"  ,
18: "poi1.5"  ,
19: "xerces1.4" ,
20: "xerces1.2"  ,
21: "xerces1.3"  ,
22: "poi2.0"  ,
23: "jEdit4.0"  ,
24: "jEdit4.1"  ,
25:" jEdit4.2"  ,
26:" jEdit4.3"  ,
27: "poi2.5"  ,
28: "ant1.4",
29: "ant1.5"  ,
30: "ant1.6"  ,
31: "ant1.7"  ,
32: "ant1.3"  ,
33: "Tomcat6.0",
34: "velocity1.6",
35: "velocity1.5",
36: "velocity1.4",
37: "synapse1.1",
38: "ivy2.0" ,
39: "ivy1.1" ,
40: "poi3.0" ,
41: "ivy1.4"
}

def data_sampling(data,num_of_samples):
    random = check_random_state(seed=None)
    n_samples, n_features = data.shape

    if(num_of_samples>n_samples):
        indexes = np.concatenate((sample_without_replacement(n_samples, n_samples, random_state=random), random.randint(0, n_samples, num_of_samples-n_samples)), axis=None)
    else:
        indexes = sample_without_replacement(n_samples, num_of_samples, random_state=random)

    return data.loc[indexes]

def load_training_set(CS_project,all_projects,sampling,num_of_samples = 100):
    training_by_model = {}
    datasets = pd.DataFrame()
    for proj_name, (model, testing_set) in all_projects.items():
        if CS_project[:-3] != proj_name[:-3]:
            data = testing_set.copy()
            data.reset_index(drop=True, inplace=True)
            data = data.rename(columns={'bugs': 'label'})
            data.label = promise_projects_to_number[proj_name]
            if sampling:
                datasets = datasets.append(data_sampling(data,num_of_samples), ignore_index=True)
            else:
                datasets = datasets.append(data, ignore_index=True)
    return datasets

def separated_data_by_predicted_model(CS_project,all_projects,pred, x_test):
    all_data_separated_dict = {}
    for proj_name, (model, testing_set) in all_projects.items():
        if CS_project[:-3] != proj_name[:-3]:
            all_data_separated_dict[promise_projects_to_number[proj_name]] = x_test.loc[np.where(pred == promise_projects_to_number[proj_name])]
    return all_data_separated_dict

def get_all_eval_based_on_model(separated,all_projects,within_model):
    pred = np.array([])
    real = np.array([])
    for key, data_to_test in separated.items():
        x_test = data_to_test.copy()
        try:
            if x_test.shape[0] != 0:
                x_test = x_test.drop('bugs', axis=1)
                if within_model == "ELM":
                    pred = np.concatenate((pred,  all_projects[promise_number_to_project[key]][0].predict(x_test.rename_axis('ID').values)), axis=None)
                    real = np.concatenate((real,  data_to_test['bugs']), axis=None)
                else:
                    pred = np.concatenate((pred, all_projects[promise_number_to_project[key]][0].predict(x_test)), axis=None)
                    real = np.concatenate((real, data_to_test['bugs']), axis=None)
        except:
            print(list(x_test))
    return pred.tolist(),real.tolist()


def create_models_and_eval(all_projects,sampling,model_details,model,num_of_samples,within_model):
    for cold_start_project_name, ( cold_start_model, cold_start_testing_set) in all_projects.items():
        training_by_models = load_training_set(cold_start_project_name,all_projects,sampling,num_of_samples)

        print("start process for: "+str(cold_start_project_name))
        tr_data_all = training_by_models.drop('label', axis=1)
        belonging_model = model.fit(tr_data_all, training_by_models['label'])
        all_x_test = cold_start_testing_set.copy()
        all_x_test.reset_index(drop=True, inplace=True)
        x_test = all_x_test.copy()
        x_test = x_test.drop('bugs', axis=1)

        # pred_ours is the list of belongingness prediction by our models
        pred_models_ours = belonging_model.predict(x_test)
        separated_ours = separated_data_by_predicted_model(cold_start_project_name,all_projects,pred_models_ours.copy(), all_x_test)
        #export_info_about_seperation(separated_ours,type,key,saving_path,sampling,model_details,num_of_samples,system_features)
        pred_ours,real_ours = get_all_eval_based_on_model(separated_ours,all_projects,within_model)
        num_of_bugs = real_ours.count(1)
        num_of_all_instances = len(real_ours)
        try:
            bug_precent = float(num_of_bugs) / float(num_of_all_instances)
        except:
            bug_precent = 0

        #best_prediction, worse_prediction,percent_ours = create_prediction_best_and_worse(all_x_test, type,pred_models_ours)
        #separated_random = separated_data_randomly(all_x_test, system_features, type)
        #export_info_about_seperation(separated_random, type, key, saving_path, sampling, model_details, num_of_samples,system_features)
        #pred_random, real_random = get_all_eval_based_on_model(separated_random, type)

        create_all_eval_results(True, real_ours, pred_ours, cold_start_project_name,
                                                   num_of_bugs, num_of_all_instances, bug_precent," "," "," ", "OSCAR_"+str(model_details)+"_"+str(sampling)+"_"+str(num_of_samples)+"_within"+within_model)

        #create_all_eval_results(real_random, pred_random,str(data_names[key]).split('\\')[-1],"testing",type,num_of_bugs,num_of_all_instances,bug_precent,model_details,system_features,"random")
        #create_all_eval_results(all_x_test['hasBug'], worse_prediction,str(data_names[key]).split('\\')[-1],"testing",type,num_of_bugs,num_of_all_instances,bug_precent,model_details,system_features,"Worst")
        #create_all_eval_results(all_x_test['hasBug'], best_prediction,str(data_names[key]).split('\\')[-1],"testing",type,num_of_bugs,num_of_all_instances,bug_precent,model_details,system_features,"Best")


def OSCAR(all_projects,within_model):
    index = 0
    models = {
        "random_forest_100": RandomForestClassifier(n_estimators=100, max_depth=5)
        # "xgb": XGBClassifier(n_estimators=100, max_depth=6)
        # "gradient_boostong": GradientBoostingClassifier(learning_rate=0.01, max_depth=5,n_estimators=100)
    }
    for model_details, model in models.items():
        for sampling in [True, False]:
            if (sampling):
                #for num_of_samples in [4000, 10000, 15000]:
                for num_of_samples in [400,700,1000]:
                    index += 1
                    print("start process_" + str(sampling) + "_" + str(num_of_samples))
                    create_models_and_eval(all_projects, sampling, model_details, model,num_of_samples,within_model)

                    #results_all_projects.to_csv(
                    #    os.path.join(results_path, "gan_results_all_belong" + str(index) + ".csv"), index=False)
                    # gan_val.to_csv(os.path.join(results_path, "gan_seperation_model_results_random" + str(index) + ".csv"),index=False)
            else:
                index += 1
                print("start process_" + str(sampling))
                create_models_and_eval(all_projects, sampling, model_details, model, "-",within_model)
                #results_all_projects.to_csv(
                #os.path.join(results_path, "gan_results_all_belong" + str(index) + ".csv"), index=False)
                # gan_val.to_csv(os.path.join(results_path, "gan_seperation_model_results_random" + str(index) + ".csv"),index=False)

def load_training_set_all_others(CS_project,all_projects,use_everyone=False):
    datasets = pd.DataFrame()
    if use_everyone:
        for proj_name, (model, testing_set) in all_projects.items():
            if CS_project != proj_name:
                data = testing_set.copy()
                data.reset_index(drop=True, inplace=True)
                datasets = datasets.append(data, ignore_index=True)
    else:
        for proj_name, (model, testing_set) in all_projects.items():
            if CS_project[:-3] != proj_name[:-3]:
                data = testing_set.copy()
                data.reset_index(drop=True, inplace=True)
                datasets = datasets.append(data, ignore_index=True)
    return datasets

def one_ELM(all_projects,use_everyone,within_model):
    for cold_start_project_name, ( cold_start_model, cold_start_testing_set) in all_projects.items():
        training_set = load_training_set_all_others(cold_start_project_name,all_projects,use_everyone)

        print("start process for: "+str(cold_start_project_name))
        tr_data_all = training_set.drop('bugs', axis=1)

        nh = 10
        srhl_rbf = RBFRandomLayer(n_hidden=nh * 2, rbf_width=0.1, random_state=0)
        model = GenELMClassifier(hidden_layer=srhl_rbf)

        model = model.fit(tr_data_all.rename_axis('ID').values, training_set['bugs'])
        all_x_test = cold_start_testing_set.copy()
        all_x_test.reset_index(drop=True, inplace=True)
        x_test = all_x_test.copy()
        x_test = x_test.drop('bugs', axis=1)

        pred = model.predict(x_test.rename_axis('ID').values)

        num_of_bugs_test = all_x_test['bugs'].tolist().count(1)
        num_of_all_instances_test = len(all_x_test['bugs'])
        try:
            bug_precent_test = float(num_of_bugs_test) / float(num_of_all_instances_test)
        except:
            bug_precent_test = 0

        num_of_bugs_train = training_set['bugs'].tolist().count(1)
        num_of_all_instances_train = len(training_set['bugs'])
        try:
            bug_precent_train = float(num_of_bugs_train) / float(num_of_all_instances_train)
        except:
            bug_precent_train = 0

        create_all_eval_results(True, all_x_test['bugs'].tolist(), pred.tolist(), cold_start_project_name,
        num_of_bugs_test, num_of_all_instances_test, bug_precent_test
                                ,num_of_bugs_train, num_of_all_instances_train, bug_precent_train
                                , ("ELM_useEveryone_" +str(use_everyone)+"_within"+within_model))


directory_ELM= r'D:\Debbuger\PROMISE\ELM_normal'
directory_RF= r'D:\Debbuger\PROMISE\TREE_normal'

#data_file = r'D:\Debbuger\PROMISE\all_training_data.sav'
#create_all_data_with_models_sav(directory,data_file)
file_path_ELM = os.path.join(directory_ELM, 'all_data_with_models_ELM.sav')
file_path_RF = os.path.join(directory_RF, 'all_data_with_models_TREE.sav')

'''
with open(file_path_RF, 'rb') as f:
    u = pickle._Unpickler(f)
    u.encoding = 'latin1'
    data = u.load()
    for cold_start_project_name, (cold_start_model, cold_start_testing_set) in data.items():
        data[cold_start_project_name] = (
        cold_start_model, cold_start_testing_set.drop(['Class', 'unique_name'], axis=1))

    best_of_breed(data, "RF")
    OSCAR(data, "RF")
    one_ELM(data, False, "RF")
    one_ELM(data, True, "RF")
'''

data = pickle.load(open(file_path_RF, "rb"))

for cold_start_project_name, (cold_start_model, cold_start_testing_set) in data.items():
    if 'Class' in cold_start_testing_set.columns:
        data[cold_start_project_name] = (cold_start_model, cold_start_testing_set.drop(['Class', 'unique_name'], axis=1))
    if '.' not in cold_start_project_name:
        data[cold_start_project_name+".0"] = data[cold_start_project_name]
        del data[cold_start_project_name]

best_of_breed(data,"RF")
OSCAR(data,"RF")
one_ELM(data,False,"RF")
one_ELM(data,True,"RF")


data = pickle.load(open(file_path_ELM, "rb"))
for cold_start_project_name, (cold_start_model, cold_start_testing_set) in data.items():
    if 'Class' in cold_start_testing_set.columns:
        data[cold_start_project_name] = (cold_start_model, cold_start_testing_set.drop(['Class', 'unique_name'], axis=1))
    if '.' not in cold_start_project_name:
        data[cold_start_project_name+".0"] = data[cold_start_project_name]
        del data[cold_start_project_name]

best_of_breed(data,"ELM")
OSCAR(data,"ELM")
one_ELM(data,False,"ELM")
one_ELM(data,True,"ELM")



results_all_projects.to_csv(r"D:\Debbuger\PROMISE\ALL_results_normal.csv", index=False)
