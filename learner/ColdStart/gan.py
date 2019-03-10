
from collections import Counter
import numpy as np
import arff
import os
import pandas as pd
from scipy.io.arff import loadarff
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
from sklearn.preprocessing import LabelEncoder

#import tensorflow as tf

data_arff = r"D:\Debbuger\BestOverAllProjectData\BOOKKEEPER\weka\All_training_File.arff"

cold_start_index = 4

all_file_training = {
    "1" : "D:\Debbuger\GAN\BOOKKEEPER\weka\All_training_File.arff",
    #"2" : "D:\Debbuger\GAN\DERBY\weka\All_training_File.arff",
    #"3" : "D:\Debbuger\GAN\FOP\weka\All_training_File.arff",
    "4" : "D:\Debbuger\GAN\KAFKA\weka\All_training_File.arff",
    "5" : "D:\Debbuger\GAN\OOZIE\weka\All_training_File.arff",
    "6" : "D:\Debbuger\GAN\OPENNLP\weka\All_training_File.arff",
    "7" : "D:\Debbuger\GAN\SENTRY\weka\All_training_File.arff",
    "8" : "D:\Debbuger\GAN\TAJO\weka\All_training_File.arff",
	"9" : "D:\Debbuger\GAN\TILES\weka\All_training_File.arff"
	}

data_names = {
    "1" : "BOOKKEEPER",
    "2" : "DERBY",
    "3" : "FOP",
    "4" : "KAFKA",
    "5" : "OOZIE",
    "6" : "OPENNLP",
    "7" : "SENTRY",
    "8" : "TAJO",
	"9" : "TILES"
	}

all_file_models = {
    "1" : "D:\Debbuger\GAN\BOOKKEEPER\modelfiles_All.model",
    #"2" : "D:\Debbuger\GAN\DERBY\modelfiles_All.model",
    #"3" : "D:\Debbuger\GAN\FOP\modelfiles_All.model",
    "4" : "D:\Debbuger\GAN\KAFKA\modelfiles_All.model",
    "5" : "D:\Debbuger\GAN\OOZIE\modelfiles_All.model",
    "6" : "D:\Debbuger\GAN\OPENNLP\modelfiles_All.model",
    "7" : "D:\Debbuger\GAN\SENTRY\modelfiles_All.model",
    "8" : "D:\Debbuger\GAN\TAJO\modelfiles_All.model",
	"9" : "D:\Debbuger\GAN\TILES\modelfiles_All.model"
	}

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


def train_model(x_train,y_train):
    x_train = encode_categorial(x_train)
    model = RandomForestClassifier()
    model.fit(x_train, y_train)
    #pickle.dump(model, open("D:\Debbuger\GAN", 'wb'))
    return model


def predict_model(model,x_test):
    x_test = encode_categorial(x_test)
    pred = model.predict(x_test)
    return pred


def load_arff(label,data_arff):
    raw_data = loadarff(data_arff)
    df_data = pd.DataFrame(raw_data[0])
    df_data = df_data.rename(columns={'hasBug': 'label'})
    df_data.label = label
    return df_data


def load_cold_start_arff_into_dataFrames():
    cold = load_arff(cold_start_index,all_file_training[str(cold_start_index)])
    return cold


def load_arff_from_dir_into_dataFrames():
    datasets = pd.DataFrame()
    for key, val in all_file_training.items():
        if int(key) != int(cold_start_index):
            print key, "=>", val
            datasets = datasets.append(load_arff(key,val), ignore_index=True)
    return datasets

def pre_processing(data):
    print(data.isnull().sum())
    null_data = data[data.isnull().any(axis=1)]
    print(null_data.shape)
    tr_data_noNa = data.copy()
    for col in tr_data_noNa.columns[:-1]:
        if col!='label' or col!='hasBug':
            if tr_data_noNa[col].dtype == 'object':
                #         col_mode = mode(tr_data[col].astype(str)).mode[0]
                #         tr_data[col].fillna(col_mode,inplace=True)
                tr_data_noNa[col].fillna("Unknown", inplace=True)
            else:
                col_mean = data[col].mean()
                tr_data_noNa[col].fillna(col_mean, inplace=True)
    return tr_data_noNa


def separated_data_by_predicted_model(pred,x_test):
    all_data_separated_dict = {}
    for key, val in all_file_training.items():
        if int(key) != int(cold_start_index):
            all_data_separated_dict[key] = x_test.loc[np.where(pred == str(key))]
    return all_data_separated_dict

def create_arff_from_dataframes(df_dictionry):

    for key, val in df_dictionry.items():
        if int(key) != int(cold_start_index):
            arff.dump(str(key)+'.arff'
              , val.values
              , relation='relation name'
              , names=val.columns)

def run_testing_files(weka, testing, name, wekaJar):
    algorithm="weka.classifiers.trees.RandomForest"
    os.system("cd /d  "+ (weka) +" & java -Xmx2024m  -cp "+ (wekaJar) +" weka.Run " +algorithm+ " -l .\\model"+name+".model -T "+testing+" -classifications \"weka.classifiers.evaluation.output.prediction.CSV -file testing"+name+".csv\" ")
    os.system("cd /d  "+ (weka) +" & java -Xmx2024m  -cp "+ (wekaJar) +" weka.Run " +algorithm+ " -l .\\bestModel.model -T "+testing+" > "+name+".txt ")


def create_all_predictions_based_on_dest_model():
    pass




df = load_arff_from_dir_into_dataFrames()
tr_data = df.drop('label', axis=1)
tr_data = pre_processing(tr_data)
my_model = train_model(tr_data,df['label'])
all_x_test = load_cold_start_arff_into_dataFrames()
x_test = all_x_test.copy()
x_test = x_test.drop('label', axis=1)
x_test = pre_processing(x_test)
pred = predict_model(my_model,x_test)
separated = separated_data_by_predicted_model(pred,x_test)

a=1