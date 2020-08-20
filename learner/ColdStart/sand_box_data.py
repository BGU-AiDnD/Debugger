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
model,cur_bookkeeper,_ = data['bookkeeper']
#cur_bookkeeper.to_csv(r'D:\Debbuger\our projects style promise\within_models_full_ours_f\data.csv',index=False)
print(model.feature_importances_)