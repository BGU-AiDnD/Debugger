import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
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
from imblearn.ensemble import BalancedRandomForestClassifier


import os
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
                if tr_data_noNa[col].dtype != 'object':
                    col_mean = data[col].mean()
                    tr_data_noNa[col].fillna(col_mean, inplace=True)
    return tr_data_noNa



tr_data = pd.read_csv(r'C:\Users\USER\Documents\repo.csv')
tr_data = tr_data.replace(r'-', np.NaN )
print(tr_data.dtypes)
print('train shape is: {} '.format(tr_data.shape))

tr_data['noc'] = tr_data.noc.astype(float)
tr_data['ce'] = tr_data.ce.astype(float)
print(tr_data.dtypes)

#tr_data['noc'].astype(str).astype(int)
#tr_data['ce'].astype(str).astype(int)

print(tr_data.isnull().sum())
null_data = tr_data[tr_data.isnull().any(axis=1)]
print(null_data.shape)


print(tr_data.head())

tr_data = pre_processing(tr_data)

print(tr_data.isnull().sum())
null_data = tr_data[tr_data.isnull().any(axis=1)]
print(null_data.shape)

#TODO: create new col from proj and version and seperate the data to mini dataframes .

uniq_projects = tr_data.name.unique()










