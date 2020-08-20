import pandas as pd
import xml.etree.ElementTree as et
from scipy.io import arff
from scipy.io.arff import loadarff
import os
import pickle
from imblearn.ensemble import BalancedRandomForestClassifier
import numpy as np
from decimal import *


metrics_traditional = ['WMC','DIT','NOCh','LCOM*','Ma','NPM','RTLOC','MIF']
metrics_smells = ['GodClass',	'ClassDataShouldBePrivate',	'ComplexClass',	'LazyClass',	'RefusedBequest','SpaghettiCode','SpeculativeGenerality','DataClass','BrainClass','LargeClass','SwissArmyKnife','AntiSingleton']
lable_metric = 'Bugged'
metric_always_drop = ['NPathComplexity']

directory_path = r'D:\Debbuger\to_inbal\to_inbal\fowler_traditional'
folder_data = 'dataset'
testing_file = 'testing.csv'
training_file = 'training.csv'

directory_path_all = r'D:\Debbuger\b_data\all'
directory_path_fowler = r'D:\Debbuger\b_data\fowler'
directory_path_trad = r'D:\Debbuger\b_data\trad'

dict_name = 'dict_all_models_and_data'

dict_trad = {}
dict_fowler = {}
dict_all = {}

def save_model_dump(path,name,model):
    file_path = os.path.join(path, name)
    pickle.dump(model, open(file_path, 'wb'))

def fit_model(data):
    model = BalancedRandomForestClassifier(n_estimators=1000, max_depth=5)
    x = data.drop(lable_metric, axis=1)
    y = data[lable_metric]
    num_of_bugs = data.loc[data[lable_metric] == 1].shape[0]
    if num_of_bugs == 0:
        print("NO BUGS")
        return None
    model.fit(x, y)
    return model

def preper_fowler(training_set, testing_set):
    training_set_f = training_set.copy()
    training_set_f = training_set_f[metrics_smells]
    training_set_f[lable_metric] = training_set[lable_metric]
    testing_set_f = testing_set.copy()
    testing_set_f = testing_set_f[metrics_smells]
    testing_set_f[lable_metric] = testing_set[lable_metric]
    testing_set_f = testing_set_f.dropna()
    training_set_f = training_set_f.dropna()
    for col in training_set_f:
        training_set_f[col] = training_set_f[col].map(
            {'true': 1, 'false': 0, 'True': 1, 'False': 0, 'TRUE': 1, 'FALSE': 0, False: 0, True: 1})
        testing_set_f[col] = testing_set_f[col].map(
            {'true': 1, 'false': 0, 'True': 1, 'False': 0, 'TRUE': 1, 'FALSE': 0, False: 0, True: 1})

    cur_model = fit_model(training_set_f)
    if cur_model is None:
        return None, None, None

    return training_set_f, testing_set_f, cur_model

def preper_trad(training_set, testing_set):
    training_set_f = training_set.copy()
    testing_set_f = testing_set.copy()
    training_set_f = training_set_f.replace([np.inf, -np.inf], np.nan)
    testing_set_f = testing_set_f.replace([np.inf, -np.inf], np.nan)
    testing_set_f = testing_set_f.dropna()
    training_set_f = training_set_f.dropna()
    training_set_f = training_set_f.drop(metrics_smells,axis = 1)
    testing_set_f = testing_set_f.drop(metrics_smells,axis = 1)

    training_set_f[lable_metric] = training_set_f[lable_metric].map(
        {'true': 1, 'false': 0, 'True': 1, 'False': 0, 'TRUE': 1, 'FALSE': 0, False: 0, True: 1})
    testing_set_f[lable_metric] = testing_set_f[lable_metric].map(
        {'true': 1, 'false': 0, 'True': 1, 'False': 0, 'TRUE': 1, 'FALSE': 0, False: 0, True: 1})

    training_set_f = training_set_f.reset_index()
    cur_model = fit_model(training_set_f)
    if cur_model is None:
        return None, None, None

    return training_set_f, testing_set_f, cur_model

def preper_all_f(training_set, testing_set):
    training_set_f = training_set.copy()
    testing_set_f = testing_set.copy()
    training_set_f = training_set_f.replace([np.inf, -np.inf], np.nan)
    testing_set_f = testing_set_f.replace([np.inf, -np.inf], np.nan)
    testing_set_f = testing_set_f.dropna()
    training_set_f = training_set_f.dropna()
    for col in training_set_f:
        if col in metrics_smells:
            training_set_f[col] = training_set_f[col].map(
                {'true': 1, 'false': 0, 'True': 1, 'False': 0, 'TRUE': 1, 'FALSE': 0, False: 0, True: 1})
            testing_set_f[col] = testing_set_f[col].map(
                {'true': 1, 'false': 0, 'True': 1, 'False': 0, 'TRUE': 1, 'FALSE': 0, False: 0, True: 1})
    training_set_f[lable_metric] = training_set_f[lable_metric].map(
        {'true': 1, 'false': 0, 'True': 1, 'False': 0, 'TRUE': 1, 'FALSE': 0, False: 0, True: 1})
    testing_set_f[lable_metric] = testing_set_f[lable_metric].map(
        {'true': 1, 'false': 0, 'True': 1, 'False': 0, 'TRUE': 1, 'FALSE': 0, False: 0, True: 1})

    cur_model = fit_model(training_set_f)
    if cur_model is None:
        return None, None, None

    return training_set_f, testing_set_f, cur_model

for project_name in os.listdir(directory_path):
     folder = os.path.join(directory_path, project_name)
     if os.path.isdir(folder):
         testing_file_path = os.path.join(os.path.join(os.path.join(directory_path,folder),folder_data),testing_file)
         training_file_path = os.path.join(os.path.join(os.path.join(directory_path,folder),folder_data),training_file)
         if os.path.isfile(testing_file_path) and os.path.isfile(training_file_path):
            print("start working on "+ folder)
            train_data = pd.read_csv(training_file_path)
            test_data = pd.read_csv(testing_file_path)
            train_data = train_data.drop(metric_always_drop,axis = 1)
            test_data = test_data.drop(metric_always_drop,axis = 1)
            training_set_f, testing_set_f, cur_model_f = preper_fowler(train_data,test_data)
            training_set_t, testing_set_t, cur_model_t = preper_trad(train_data,test_data)
            training_set_a, testing_set_a, cur_model_a = preper_all_f(train_data,test_data)
            if training_set_f is not None and training_set_t is not None and training_set_a is not None:
                #proj_name, (model,training_set, testing_set)
                dict_fowler[project_name] = (cur_model_f,training_set_f,testing_set_f)
                dict_trad[project_name] = (cur_model_t,training_set_t,testing_set_t)
                dict_all[project_name] = (cur_model_a,training_set_a,testing_set_a)
                print("folder all done")

save_model_dump(directory_path_all,dict_name,dict_all)
save_model_dump(directory_path_fowler,dict_name,dict_fowler)
save_model_dump(directory_path_trad,dict_name,dict_trad)

len(dict_all)
index = 1
for key, val in dict_all.items():
    print(str(index) + " :   " + str(key))
    index = index+1

