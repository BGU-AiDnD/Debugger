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

#adding extreme learning
from sklearn_extensions.extreme_learning_machines.elm import GenELMClassifier
from sklearn_extensions.extreme_learning_machines.random_layer import RBFRandomLayer, MLPRandomLayer

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
import elm


results_all_projects = pd.DataFrame(
        columns=['cold_start_project','model_source', 'precision_bug', 'recall_bug','F_bug', 'F2_bug','roc_area_bug', 'prc_area_bug', 'precision', 'recall',
                 'F1', 'F2', 'roc_area','prc_area','num_bugs','num_all_inst','precent_bugs'])

def save_model_dump(path,name,model):
    file_path = os.path.join(path, name)
    pickle.dump(model, open(file_path, 'wb'))

def pre_processing(data):
    # data = selectFeatures(data)
    # print(data.isnull().sum())
    null_data = data[data.isnull().any(axis=1)]
    print(null_data.shape)
    num_of_rows = null_data.shape[0]
    tr_data_noNa = data.copy()
    if num_of_rows!= 0:
        for col in tr_data_noNa.columns[:-1]:
            if tr_data_noNa[col].dtype != 'object':
                col_mean = data[col].mean()
                tr_data_noNa[col].fillna(col_mean, inplace=True)
            if col not in ['Project', 'label', 'bugs', 'Version', 'unique_name', 'Class']:
                    ############for normalization:
                print(col)
                print(tr_data_noNa[col])
                tr_data_noNa[col] = (tr_data_noNa[col] - tr_data_noNa[col].min()) / (
                                tr_data_noNa[col].max() - tr_data_noNa[col].min())

    return tr_data_noNa

def calculateF2(precision, recall):
    if ((4 * precision) + recall) != 0:
        F2BUGS = (5 * ((precision * recall) / ((4 * precision) + recall)))
    else:
        F2BUGS = 0
    return F2BUGS
def create_all_eval_results(export,y_true, y_pred, key,result_type,num_of_bugs,num_of_all_instances,bugs_Precent,from_model):

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
                                                           roc_all, prc_all, num_of_bugs, num_of_all_instances,
                                                           bugs_Precent]


    return np.array(list((precision_bugged,recall_bugged, f_measure_bugged,
                                            f2_measure_bugged, roc_bugged, prc_bugged,
                                            precision_all, recall_all, f_measure_all, f2_measure_all,
                                            roc_all, prc_all, num_of_bugs, num_of_all_instances,
                                            bugs_Precent)))
def predict_model_kfold(name,data):
    kfold = KFold(5, True)
    model = BalancedRandomForestClassifier(n_estimators=1000,max_depth=5)
    nh = 10
    #srhl_rbf = RBFRandomLayer(n_hidden=nh * 2, rbf_width=0.1, random_state=0)
    #model = GenELMClassifier(hidden_layer=srhl_rbf)

    index = 0
    all_predictions = 0
    x = data.drop('bugs', axis=1)
    y = data['bugs']
    num_of_bugs = data.loc[data['bugs'] == 1].shape[0]
    num_of_all_instances = data.shape[0]
    bug_precent = float(num_of_bugs) / float(num_of_all_instances)
    for train, test in kfold.split(data):
        index += 1
        #X = (x.iloc[train]).rename_axis('ID').values
        X = (x.iloc[train])

        Y = y.iloc[train]

        #X_test = (x.iloc[test]).rename_axis('ID').values
        X_test = (x.iloc[test])

        #prediction_train = model.fit(X,Y).predict(X_test)
        prediction_train = model.fit(X,Y).predict(X_test)
        all_predictions += create_all_eval_results(True,(y.iloc[test]).tolist(),prediction_train.tolist(),name,"K-FOLD",num_of_bugs,num_of_all_instances,bug_precent,"K-FOLD")

    all_predictions /= index
    start_list = [name,"K-FOLD-AVG"]
    result_list = start_list+ all_predictions.tolist()

    global results_all_projects
    results_all_projects.loc[len(results_all_projects)] = result_list

    #model.fit(x.rename_axis('ID').values,y)
    model.fit(x,y)
    return model

def prep_within_models(dict_all_data_sets,path):
    for name_train, df_train in dict_all_data_sets.items():
        print(name_train)
        df_train = df_train.drop(['Class', 'unique_name'], axis=1)
        model = predict_model_kfold(name_train,df_train)
        save_model_dump(path,name_train+".sav",model)


def create_all_data_with_models_sav(directory,data_file):
    data = pickle.load(open( data_file, "rb" ))
    #del data['ckjm1.8']
    for filename in os.listdir(directory):
        if filename.endswith(".sav"):
            print(os.path.join(directory, filename))
            current_model = pickle.load(open( os.path.join(directory, filename) , "rb" ))
            data[filename[:-4]] = (current_model,data[filename[:-4]])
            print(os.path.join(directory, filename))

    file_path = os.path.join(directory, 'all_data_with_models_TREE.sav')
    pickle.dump(data, open(file_path, 'wb'))



nh = 10

'''
tr_data = pd.read_csv(r'D:\Debbuger\PROMISE\repo.csv')
tr_data = tr_data.replace(r'-', np.NaN )
#print(tr_data.dtypes)
#print('train shape is: {} '.format(tr_data.shape))

tr_data['noc'] = tr_data.noc.astype(float)
tr_data['ce'] = tr_data.ce.astype(float)
#print(tr_data.dtypes)
#tr_data['noc'].astype(str).astype(int)
#tr_data['ce'].astype(str).astype(int)

#print(tr_data.isnull().sum())
#null_data = tr_data[tr_data.isnull().any(axis=1)]
#print(null_data.shape)
#print(tr_data.head())
tr_data = pre_processing(tr_data)
print(tr_data.head)
#print(tr_data.isnull().sum())
#null_data = tr_data[tr_data.isnull().any(axis=1)]
#print(null_data.shape)
tr_data.loc[tr_data['bugs'] > 0, 'bugs'] = 1
#TODO: create new col from proj and version and seperate the data to mini dataframes .

uniq_projects = tr_data.Project.unique()
#print(uniq_projects)
tr_data['unique_name'] = tr_data.apply(lambda row: row.Project +row.Version[:3], axis=1)
a = (tr_data.unique_name.unique())
tr_data= tr_data.drop(['Project', 'Version'], axis=1)
print(a)
dict = tr_data.groupby(['unique_name'])
dict= {name:group for name,group in dict}
save_model_dump(r'D:\Debbuger\PROMISE',"all_training_data_normalize.sav", dict)

'''

#'''
#file_path = os.path.join(r'D:\Debbuger\PROMISE', "all_training_data.sav")


dict = pickle.load(open( r'D:\Debbuger\PROMISE\all_training_data_normalize.sav', "rb" ))

#save_model_dump("all_training_data_new.sav", dict)

prep_within_models(dict,r'D:\Debbuger\PROMISE\TREE_normal')

results_all_projects.to_csv(r"D:\Debbuger\PROMISE\all_results_with_TREE_normal.csv", index=False)

#'''

create_all_data_with_models_sav(r'D:\Debbuger\PROMISE\TREE_normal',r'D:\Debbuger\PROMISE\all_training_data_normalize.sav')


#dict.get_group('poi2.5')
#dict.groups



