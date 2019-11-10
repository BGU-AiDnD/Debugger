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

def separated_data_randomly( x_test,system_features,type):
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
