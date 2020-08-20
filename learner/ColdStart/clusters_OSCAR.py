import numpy as np
import pandas as pd
import sklearn.metrics as metrics
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.utils import check_random_state
from sklearn.utils.random import sample_without_replacement
import os
from imblearn.ensemble import BalancedRandomForestClassifier
from sklearn_extensions.extreme_learning_machines.elm import GenELMClassifier
from sklearn_extensions.extreme_learning_machines.random_layer import RBFRandomLayer, MLPRandomLayer
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.multiclass import OneVsOneClassifier,OneVsRestClassifier
import itertools
from sklearn.metrics import pairwise_distances_argmin_min
import math
import csv

projects_to_number = {
"bookkeeper" : 0,
"fop" :         1,
"kafka"  :      2,
"oozie"  :      3,
"sentry"  :    4,
"tajo"  :     5 #,
#"tiles"  :      6
}
number_to_project = {
0: "bookkeeper"     ,
1: "fop"             ,
2:"kafka"           ,
3:"oozie"          ,
4:"sentry"         ,
5:"tajo"         # ,
#6:"tiles"
}
project_to_describe_f={
"bookkeeper" : 0,
"fop" :         1,
"kafka"  :      2,
"oozie"  :      3,
"sentry"  :    4,
"tajo"  :     5#,
#"tiles"  :      6
}
project_to_systems_metrics={
"bookkeeper" : 0,
"fop" :         1,
"kafka"  :      2,
"oozie"  :      3,
"sentry"  :    4,
"tajo"  :     5#,
#"tiles"  :      6
}

results_all_projects = pd.DataFrame(
        columns=['cold_start_project','model_source', 'precision_bug', 'recall_bug','F_bug', 'F2_bug','roc_area_bug', 'prc_area_bug', 'precision', 'recall',
                 'F1', 'F2', 'roc_area','prc_area','num_bugs_test','num_all_inst_test','percent_bugs_test','num_bugs_train','num_all_inst_train','percent_bugs_train',"percent_group_training_set"])


def create_describe_data(all_projects,drop_bugs=True):
    global project_to_describe_f
    for ind in range(len(projects_to_number)):
        proj_name = number_to_project[ind]
        train_index = 1
        print(ind)
        print(proj_name)
        if(drop_bugs):
            des = all_projects[proj_name][train_index].drop([label_bugs], axis=1).describe().drop(['count', '25%', '50%', '75%']).values
        else:
            des = all_projects[proj_name][train_index].describe().drop(['count', '25%', '50%', '75%']).values

        all_arr = [0.0 if math.isnan(i) else i for i in des.flatten()]
        project_to_describe_f[proj_name] = all_arr

def create_system_metrics_data(path):
    global project_to_systems_metrics
    for roject_name in projects_to_number.keys():
        project_metrics = pd.read_csv(os.path.join(path, start_file_system + roject_name + ".csv"))
        project_to_systems_metrics[roject_name] = project_metrics.values.flatten()

def create_training_cluster(cold_start_proj_num, k_means_number,project_to):
    all_classes = np.array([[]])
    first = True
    for ind in range(len(projects_to_number)):
        if ind != cold_start_proj_num:
            proj_name = number_to_project[ind]
            if first:
                all_classes = np.array([project_to[proj_name]])
                first = False
            else:
                all_classes = np.append(all_classes, np.array([project_to[proj_name]]), axis=0)

    kmeans = KMeans(n_clusters=k_means_number, random_state=0)
    kmeans.fit(all_classes)
    all_clusters = []
    for index in range(k_means_number):
        list_cluser = [proj_num if proj_num<cold_start_proj_num else proj_num+1 for proj_num in (np.where(kmeans.labels_ == index))[0].tolist()]
        orig = (np.where(kmeans.labels_ == index))[0].tolist()
        all_clusters.insert(len(all_clusters), list_cluser )

    return kmeans,all_clusters

def predict_closest_cluster(cold_start_proj_num, kmeans,project_to):
    proj_name = number_to_project[cold_start_proj_num]
    to_pred = np.array([project_to[proj_name]])
    prediction = kmeans.predict(to_pred)[0]
    return prediction

'''
def create_all_clusters_with_system_metrics(path,k_means_number):
    global project_to_systems_metrics
    first = True
    for roject_name in projects_to_number.keys():
        project_metrics = pd.read_csv(os.path.join(path,start_file_system+roject_name+".csv"))
        project_to_systems_metrics[roject_name] = project_metrics.values.flatten()
        if first:
            all_classes = np.array([project_to_systems_metrics[roject_name]])
            first = False
        else:
            all_classes = np.append(all_classes, np.array([project_to_systems_metrics[roject_name]]), axis=0)

    kmeans = KMeans(n_clusters=k_means_number, random_state=0)
    kmeans.fit(all_classes)
    all_clusters = []
    for index in range(k_means_number):
        all_clusters.insert(len(all_clusters), (np.where(kmeans.labels_ == index))[0].tolist())

    return kmeans, all_clusters
def create_all_clusters_with_describe(all_projects,k_means_number,drop_bugs=True):
    global project_to_describe_f
    all_classes = np.array([[]])
    first = True

    for ind in range(len(projects_to_number)):
        proj_name = number_to_project[ind]
        train_index = 1
        print(ind)
        print(proj_name)
        if (drop_bugs):
            des = all_projects[proj_name][train_index].drop([label_bugs], axis=1).describe().drop(
                ['count', '25%', '50%', '75%']).values
        else:
            des = all_projects[proj_name][train_index].describe().drop(['count', '25%', '50%', '75%']).values

        proj_name = number_to_project[ind]
        all_arr = [0.0 if math.isnan(i) else i for i in des.flatten()]
        project_to_describe_f[proj_name] = all_arr
        if first:
            all_classes = np.array([all_arr])
            first = False
        else:
            all_classes = np.append(all_classes, np.array([all_arr]), axis=0)

    kmeans = KMeans(n_clusters=k_means_number, random_state=0)
    kmeans.fit(all_classes)
    all_clusters = []
    for index in range(k_means_number):
        all_clusters.insert(len(all_clusters), (np.where(kmeans.labels_ == index))[0].tolist() )

    return kmeans,all_clusters
'''

def load_training_set_all_others(CS_project,all_projects,use_everyone=False):
    datasets = pd.DataFrame()
    if use_everyone:
        for proj_name, (model,training_set, testing_set) in all_projects.items():
            if CS_project != proj_name:
                data = training_set.copy()
                data.reset_index(drop=True, inplace=True)
                datasets = datasets.append(data, ignore_index=True)
    else:
        for proj_name, (model, training_set,testing_set) in all_projects.items():
            #if CS_project[:-3] != proj_name[:-3]:
            #if CS_project != proj_name:
            if CS_project.split('_')[0] != proj_name.split('_')[0]:
                data = training_set.copy()
                data.reset_index(drop=True, inplace=True)
                datasets = datasets.append(data, ignore_index=True)
    return datasets
def data_sampling(data,num_of_samples):
    random = check_random_state(seed=None)
    n_samples, n_features = data.shape

    if(num_of_samples>n_samples):
        indexes = np.concatenate((sample_without_replacement(n_samples, n_samples, random_state=random), random.randint(0, n_samples, num_of_samples-n_samples)), axis=None)
    else:
        indexes = sample_without_replacement(n_samples, num_of_samples, random_state=random)

    return data.loc[indexes]


def find_inside_cluster(clusters,project_name):
    project_num = projects_to_number[project_name]
    for ind in range(len(clusters)):
        if project_num in clusters[ind]:
            return ind


def load_training_set(clusters,CS_project,all_projects,sampling,num_of_samples = 100):
    datasets = pd.DataFrame()
    if clusters :
        cluster_number = find_inside_cluster(clusters,CS_project)
        cluster_group = clusters[cluster_number]
    else:
        cluster_group = number_to_project.keys()

    for proj_name, (model,training_set, testing_set) in all_projects.items():
        proj_number = projects_to_number[proj_name]
        if proj_number in cluster_group:
            if CS_project.split('_')[0] != proj_name.split('_')[0]:
                data = training_set.copy()
                data.reset_index(drop=True, inplace=True)
                data = data.rename(columns={label_bugs: 'label'})
                data.label = proj_number
                if sampling:
                    datasets = datasets.append(data_sampling(data, num_of_samples), ignore_index=True)
                else:
                    datasets = datasets.append(data, ignore_index=True)

    return datasets

def separated_data_by_predicted_model(CS_project,all_projects,pred, x_test):
    all_data_separated_dict = {}
    for proj_name, (model,training_set, testing_set) in all_projects.items():
        #if CS_project[:-3] != proj_name[:-3]:
        #if CS_project != proj_name:
        if CS_project.split('_')[0] != proj_name.split('_')[0]:
            all_data_separated_dict[projects_to_number[proj_name]] = x_test.loc[np.where(pred == projects_to_number[proj_name])]
    return all_data_separated_dict

def get_all_eval_based_on_model(separated,all_projects,within_model):
    pred = np.array([])
    real = np.array([])
    for key, data_to_test in separated.items():
        x_test = data_to_test.copy()
        #try:
        if x_test.shape[0] != 0:
            x_test = x_test.drop(label_bugs, axis=1)
            if within_model == "ELM":
                pred = np.concatenate((pred,  all_projects[number_to_project[key]][0].predict(x_test.rename_axis('ID').values)), axis=None)
                real = np.concatenate((real,  data_to_test[label_bugs]), axis=None)
            else:
                pred = np.concatenate((pred, all_projects[number_to_project[key]][0].predict(x_test)), axis=None)
                real = np.concatenate((real, data_to_test[label_bugs]), axis=None)
        #except:
            #print(list(x_test))
            #print(key)

    return pred.tolist(),real.tolist()

def get_all_eval_based_on_ensamble_inside_cluster(all_clusters,cold_start_project_name,all_projects):
    cluster_number = find_inside_cluster(all_clusters, cold_start_project_name)
    cluster_group = all_clusters[cluster_number]
    pred = np.array([])
    real = np.array([])
    x_test = (all_projects[cold_start_project_name][2]).copy()
    real = np.concatenate((real, x_test[label_bugs]), axis=None)
    x_test = x_test.drop(label_bugs, axis=1)
    first = True
    for project_number in cluster_group:
        proj_name = number_to_project[project_number]
        if cold_start_project_name != proj_name:
            if first:
                pred = np.concatenate((pred, all_projects[proj_name][0].predict(x_test)), axis=None)
                first = False
            else:
                pred = pred +  all_projects[proj_name][0].predict(x_test)

    pred_avg = pred / (len(cluster_group)-1)
    pred_avg = np.round(pred_avg)
    return pred_avg.tolist(),real.tolist()

def get_all_eval_based_on_one_model_inside_cluster(all_clusters,cold_start_project_name,all_projects):
    cluster_number = find_inside_cluster(all_clusters, cold_start_project_name)
    cluster_group = all_clusters[cluster_number]
    real = np.array([])
    x_test = (all_projects[cold_start_project_name][2]).copy()
    real = np.concatenate((real, x_test[label_bugs]), axis=None)
    x_test = x_test.drop(label_bugs, axis=1)
    x_test.reset_index(drop=True, inplace=True)

    dataset = pd.DataFrame()
    for project_number in cluster_group:
        proj_name = number_to_project[project_number]
        if cold_start_project_name != proj_name:
            data = all_projects[proj_name][1].copy()
            data.reset_index(drop=True, inplace=True)
            dataset = dataset.append(data, ignore_index=True)

    cur_model = BalancedRandomForestClassifier(n_estimators=1000, max_depth=5)
    one_ba_model = cur_model.fit(dataset.drop(label_bugs, axis=1), dataset[label_bugs])
    pred = one_ba_model.predict(x_test)

    return pred.tolist(), real.tolist()

def calculateF2(precision, recall):
    if ((4 * precision) + recall) != 0:
        F2BUGS = (5 * ((precision * recall) / ((4 * precision) + recall)))
    else:
        F2BUGS = 0
    return F2BUGS

def create_all_eval_results(export,y_true, y_pred, key,num_of_bugs_test,num_of_all_instances_test,bugs_Precent_test,num_of_bugs_train,num_of_all_instances_train,bugs_Precent_train,from_model,percent_group_name=None):
    #print(y_pred)
    #print(y_true)
    un_true, _ = np.unique(y_true, return_counts=True)
    un_pred, _ = np.unique(y_pred, return_counts=True)
    if len(un_true) == 1 or len(un_pred) == 1:
        y_true.append(0)
        y_true.append(1)
        y_pred.append(0)
        y_pred.append(1)
        y_true.append(0)
        y_true.append(1)
        y_pred.append(1)
        y_pred.append(0)
        print("zero or ones")

    precision_bugged = metrics.precision_score(y_true, y_pred, pos_label=1, average='binary')
    recall_bugged = metrics.recall_score(y_true, y_pred, pos_label=1, average='binary')
    f_measure_bugged = metrics.f1_score(y_true, y_pred, pos_label=1, average='binary')
    f2_measure_bugged = calculateF2(precision_bugged, recall_bugged)

    try:
        roc_bugged = metrics.roc_auc_score(y_true, y_pred, average=None)
    except:
        print("exception_roc")
        roc_bugged = 0
    #try:
    precision, recall, thresholds = metrics.precision_recall_curve(y_true, y_pred, pos_label=1)
    prc_bugged = metrics.auc(recall,precision)
    #except:
    #    print("exception_prc - BUG")
    #    prc_bugged = 0.5

    precision_all = metrics.precision_score(y_true, y_pred)
    recall_all = metrics.recall_score(y_true, y_pred)
    f_measure_all = metrics.f1_score(y_true, y_pred)
    f2_measure_all = calculateF2(precision_all, recall_all)
    try:
        roc_all = metrics.roc_auc_score(y_true, y_pred)
    except:
        print("exception_roc")
        roc_all = 0
    try:
        precision, recall, thresholds = metrics.precision_recall_curve(y_true, y_pred)
        prc_all = metrics.auc(recall, precision)
    except:
        print("exception_prc - N")
        prc_all = 1


    if export:
        global results_all_projects
        results_all_projects.loc[len(results_all_projects)] = [key, from_model, precision_bugged,
                                                           recall_bugged, f_measure_bugged,
                                                           f2_measure_bugged, roc_bugged, prc_bugged,
                                                           precision_all, recall_all, f_measure_all, f2_measure_all,
                                                           roc_all, prc_all, num_of_bugs_test, num_of_all_instances_test,
                                                           bugs_Precent_test, num_of_bugs_train, num_of_all_instances_train,
                                                           bugs_Precent_train,percent_group_name]


    return np.array(list((precision_bugged,recall_bugged, f_measure_bugged,
                                            f2_measure_bugged, roc_bugged, prc_bugged,
                                            precision_all, recall_all, f_measure_all, f2_measure_all,
                                            roc_all, prc_all, num_of_bugs_test, num_of_all_instances_test,
                                            bugs_Precent_test, num_of_bugs_train, num_of_all_instances_train,
                                            bugs_Precent_train))) , f2_measure_all


def create_models_and_eval_inside_cluster(all_projects,sampling,model_details,model,num_of_samples,within_model,project_to = None,k_means_number = 2):
    for cold_start_project_name, ( cold_start_model,cold_start_training_set ,cold_start_testing_set) in all_projects.items():
        proj_num = projects_to_number[cold_start_project_name]
        if project_to :
            kmeans,all_clusters = create_training_cluster(proj_num,k_means_number,project_to)
            prediction = predict_closest_cluster(proj_num,kmeans,project_to)
            precent_g = str([number_to_project[num] for num in all_clusters[prediction]])
            all_clusters[prediction].append(proj_num)
        else:
            kmeans,all_clusters = None,None
            precent_g = None

        training_by_models = load_training_set(all_clusters,cold_start_project_name,all_projects,sampling,num_of_samples)
        print("start process for: "+str(cold_start_project_name))
        tr_data_all = training_by_models.drop('label', axis=1)
        belonging_model = model.fit(tr_data_all, training_by_models['label'])
        all_x_test = cold_start_testing_set.copy()
        all_x_test.reset_index(drop=True, inplace=True)
        x_test = all_x_test.copy()
        x_test = x_test.drop(label_bugs, axis=1)

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

        create_all_eval_results(True, real_ours, pred_ours, cold_start_project_name,
                                                   num_of_bugs, num_of_all_instances, bug_precent," "," "," ", "OSCAR_"+str(model_details)+"_"+str(sampling)+"_"+str(num_of_samples)+"_within"+within_model,precent_g)

        if project_to:
            # doing ensamble inside cluster
            pred_ours,real_ours = get_all_eval_based_on_ensamble_inside_cluster(all_clusters,cold_start_project_name,all_projects)
            create_all_eval_results(True, real_ours, pred_ours, cold_start_project_name,
                                    num_of_bugs, num_of_all_instances, bug_precent, " ", " ", " ",
                                    "cluster_baseline_ensamble" + str(model_details) + "_" + str(sampling) + "_" + str(
                                        num_of_samples) + "_within" + within_model, precent_g)
            # create one model from training set
            pred_ours, real_ours = get_all_eval_based_on_one_model_inside_cluster(all_clusters,cold_start_project_name,all_projects)
            create_all_eval_results(True, real_ours, pred_ours, cold_start_project_name,
                                    num_of_bugs, num_of_all_instances, bug_precent, " ", " ", " ",
                                    "cluster_baseline_oneModel" + str(model_details) + "_" + str(sampling) + "_" + str(
                                        num_of_samples) + "_within" + within_model, precent_g)


def OSCAR(all_projects,within_model_kind,project_to = None,k_means_number = 2):
    index = 0
    models = {
        "random_forest_100": RandomForestClassifier(n_estimators=100, max_depth=5)
        # "xgb": XGBClassifier(n_estimators=100, max_depth=6)
        #"gradient_boostong": GradientBoostingClassifier(learning_rate=0.01, max_depth=5,n_estimators=100)
    }
    for model_details, model in models.items():
        for sampling in [True, False]:
            if (sampling):
                 for num_of_samples in [400,1000,4000]:
                    index += 1
                    print("start process_" + str(sampling) + "_" + str(num_of_samples))
                    create_models_and_eval_inside_cluster(all_projects, sampling, model_details, model,num_of_samples,within_model_kind,project_to ,k_means_number)
            else:
                index += 1
                print("start process_" + str(sampling))
                create_models_and_eval_inside_cluster(all_projects, sampling, model_details, model, "-",within_model_kind,project_to ,k_means_number )



def create_training_cluster_using_all_instances(CS_proj_num, k_means_number, all_projects,sampling=None,num_of_samples=100):
    dataset = pd.DataFrame()
    for proj_name, (model, training_set, testing_set) in all_projects.items():
        proj_number = projects_to_number[proj_name]
        if CS_proj_num != proj_number:
            data = training_set.copy()
            data.reset_index(drop=True, inplace=True)
            if sampling:
                dataset = dataset.append(data_sampling(data, num_of_samples), ignore_index=True)
            else:
                dataset = dataset.append(data, ignore_index=True)

    dataset_train = dataset.drop(label_bugs, axis=1)

    all_classes = np.array([[]])
    first = True
    '''
    for inde in range(len(dataset_train)):
        all_arr = [0.0 if math.isnan(i) else i for i in dataset_train.loc[inde].values ]
        if first:
            all_classes = np.array([all_arr])
            first = False
        else:
            all_classes = np.append(all_classes, np.array([all_arr]), axis=0)
    '''
    all_classes = dataset_train.values
    kmeans = KMeans(n_clusters=k_means_number, random_state=0)
    kmeans.fit(all_classes)
    all_clusters = {}
    all_clusters_num_of_train = {}

    for index in range(k_means_number):
        list_cluser = (np.where(kmeans.labels_ == index))[0].tolist()
        df_from_cluster = dataset.loc[list_cluser]

        if len(list(set(df_from_cluster[label_bugs]))) > 1:
            print("balanced")
            cur_model = BalancedRandomForestClassifier(n_estimators=1000, max_depth=5)
            all_clusters[index] = cur_model.fit(df_from_cluster.drop(label_bugs, axis=1),df_from_cluster[label_bugs])
        else:
            print("normal")
            cur_model = RandomForestClassifier(n_estimators=1000, max_depth=5)
            all_clusters[index] = cur_model.fit(df_from_cluster.drop(label_bugs, axis=1), df_from_cluster[label_bugs])

        all_clusters_num_of_train[index] = df_from_cluster.shape[0]

    return kmeans,all_clusters,all_clusters_num_of_train

def predict_all_closest_clusters_for_CSinstances(cold_start_proj_num,kmeans,cold_start_testing_set):
    cold_start_testing_set.reset_index(drop=True, inplace=True)
    cold_start_testing_set_prep = cold_start_testing_set.drop(label_bugs, axis=1)
    prediction = kmeans.predict(cold_start_testing_set_prep.values).tolist()
    uniq_val = list(set(prediction))
    all_clusters_prediction = {}
    for index in uniq_val:
        #list_cluser = (np.where(kmeans.labels_ == index))[0].tolist()
        #print(prediction)
        #print(index)
        list_cluser = (np.where(np.asarray(prediction) == index))[0].tolist()
        df_from_cluster = cold_start_testing_set.loc[list_cluser]
        df_from_cluster.reset_index(drop=True, inplace=True)
        all_clusters_prediction[index] = df_from_cluster

    return all_clusters_prediction


def get_all_eval_based_on_cluster(prediction_dict_cluster_df,all_clusters_models):
    pred = np.array([])
    real = np.array([])
    for index, data_to_test in prediction_dict_cluster_df.items():
        x_test = data_to_test.copy()
        #try:
        if x_test.shape[0] != 0:
            x_test = x_test.drop(label_bugs, axis=1)
            pred = np.concatenate((pred, all_clusters_models[index].predict(x_test)), axis=None)
            real = np.concatenate((real, data_to_test[label_bugs]), axis=None)
        #except:
        #    print(x_test)
        #    print(all_clusters_models[index])

    return pred.tolist(),real.tolist()



def create_models_and_eval_ONE_model_cluster(all_projects,k_means_number = 2,sampling=True,num_of_samples = 100):

    for cold_start_project_name, ( cold_start_model,cold_start_training_set ,cold_start_testing_set) in all_projects.items():
        print("start process for: "+str(cold_start_project_name))
        proj_num = projects_to_number[cold_start_project_name]

        kmeans, all_clusters_models,all_clusters_num_of_train = create_training_cluster_using_all_instances(proj_num, k_means_number, all_projects,sampling,num_of_samples)
        prediction_dict_cluster_df = predict_all_closest_clusters_for_CSinstances(proj_num,kmeans,cold_start_testing_set)

        pred_ours,real_ours = get_all_eval_based_on_cluster(prediction_dict_cluster_df,all_clusters_models)

        to_show_stat = str(all_clusters_num_of_train)
        to_show_stat_pred = str({k: v.shape[0] for k,v in prediction_dict_cluster_df.items()} )
        precent_g = to_show_stat+" , "+to_show_stat_pred
        num_of_bugs = real_ours.count(1)
        num_of_all_instances = len(real_ours)
        try:
            bug_precent = float(num_of_bugs) / float(num_of_all_instances)
        except:
            bug_precent = 0

        create_all_eval_results(True, real_ours, pred_ours, cold_start_project_name,
                                                   num_of_bugs, num_of_all_instances, bug_precent," "," "," ", "OSCAR_"+str(sampling)+"_"+str(num_of_samples)+"_oneModel_perCluster_"+str(k_means_number),precent_g)




label_bugs = 'hasBug'
##############################!!!!!!!!
directory_RF = r'D:\Debbuger\our projects style promise\within_models_full_ours_f'
all_data_with_models_name = 'dict_all_models_and_data'
#file_path_RF = os.path.join(directory_RF, all_data_with_models_name)
file_path_RF = r'D:\Debbuger\our projects style promise\within_models_full_ours_f\within_models_full_ours_f.sav'
system_metrics = r'D:\Debbuger\systemMetrics'
start_file_system = 'SystemMetrics'

#dict_name_path = os.path.join(r'D:\Debbuger\PROMISE', dict_name)
###############################!!!!!!!

print(file_path_RF)
data = pickle.load(open(file_path_RF, "rb"))

for proj_name, (model, training_set, testing_set) in data.items():
    training_set.reset_index(drop=True, inplace=True)
    testing_set.reset_index(drop=True, inplace=True)

del data['tiles']

#print("oscar")
#OSCAR(data,"RF",oracle=True)

#create_all_clusters_with_system_metrics(system_metrics,2)

#kmeans, all_clusters = create_all_clusters_with_describe(data,2)


#def create_models_and_eval_ONE_model_cluster(all_projects,k_means_number = 2,sampling=True,num_of_samples = 100):
print("oscar - using all the data")
OSCAR(data,"RF")

print("cluster - one - 4")
create_models_and_eval_ONE_model_cluster(data,k_means_number = 4,sampling=False)
create_models_and_eval_ONE_model_cluster(data,k_means_number = 4,sampling=True,num_of_samples = 1000)

print("cluster - one - 3")
create_models_and_eval_ONE_model_cluster(data,k_means_number = 3,sampling=False)
create_models_and_eval_ONE_model_cluster(data,k_means_number = 3,sampling=True,num_of_samples = 1000)

create_describe_data(data)
create_system_metrics_data(system_metrics)

print("cluster - using the system metrics")
OSCAR(data,"RF_clusters_system_2",project_to = project_to_systems_metrics,k_means_number = 2)
OSCAR(data,"RF_clusters_system_3",project_to = project_to_systems_metrics,k_means_number = 3)


print("cluster - using the describe data")
OSCAR(data,"RF_clusters_describe_2",project_to = project_to_describe_f ,k_means_number = 2)
OSCAR(data,"RF_clusters_describe_3",project_to = project_to_describe_f ,k_means_number = 3)

results_all_projects.to_csv(os.path.join(directory_RF,"clusters_results_ALL_NO_T.csv"), index=False)

