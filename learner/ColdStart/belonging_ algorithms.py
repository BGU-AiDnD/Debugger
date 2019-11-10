from collections import Counter
import numpy as np
import arff
import os
import pandas as pd
import random
from scipy.io.arff import loadarff
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
# xgboost
from xgboost.sklearn import XGBClassifier
import xgboost as xgb
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split, KFold
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import check_random_state
from sklearn.utils.random import sample_without_replacement
import from_weka_to_python
# import tensorflow as tf

# mycomp:
wekaJar = 'C:\\Users\\USER\\Documents\\Debugger\\Debugger\\utils\\weka.jar'  # os.path.join(utilsPath, "weka.jar")

# server:
# wekaJar = 'C:\\Users\\inbalros\\PycharmProjects\\Debugger\\utils\\weka.jar'

end_file_no_process="_no_process.sav"
end_file_no_bugs="_no_bugs.sav"
end_file_all="_all.sav"

models_no_process = {}
models_no_bugs = {}
models_all ={}

all_projects_training_no_process= {}
all_projects_training_no_bugs= {}
all_projects_training_all= {}
all_projects_testing_no_process= {}
all_projects_testing_no_bugs= {}
all_projects_testing_all = {}

results_path = r'D:\Debbuger\GAN\diff_alg'

all_files ={
    "1": "D:\Debbuger\GAN\BOOKKEEPER\weka" ,
    # "2": "D:\Debbuger\GAN\DERBY\weka",
    "3": "D:\Debbuger\GAN\FOP\weka",
    "4": "D:\Debbuger\GAN\KAFKA\weka",
    "5": "D:\Debbuger\GAN\OOZIE\weka",
    "6": "D:\Debbuger\GAN\OPENNLP\weka",
    "7": "D:\Debbuger\GAN\SENTRY\weka",
    "8": "D:\Debbuger\GAN\TAJO\weka",
    "9": "D:\Debbuger\GAN\TILES\weka"
     }

cold_start_index = -1

data_names = {
    "1": r"D:\Debbuger\GAN\BOOKKEEPER",
    # "2": r"D:\Debbuger\GAN\DERBY",
    "3": r"D:\Debbuger\GAN\FOP",
    "4": r"D:\Debbuger\GAN\KAFKA",
    "5": r"D:\Debbuger\GAN\OOZIE",
    "6": r"D:\Debbuger\GAN\OPENNLP",
    "7": r"D:\Debbuger\GAN\SENTRY",
    "8": r"D:\Debbuger\GAN\TAJO",
    "9": r"D:\Debbuger\GAN\TILES"
}

system_metrics = {
    "1": r"D:\Debbuger\systemMetrics\SystemMetricsbookeeper.csv",
    # "2": r"D:\Debbuger\systemMetrics\SystemMetricsderby.csv",
    "3": r"D:\Debbuger\systemMetrics\SystemMetricsfop.csv",
    "4": r"D:\Debbuger\systemMetrics\SystemMetricskafka.csv",
    "5": r"D:\Debbuger\systemMetrics\SystemMetricsoozie.csv",
    "6": r"D:\Debbuger\systemMetrics\SystemMetricsopennlp.csv",
    "7": r"D:\Debbuger\systemMetrics\SystemMetricssentry.csv",
    "8": r"D:\Debbuger\systemMetrics\SystemMetricstajo.csv",
    "9": r"D:\Debbuger\systemMetrics\SystemMetricstiles.csv"
}

all_projects_data_selected_features = {}
system_metrics_attributes = None
# results = pd.DataFrame(columns=['cold_start_project', 'precision_bug', 'recall_bug','F2_bug','prc_area_bug', 'precision', 'recall','F2','prc_area'])
results_all_projects = pd.DataFrame(
        columns=['cold_start_project','host_model','result_type','features_type','model_source', 'precision_bug', 'recall_bug','F_bug', 'F2_bug','roc_area_bug', 'prc_area_bug', 'precision', 'recall',
                 'F1', 'F2', 'roc_area','prc_area','num_bugs','num_all_inst','percent_bugs','system_features','sampling','num_of_sampling','belongingness','percent_from_best'])

gan_val = pd.DataFrame(
    columns=['cold_start_project','model','system_features','features_type','sampling','num_of_sampling','precision_all', 'recall_all', 'f_measure_all', 'f2_measure_all','accuracy']
)

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

def selectFeatures(data):
    g2_f = g2_attributes()
    all2_att_names = [tup[0] for tup in g2_f]
    if all2_att_names[0] in data.columns:
        g3_f = g3_attributes()
        all3_att_names = [tup[0] for tup in g3_f]
        print data.shape
        new_data = data.drop(all2_att_names, axis=1)
        print new_data.shape
        new_data = new_data.drop(all3_att_names, axis=1)
        print new_data.shape
        data = new_data
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

def encode_categorial(data):
    """
    change the category data to numbers represent the value
    :param data:
    :return:
    """
    le = LabelEncoder()
    for col in data:
        # categorial
        if data[col].dtype == 'object':
            data[col] = data[col].astype('category')
            data[col] = data[col].cat.codes
            data[col] = data[col].astype('category')
    return data

def predict_model_kfold(name,model_details,model,system_features,features_type, x_train, y_train,sampling,num_of_sampling):
    kfold = KFold(5, True)
    # RandomForest -I 1000 -K 0 -S 1 -num-slots 1
    index = 0
    all_predictions = 0
    for train, test in kfold.split(x_train):
        index += 1
        prediction_train = model.fit(x_train.iloc[train], y_train.iloc[train]).predict(x_train.iloc[test])
        all_predictions += create_all_eval_results_gan(y_train.iloc[test], prediction_train)

    all_predictions /= index
    start_list = [str(name), str(model_details), str(system_features), str(features_type), str(sampling),
                  str(num_of_sampling)]
    result_list = start_list + all_predictions.tolist()

    global gan_val
    gan_val.loc[len(gan_val)] = result_list
    model.fit(x_train, y_train)
    return model

def predict_model(model, x_test):
    x_test = encode_categorial(x_test)
    pred = model.predict(x_test)
    return pred

def load_cold_start_testing(type):
    if type=='all':
        return all_projects_testing_all[str(cold_start_index)].copy()
    elif type == 'no_bugs':
        return all_projects_testing_no_bugs[str(cold_start_index)].copy()
    elif type == 'no_process':
        return all_projects_testing_no_process[str(cold_start_index)].copy()

def add_system_features(data,key):
    key_system_metrics = pd.read_csv(system_metrics[key])
    global system_metrics_attributes
    if system_metrics_attributes is None:
        system_metrics_attributes = [column for column in key_system_metrics]
    for column in key_system_metrics:
        data[column] = key_system_metrics[column][0]

    return data


def load_all_models():
    global models_no_process
    global models_no_bugs
    global models_all
    for key, weka_path in all_files.items():
        print("load models - "+str(weka_path))
        models_no_process[key] = pickle.load(open(os.path.join(weka_path, str(data_names[key]).split('\\')[-1] + end_file_no_process), 'rb'))
        models_no_bugs[key] = pickle.load(open(os.path.join(weka_path, str(data_names[key]).split('\\')[-1] + end_file_no_bugs), 'rb'))
        models_all[key] = pickle.load(open(os.path.join(weka_path, str(data_names[key]).split('\\')[-1] + end_file_all), 'rb'))


def get_all_eval_based_on_model(separated,type):
    pred = np.array([])
    real = np.array([])
    if type == 'all':
        global models_all
        dic_models = models_all
    elif type == 'no_bugs':
        global models_no_bugs
        dic_models = models_no_bugs
    else:
        global models_no_process
        dic_models = models_no_process
    for key, data_to_test in separated.items():
        x_test = data_to_test.copy()
        try:
            if x_test.shape[0] != 0:
                x_test = x_test.drop('hasBug', axis=1)
                pred = np.concatenate((pred,  dic_models[key].predict(x_test)), axis=None)
                real = np.concatenate((real,  data_to_test['hasBug']), axis=None)
        except:
            print(list(x_test))
    return pred.tolist(),real.tolist()

def load_arff_from_dir_into_dataFrames_dictionery(system_features):
    for key, val in all_files.items():
        print key, "=>", val
        all_projects_training_selected_features = from_weka_to_python.load_arff(os.path.join(val,from_weka_to_python.training_file))
        all_projects_testing_selected_features = from_weka_to_python.load_arff(os.path.join(val,from_weka_to_python.testing_file))

        if(system_features):
            all_projects_training_selected_features= add_system_features(all_projects_training_selected_features, key)
            all_projects_testing_selected_features= add_system_features(all_projects_testing_selected_features, key)

        all_projects_training_selected_features = from_weka_to_python.pre_processing(all_projects_training_selected_features)
        all_projects_testing_selected_features['hasBug'] = all_projects_testing_selected_features['hasBug'].map({'valid': 0, 'bugged': 1})
        all_projects_testing_selected_features = from_weka_to_python.pre_processing(all_projects_testing_selected_features)

        all_projects_training_selected_features = from_weka_to_python.selectFeatures(all_projects_training_selected_features, False, False)
        all_projects_training_all[key] =all_projects_training_selected_features.copy()
        all_projects_training_selected_features = from_weka_to_python.selectFeatures(all_projects_training_selected_features, True, False)
        all_projects_training_no_bugs[key] = all_projects_training_selected_features.copy()
        all_projects_training_selected_features = from_weka_to_python.selectFeatures(all_projects_training_selected_features, True, True)
        all_projects_training_no_process[key] = all_projects_training_selected_features.copy()

        all_projects_testing_selected_features = from_weka_to_python.selectFeatures(all_projects_testing_selected_features, False, False)
        all_projects_testing_all[key] = all_projects_testing_selected_features.copy()
        all_projects_testing_selected_features = from_weka_to_python.selectFeatures(all_projects_testing_selected_features, True, False)
        all_projects_testing_no_bugs[key] = all_projects_testing_selected_features.copy()
        all_projects_testing_selected_features = from_weka_to_python.selectFeatures(all_projects_testing_selected_features, True, True)
        all_projects_testing_no_process[key] = all_projects_testing_selected_features.copy()

def load_training_set(sampling,num_of_samples = 100):
    training_by_model = {}
    for type in ['all','no_bugs','no_process']:
    # for type in ['all','no_process']:
        if type == 'all':
            global all_projects_training_all
            dic_projects_data =all_projects_training_all
        elif type == 'no_bugs':
            global all_projects_training_no_bugs
            dic_projects_data = all_projects_training_no_bugs
        else:
            global all_projects_training_no_process
            dic_projects_data = all_projects_training_no_process
        datasets = pd.DataFrame()
        for key, val in dic_projects_data.items():
            if int(key) != int(cold_start_index):
                data = val.copy()
                data = data.rename(columns={'hasBug': 'label'})
                data.label = key
                if sampling:
                    datasets = datasets.append(data_sampling(data,num_of_samples), ignore_index=True)
                else:
                    datasets = datasets.append(data, ignore_index=True)
        training_by_model[type] = datasets.copy()
    return training_by_model


def data_sampling(data,num_of_samples):
    random = check_random_state(seed=None)
    n_samples, n_features = data.shape

    if(num_of_samples>n_samples):
        indexes = np.concatenate((sample_without_replacement(n_samples, n_samples, random_state=random), random.randint(0, n_samples, num_of_samples-n_samples)), axis=None)
    else:
        indexes = sample_without_replacement(n_samples, num_of_samples, random_state=random)

    return data.loc[indexes]


def separated_data_by_predicted_model(pred, x_test,system_features,type):
    all_data_separated_dict = {}
    if type == 'all':
        global all_projects_training_all
        dic_projects_data = all_projects_training_all
    elif type == 'no_bugs':
        global all_projects_training_no_bugs
        dic_projects_data = all_projects_training_no_bugs
    else:
        global all_projects_training_no_process
        dic_projects_data = all_projects_training_no_process
    for key, val in dic_projects_data.items():
        if int(key) != int(cold_start_index):
            all_data_separated_dict[key] = x_test.loc[np.where(pred == str(key))]
            if system_features and (not system_metrics_attributes is None):
                all_data_separated_dict[key] = all_data_separated_dict[key].drop(system_metrics_attributes, axis = 1)
    return all_data_separated_dict


def change_pred(pred_num):
    if pred_num == 1 :
        return 0
    else:
        return 1

def create_prediction_best_and_worse(x_test,type,pred_ours):
    df_all_pred = pd.DataFrame(columns=range(x_test.shape[0]))

    if type == 'all':
        global models_all
        dic_models = models_all
    elif type == 'no_bugs':
        global models_no_bugs
        dic_models = models_no_bugs
    else:
        global models_no_process
        dic_models = models_no_process

    x_test_no_label = x_test.drop('hasBug', axis=1)
    label_true = x_test['hasBug']

    for key, model in dic_models.items():
        if int(key) != int(cold_start_index):
            predict = model.predict(x_test_no_label)
            l_pred = [tuple(predict)]
            df_all_pred = df_all_pred.append(l_pred).rename(index={0:int(key)})

    best_model_to_predict = []
    worst_model_to_predict = []
    for component in range(x_test.shape[0]):
        comp_sieries = df_all_pred[component]
        best_model_to_predict.append((list(comp_sieries[comp_sieries==label_true[component]].index),label_true[component]))
        worst_model_to_predict.append((list(comp_sieries[comp_sieries!=label_true[component]].index),label_true[component]))

    best_prediction = [prediction[1] if len(prediction[0])>0 else change_pred(prediction[1]) for prediction in best_model_to_predict ]
    worse_prediction = [change_pred(prediction[1]) if len(prediction[0])>0 else prediction[1] for prediction in worst_model_to_predict ]

    same = 0
    for our_model_prediction , best_models_prediction in zip(pred_ours,best_model_to_predict) :
       if long(our_model_prediction) in best_models_prediction[0]:
           same+=1

    precent_ours = float(same) / len(pred_ours)

    return best_prediction,worse_prediction,precent_ours


def separated_data_randomly(x_test,system_features,type):
    all_data_separated_dict = {}
    if type == 'all':
        global all_projects_training_all
        dic_projects_data = all_projects_training_all
    elif type == 'no_bugs':
        global all_projects_training_no_bugs
        dic_projects_data = all_projects_training_no_bugs
    else:
        global all_projects_training_no_process
        dic_projects_data = all_projects_training_no_process

    random = check_random_state(seed=None)
    x_test_mat = x_test.copy()
    for key, val in dic_projects_data.items():
        if int(key) != int(cold_start_index):
            num_of_recored_left = x_test_mat.shape[0]
            if num_of_recored_left > 1:
                try:
                    num_of_record_to_take = random.randint(0, num_of_recored_left)
                    indexes = sample_without_replacement(num_of_recored_left, num_of_record_to_take, random_state=random)
                    all_data_separated_dict[key] = x_test_mat.iloc[indexes]
                    x_test_mat = x_test_mat.drop(x_test_mat.index[indexes])
                    if system_features and (not system_metrics_attributes is None):
                        all_data_separated_dict[key] = all_data_separated_dict[key].drop(system_metrics_attributes, axis = 1)
                except:
                    all_data_separated_dict[key] = pd.DataFrame()
            else:
                all_data_separated_dict[key] = pd.DataFrame()

    if x_test_mat.shape[0] != 0:
        key_choosen = random.choice(all_data_separated_dict.keys())
        all_data_separated_dict[key_choosen] = all_data_separated_dict[key_choosen].append(x_test_mat,ignore_index = True)

    return all_data_separated_dict

def export_info_about_seperation(separated_dataframe,type,cold_start_proj,saving_path,sampling,model_details,number_of_sampling,system_features):
    sep_results = pd.DataFrame(
        columns=['cold_start_project', 'model_chosen','model_details','number_of_records_in_train','number_of_records_to_the_model','features_type'])

    for key, val in separated_dataframe.items():
        if sampling:
            sep_results.loc[len(sep_results)] = [str(data_names[cold_start_proj]).split('\\')[-1], str(data_names[key]).split('\\')[-1],model_details,
                                                 number_of_sampling,val.shape[0],type]
        else:
            if type == 'all':
                global all_projects_training_all
                dic_projects_data = all_projects_training_all
            elif type == 'no_bugs':
                global all_projects_training_no_bugs
                dic_projects_data = all_projects_training_no_bugs
            else:
                global all_projects_training_no_process
                dic_projects_data = all_projects_training_no_process
            sep_results.loc[len(sep_results)] = [str(data_names[cold_start_proj]).split('\\')[-1], str(data_names[key]).split('\\')[-1],model_details,
                                                 dic_projects_data[key].shape[0], val.shape[0],type]

    sep_results.to_csv(os.path.join(saving_path, str(data_names[cold_start_proj]).split('\\')[-1]+"_"+str(sampling)+"_"+str(system_features)+"_"+str(number_of_sampling)+"_"+str(type)+"_"+str(model_details)+".csv"), index=False)

def get_eval(saving_path):
    datasets = pd.DataFrame()
    for filename in os.listdir(saving_path):
        if filename.endswith('.csv'):
            csv_file = os.path.join(saving_path, filename)
            print(csv_file)
            datasets = datasets.append(pd.read_csv(csv_file), ignore_index=True)
    return datasets


def calculateF2(precision, recall):
    if ((4 * precision) + recall) != 0:
        F2BUGS = (5 * ((precision * recall) / ((4 * precision) + recall)))
    else:
        F2BUGS = 0
    return F2BUGS
def create_all_eval_results_gan(y_true, y_pred):
    precision_all = metrics.precision_score(y_true, y_pred, average='weighted')
    recall_all = metrics.recall_score(y_true, y_pred, average='weighted')
    f_measure_all = metrics.f1_score(y_true, y_pred,average='weighted')
    f2_measure_all = calculateF2(precision_all, recall_all)
    accuracy = metrics.accuracy_score(y_true,y_pred)

    return np.array(list((precision_all, recall_all, f_measure_all, f2_measure_all,accuracy)))

def create_all_eval_results(y_true, y_pred, key,result_type,features_type,num_of_bugs,num_of_all_instances,bugs_Precent,from_model,system_features,belong,percent=" "):
    precision_bugged = metrics.precision_score(y_true,y_pred,pos_label=1,average='binary')
    recall_bugged = metrics.recall_score(y_true,y_pred,pos_label=1,average='binary')
    f_measure_bugged = metrics.f1_score(y_true,y_pred,pos_label=1,average='binary')
    f2_measure_bugged = calculateF2(precision_bugged,recall_bugged)

    un_true,_ = np.unique(y_true, return_counts=True)
    un_pred,_ = np.unique(y_pred, return_counts=True)
    if len(un_true) ==1 or len(un_pred)==1:
        y_true.append(0)
        y_true.append(1)
        y_pred.append(0)
        y_pred.append(1)
        print("zero or ones")
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

    global results_all_projects
    results_all_projects.loc[len(results_all_projects)] = [key, from_model, result_type, features_type,
                                                           "record-sensitive", precision_bugged,
                                                           recall_bugged, f_measure_bugged,
                                                           f2_measure_bugged, roc_bugged, prc_bugged,
                                                           precision_all, recall_all, f_measure_all, f2_measure_all,
                                                           roc_all, prc_all, num_of_bugs, num_of_all_instances,
                                                           bugs_Precent, str(system_features), str(sampling),
                                                           str(num_of_samples),belong,percent]

def set_global_cold_start(number):
    global cold_start_index
    cold_start_index = number


def create_models_and_eval(system_features,sampling,model_details,model,num_of_samples):
    for key, saving_path in data_names.items():
        set_global_cold_start(int(key))
        training_by_models = load_training_set(sampling,num_of_samples)
        for type in ['all', 'no_bugs', 'no_process']:
            print("start process for: "+str(saving_path))
            tr_data_all = training_by_models[type].drop('label', axis=1)
            #my_model = predict_model_kfold(str(data_names[key]).split('\\')[-1], model_details, model, system_features,
            #                           type, tr_data_all, training_by_models[type]['label'], sampling, num_of_samples)
            belonging_model = model.fit(tr_data_all, training_by_models[type]['label'])
            all_x_test = load_cold_start_testing(type)
            x_test = all_x_test.copy()
            x_test = x_test.drop('hasBug', axis=1)

            # pred_ours is the list of belongingness prediction by our models
            pred_models_ours = belonging_model.predict(x_test)
            separated_ours = separated_data_by_predicted_model(pred_models_ours.copy(), all_x_test,system_features,type)
            #export_info_about_seperation(separated_ours,type,key,saving_path,sampling,model_details,num_of_samples,system_features)
            pred_ours,real_ours = get_all_eval_based_on_model(separated_ours,type)

            num_of_bugs = real_ours.count(1)
            num_of_all_instances = len(real_ours)
            try:
                bug_precent = float(num_of_bugs) / float(num_of_all_instances)
            except:
                bug_precent = 0

            best_prediction, worse_prediction,percent_ours = create_prediction_best_and_worse(all_x_test, type,pred_models_ours)
            separated_random = separated_data_randomly(all_x_test, system_features, type)

            #export_info_about_seperation(separated_random, type, key, saving_path, sampling, model_details, num_of_samples,system_features)

            pred_random, real_random = get_all_eval_based_on_model(separated_random, type)


            create_all_eval_results(real_ours, pred_ours, str(data_names[key]).split('\\')[-1], "testing", type, num_of_bugs,
                                    num_of_all_instances, bug_precent, model_details, system_features,"DSFPM",percent_ours)

            create_all_eval_results(real_random, pred_random,str(data_names[key]).split('\\')[-1],"testing",type,num_of_bugs,num_of_all_instances,bug_precent,model_details,system_features,"random")

            create_all_eval_results(all_x_test['hasBug'], worse_prediction,str(data_names[key]).split('\\')[-1],"testing",type,num_of_bugs,num_of_all_instances,bug_precent,model_details,system_features,"Worst")
            create_all_eval_results(all_x_test['hasBug'], best_prediction,str(data_names[key]).split('\\')[-1],"testing",type,num_of_bugs,num_of_all_instances,bug_precent,model_details,system_features,"Best")




def create_models_and_eval_all_random(system_features,sampling,model_details,model,num_of_samples):
    for key, saving_path in data_names.items():
        set_global_cold_start(int(key))
        # training_by_models = load_training_set(sampling,num_of_samples)
        for type in ['all', 'no_bugs', 'no_process']:
            print("start process for: "+str(saving_path))
            # tr_data_all = training_by_models[type].drop('label', axis=1)
            # my_model = predict_model_kfold(str(data_names[key]).split('\\')[-1], model_details, model, system_features,
            #                            type, tr_data_all, training_by_models[type]['label'], sampling, num_of_samples)
            all_x_test = load_cold_start_testing(type)
            # x_test = all_x_test.copy()
            # x_test = x_test.drop('hasBug', axis=1)
            # pred = my_model.predict(x_test)
            separated = separated_data_randomly(all_x_test,system_features,type)
            export_info_about_seperation(separated,type,key,saving_path,sampling,model_details,num_of_samples,system_features)
            pred,real = get_all_eval_based_on_model(separated,type)
            num_of_bugs = real.count(1)
            num_of_all_instances = len(real)
            try:
                bug_precent = float(num_of_bugs) / float(num_of_all_instances)
            except:
                bug_precent = 0
            create_all_eval_results(real, pred,str(data_names[key]).split('\\')[-1],"testing",type,num_of_bugs,num_of_all_instances,bug_precent,model_details,system_features)



models ={
        "random_forest_100": RandomForestClassifier(n_estimators=100,max_depth=5)
        # "xgb": XGBClassifier(n_estimators=100, max_depth=6)
        # "gradient_boostong": GradientBoostingClassifier(learning_rate=0.01, max_depth=5,n_estimators=100)
    }

print("load all models...")
load_all_models()
print("finished load all models...")

index = 0
for model_details, model in models.items():
    for system_features in [False]:
        load_arff_from_dir_into_dataFrames_dictionery(system_features)
        for sampling in [True,False]:
            if(sampling):
                for num_of_samples in [4000,10000,15000]:
                    index+=1
                    print("start process_"+str(system_features)+"_"+str(sampling)+"_"+str(num_of_samples))
                    create_models_and_eval(system_features, sampling,model_details,model,num_of_samples)
                    #create_models_and_eval_all_random(system_features, sampling,model_details,model,num_of_samples)

                    results_all_projects.to_csv(os.path.join(results_path, "gan_results_all_belong" + str(index) + ".csv"), index=False)
                    #gan_val.to_csv(os.path.join(results_path, "gan_seperation_model_results_random" + str(index) + ".csv"),index=False)
            else:
                index += 1
                print("start process_" + str(system_features) + "_" + str(sampling))

                create_models_and_eval(system_features, sampling, model_details,model,"-")
                #create_models_and_eval_all_random(system_features, sampling, model_details,model,"-")
                results_all_projects.to_csv(os.path.join(results_path, "gan_results_all_belong"+str(index)+".csv"), index=False)
                #gan_val.to_csv(os.path.join(results_path, "gan_seperation_model_results_random" + str(index) + ".csv"),index=False)

        global all_projects_training_no_process
        global all_projects_training_no_bugs
        global all_projects_training_all
        global all_projects_testing_no_process
        global all_projects_testing_no_bugs
        global all_projects_testing_all
        all_projects_training_no_process = {}
        all_projects_training_no_bugs = {}
        all_projects_training_all = {}
        all_projects_testing_no_process = {}
        all_projects_testing_no_bugs = {}
        all_projects_testing_all = {}

index+=1
results_all_projects.to_csv(os.path.join(results_path, "gan_results_all_belong" + str(index) + str(index) + ".csv"), index=False)
#gan_val.to_csv(os.path.join(results_path, "gan_seperation_model_results_random" + str(index) +  ".csv"), index=False)


