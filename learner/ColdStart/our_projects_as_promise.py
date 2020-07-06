import pandas as pd
import xml.etree.ElementTree as et
from scipy.io import arff
from scipy.io.arff import loadarff
import os
import pickle
from imblearn.ensemble import BalancedRandomForestClassifier

metrics = ['WMC','DIT','NOCh','LCOM*','Ma','NPM','RTLOC','MIF']
directory_path = r'D:\Debbuger\our projects style promise'
ver_file_name = "versions.xlsx"

def predict_model_kfold(name, data):
    model = BalancedRandomForestClassifier(n_estimators=1000, max_depth=5)
    x = data.drop('hasBug', axis=1)
    y = data['hasBug']
    num_of_bugs = data.loc[data['hasBug'] == 1].shape[0]
    if num_of_bugs == 0:
        print("NOT - " + str(name))
        return None
    num_of_all_instances = data.shape[0]
    model.fit(x, y)
    return model

def save_model_dump(path,name,model):
    file_path = os.path.join(path, name)
    pickle.dump(model, open(file_path, 'wb'))


directory_RF = r'D:\Debbuger\our projects style promise\within_models_full_ours_f'
all_data_with_models_name = 'all_data_with_models_ours_f.sav'
label_bugs = "hasBug"
file_path_RF = os.path.join(r'D:\Debbuger\our projects style promise\within_models_ours_f', all_data_with_models_name)

data = pickle.load(open(file_path_RF, "rb"))
del data['kafka_0.8.0']
del data['tiles_tiles-2.1.0']
del data['kafka_0.9.0.0']
del data['tajo_release-0.8.0']
for key, value in data.items():
    if(len(value) != 2):
        print(key)

test_set = ['tiles_tiles-2.2.0','sentry_release-2.0.0','oozie_release-4.2.0','kafka_2.0.0','fop_fop-2_2','bookkeeper_release-4.7.0','tajo_release-0.10.0']

dic_testing = {}

dic_full_proj = {"bookkeeper": pd.DataFrame(),
                 "fop": pd.DataFrame(),
                 "kafka": pd.DataFrame(),
                 "oozie": pd.DataFrame(),
                 "sentry": pd.DataFrame(),
                 "tajo": pd.DataFrame(),
                 "tiles": pd.DataFrame()
                 }
for proj_name_host, (model_host, testing_set_host) in data.items():
    cur_full_proj = proj_name_host.split('_')[0]
    if proj_name_host in test_set:
        dic_testing[cur_full_proj] = testing_set_host
    else:
        dic_full_proj[cur_full_proj] = dic_full_proj[cur_full_proj].append(testing_set_host,ignore_index=True)

for proj_name, data in dic_full_proj.items():
    model = predict_model_kfold(proj_name, data)
    if model is not None:
        save_model_dump(directory_RF, proj_name + ".sav", model)

data = {}

for filename in os.listdir(directory_RF):
    if filename.endswith(".sav"):
        print(os.path.join(directory_RF, filename))
        current_model = pickle.load(open(os.path.join(directory_RF, filename), "rb"))
        #data[filename[:-4]] = (current_model, dic_testing[filename[:-4]].drop(['sourceFile'], axis=1))
        data[filename[:-4]] = (current_model,dic_full_proj[filename[:-4]], dic_testing[filename[:-4]])
        print(os.path.join(directory_RF, filename))

file_path = os.path.join(directory_RF, "within_models_full_ours_f.sav")
pickle.dump(data, open(file_path, 'wb'))

print(data)






'''
def save_model_dump(path,name,model):
    file_path = os.path.join(path, name)
    pickle.dump(model, open(file_path, 'wb'))

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
def process_attributes(bugs):
    bugs_features = [38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62,
                     63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87,
                     88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
                     110, 111, 112, 113, 114, 115, 116, 117, 118]
    all= [( "tot_changes", "NUMERIC"), ( "sum_insert", "NUMERIC"),
          ( "sum_delets", "NUMERIC"),( "count_insert", "NUMERIC"),
          ( "count_delets", "NUMERIC"),( "avg_insert", "NUMERIC"),
          ( "avg_delets", "NUMERIC"),( "avg_insert_nonzero", "NUMERIC"),
          ( "avg_delets_nonzero", "NUMERIC"), ( "tot_bugs", "NUMERIC"),( "tot_changes_last", "NUMERIC"), ( "sum_insert_last", "NUMERIC"),
          ( "sum_delet_lasts", "NUMERIC"),( "count_insert_last", "NUMERIC"),
          ( "count_delets_last", "NUMERIC"),( "avg_insert_last", "NUMERIC"),
          ( "avg_delets_last", "NUMERIC"),( "avg_insert_nonzero_last", "NUMERIC"),
          ( "avg_delets_nonzero_last", "NUMERIC"), ( "tot_bugs_last", "NUMERIC"), ( "tot_developers", "NUMERIC"),
          ( "lastVer_tot_developers", "NUMERIC"),( "last_commit", "NUMERIC"),( "last_bug", "NUMERIC"),( "last_bug_binary", "NUMERIC"),
          ( "change_set", "NUMERIC"), ( "age", "NUMERIC"),( "age2", "NUMERIC"),( "tot_changes_bugged", "NUMERIC"), ( "sum_insert_bugged", "NUMERIC"),
          ( "sum_delet_buggeds", "NUMERIC"),( "count_insert_bugged", "NUMERIC"),
          ( "count_delets_bugged", "NUMERIC"),( "avg_insert_bugged", "NUMERIC"),
          ( "avg_delets_bugged", "NUMERIC"),( "avg_insert_nonzero_bugged", "NUMERIC"),
          ( "avg_delets_nonzero_bugged", "NUMERIC"),

          ( "tot_changes_p3", "NUMERIC"), ( "sum_insert_p3", "NUMERIC"),
          ( "sum_delet_p3s", "NUMERIC"),( "count_insert_p3", "NUMERIC"),
          ( "count_delets_p3", "NUMERIC"),( "avg_insert_p3", "NUMERIC"),
          ( "avg_delets_p3", "NUMERIC"),( "avg_insert_nonzero_p3", "NUMERIC"),
          ( "avg_delets_nonzero_p3", "NUMERIC"),

          ( "tot_changes_normal", "NUMERIC"), ( "sum_insert_normal", "NUMERIC"),
          ( "sum_delet_normals", "NUMERIC"),( "count_insert_normal", "NUMERIC"),
          ( "count_delets_normal", "NUMERIC"),( "avg_insert_normal", "NUMERIC"),
          ( "avg_delets_normal", "NUMERIC"),( "avg_insert_nonzero_normal", "NUMERIC"),
          ( "avg_delets_nonzero_normal", "NUMERIC"),

          ( "tot_changes_enhancement", "NUMERIC"), ( "sum_insert_enhancement", "NUMERIC"),
          ( "sum_delet_enhancements", "NUMERIC"),( "count_insert_enhancement", "NUMERIC"),
          ( "count_delets_enhancement", "NUMERIC"),( "avg_insert_enhancement", "NUMERIC"),
          ( "avg_delets_enhancement", "NUMERIC"),( "avg_insert_nonzero_enhancement", "NUMERIC"),
          ( "avg_delets_nonzero_enhancement", "NUMERIC"),

          ( "tot_changes_major", "NUMERIC"), ( "sum_insert_major", "NUMERIC"),
          ( "sum_delet_majors", "NUMERIC"),( "count_insert_major", "NUMERIC"),
          ( "count_delets_major", "NUMERIC"),( "avg_insert_major", "NUMERIC"),
          ( "avg_delets_major", "NUMERIC"),( "avg_insert_nonzero_major", "NUMERIC"),
          ( "avg_delets_nonzero_major", "NUMERIC"),
          ( "tot_changes_Ranking", "NUMERIC"), ( "sum_insert_Ranking", "NUMERIC"),
          ( "sum_delet_Rankings", "NUMERIC"),( "count_insert_Ranking", "NUMERIC"),
          ( "count_delets_Ranking", "NUMERIC"),( "avg_insert_Ranking", "NUMERIC"),
          ( "avg_delets_Ranking", "NUMERIC"),( "avg_insert_nonzero_Ranking", "NUMERIC"),
          ( "avg_delets_nonzero_Ranking", "NUMERIC"),


          ( "avg_submit", "NUMERIC"),
          ( "avg_modify", "NUMERIC"),
          ( "distinct_OS", "NUMERIC"),
          ( "distinct_assignedTo", "NUMERIC"),
          ( "distinct_Hardware", "NUMERIC"),
          ( "distinct_Component", "NUMERIC"),
          ( "distinct_Version", "NUMERIC"),
          ( "count_Block", "NUMERIC"),
          ( "count_Depends", "NUMERIC"),

          ( "p1_count", "NUMERIC"), ( "p2_count", "NUMERIC"), ( "p3_count", "NUMERIC"), ( "p4_count", "NUMERIC"), ( "p5_count", "NUMERIC") ,
          ( "p1_count_perc", "NUMERIC"), ( "p2_count_perc", "NUMERIC"), ( "p3_count_perc", "NUMERIC"), ( "p4_count_perc", "NUMERIC"), ( "p5_count_perc", "NUMERIC") ,

          ( "minor_count", "NUMERIC"), ( "normal_count", "NUMERIC"), ( "major_count", "NUMERIC"), ( "enhancement_count", "NUMERIC"), ( "critical_count", "NUMERIC"), ( "blocker_count", "NUMERIC"), ( "trivial_count", "NUMERIC"),
          ( "minor_count_perc", "NUMERIC"), ( "normal_count_perc", "NUMERIC"), ( "major_count_perc", "NUMERIC"), ( "enhancement_count_perc", "NUMERIC"), ( "critical_count_perc", "NUMERIC"), ( "blocker_count_perc", "NUMERIC"), ( "trivial_count_perc", "NUMERIC"),

          ( "avg_commits_files", "NUMERIC"),
          ( "avg_commits_files_bugged", "NUMERIC"),
          ( "avg_commits_files_valid", "NUMERIC")
          ]
    ret=[]
    if bugs:
        for i in range(len(all)):
            if i+1 in bugs_features:
                ret.append(all[i])
    else:
        for i in range(len(all)):
            if i+1 not in bugs_features:
                ret.append(all[i])

    return ret
def encode_categorial(data):
    true_false_att = ["ONE_elem_params","exception","externalizable",'abstract','error','serializable','ONE_elem_params_constructors']
    for col in data:
        if col == 'IsInterface':
            data[col] = data[col].str.decode('utf-8').map({'Interface': 0, 'class': 1})
        elif col == 'Parent':
            data[col] = data[col].str.decode('utf-8').map({'Has_parent': 0, 'No_parent': 1})
        elif col == 'scope':
            data[col] = data[col].str.decode('utf-8').map({'public': 0, 'protected': 1,'private':2,'default':3})
        elif col in true_false_att:
            data[col] = data[col].str.decode('utf-8').map({'true': 1, 'false': 0, 'True': 1, 'False': 0})
    return data
def pre_processing(data):
    null_data = data[data.isnull().any(axis=1)]
    #print(null_data.shape)
    num_of_rows = null_data.shape[0]
    tr_data_noNa = data.copy()
    if num_of_rows!= 0:
        for col in tr_data_noNa.columns[:-1]:
            if col != 'label' or col != 'hasBug':
                if tr_data_noNa[col].dtype == 'object':
                    tr_data_noNa[col].fillna("Unknown", inplace=True)
                else:
                    col_mean = data[col].mean()
                    tr_data_noNa[col].fillna(col_mean, inplace=True)
    tr_data_noNa = encode_categorial(tr_data_noNa)
    print(tr_data_noNa.shape)
    return tr_data_noNa
def selectFeatures(data,remove_bugs,remove_process):
    g2_f = g2_attributes()
    all2_att_names = [tup[0] for tup in g2_f]
    bugs_f = process_attributes(bugs=True)
    all_bugs_f_names = [tup[0] for tup in bugs_f]
    process_f = process_attributes(bugs=False)
    all_process_f_names = [tup[0] for tup in process_f]
    if all2_att_names[0] in data.columns:
        g3_f = g3_attributes()
        all3_att_names = [tup[0] for tup in g3_f]
        #print (data.shape)
        new_data = data.drop(all2_att_names, axis=1)
        #print (new_data.shape)
        new_data = new_data.drop(all3_att_names, axis=1)
        #print (new_data.shape)
        data = new_data
    if remove_bugs and all_bugs_f_names[0] in data.columns:
        data = data.drop(all_bugs_f_names, axis=1)
    if remove_process and all_process_f_names[0] in data.columns:
        data = data.drop(all_process_f_names, axis=1)
    return data
def load_arff(data_arff):
    raw_data = loadarff(data_arff)
    df_data = pd.DataFrame(raw_data[0])
    return df_data

dict_our_f = {}
dict_promise_f = {}

for project_name in os.listdir(directory_path):
     folder = os.path.join(directory_path, project_name)
     if os.path.isdir(folder):
         if os.path.isfile(os.path.join(folder,ver_file_name)):
            print("start working on "+ project_name)
            versions_df = pd.read_excel(os.path.join(folder,ver_file_name) ,header=None)
            for index, row in versions_df.iterrows():
                print(row[0])
                path_java_names = os.path.join(folder,str(row[0])+".csv")
                path_weka = os.path.join(folder, str(row[0]) + ".arff")
                path_promise_f = os.path.join(folder, str(row[0]) + ".xml")

                xtree = et.parse(path_promise_f)
                xroot = xtree.getroot()

                rows = []
                for c_package in xroot[1]:
                    for package_metric in c_package.findall('Metrics/Metric'):
                        if package_metric.attrib['name'] == 'Ca':
                            c_ca = float(package_metric.attrib['value'])
                        elif package_metric.attrib['name'] == 'Ce':
                            c_ce = float(package_metric.attrib['value'])
                    for c_class in c_package.findall('Classes/Class'):
                        class_name = c_class.attrib['name']
                        class_sourceFile = c_class.attrib['sourceFile']
                        metrics = c_class.find('Metrics')
                        for metric in metrics:
                            if metric.attrib['name'] == 'WMC':
                                c_WMC =  float(metric.attrib['value'])
                            elif metric.attrib['name'] == 'DIT':
                                c_DIT =  float(metric.attrib['value'])
                            elif metric.attrib['name'] == 'NOCh':
                                c_NOC =  float(metric.attrib['value'])
                            elif metric.attrib['name'] == 'LCOM*':
                                c_LCOM =  float(metric.attrib['value'])
                            elif metric.attrib['name'] == 'Ma':
                                c_RFC =  float(metric.attrib['value'])
                            elif metric.attrib['name'] == 'NPM':
                                c_NPM =  float(metric.attrib['value'])
                            elif metric.attrib['name'] == 'RTLOC':
                                c_LOC =  float(metric.attrib['value'])
                            elif metric.attrib['name'] == 'MIF':
                                c_MFA =  float(metric.attrib['value'])
                            elif metric.attrib['name'] == 'Ad':
                                c_Ad =  float(metric.attrib['value'])
                            elif metric.attrib['name'] == 'Av':
                                c_Av =  float(metric.attrib['value'])
                        methods = c_class.find('Methods')
                        f_out = 0.0
                        tloc_avg = 0.0
                        index = 0
                        vg_max = 0.0
                        vg_avg = 0.0
                        for method in methods:
                            metrics_method = method.find('Metrics')
                            index = index+1
                            for metric in metrics_method:
                                if metric.attrib['name'] == 'Fout':
                                    f_out = f_out + float(metric.attrib['value'])
                                elif metric.attrib['name'] == 'TLOC':
                                    tloc_avg = tloc_avg + float(metric.attrib['value'])
                                elif metric.attrib['name'] == 'VG':
                                    vg_avg = vg_avg + float(metric.attrib['value'])
                                    if float(metric.attrib['value']) > vg_max:
                                        vg_max = float(metric.attrib['value'])
                        tloc_avg = (tloc_avg/index) if index!=0 else 0
                        vg_avg = (vg_avg/index) if index!=0 else 0
                        dam = (c_Ad-c_Av/c_Ad) if c_Ad != 0 else 0
                        rows.append({"name": class_name, "sourceFile": class_sourceFile,
                                     "wmc": c_WMC, "dit": c_DIT,
                                     "noc": c_NOC, "cbo": f_out,
                                     "rfc": c_RFC, "lcom": c_LCOM,
                                     "ca": c_ca, "ce": c_ce,
                                     "npm": c_NPM, "loc": c_LOC,
                                     "dam": dam, "mfa": c_MFA,
                                     "amc": tloc_avg, "max(cc)": vg_max,
                                     "avg(cc)": vg_avg  })

                out_df = pd.DataFrame(rows)
                #out_df['sourceFile'] = out_df['sourceFile'].apply(lambda x: (x[2:]).replace('/', '\\'))
                out_df['sourceFile'] = out_df['sourceFile'].apply(lambda x: x[2:])

                rows_calc = []
                for name, group in out_df.groupby('sourceFile'):
                    rows_calc.append({"sourceFile": name,
                                 "wmc": group['wmc'].sum(),
                                 "dit": group['dit'].mean(),
                                 "noc": group['noc'].mean(),
                                 "cbo": group['cbo'].mean(),
                                 "rfc": group['rfc'].sum(),
                                 "lcom": group['lcom'].sum(),
                                 "ca": group['ca'].mean(),
                                 "ce": group['ce'].mean(),
                                 "npm": group['npm'].sum(),
                                 "loc": group['loc'].sum(),
                                 "dam": group['dam'].mean(),
                                 "mfa": group['mfa'].mean(),
                                 "amc": group['amc'].mean(),
                                 "max(cc)": group['max(cc)'].max(),
                                 "avg(cc)": group['avg(cc)'].mean()})

                out_df_calc = pd.DataFrame(rows_calc)
                arff_1 = load_arff(path_weka)
                names = pd.read_csv(path_java_names,header=None)
                arff_1['hasBug']= arff_1['hasBug'].str.decode('utf-8').map({'valid': 0, 'bugged': 1})
                arff_1 = selectFeatures(arff_1,True,True)
                arff_1['sourceFile'] = names[0].apply(lambda x: x.replace('\\','/'))

                our_f = pd.DataFrame()
                promise_f = pd.DataFrame()

                for index, row_c in out_df_calc.iterrows():
                    sub_df = arff_1[arff_1['sourceFile'].str.contains(row_c['sourceFile'])]
                    if sub_df.shape[0]==1:
                        row_c['hasBug'] = sub_df['hasBug'].values[0]
                        promise_f = promise_f.append(row_c)
                        our_f = our_f.append(sub_df.iloc[0])

                dict_our_f[project_name+'_'+str(row[0])] = pre_processing(our_f)
                dict_promise_f[project_name+'_'+str(row[0])] = promise_f

save_model_dump(directory_path,"dict_our_f.sav", dict_our_f)
save_model_dump(directory_path,"dict_promise_f.sav", dict_promise_f)


#out_df_calc.to_csv(r'D:\Debbuger\our projects style promise\bookkeeper\4.0.0_calc.csv',index=False)
#Package -> {Classes -> Metrics}
'''