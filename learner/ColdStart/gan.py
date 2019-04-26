from collections import Counter
import numpy as np
import arff
import os
import pandas as pd
from scipy.io.arff import loadarff
from sklearn.ensemble import RandomForestClassifier
# xgboost
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import check_random_state
from sklearn.utils.random import sample_without_replacement

# import tensorflow as tf

# mycomp:
wekaJar = 'C:\\Users\\USER\\Documents\\Debugger\\Debugger\\utils\\weka.jar'  # os.path.join(utilsPath, "weka.jar")

# server:
# wekaJar = 'C:\\Users\\inbalros\\PycharmProjects\\Debugger\\utils\\weka.jar'


results_path = r'D:\Debbuger\GAN'

arff_start_path = r'D:\Debbuger\GAN\arff_start.txt'

data_arff = r"D:\Debbuger\BestOverAllProjectData\BOOKKEEPER\weka\All_training_File.arff"


cold_start_index = -1


all_file_training = {
    "1": "D:\Debbuger\GAN\BOOKKEEPER\weka\All_training_File.arff",
    # "2" : "D:\Debbuger\GAN\DERBY\weka\All_training_File.arff",
    # "3" : "D:\Debbuger\GAN\FOP\weka\All_training_File.arff",
    "4": "D:\Debbuger\GAN\KAFKA\weka\All_training_File.arff",
    "5": "D:\Debbuger\GAN\OOZIE\weka\All_training_File.arff",
    "6": "D:\Debbuger\GAN\OPENNLP\weka\All_training_File.arff",
    "7": "D:\Debbuger\GAN\SENTRY\weka\All_training_File.arff",
    "8": "D:\Debbuger\GAN\TAJO\weka\All_training_File.arff",
    "9": "D:\Debbuger\GAN\TILES\weka\All_training_File.arff"
}


data_names = {
    "1": r"D:\Debbuger\GAN\BOOKKEEPER",
    # "2": r"D:\Debbuger\GAN\DERBY",
    # "3": r"D:\Debbuger\GAN\FOP",
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
    # "3": r"D:\Debbuger\systemMetrics\SystemMetricsfop.csv",
    "4": r"D:\Debbuger\systemMetrics\SystemMetricskafka.csv",
    "5": r"D:\Debbuger\systemMetrics\SystemMetricsoozie.csv",
    "6": r"D:\Debbuger\systemMetrics\SystemMetricsopennlp.csv",
    "7": r"D:\Debbuger\systemMetrics\SystemMetricssentry.csv",
    "8": r"D:\Debbuger\systemMetrics\SystemMetricstajo.csv",
    "9": r"D:\Debbuger\systemMetrics\SystemMetricstiles.csv"
}

all_file_models = {
    "1": "D:\Debbuger\GAN\BOOKKEEPER\modelfiles_All.model",
    # "2" : "D:\Debbuger\GAN\DERBY\modelfiles_All.model",
    # "3" : "D:\Debbuger\GAN\FOP\modelfiles_All.model",
    "4": "D:\Debbuger\GAN\KAFKA\modelfiles_All.model",
    "5": "D:\Debbuger\GAN\OOZIE\modelfiles_All.model",
    "6": "D:\Debbuger\GAN\OPENNLP\modelfiles_All.model",
    "7": "D:\Debbuger\GAN\SENTRY\modelfiles_All.model",
    "8": "D:\Debbuger\GAN\TAJO\modelfiles_All.model",
    "9": "D:\Debbuger\GAN\TILES\modelfiles_All.model"
}


all_projects_data_selected_features = {}
system_metrics_attributes = None
# results = pd.DataFrame(columns=['cold_start_project', 'precision_bug', 'recall_bug','F2_bug','prc_area_bug', 'precision', 'recall','F2','prc_area'])
results = pd.DataFrame(
        columns=['cold_start_project', 'precision_bug', 'recall_bug', 'F2_bug', 'prc_area_bug', 'precision', 'recall',
                 'F2', 'prc_area','system_features','sampling','replacement','num_of_samples'])


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


def train_model(x_train, y_train):
    x_train = encode_categorial(x_train)
    model = RandomForestClassifier()
    model.fit(x_train, y_train)
    # pickle.dump(model, open("D:\Debbuger\GAN", 'wb'))
    return model


def predict_model(model, x_test):
    x_test = encode_categorial(x_test)
    pred = model.predict(x_test)
    return pred


def load_arffload_training_set(data_arff):
    raw_data = loadarff(data_arff)
    df_data = pd.DataFrame(raw_data[0])
    return df_data


def load_cold_start_arff_into_dataFrames():
    return all_projects_data_selected_features[str(cold_start_index)].copy()


def add_system_features(data,key):
    key_system_metrics = pd.read_csv(system_metrics[key])
    global system_metrics_attributes
    if system_metrics_attributes is None:
        system_metrics_attributes = [column for column in key_system_metrics]
    for column in key_system_metrics:
        data[column] = key_system_metrics[column][0]

    return data



def load_arff_from_dir_into_dataFrames_dictionery(system_features):
    for key, val in all_file_training.items():
        print key, "=>", val
        # all_projects_data[key] = load_arff(val)
        all_projects_data_selected_features[key] = load_arff(val)
        if(system_features):
            all_projects_data_selected_features[key] = add_system_features(all_projects_data_selected_features[key],key)



def load_training_set(sampling,replacement = False ,num_of_samples = 100):
    datasets = pd.DataFrame()
    for key, val in all_projects_data_selected_features.items():
        if int(key) != int(cold_start_index):
            data = val.copy()
            data = data.rename(columns={'hasBug': 'label'})
            data.label = key
            if sampling:
                datasets = datasets.append(data_sampling(data,replacement,num_of_samples), ignore_index=True)
            else:
                datasets = datasets.append(data, ignore_index=True)
    return datasets


def pre_processing(data):
    data = selectFeatures(data)
    # print(data.isnull().sum())
    null_data = data[data.isnull().any(axis=1)]
    # print(null_data.shape)
    tr_data_noNa = data.copy()
    for col in tr_data_noNa.columns[:-1]:
        if col != 'label' or col != 'hasBug':
            if tr_data_noNa[col].dtype == 'object':
                #         col_mode = mode(tr_data[col].astype(str)).mode[0]
                #         tr_data[col].fillna(col_mode,inplace=True)
                tr_data_noNa[col].fillna("Unknown", inplace=True)
            else:
                col_mean = data[col].mean()
                tr_data_noNa[col].fillna(col_mean, inplace=True)

    return tr_data_noNa


def data_sampling(data, replacement,num_of_samples):
    random = check_random_state(seed=None)
    n_samples, n_features = data.shape

    if replacement:
        indexes = random.randint(0, n_samples, num_of_samples)
    else:
        if(num_of_samples>n_samples):
            indexes = sample_without_replacement(n_samples, n_samples, random_state=random)
        else:
            indexes = sample_without_replacement(n_samples, num_of_samples, random_state=random)

    return data.loc[indexes]


def separated_data_by_predicted_model(pred, x_test,system_features):
    all_data_separated_dict = {}
    for key, val in all_file_training.items():
        if int(key) != int(cold_start_index):
            all_data_separated_dict[key] = x_test.loc[np.where(pred == str(key))]
            if system_features and (not system_metrics_attributes is None):
                all_data_separated_dict[key] = all_data_separated_dict[key].drop( system_metrics_attributes, axis = 1)
    return all_data_separated_dict


def create_arff_from_dataframes(df_dic,path):
    for key, val in df_dic.items():
        if int(key) != int(cold_start_index):
            arff.dump(os.path.join(path, str(key) + '.arff')
                      , val.values
                      , relation='relation name'
                      , names=val.columns)
            lines_to_save = None


def change_start_of_arff_files():
    start_lines = None
    with open(arff_start_path) as start:
        start_lines = start.readlines()
        start_lines.append('\n')

    for key, saving_path in data_names.items():
        for filename in os.listdir(saving_path):
            if filename.endswith('.arff'):
                change = True
                lines_to_save = None
                with open(os.path.join(saving_path, str(filename))) as file_to_change:
                    change_lines = file_to_change.readlines()
                    if len(change_lines) > 1:
                        lines_to_save = start_lines + change_lines[364:]
                    else:
                        change = False

                if change:
                    with open(os.path.join(saving_path, str(filename)), "w") as f:
                        f.writelines(lines_to_save)

def run_weka(testing, name,path):
    algorithm = "weka.classifiers.trees.RandomForest"
    name = name.split(".")[0]
    # os.system("cd /d  "+ (path) +" & java -Xmx2024m  -cp "+ (wekaJar) +" weka.Run " +algorithm+ " -l .\\model"+name+".model -T "+testing+" -classifications \"weka.classifiers.evaluation.output.prediction.CSV -file testing"+name+".csv\" ")
    # os.system("cd /d  "+ (path) +" & java -Xmx2024m  -cp "+ (wekaJar) +" weka.Run " +algorithm+ " -l .\\bestModel.model -T "+testing+" > "+name+".txt ")
    os.system("cd /d  " + (path) + " & java -Xmx2024m  -cp " + (wekaJar) + " weka.Run " + algorithm + " -l " +
              all_file_models[str(
                  name)] + " -T " + testing + " -classifications \"weka.classifiers.evaluation.output.prediction.CSV -file prediction_" + name + ".csv\" ")
    # os.system("cd /d  " + (path) + " & java -Xmx2024m  -cp " + (wekaJar) + " weka.Run " + algorithm + " -l " +
    #           all_file_models[str(name)] + " -T " + testing + " > accu_" + name + ".txt ")


def create_all_predictions_based_on_dest_model(saving_path):
    for filename in os.listdir(saving_path):
        if filename.endswith('.arff'):
            testingWeka = os.path.join(saving_path, filename)
            print(testingWeka)
            run_weka(testingWeka, filename,saving_path)


def division_label(separated):
    keys_list = separated.keys()
    keys_list.sort(key=int)
    labels = []
    for key in keys_list:
        print key
        # my_list = separated[key]["hasBug"].tolist()
        labels.extend(separated[key]["hasBug"].tolist())
        separated[key] = separated[key].drop('hasBug', axis=1)
    return labels, separated


def read_true_lable_from_csv(path):
    with open(os.path.join(path, "true_labels.csv"), 'r') as file:
        return file.read().split('\n')


def save_true_label_to_csv(true_labels,path):
    with open(os.path.join(path, "true_labels.csv"), 'w') as file:
        file.write('\n'.join(true_labels))


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


def create_all_eval_results(y_true,y_pred,key,system_features,sampling,replacement,num_of_samples):
    # precision = metrics.precision_score(y_true, y_pred, average='weighted')
    # recall = metrics.recall_score(y_true, y_pred, average='weighted')
    # F2 = calculateF2(precision, recall)
    name = data_names[key]

    y_true_bugs, y_pred_bugs = zip(*[[y_true[i], y_pred[i]] for i in range(len(y_true)) if y_true[i] == 1])
    # precision_bug, recall_bug, F_measure_bug ,_ = metrics.precision_recall_fscore_support(y_true_bugs,
    #                                                                                                  y_pred_bugs,
    #                                                                                                  average='micro')
    precision_bug =metrics.precision_score(y_true_bugs,y_pred_bugs,average='micro')
    recall_bug =metrics.recall_score(y_true_bugs,y_pred_bugs,average='micro')
    F2_bug = calculateF2(precision_bug,recall_bug)
    precision_bug_all, recall_bug_all,_ = metrics.precision_recall_curve(y_true_bugs, y_pred_bugs)
    prc_area_bug = metrics.auc(recall_bug_all, precision_bug_all)

    # precision, recall, F_measure,_ = metrics.precision_recall_fscore_support(y_true,
    #                                                                                                 y_pred,
    #                                                                                                 average='micro')
    precision = metrics.average_precision_score(y_true, y_pred, average='micro')
    recall = metrics.recall_score(y_true, y_pred, average='micro')
    F2 = calculateF2(precision, recall)
    precision_all, recall_all, _ = metrics.precision_recall_curve(y_true, y_pred)
    prc_area = metrics.auc(recall_all, precision_all)

    global results
    results.loc[len(results)] = [name,precision_bug,recall_bug,F2_bug,prc_area_bug, precision, recall,F2,prc_area,str(system_features),str(sampling),str(replacement),str(num_of_samples)]
    # aps = metrics.average_precision_score(y_true, y_pred)
    # f1_score = metrics.f1_score(y_true, y_pred)
    # accuracy_score = metrics.accuracy_score(y_true, y_pred)
    # roc_curve = metrics.roc_curve(y_true, y_pred)


def write_results_to_csv(name):
    results.to_csv(os.path.join(results_path, name+".csv"), index=False)


def set_global_cold_start(number):
    global cold_start_index
    cold_start_index = number

def clean_data():
    for key, saving_path in data_names.items():
        print(saving_path)
        for filename in os.listdir(saving_path):
            if filename.endswith('.csv') or filename.endswith('.arff'):
                to_delete = os.path.join(saving_path, filename)
                print(to_delete)
                os.remove(to_delete)

#main num.1
def create_models_and_arffs(system_features,sampling,replacement=False,num_of_samples= 100):
    # load_arff_from_dir_into_dataFrames_dictionery(system_features)
    for key, saving_path in data_names.items():
        set_global_cold_start(int(key))
        df = load_training_set(sampling,replacement,num_of_samples)
        tr_data = df.drop('label', axis=1)
        tr_data = pre_processing(tr_data)
        my_model = train_model(tr_data, df['label'])
        all_x_test = load_cold_start_arff_into_dataFrames()
        x_test = all_x_test.copy()
        x_test = x_test.drop('hasBug', axis=1)
        x_test = pre_processing(x_test)
        pred = predict_model(my_model, x_test)
        separated = separated_data_by_predicted_model(pred, all_x_test,system_features)
        true_labels, separated_no_label = division_label(separated.copy())

        # save_true_label_to_csv(true_labels,saving_path)
        create_arff_from_dataframes(separated,saving_path)


#main num.2
def create_prediction_results(system_features,sampling,replacement,num_of_samples):
    change_start_of_arff_files()
    for key, saving_path in data_names.items():
        print(saving_path)
        # true_label = read_true_lable_from_csv()
        create_all_predictions_based_on_dest_model(saving_path)
        all_predictions = get_eval(saving_path)
        all_predictions['actual'] = all_predictions['actual'].map({'2:valid': 0, '1:bugged': 1})
        all_predictions['predicted'] = all_predictions['predicted'].map({'2:valid': 0, '1:bugged': 1})
        y_true = all_predictions['actual']
        y_pred = all_predictions['predicted']
        create_all_eval_results(y_true, y_pred,key,system_features,sampling,replacement,num_of_samples)
    # if sampling:
        # name = "systemFeatures_"+str(system_features)+"_sampling_"+str(sampling)+"_replacement_"+str(replacement)+"_numOfSamples_"+str(num_of_samples)
    # else:
        # name = "systemFeatures_"+str(system_features)+"_sampling_"+str(sampling)

    # write_results_to_csv("gan_results_all")


for system_features in [True,False]:
    load_arff_from_dir_into_dataFrames_dictionery(system_features)
    for sampling in [True,False]:
        if(sampling):
            for replacement in [True,False]:
                for num_of_samples in [1200,5000,7000,10000]:
                    create_models_and_arffs(system_features=system_features, sampling=sampling, replacement=replacement,
                                            num_of_samples=num_of_samples)
                    create_prediction_results(system_features=system_features, sampling=sampling,
                                              replacement=replacement, num_of_samples=num_of_samples)
                    clean_data()
        else:
            create_models_and_arffs(system_features=system_features, sampling=sampling, replacement="-",
                                    num_of_samples="-")
            create_prediction_results(system_features=system_features, sampling=sampling, replacement="-",
                                      num_of_samples="-")
            clean_data()
    global all_projects_data_selected_features
    all_projects_data_selected_features = {}


write_results_to_csv("gan_results_all")
# clean_data()
