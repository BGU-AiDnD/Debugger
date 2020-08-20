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
#adding extreme learning
from sklearn_extensions.extreme_learning_machines.elm import GenELMClassifier
from sklearn_extensions.extreme_learning_machines.random_layer import RBFRandomLayer, MLPRandomLayer

results_all_projects = pd.DataFrame(
        columns=['cold_start_project','model_source', 'precision_bug', 'recall_bug','F_bug', 'F2_bug','roc_area_bug', 'prc_area_bug', 'precision', 'recall',
                 'F1', 'F2', 'roc_area','prc_area','num_bugs_test','num_all_inst_test','percent_bugs_test','num_bugs_train','num_all_inst_train','percent_bugs_train',"percent_group_training_set"])

def create_all_data_with_models_sav(directory,data_file):
    data = pickle.load(open( data_file, "rb" ))
    #del data['ckjm1.8']
    for filename in os.listdir(directory):
        if filename.endswith(".sav"):
            print(os.path.join(directory, filename))
            current_model = pickle.load(open( os.path.join(directory, filename) , "rb" ))
            data[filename[:-4]] = (current_model,data[filename[:-4]])
            print(os.path.join(directory, filename))

    file_path = os.path.join(directory, 'all_data_with_models.sav')
    pickle.dump(data, open(file_path, 'wb'))

def calculateF2(precision, recall):
    if ((4 * precision) + recall) != 0:
        F2BUGS = (5 * ((precision * recall) / ((4 * precision) + recall)))
    else:
        F2BUGS = 0
    return F2BUGS

def create_all_eval_results(export,y_true, y_pred, key,num_of_bugs_test,num_of_all_instances_test,bugs_Precent_test,num_of_bugs_train,num_of_all_instances_train,bugs_Precent_train,from_model,percent_group_name=None):

    un_true, _ = np.unique(y_true, return_counts=True)
    un_pred, _ = np.unique(y_pred, return_counts=True)
    #if len(un_true) == 1 or len(un_pred) == 1:
    #    y_true.append(0)
    #    y_true.append(1)
    #    y_pred.append(0)
    #    y_pred.append(1)
    #    y_true.append(0)
    #    y_true.append(1)
    #    y_pred.append(1)
    #    y_pred.append(0)
    #    print("zero or ones")

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
        prc_bugged = metrics.auc(recall,precision)
    except:
        print("exception_prc - BUG")
        prc_bugged = 0.5

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

def  predict_model(cur_proj_name,data,proj_name_host,model_host,testing_set_host,within_model):
    x = data.drop(label_bugs, axis=1)
    y = data[label_bugs]
    num_of_bugs_test = data[label_bugs].tolist().count(1)
    num_of_all_instances_test = data.shape[0]
    bug_precent_test = float(num_of_bugs_test) / float(num_of_all_instances_test)

    num_of_bugs_train = testing_set_host[label_bugs].tolist().count(1)
    num_of_all_instances_train  = testing_set_host.shape[0]
    bug_precent_train = float(num_of_bugs_train) / float(num_of_all_instances_train)

    if (within_model == "ELM"):
        prediction_test = model_host.predict(x.rename_axis('ID').values)
    else:
        prediction_test = model_host.predict(x)

    new_pred, new_f2 = create_all_eval_results(False,y.tolist(),prediction_test.tolist(),cur_proj_name,num_of_bugs_test,num_of_all_instances_test,bug_precent_test,num_of_bugs_train,num_of_all_instances_train,bug_precent_train,proj_name_host+"_within_"+within_model)
    start_list = [cur_proj_name,proj_name_host]
    last_list = ["-"]
    result_list = start_list+ new_pred.tolist() +last_list

    global results_all_projects
    results_all_projects.loc[len(results_all_projects)] = result_list

    return new_f2

def best_of_breed(data,within_model):
    all_projects_bob = {}
    for proj_name_host, ( model_host,training_set_host,testing_set_host ) in data.items():
        f2_score = 0
        num_of_projects = 0
        for cur_proj_name, (cur_model,cur_training_set,cur_testing_set) in data.items():
            #if proj_name_host[:-3] != cur_proj_name[:-3]:
            #if proj_name_host != cur_proj_name:
            if proj_name_host.split('_')[0] != cur_proj_name.split('_')[0]:
                num_of_projects +=1
                f2_score += predict_model(cur_proj_name,cur_testing_set,"bob("+proj_name_host+")",model_host,training_set_host,within_model)

        f2_score /= num_of_projects
        all_projects_bob[proj_name_host] = f2_score

    index = max(all_projects_bob, key=lambda i: all_projects_bob[i])
    print("max is: " + str(index) + " - " + str(all_projects_bob[index]))
    for proj, f2 in all_projects_bob.items():
        print(str(proj)+ "  :  " + str(f2))

##############################################################
promise_projects_to_number_old = {
"xalan2.6"  : 1,
"xalan2.7" :  2,
"xalan2.4"  :  3,
"xalan2.5"  :  4,
"jEdit3.2"  :  5,
"log4j1.2"  :  6,
"log4j1.1"  :  7,
"log4j1.0"  :  8,
"camel1.0"  :  9,
"camel1.2"  :  10,
"camel1.4"  :  11,
"camel1.6"  :  12,
"lucene2.2"  :  13,
"lucene2.0"  :  14,
"synapse1.2"  :  15,
"synapse1.0"  :  16,
"lucene2.4"  :  17,
"poi1.5"  :  18,
"xerces1.4"  : 19 ,
"xerces1.2"  :  20,
"xerces1.3"  :  21,
"poi2.0"  :  22,
"jEdit4.0"  :  23,
"jEdit4.1"  :  24,
"jEdit4.2"  :  25,
"jEdit4.3"  :  26,
"poi2.5"  :  27,
"ant1.4"  :28,
"ant1.5"  :  29,
"ant1.6"  :  30,
"ant1.7"  :  31,
"ant1.3"  :  32,
"Tomcat6.0":  33,
"velocity1.6":  34,
"velocity1.5":  35,
"velocity1.4" :  36,
"synapse1.1" : 37,
"ivy2.0"  :  38,
"ivy1.1"  :39,
"poi3.0"  : 40,
"ivy1.4"  :  41
}
promise_number_to_project_old = {
 1 : "xalan2.6",
 2 : "xalan2.7",
 3 : "xalan2.4",
 4 : "xalan2.5",
 5 : "jEdit3.2",
 6 : "log4j1.2",
 7 : "log4j1.1",
 8 : "log4j1.0",
 9 : "camel1.0",
10 : "camel1.2",
11 : "camel1.4",
12 : "camel1.6",
13: "lucene2.2" ,
14: "lucene2.0" ,
15: "synapse1.2" ,
16: "synapse1.0" ,
17: "lucene2.4"  ,
18: "poi1.5"  ,
19: "xerces1.4" ,
20: "xerces1.2"  ,
21: "xerces1.3"  ,
22: "poi2.0"  ,
23: "jEdit4.0"  ,
24: "jEdit4.1"  ,
25:" jEdit4.2"  ,
26:" jEdit4.3"  ,
27: "poi2.5"  ,
28: "ant1.4",
29: "ant1.5"  ,
30: "ant1.6"  ,
31: "ant1.7"  ,
32: "ant1.3"  ,
33: "Tomcat6.0",
34: "velocity1.6",
35: "velocity1.5",
36: "velocity1.4",
37: "synapse1.1",
38: "ivy2.0" ,
39: "ivy1.1" ,
40: "poi3.0" ,
41: "ivy1.4"
}

promise_projects_to_number_p = {
"xalan"  : 1,
"log4j"  :  2,
"camel"  :  3,
"lucene"  :  4,
"synapse"  :  5,
"poi"  :  6,
"xerces"  : 7 ,
"ant"  :8,
"Tomcat":  9,
"velocity":  10,
"ivy"  :  11
}
promise_number_to_project_p = {
 1 : "xalan",
 2 : "log4j",
 3 : "camel",
 4 : "lucene",
 5 : "synapse",
 6 : "poi",
 7 : "xerces",
 8 : "ant",
 9 : "Tomcat",
10 : "velocity",
11 : "ivy"
}

promise_projects_to_number_v = {
"bookkeeper_release-4.0.0" : 1,
"bookkeeper_release-4.1.0" : 2,
"bookkeeper_release-4.2.0" : 3,
"bookkeeper_release-4.3.0" : 4,
"bookkeeper_release-4.4.0" : 5,
"bookkeeper_release-4.5.0" : 6,
"bookkeeper_release-4.6.0" : 7,
"bookkeeper_release-4.7.0" : 8,
"fop_batik-1_6"  :           9,
"fop_fop-0_20_0" :           10,
"fop_fop-1_0"  :             11,
"fop_fop-1_1"  :             12,
"fop_fop-2_0"  :             13,
"fop_fop-2_1"  :             14,
"fop_fop-2_2"  :             15,
"kafka_0.8.1.0"  :           16,
"kafka_0.8.2.0"  :           17,
"kafka_0.10.1.0"  :          18,
"kafka_0.10.0.0"  :          19,
"kafka_0.10.2.0"  :          20,
"kafka_0.11.0.0"  :          21,
"kafka_1.0.0"  :             22,
"kafka_1.1.0" :              23,
"kafka_2.0.0"  :             24,
"oozie_3.2"  :               25,
"oozie_release-3.3.0"  :     26,
"oozie_release-4.0.0"  :     27,
"oozie_release-4.1.0"  :     28,
"oozie_release-4.2.0"  :     29,
"sentry_release-1.0.0"  :    30,
"sentry_release-1.1.0"  :    31,
"sentry_release-1.4.0"   :   32,
"sentry_release-1.7.0"  :    33,
"sentry_release-1.8.0"   :   34,
"sentry_release-2.0.0"  :    35,
"tajo_release-0.10.0"  :     36,
"tajo_release-0.9.0"  :      37,
"tajo_release-0.2.0"  :      38,
"tiles_tiles-2.0.0"  :       39,
"tiles_tiles-2.2.0"  :       40,
"tiles_tiles-parent-2.0.0":  41
}
promise_number_to_project_v = {
1: "bookkeeper_release-4.0.0"         ,
2: "bookkeeper_release-4.1.0"         ,
3: "bookkeeper_release-4.2.0"         ,
4: "bookkeeper_release-4.3.0"         ,
5: "bookkeeper_release-4.4.0"         ,
6: "bookkeeper_release-4.5.0"         ,
7: "bookkeeper_release-4.6.0"         ,
8: "bookkeeper_release-4.7.0"         ,
9: "fop_batik-1_6"                   ,
10:"fop_fop-0_20_0"                  ,
11:"fop_fop-1_0"                     ,
12:"fop_fop-1_1"                     ,
13:"fop_fop-2_0"                     ,
14:"fop_fop-2_1"                     ,
15:"fop_fop-2_2"                    ,
16:"kafka_0.8.1.0"                   ,
17:"kafka_0.8.2.0"                   ,
18:"kafka_0.10.1.0"                  ,
19:"kafka_0.10.0.0"                  ,
20:"kafka_0.10.2.0"                 ,
21:"kafka_0.11.0.0"                  ,
22:"kafka_1.0.0"                     ,
23:"kafka_1.1.0"                     ,
24:"kafka_2.0.0"                     ,
25:"oozie_3.2"                      ,
26:"oozie_release-3.3.0"          ,
27:"oozie_release-4.0.0"          ,
28:"oozie_release-4.1.0"          ,
29:"oozie_release-4.2.0"          ,
30:"sentry_release-1.0.0"         ,
31:"sentry_release-1.1.0"         ,
32:"sentry_release-1.4.0"         ,
33:"sentry_release-1.7.0"         ,
34:"sentry_release-1.8.0"         ,
35:"sentry_release-2.0.0"         ,
36:"tajo_release-0.10.0"          ,
37:"tajo_release-0.9.0"          ,
38:"tajo_release-0.2.0"          ,
39:"tiles_tiles-2.0.0"           ,
40:"tiles_tiles-2.2.0"           ,
41:"tiles_tiles-parent-2.0.0"
}

promise_projects_to_number_full_old_p = {
"bookkeeper" : 1,
"fop" :         2,
"kafka"  :      3,
"oozie"  :      4,
"sentry"  :    5,
"tajo"  :     6,
"tiles"  :      7
}
promise_number_to_project_full_old_p = {
1: "bookkeeper"         ,
2: "fop"                   ,
3:"kafka"                        ,
4:"oozie"          ,
5:"sentry"         ,
6:"tajo"          ,
7:"tiles"
}


promise_projects_to_number = {
"accumulo"  :1 ,
"activemq"  :2 ,
"archiva"  :3 ,
"asterixdb"  :4 ,
"atlas"  :5 ,
"avro"  :6 ,
"beam"  :7 ,
"bookkeeper"  :8 ,
"calcite"  :9 ,
"camel"  :10,
"carbondata"  :11,
"cassandra"  :12,
"cayenne"  :13,
"clerezza"  :14,
"cocoon"  :15,
"commons-beanutils"  :16,
"commons-cli"  :17,
"commons-codec"  :18,
"commons-collections"  :19,
"commons-compress"  :20,
"commons-csv"  :21,
"commons-dbcp"  :22,
"commons-email"  :23,
"commons-io"  :24,
"commons-jexl"  :25,
"commons-lang"  :26,
"commons-math"  :27,
"commons-net"  :28,
"commons-validator"  :29,
"commons-vfs"  :30,
"continuum"  :31,
"crunch"  :32,
"curator"  :33,
"cxf"  :34,
"deltaspike"  :35,
"directory-kerby"  :36,
"directory-server"  :37,
"directory-studio"  :38,
"drill"  :39,
"flink"  :40,
"giraph"  :41,
"hadoop"  :42,
"hbase"  :43,
"helix"  :44,
"hive"  :45,
"isis"  :46,
"jackrabbit"  :47,
"jackrabbit-oak"  :48,
"johnzon"  :49,
"kafka"  :50,
"karaf"  :51,
"knox"  :52,
"kylin"  :53,
"maven"  :54,
"maven-surefire"  :55,
"metron"  :56,
"myfaces"  :57,
"myfaces-tobago"  :58,
"nifi"  :59,
"nutch"  :60,
"olingo-odata4"  :61,
"openjpa"  :62,
"openmeetings"  :63,
"opennlp"  :64,
"openwebbeans"  :65,
"parquet-mr"  :66,
"phoenix"  :67,
"plc4x"  :68,
"pulsar"  :69,
"qpid-jms"  :70,
"reef"  :71,
"roller"  :72,
"samza"  :73,
"santuario-java"  :74,
"servicecomb-java-chassis"  :75,
"shiro"  :76,
"struts"  :77,
"syncope"  :78,
"tajo"  :79,
"tapestry-5"  :80,
"tez"  :81,
"tika"  :82,
"tinkerpop"  :83,
"tomcat"  :84,
"uima-ruta"  :85,
"wicket"  :86,
"xmlgraphics-fop"  :87,
"zeppelin"  : 88
}
promise_number_to_project = {
1 :   "accumulo",
2 :   "activemq",
3 :   "archiva",
4 :   "asterixdb",
5 :   "atlas",
6 :   "avro",
7 :   "beam",
8 :   "bookkeeper",
9 :   "calcite",
10 :   "camel",
11 :   "carbondata",
12 :   "cassandra",
13 :   "cayenne",
14 :   "clerezza",
15 :   "cocoon",
16 :   "commons-beanutils",
17 :   "commons-cli",
18 :   "commons-codec",
19 :   "commons-collections",
20 :   "commons-compress",
21 :   "commons-csv",
22 :   "commons-dbcp",
23 :   "commons-email",
24 :   "commons-io",
25 :   "commons-jexl",
26 :   "commons-lang",
27 :   "commons-math",
28 :   "commons-net",
29 :   "commons-validator",
30 :   "commons-vfs",
31 :   "continuum",
32 :   "crunch",
33 :   "curator",
34 :   "cxf",
35 :   "deltaspike",
36 :   "directory-kerby",
37 :   "directory-server",
38 :   "directory-studio",
39 :   "drill",
40 :   "flink",
41 :   "giraph",
42 :   "hadoop",
43 :   "hbase",
44 :   "helix",
45 :   "hive",
46 :   "isis",
47 :   "jackrabbit",
48 :   "jackrabbit-oak",
49 :   "johnzon",
50 :   "kafka",
51 :   "karaf",
52 :   "knox",
53 :   "kylin",
54 :   "maven",
55 :   "maven-surefire",
56 :   "metron",
57 :   "myfaces",
58 :   "myfaces-tobago",
59 :   "nifi",
60 :   "nutch",
61 :   "olingo-odata4",
62 :   "openjpa",
63 :   "openmeetings",
64 :   "opennlp",
65 :   "openwebbeans",
66 :   "parquet-mr",
67 :   "phoenix",
68 :   "plc4x",
69 :   "pulsar",
70 :   "qpid-jms",
71 :   "reef",
72 :   "roller",
73 :   "samza",
74 :   "santuario-java",
75 :   "servicecomb-java-chassis",
76 :   "shiro",
77 :   "struts",
78 :   "syncope",
79 :   "tajo",
80 :   "tapestry-5",
81 :   "tez",
82 :   "tika",
83 :   "tinkerpop",
84 :   "tomcat",
85 :   "uima-ruta",
86 :   "wicket",
87 :   "xmlgraphics-fop",
88 :   "zeppelin"
}




best_F1 = {
"camel1.4",
"camel1.2",
"ivy1.1",
"camel1.0",
"ivy1.4",
"jEdit4.0"
}

best_F2 = {
"xerces1.4",
"camel1.2",
"xalan2.7",
"log4j1.2",
"camel1.4",
"lucene2.2"
}
best_roc={
"xalan2.6",
"jEdit4.0",
"lucene2.0",
"ivy1.1",
"log4j1.0",
"velocity1.6"
}
best_prc ={
"xerces1.4",
"camel1.2",
"xalan2.7",
"camel1.4",
"log4j1.2",
"lucene2.2"
}

best_group =[
"camel1.4",
"camel1.2",
"ivy1.1",
"xerces1.4",
"xalan2.7",
"xalan2.6",
"jEdit4.0",
"lucene2.0"
]

bug_p_0_10 =[
"ant1.3",
"synapse1.0",
"poi2.0",
"ivy2.0",
"ant1.5",
"Tomcat6.0",
#"jEdit4.2",
"ivy1.4",
"camel1.0"
#"jEdit4.3"
]
bug_p_0_16=[
'ant1.7',
'ant1.4',
'camel1.6',
'xerces1.2',
'camel1.4',
'xalan2.4',
'xerces1.3',
'jEdit4.0',
'jEdit4.1',
'ant1.3',
'synapse1.0',
'poi2.0',
'ivy2.0',
'ant1.5',
'Tomcat6.0',
#'jEdit4.2',
'ivy1.4',
'camel1.0'
#'jEdit4.3'
]
bug_p_8_25 =[
'synapse1.1',
'log4j1.0',
'jEdit3.2',
'ant1.6',
'ant1.7',
'ant1.4',
'camel1.6',
'xerces1.2',
'camel1.4',
'xalan2.4',
'xerces1.3',
'jEdit4.0',
'jEdit4.1',
'ant1.3',
'synapse1.0',
'poi2.0',
'ivy2.0'
]
bug_p_22_41=[
'xalan2.5',
'lucene2.4',
'lucene2.2',
'xalan2.6',
'synapse1.2',
'lucene2.0',
'log4j1.1',
'velocity1.6',
'camel1.2',
'synapse1.1',
'log4j1.0'
]
bug_p_37_65=[
'velocity1.4',
'xerces1.4',
'velocity1.5',
'poi2.5',
'poi3.0',
'poi1.5',
'ivy1.1',
'xalan2.5',
'lucene2.4',
'lucene2.2'
]
bug_p_50_76=[
'xalan2.7',
'log4j1.2',
'velocity1.4',
'xerces1.4',
'velocity1.5',
'poi2.5',
'poi3.0'
]
bug_p_37_76=[
'xalan2.7',
'log4j1.2',
'velocity1.4',
'xerces1.4',
'velocity1.5',
'poi2.5',
'poi3.0',
'poi1.5',
'ivy1.1',
'xalan2.5',
'lucene2.4',
'lucene2.2'
]

def data_sampling(data,num_of_samples):
    random = check_random_state(seed=None)
    n_samples, n_features = data.shape

    if(num_of_samples>n_samples):
        indexes = np.concatenate((sample_without_replacement(n_samples, n_samples, random_state=random), random.randint(0, n_samples, num_of_samples-n_samples)), axis=None)
    else:
        indexes = sample_without_replacement(n_samples, num_of_samples, random_state=random)

    return data.loc[indexes]

def load_training_set(CS_project,all_projects,sampling,num_of_samples = 100,percent_group= False):
    training_by_model = {}
    datasets = pd.DataFrame()
    for proj_name, (model,training_set, testing_set) in all_projects.items():
        #if CS_project[:-3] != proj_name[:-3]:
        #if CS_project != proj_name:
        if CS_project.split('_')[0] != proj_name.split('_')[0]:
            if(percent_group):
                if(proj_name in percent_group):
                    data = training_set.copy()
                    data.reset_index(drop=True, inplace=True)
                    data = data.rename(columns={label_bugs: 'label'})
                    data.label = promise_projects_to_number[proj_name]
                    if sampling:
                        datasets = datasets.append(data_sampling(data,num_of_samples), ignore_index=True)
                    else:
                        datasets = datasets.append(data, ignore_index=True)
            else:
                #print("no precent")
                data = training_set.copy()
                data.reset_index(drop=True, inplace=True)
                data = data.rename(columns={label_bugs: 'label'})
                data.label = promise_projects_to_number[proj_name]
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
            all_data_separated_dict[promise_projects_to_number[proj_name]] = x_test.loc[np.where(pred == promise_projects_to_number[proj_name])]
    return all_data_separated_dict

def get_all_eval_based_on_model(separated,all_projects,within_model):
    pred = np.array([])
    real = np.array([])
    for key, data_to_test in separated.items():
        x_test = data_to_test.copy()
        try:
            if x_test.shape[0] != 0:
                x_test = x_test.drop(label_bugs, axis=1)
                if within_model == "ELM":
                    pred = np.concatenate((pred,  all_projects[promise_number_to_project[key]][0].predict(x_test.rename_axis('ID').values)), axis=None)
                    real = np.concatenate((real,  data_to_test[label_bugs]), axis=None)
                else:
                    pred = np.concatenate((pred, all_projects[promise_number_to_project[key]][0].predict(x_test)), axis=None)
                    real = np.concatenate((real, data_to_test[label_bugs]), axis=None)
        except:
            print(list(x_test))
            print(key)

    return pred.tolist(),real.tolist()


def create_models_and_eval(all_projects,sampling,model_details,model,num_of_samples,within_model,percent_group=None,percent_group_name = None):
    for cold_start_project_name, ( cold_start_model,cold_start_training_set ,cold_start_testing_set) in all_projects.items():
        training_by_models = load_training_set(cold_start_project_name,all_projects,sampling,num_of_samples,percent_group)

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

        #best_prediction, worse_prediction,percent_ours = create_prediction_best_and_worse(all_x_test, type,pred_models_ours)
        #separated_random = separated_data_randomly(all_x_test, system_features, type)
        #export_info_about_seperation(separated_random, type, key, saving_path, sampling, model_details, num_of_samples,system_features)
        #pred_random, real_random = get_all_eval_based_on_model(separated_random, type)

        create_all_eval_results(True, real_ours, pred_ours, cold_start_project_name,
                                                   num_of_bugs, num_of_all_instances, bug_precent," "," "," ", "OSCAR_"+str(model_details)+"_"+str(sampling)+"_"+str(num_of_samples)+"_within"+within_model,percent_group_name)

        #create_all_eval_results(real_random, pred_random,str(data_names[key]).split('\\')[-1],"testing",type,num_of_bugs,num_of_all_instances,bug_precent,model_details,system_features,"random")
        #create_all_eval_results(all_x_test['hasBug'], worse_prediction,str(data_names[key]).split('\\')[-1],"testing",type,num_of_bugs,num_of_all_instances,bug_precent,model_details,system_features,"Worst")
        #create_all_eval_results(all_x_test['hasBug'], best_prediction,str(data_names[key]).split('\\')[-1],"testing",type,num_of_bugs,num_of_all_instances,bug_precent,model_details,system_features,"Best")

def change_pred(pred_num):
    if pred_num == 1 :
        return 0
    else:
        return 1

def create_prediction_best_and_worse(CS_project,all_projects,pred_ours,x_test):
    df_all_pred = pd.DataFrame(columns=range(x_test.shape[0]))

    x_test_no_label = x_test.drop(label_bugs, axis=1)
    label_true = x_test[label_bugs]

    for proj_name, (model,training_set, testing_set) in all_projects.items():
        #if CS_project[:-3] != proj_name[:-3]:
        #if CS_project != proj_name:
        if CS_project.split('_')[0] != proj_name.split('_')[0]:
            predict = model.predict(x_test_no_label)
            l_pred = [tuple(predict)]
            df_all_pred = df_all_pred.append(l_pred).rename(index={0:int(promise_projects_to_number[proj_name])})

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
       if int(our_model_prediction) in best_models_prediction[0]:
           same+=1

    precent_ours = float(same) / len(pred_ours)

    return best_prediction,worse_prediction,precent_ours

def separated_data_randomly(CS_project,all_projects,x_test):
    all_data_separated_dict = {}
    random = check_random_state(seed=None)
    x_test_mat = x_test.copy()
    for proj_name, (model,training_set, testing_set) in all_projects.items():
        #if CS_project[:-3] != proj_name[:-3]:
        #if CS_project != proj_name:
        if CS_project.split('_')[0] != proj_name.split('_')[0]:
            num_of_recored_left = x_test_mat.shape[0]
            key = promise_projects_to_number[proj_name]
            if num_of_recored_left > 1:
                try:
                    num_of_record_to_take = random.randint(0, num_of_recored_left)
                    indexes = sample_without_replacement(num_of_recored_left, num_of_record_to_take, random_state=random)
                    all_data_separated_dict[key] = x_test_mat.iloc[indexes]
                    x_test_mat = x_test_mat.drop(x_test_mat.index[indexes])
                except:
                    all_data_separated_dict[key] = pd.DataFrame()
            else:
                all_data_separated_dict[key] = pd.DataFrame()

    if x_test_mat.shape[0] != 0:
        #print(list(all_data_separated_dict))
        #print(all_data_separated_dict.keys())
        key_choosen = random.choice(list(all_data_separated_dict))
        all_data_separated_dict[key_choosen] = all_data_separated_dict[key_choosen].append(x_test_mat,ignore_index = True)

    return all_data_separated_dict

def create_models_and_eval_using_oracle_and_worse(all_projects,sampling,model_details,model,num_of_samples,within_model,percent_group=None,percent_group_name = None):
    for cold_start_project_name, ( cold_start_model,cold_start_training_set, cold_start_testing_set) in all_projects.items():
        training_by_models = load_training_set(cold_start_project_name,all_projects,sampling,num_of_samples,percent_group)

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

        best_prediction, worse_prediction,percent_ours = create_prediction_best_and_worse(cold_start_project_name,all_projects,pred_models_ours.copy(), all_x_test)
        separated_random = separated_data_randomly(cold_start_project_name,all_projects, all_x_test)

        #export_info_about_seperation(separated_random, key, saving_path, sampling, model_details, num_of_samples,system_features)

        pred_random, real_random = get_all_eval_based_on_model(separated_random,all_projects,"random-RF")

        create_all_eval_results(True, real_ours, pred_ours, cold_start_project_name,
                                                   num_of_bugs, num_of_all_instances, bug_precent," ",percent_ours," ",
                                                   "OSCAR_"+str(model_details)+"_"+str(sampling)+"_"+str(num_of_samples)+"_within"+within_model,percent_group_name)
        create_all_eval_results(True,real_random, pred_random,cold_start_project_name,
                                                   num_of_bugs,num_of_all_instances,bug_precent," "," "," ",
                                                   "OSCAR_"+str(model_details)+"_random",percent_group_name)
        create_all_eval_results(True,all_x_test[label_bugs], worse_prediction,cold_start_project_name,
                                                   num_of_bugs,num_of_all_instances,bug_precent," "," "," ",
                                                   "OSCAR_"+str(model_details)+"_worst",percent_group_name)
        create_all_eval_results(True,all_x_test[label_bugs], best_prediction,cold_start_project_name,
                                                   num_of_bugs,num_of_all_instances,bug_precent," "," "," ",
                                                   "OSCAR_"+str(model_details)+"_oracle",percent_group_name)

def OSCAR(all_projects,within_model,oracle = False):
    index = 0
    models = {
        "random_forest_100": RandomForestClassifier(n_estimators=100, max_depth=5)
        # "xgb": XGBClassifier(n_estimators=100, max_depth=6)
        #"gradient_boostong": GradientBoostingClassifier(learning_rate=0.01, max_depth=5,n_estimators=100)
    }
    for model_details, model in models.items():
        for sampling in [True, False]:
            if (sampling):
                #for num_of_samples in [4000, 10000, 15000]:
                #for num_of_samples in [400,700,1000]:
                #for num_of_samples in [700,1000,5000]:
                for num_of_samples in [400,1000]:
                    index += 1
                    print("start process_" + str(sampling) + "_" + str(num_of_samples))
                    if oracle:
                        create_models_and_eval_using_oracle_and_worse(all_projects, sampling, model_details, model,num_of_samples,within_model)
                    else:
                        create_models_and_eval(all_projects, sampling, model_details, model,num_of_samples,within_model)

                    #results_all_projects.to_csv(
                    #    os.path.join(results_path, "gan_results_all_belong" + str(index) + ".csv"), index=False)
                    # gan_val.to_csv(os.path.join(results_path, "gan_seperation_model_results_random" + str(index) + ".csv"),index=False)
            else:
                index += 1
                print("start process_" + str(sampling))
                if oracle:
                    create_models_and_eval_using_oracle_and_worse(all_projects, sampling, model_details, model, "-",within_model)
                else:
                    create_models_and_eval(all_projects, sampling, model_details, model, "-",within_model)
                #results_all_projects.to_csv(
                #os.path.join(results_path, "gan_results_all_belong" + str(index) + ".csv"), index=False)
                # gan_val.to_csv(os.path.join(results_path, "gan_seperation_model_results_random" + str(index) + ".csv"),index=False)

def OSCAR_PERCENT_TEST(all_projects,within_model):
    create_models_and_eval(all_projects, False, "random_forest_100",
                           RandomForestClassifier(n_estimators=100, max_depth=5), "-", within_model, None, "all")
    create_models_and_eval(all_projects, True, "random_forest_100",
                           RandomForestClassifier(n_estimators=100, max_depth=5), 1000, within_model, None, "all")
    bug_per = {
        "best_group": best_group,
        "0-10: 10v" :bug_p_0_10,
               "0-16: 16v" : bug_p_0_16,
               "8-25: 16v" : bug_p_8_25,
               "22-41: 11v": bug_p_22_41,
               "37-65: 10v": bug_p_37_65,
               "50-76: 7v" : bug_p_50_76,
               "37-76: 12v": bug_p_37_76}

    bug_best ={
        "best_group" : best_group,
        "best_F" : best_F1,
        "best_F2" : best_F2,
        "best_roc": best_roc,
        "best_prc": best_prc
    }
    for group_name, percent_group in bug_best.items():
        create_models_and_eval(all_projects, False,"random_forest_100", RandomForestClassifier(n_estimators=100, max_depth=5), "-", within_model , percent_group,group_name)
        create_models_and_eval(all_projects, True,"random_forest_100", RandomForestClassifier(n_estimators=100, max_depth=5), 1000, within_model,percent_group,group_name)



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

def one_ELM(all_projects,use_everyone,within_model):
    for cold_start_project_name, ( cold_start_model,cold_start_training_set, cold_start_testing_set) in all_projects.items():
        training_set = load_training_set_all_others(cold_start_project_name,all_projects,use_everyone)

        print("start process for: "+str(cold_start_project_name))
        tr_data_all = training_set.drop(label_bugs, axis=1)

        nh = 10
        srhl_rbf = RBFRandomLayer(n_hidden=nh * 2, rbf_width=0.1, random_state=0)
        model = GenELMClassifier(hidden_layer=srhl_rbf)

        model = model.fit(tr_data_all.rename_axis('ID').values, training_set[label_bugs])
        all_x_test = cold_start_testing_set.copy()
        all_x_test.reset_index(drop=True, inplace=True)
        x_test = all_x_test.copy()
        x_test = x_test.drop(label_bugs, axis=1)

        pred = model.predict(x_test.rename_axis('ID').values)

        num_of_bugs_test = all_x_test[label_bugs].tolist().count(1)
        num_of_all_instances_test = len(all_x_test[label_bugs])
        try:
            bug_precent_test = float(num_of_bugs_test) / float(num_of_all_instances_test)
        except:
            bug_precent_test = 0

        num_of_bugs_train = training_set[label_bugs].tolist().count(1)
        num_of_all_instances_train = len(training_set[label_bugs])
        try:
            bug_precent_train = float(num_of_bugs_train) / float(num_of_all_instances_train)
        except:
            bug_precent_train = 0

        create_all_eval_results(True, all_x_test[label_bugs].tolist(), pred.tolist(), cold_start_project_name,
        num_of_bugs_test, num_of_all_instances_test, bug_precent_test
                                ,num_of_bugs_train, num_of_all_instances_train, bug_precent_train
                                , ("ELM_useEveryone_" +str(use_everyone)+"_within"+within_model))


#directory_ELM= r'D:\Debbuger\PROMISE\ELM_normal'
#directory_RF= r'D:\Debbuger\PROMISE\tree_normalRF'

#data_file = r'D:\Debbuger\PROMISE\all_training_data.sav'
#create_all_data_with_models_sav(directory,data_file)
#file_path_ELM = os.path.join(directory_ELM, 'all_data_with_models_ELM.sav')
#file_path_RF = os.path.join(directory_RF, 'all_data_with_models_NRF.sav')


to_delete =["plc4x",
"tomcat",
"directory-kerby",
"cocoon",
"clerezza",
"pulsar",
"isis",
"deltaspike",
"tez",
"directory-studio",
"commons-math",
"uima-ruta",
"myfaces-tobago",
"reef",
"asterixdb",
"giraph",
"tinkerpop",
"shiro",
"commons-vfs",
"karaf",
"cxf",
"myfaces",
"directory-server",
"flink",
"servicecomb-java-chassis",
"cayenne",
"cassandra",
"olingo-odata4",
"santuario-java",
"camel",
"jackrabbit",
"nifi",
"opennlp",
"wicket",
"commons-cli"]



##############################
### only because memory problem ########
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
            #print(test_data.columns)
            #training_set_f, testing_set_f, cur_model_f = preper_fowler(train_data,test_data)
            training_set_tr, testing_set_tr, cur_model_tr = preper_trad(train_data,test_data)
            #training_set_a, testing_set_a, cur_model_a = preper_all_f(train_data,test_data)
            if training_set_tr is not None:
                #proj_name, (model,training_set, testing_set)
                #dict_fowler[project_name] = (cur_model_f,training_set_f,testing_set_f)
                dict_trad[project_name] = (cur_model_tr,training_set_tr,testing_set_tr)
                #dict_all[project_name] = (cur_model_a,training_set_a,testing_set_a)
                print("folder all done")

label_bugs = 'Bugged'

'''
print("all")
directory_RF = r'D:\Debbuger\b_data\all'
for name in to_delete:
    del dict_all[name]
print("bob")
best_of_breed(dict_all,"RF")
print("oscar")
OSCAR(dict_all,"RF",oracle=True)
print("alm")
one_ELM(dict_all,False,"RF")

results_all_projects.to_csv(os.path.join(directory_RF,"all_results_all.csv"), index=False)

results_all_projects = pd.DataFrame(
        columns=['cold_start_project','model_source', 'precision_bug', 'recall_bug','F_bug', 'F2_bug','roc_area_bug', 'prc_area_bug', 'precision', 'recall',
                 'F1', 'F2', 'roc_area','prc_area','num_bugs_test','num_all_inst_test','percent_bugs_test','num_bugs_train','num_all_inst_train','percent_bugs_train',"percent_group_training_set"])


print("fowler")
directory_RF = r'D:\Debbuger\b_data\fowler'
for name in to_delete:
    del dict_fowler[name]
print("bob")
best_of_breed(dict_fowler,"RF")
print("oscar")
OSCAR(dict_fowler,"RF",oracle=True)
print("alm")
one_ELM(dict_fowler,False,"RF")

results_all_projects.to_csv(os.path.join(directory_RF,"all_results_all.csv"), index=False)

results_all_projects = pd.DataFrame(
        columns=['cold_start_project','model_source', 'precision_bug', 'recall_bug','F_bug', 'F2_bug','roc_area_bug', 'prc_area_bug', 'precision', 'recall',
                 'F1', 'F2', 'roc_area','prc_area','num_bugs_test','num_all_inst_test','percent_bugs_test','num_bugs_train','num_all_inst_train','percent_bugs_train',"percent_group_training_set"])


'''
print("trad")
directory_RF = r'D:\Debbuger\b_data\trad'
for name in to_delete:
    del dict_trad[name]
print("bob")
best_of_breed(dict_trad,"RF")
print("oscar")
OSCAR(dict_trad,"RF",oracle=True)
print("alm")
one_ELM(dict_trad,False,"RF")

results_all_projects.to_csv(os.path.join(directory_RF,"all_results_all.csv"), index=False)

results_all_projects = pd.DataFrame(
        columns=['cold_start_project','model_source', 'precision_bug', 'recall_bug','F_bug', 'F2_bug','roc_area_bug', 'prc_area_bug', 'precision', 'recall',
                 'F1', 'F2', 'roc_area','prc_area','num_bugs_test','num_all_inst_test','percent_bugs_test','num_bugs_train','num_all_inst_train','percent_bugs_train',"percent_group_training_set"])





























'''

##############################!!!!!!!!
directory_RF = r'D:\Debbuger\b_data\all'
all_data_with_models_name = 'dict_all_models_and_data'
label_bugs = 'Bugged'
#dict_name = "by_projects.sav"
file_path_RF = os.path.join(directory_RF, all_data_with_models_name)

#dict_name_path = os.path.join(r'D:\Debbuger\PROMISE', dict_name)
###############################!!!!!!!





with open(file_path_RF, 'rb') as f:
    u = pickle._Unpickler(f)
    u.encoding = 'latin1'
    data = u.load()
    for cold_start_project_name, (cold_start_model, cold_start_testing_set) in data.items():
        data[cold_start_project_name] = (
        cold_start_model, cold_start_testing_set.drop(['Class', 'unique_name'], axis=1))

    best_of_breed(data, "RF")
    OSCAR(data, "RF")
    one_ELM(data, False, "RF")
    one_ELM(data, True, "RF")


print(file_path_RF)
data = pickle.load(open(file_path_RF, "rb"))

for name in to_delete:
    del data[name]

#del data['tiles']
#del data['tiles_tiles-2.1.0']
#del data['kafka_0.9.0.0']
#del data['tajo_release-0.8.0']
for key, value in data.items():
    if(len(value) != 3):
        print(key)


for cold_start_project_name, (cold_start_model, cold_start_testing_set) in data.items():
    if 'Class' in cold_start_testing_set.columns:
        data[cold_start_project_name] = (cold_start_model, cold_start_testing_set.drop(['Class', 'unique_name'], axis=1))
    if '.' not in cold_start_project_name:
        data[cold_start_project_name+".0"] = data[cold_start_project_name]
        del data[cold_start_project_name]
    #if cold_start_project_name in ['jEdit4.2','jEdit4.3']:
        #del data[cold_start_project_name]

#del data['xerces1.4']
#del data['jEdit4.3']
#del data['jEdit3.2']

#OSCAR_PERCENT_TEST(data,"RF")

#this is all the expi
print("bob")
best_of_breed(data,"RF")
print("oscar")
OSCAR(data,"RF",oracle=True)
print("alm")
one_ELM(data,False,"RF")

results_all_projects.to_csv(os.path.join(directory_RF,"all_results_all.csv"), index=False)


results_all_projects = pd.DataFrame(
        columns=['cold_start_project','model_source', 'precision_bug', 'recall_bug','F_bug', 'F2_bug','roc_area_bug', 'prc_area_bug', 'precision', 'recall',
                 'F1', 'F2', 'roc_area','prc_area','num_bugs_test','num_all_inst_test','percent_bugs_test','num_bugs_train','num_all_inst_train','percent_bugs_train',"percent_group_training_set"])

##############################!!!!!!!!
directory_RF = r'D:\Debbuger\b_data\fowler'
all_data_with_models_name = 'dict_all_models_and_data'
file_path_RF = os.path.join(directory_RF, all_data_with_models_name)

#dict_name_path = os.path.join(r'D:\Debbuger\PROMISE', dict_name)
###############################!!!!!!!


print(file_path_RF)
data = pickle.load(open(file_path_RF, "rb"))
#del data['tiles']
#del data['tiles_tiles-2.1.0']
#del data['kafka_0.9.0.0']
#del data['tajo_release-0.8.0']

for name in to_delete:
    del data[name]

for key, value in data.items():
    if(len(value) != 3):
        print(key)

print("bob")
best_of_breed(data,"RF")
print("oscar")
OSCAR(data,"RF",oracle=True)
print("alm")
one_ELM(data,False,"RF")

results_all_projects.to_csv(os.path.join(directory_RF,"all_results_fowler.csv"), index=False)


results_all_projects = pd.DataFrame(
        columns=['cold_start_project','model_source', 'precision_bug', 'recall_bug','F_bug', 'F2_bug','roc_area_bug', 'prc_area_bug', 'precision', 'recall',
                 'F1', 'F2', 'roc_area','prc_area','num_bugs_test','num_all_inst_test','percent_bugs_test','num_bugs_train','num_all_inst_train','percent_bugs_train',"percent_group_training_set"])

##############################!!!!!!!!
directory_RF = r'D:\Debbuger\b_data\trad'
all_data_with_models_name = 'dict_all_models_and_data'
file_path_RF = os.path.join(directory_RF, all_data_with_models_name)

#dict_name_path = os.path.join(r'D:\Debbuger\PROMISE', dict_name)
###############################!!!!!!!

print(file_path_RF)
data = pickle.load(open(file_path_RF, "rb"))
#del data['tiles']
#del data['tiles_tiles-2.1.0']
#del data['kafka_0.9.0.0']
#del data['tajo_release-0.8.0']

for name in to_delete:
    del data[name]

for key, value in data.items():
    if(len(value) != 3):
        print(key)

print("bob")
best_of_breed(data,"RF")
print("oscar")
OSCAR(data,"RF",oracle=True)
print("alm")
one_ELM(data,False,"RF")

results_all_projects.to_csv(os.path.join(directory_RF,"all_results_trad.csv"), index=False)











#one_ELM(data,True,"RF")


data = pickle.load(open(file_path_ELM, "rb"))
for cold_start_project_name, (cold_start_model, cold_start_testing_set) in data.items():
    if 'Class' in cold_start_testing_set.columns:
        data[cold_start_project_name] = (cold_start_model, cold_start_testing_set.drop(['Class', 'unique_name'], axis=1))
    if '.' not in cold_start_project_name:
        data[cold_start_project_name+".0"] = data[cold_start_project_name]
        del data[cold_start_project_name]

best_of_breed(data,"ELM")
OSCAR(data,"ELM")
one_ELM(data,False,"ELM")
one_ELM(data,True,"ELM")

'''


