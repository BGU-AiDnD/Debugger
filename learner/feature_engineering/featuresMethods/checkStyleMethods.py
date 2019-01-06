__author__ = 'amir'

from feature_engineering.articles import *
import feature_engineering.articles
import featureExtractorBase

best_features=[7,15,19,1,23,16,63,22,30,6,2,31,54,62,4,55,27,11,17,26,67,10,35,47,51,24,20,8,48,34,59,66,49,58,52,32]
class checkStyleMethods(featureExtractorBase.FeatureExtractorBase):
    def get_attributesOLD(self):
        return [("McCabe" , "NUMERIC"),
    ("fanOut" , "NUMERIC"),
    ("NPath" , "NUMERIC"),
    ("FileLen" , "NUMERIC"),("NCSS" , "NUMERIC"),("outer" , "NUMERIC"),
    ("publicMethods" , "NUMERIC"),("totalMethods" , "NUMERIC"),("thorwsSTM" , "NUMERIC")
    ]

    def get_featuresOLD(self, c, files_dict,prev_date,start_date,end_date):
        style='select * from checkStyle group by name'
        feature_engineering.articles.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, style)

    def get_attributes(self):
        all=[("NCSS" , "NUMERIC"),("FileLen" , "NUMERIC"),("sum_fors" , "NUMERIC"),("sum_ifs" , "NUMERIC"),("sum_tries" , "NUMERIC"),
                ("len_mccab" , "NUMERIC"),("sum_mccab" , "NUMERIC"),("mean_mccab" , "NUMERIC"),("median_mccab" , "NUMERIC"),
                ("var_mccab" , "NUMERIC"),("max_mccab" , "NUMERIC"),("min_mccab" , "NUMERIC"),("oneElement_mccab" , "NUMERIC"),
                ("len_fanOut" , "NUMERIC"),("sum_fanOut" , "NUMERIC"),("mean_fanOut" , "NUMERIC"),("median_fanOut" , "NUMERIC"),
                ("var_fanOut" , "NUMERIC"),("max_fanOut" , "NUMERIC"),("min_fanOut" , "NUMERIC"),("oneElement_fanOut" , "NUMERIC"),
                ("len_NPath" , "NUMERIC"),("sum_NPath" , "NUMERIC"),("mean_NPath" , "NUMERIC"),("median_NPath" , "NUMERIC"),
                ("var_NPath" , "NUMERIC"),("max_NPath" , "NUMERIC"),("min_NPath" , "NUMERIC"),("oneElement_NPath" , "NUMERIC"),
                ("len_JavaNCSSmet" , "NUMERIC"),("sum_JavaNCSSmet" , "NUMERIC"),("mean_JavaNCSSmet" , "NUMERIC"),("median_JavaNCSSmet" , "NUMERIC"),
                ("var_JavaNCSSmet" , "NUMERIC"),("max_JavaNCSSmet" , "NUMERIC"),("min_JavaNCSSmet" , "NUMERIC"),("oneElement_JavaNCSSmet" , "NUMERIC"),
                ("len_thorwsSTM" , "NUMERIC"),("sum_thorwsSTM" , "NUMERIC"),("mean_thorwsSTM" , "NUMERIC"),("median_thorwsSTM" , "NUMERIC"),("var_thorwsSTM" , "NUMERIC"),
                ("max_thorwsSTM" , "NUMERIC"),("min_thorwsSTM" , "NUMERIC"),("oneElement_thorwsSTM" , "NUMERIC"),("len_coupl" , "NUMERIC"),("sum_coupl" , "NUMERIC"),
                ("mean_coupl" , "NUMERIC"),("median_coupl" , "NUMERIC"),("var_coupl" , "NUMERIC"),("max_coupl" , "NUMERIC"),("min_coupl" , "NUMERIC"),
                ("oneElement_coupl" , "NUMERIC"),("len_executables" , "NUMERIC"),("sum_executables" , "NUMERIC"),("mean_executables" , "NUMERIC"),
                ("median_executables" , "NUMERIC"),("var_executables" , "NUMERIC"),("max_executables" , "NUMERIC"),("min_executables" , "NUMERIC"),
                ("oneElement_executables" , "NUMERIC"),("len_lens" , "NUMERIC"),("sum_lens" , "NUMERIC"),("mean_lens" , "NUMERIC"),("median_lens" , "NUMERIC"),
                ("var_lens" , "NUMERIC"),("max_lens" , "NUMERIC"),("min_lens" , "NUMERIC"),("oneElement_lens" , "NUMERIC")]
        ret=[]
        for i in range(len(all)):
            if i+1 in best_features:
                ret.append(all[i])
        return ret

    def get_features(self, c, files_dict,prev_date,start_date,end_date):
        style='select * from checkStyleExtends group by name'
        feature_engineering.articles.sqlToAttributesBest(["0" for x in best_features], c, files_dict, style, best_features)

