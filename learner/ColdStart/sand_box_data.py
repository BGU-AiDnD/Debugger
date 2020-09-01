import pandas as pd
import xml.etree.ElementTree as et
from scipy.io import arff
from scipy.io.arff import loadarff
import os
import pickle
from imblearn.ensemble import BalancedRandomForestClassifier
import numpy as np
from decimal import *

data = pickle.load(open(r'D:\Debbuger\our projects style promise\within_models_full_ours_f\within_models_full_ours_f.sav', "rb"))

dir = r'D:\Debbuger\new_data\DATA-SET'
for proj_name_host, (model_host, training_set_host, testing_set_host) in data.items():
    print(proj_name_host)
    print("trainng set shape: "+ str(training_set_host.shape))
    training_set_host.to_csv(os.path.join( os.path.join( dir ,proj_name_host) ,"training.csv"),index=False)
    print("testing set shape: "+ str(testing_set_host.shape))
    testing_set_host.to_csv(os.path.join( os.path.join( dir ,proj_name_host) ,"testing.csv"),index=False)


#model,cur_bookkeeper,_ = data['bookkeeper']
#cur_bookkeeper.to_csv(r'D:\Debbuger\our projects style promise\within_models_full_ours_f\data.csv',index=False)
#print(model.feature_importances_)