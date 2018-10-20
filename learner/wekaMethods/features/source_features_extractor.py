""""""
import json
from os import path

import numpy

from wekaMethods.features.features_extractor import FeaturesExtractor


class SourceFeaturesExtractor(FeaturesExtractor):
    """"""

    @cached_property
    def features_object(self):
        with open(path.abspath(path.join(self.FEATURES_FOLDER, "source_code_features.json")),
                  "r") as features_file:
            return json.load(features_file)

    def get_attributes(self):
        attributes = []
        for feature_index, feature_key, feature_type in enumerate(self.all_features.items(), 1):
            if feature_index in self.best_features_indexes:
                attributes.append((feature_key, feature_type))

        return attributes

    # TODO: check this method if needed please. I smell dead code in here...
    def stat(self, lst):
        return len(lst), sum(lst), numpy.mean(lst), numpy.median(lst), numpy.var(lst), max(
            lst), min(lst)

    def addFromDict(self, files_dict, dict):
        Att_dict = {}
        for f in files_dict.keys():
            Att_dict[f] = [0, 0, 0, 0, 0, 0, 0]
        for d in dict:
            if d in Att_dict and dict[d] != []:
                Att_dict[d] = list(self.stat(dict[d]))
        for f in Att_dict:
            files_dict[f] = files_dict[f] + Att_dict[f]

    # TODO: RENAME THE QUERIES & DOCUMENT THE MEANING!
    def get_features(self, prev_date, start_date, end_date):
        sourceMethodsFiles = \
            '''select  name, Lines,	Statements,	Percent_Branch_Statements, Method_Call_Statements,
            Percent_Lines_with_Comments, Classes_and_interfaces, Methods_per_Class, 
            Maximum_Complexity, Average_Block_Depth, Average_Complexity,
            Statements_at_block_level_0, Statements_at_block_level_1, Statements_at_block_level_2,
            Statements_at_block_level_3, Statements_at_block_level_4, Statements_at_block_level_5,
            Statements_at_block_level_6 ,Statements_at_block_level_7 from JAVAfilesFix'''

        self.convert_sql_queries_to_attributes(["0"] * 18, sourceMethodsFiles)

        sourceMethodsFiles = '''select name, 
        Statements_at_block_level_3 /(1.0*(case When Statements= 0 Then 1 Else Statements End)),
        Statements_at_block_level_4/(1.0*(case When Statements= 0 Then 1 Else Statements End)),
        Statements_at_block_level_5 /(1.0*(case When Statements= 0 Then 1 Else Statements End)),
        Statements_at_block_level_6 /(1.0*(case When Statements= 0 Then 1 Else Statements End)),
        Statements_at_block_level_7/(1.0*(case When Statements= 0 Then 1 Else Statements End))
        from JAVAfilesFix'''

        self.convert_sql_queries_to_attributes(["0"] * 5, sourceMethodsFiles)
        sourceMethodsFiles = \
            '''select name, max(Statements_at_block_level_0, Statements_at_block_level_1, 
            Statements_at_block_level_2, Statements_at_block_level_3, Statements_at_block_level_4,
            Statements_at_block_level_5, Statements_at_block_level_6, Statements_at_block_level_7, 
            Statements_at_block_level_8, Statements_at_block_level_9) from JAVAfilesFix'''

        self.convert_sql_queries_to_attributes(["0"], sourceMethodsFiles)
        sourceMethodsFiles = \
            '''select name, max(
            Statements_at_block_level_0/(1.0*(case When Statements= 0 Then 1 Else Statements End)),
            Statements_at_block_level_1/(1.0*(case When Statements= 0 Then 1 Else Statements End)),
            Statements_at_block_level_2/(1.0*(case When Statements= 0 Then 1 Else Statements End)),
            Statements_at_block_level_3 /(1.0*(case When Statements= 0 Then 1 Else Statements End)),
            Statements_at_block_level_4/(1.0*(case When Statements= 0 Then 1 Else Statements End)),
            Statements_at_block_level_5 /(1.0*(case When Statements= 0 Then 1 Else Statements End)),
            Statements_at_block_level_6 /(1.0*(case When Statements= 0 Then 1 Else Statements End)),
            Statements_at_block_level_7/(1.0*(case When Statements= 0 Then 1 Else Statements End)),
            Statements_at_block_level_8/(1.0*(case When Statements= 0 Then 1 Else Statements End)),
            Statements_at_block_level_9/(1.0*(case When Statements= 0 Then 1 Else Statements End)))
            from JAVAfilesFix'''
        self.convert_sql_queries_to_attributes(["0"], sourceMethodsFiles)

        # TODO: explain this to me so that i'd understand and refactore
        complexity_d = dict(map(lambda f: (f, list()), files_dict.keys()))
        statements_d = dict(map(lambda f: (f, list()), files_dict.keys()))
        depth_d = dict(map(lambda f: (f, list()), files_dict.keys()))
        calls_d = dict(map(lambda f: (f, list()), files_dict.keys()))
        for row in c.execute(
                'select File_Name, Complexity, Statements, Maximum_Depth, Calls from SourcemethodsFix'):
            name = row[0]
            if name in files_dict:
                complexity_d[name].append(int(row[1]))
                statements_d[name].append(int(row[2]))
                depth_d[name].append(int(row[3]))
                calls_d[name].append(int(row[4]))
        self.addFromDict(files_dict, complexity_d)
        self.addFromDict(files_dict, statements_d)
        self.addFromDict(files_dict, depth_d)
        self.addFromDict(files_dict, calls_d)
