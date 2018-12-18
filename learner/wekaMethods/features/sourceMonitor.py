__author__ = 'amir'

from wekaMethods.articles import *
import wekaMethods.articles
#from wekaMethods.articles import sqlToAttributes
import numpy
from collections import Counter
class sourceMonitor:
    def get_attributes(self):
        return [("Lines" ,"NUMERIC"),("Statements" ,"NUMERIC"),
    ("Percent_Branch_Statements" ,"NUMERIC"),
    ("Method_Call_Statements" ,"NUMERIC"),
    ("Percent_Lines_with_Comments" ,"NUMERIC"),
    ("Classes_and_interfaces" ,"NUMERIC"),
    ("Methods_per_Class" ,"NUMERIC"),
    ("Maximum_Complexity" ,"NUMERIC"),
    #("Maximum_Block_Depth" ,"NUMERIC"),
    ("Average_Block_Depth" ,"NUMERIC"),
    ("Average_Complexity" ,"NUMERIC"),
    ("Statements_at_block_level_0" ,"NUMERIC"),
    ("Statements_at_block_level_1" ,"NUMERIC"),
    ("Statements_at_block_level_2" ,"NUMERIC"),
    ("Statements_at_block_level_3" ,"NUMERIC"),
    ("Statements_at_block_level_4" ,"NUMERIC"),
    ("Statements_at_block_level_5" ,"NUMERIC"),
    ("Statements_at_block_level_6" ,"NUMERIC"),
    ("Statements_at_block_level_7" ,"NUMERIC"),
    ("Statements_at_block_level_3_percent" ,"NUMERIC"),
    ("Statements_at_block_level_4_percent" ,"NUMERIC"),
    ("Statements_at_block_level_5_percent" ,"NUMERIC"),
    ("Statements_at_block_level_6_percent" ,"NUMERIC"),
    ("Statements_at_block_level_7_percent" ,"NUMERIC"),
    ("Statements_max_at_block" ,"NUMERIC"),
    ("Statements_max_at_blockPercent" ,"NUMERIC"),
( "len_complexity", "NUMERIC"),( "sum_complexity", "NUMERIC"),( "mean_complexity", "NUMERIC"),( "median_complexity", "NUMERIC"),
( "var_complexity", "NUMERIC"),( "max_complexity", "NUMERIC"),( "min_complexity", "NUMERIC"),
( "len_Statements", "NUMERIC"),( "sum_Statements", "NUMERIC"),( "mean_Statements", "NUMERIC"),( "median_Statements", "NUMERIC"),
( "var_Statements", "NUMERIC"),( "max_Statements", "NUMERIC"),( "min_Statements", "NUMERIC"),
( "len_depth", "NUMERIC"),( "sum_depth", "NUMERIC"),( "mean_depth", "NUMERIC"),( "median_depth", "NUMERIC"),
( "var_depth", "NUMERIC"),( "max_depth", "NUMERIC"),( "min_depth", "NUMERIC"),
( "len_Calls", "NUMERIC"),( "sum_Calls", "NUMERIC"),( "mean_Calls", "NUMERIC"),( "median_Calls", "NUMERIC"),
( "var_Calls", "NUMERIC"),( "max_Calls", "NUMERIC"),( "min_Calls", "NUMERIC")
        ]


    def stat(self,lst):
        counts= Counter(lst)
        return len(lst),sum(lst),numpy.mean(lst),numpy.median(lst),numpy.var(lst),max(lst),min(lst)

    def addFromDict(self,files_dict,dict):
        Att_dict = {}
        for f in files_dict.keys():
            Att_dict[f] = [0,0,0,0,0,0,0]
        for d in dict:
                if d in Att_dict and dict[d]!=[]:
                    Att_dict[d]=list(self.stat(dict[d]))
        for f in Att_dict:
            files_dict[f] = files_dict[f] + Att_dict[f]

    def get_features(self, c, files_dict, prev_date, start_date, end_date):
        sourceMethodsFiles='''select  name ,Lines ,	Statements ,	Percent_Branch_Statements ,Method_Call_Statements ,Percent_Lines_with_Comments
 ,Classes_and_interfaces ,Methods_per_Class ,
 Maximum_Complexity
   ,Average_Block_Depth	, Average_Complexity	,
 Statements_at_block_level_0 ,Statements_at_block_level_1 ,Statements_at_block_level_2 ,Statements_at_block_level_3 ,Statements_at_block_level_4 ,
 Statements_at_block_level_5 ,Statements_at_block_level_6 ,Statements_at_block_level_7   from JAVAfilesFix'''
        wekaMethods.articles.sqlToAttributes(["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"], c, files_dict, sourceMethodsFiles)
        sourceMethodsFiles='''
select  name  ,
 Statements_at_block_level_3 /(1.0*(case When Statements= 0 Then 1 Else Statements End)),Statements_at_block_level_4/(1.0*(case When Statements= 0 Then 1 Else Statements End)) ,
 Statements_at_block_level_5 /(1.0*(case When Statements= 0 Then 1 Else Statements End)),Statements_at_block_level_6 /(1.0*(case When Statements= 0 Then 1 Else Statements End)),Statements_at_block_level_7/(1.0*(case When Statements= 0 Then 1 Else Statements End))  from JAVAfilesFix'''
        wekaMethods.articles.sqlToAttributes(["0","0","0","0","0",], c, files_dict, sourceMethodsFiles)
        sourceMethodsFiles='''select  name ,
 max(Statements_at_block_level_0 ,Statements_at_block_level_1 ,Statements_at_block_level_2 ,Statements_at_block_level_3 ,Statements_at_block_level_4 ,
 Statements_at_block_level_5 ,Statements_at_block_level_6 ,Statements_at_block_level_7 ,Statements_at_block_level_8 ,Statements_at_block_level_9)  from JAVAfilesFix'''
        wekaMethods.articles.sqlToAttributes(["0"], c, files_dict, sourceMethodsFiles)
        sourceMethodsFiles='''select  name  ,
 max(Statements_at_block_level_0/(1.0*(case When Statements= 0 Then 1 Else Statements End)) ,Statements_at_block_level_1/(1.0*(case When Statements= 0 Then 1 Else Statements End)) ,Statements_at_block_level_2/(1.0*(case When Statements= 0 Then 1 Else Statements End)) ,Statements_at_block_level_3 /(1.0*(case When Statements= 0 Then 1 Else Statements End)),Statements_at_block_level_4/(1.0*(case When Statements= 0 Then 1 Else Statements End)) ,
 Statements_at_block_level_5 /(1.0*(case When Statements= 0 Then 1 Else Statements End)),Statements_at_block_level_6 /(1.0*(case When Statements= 0 Then 1 Else Statements End)),Statements_at_block_level_7/(1.0*(case When Statements= 0 Then 1 Else Statements End)) ,Statements_at_block_level_8/(1.0*(case When Statements= 0 Then 1 Else Statements End)) ,Statements_at_block_level_9/(1.0*(case When Statements= 0 Then 1 Else Statements End)) )  from JAVAfilesFix'''
        wekaMethods.articles.sqlToAttributes(["0"], c, files_dict, sourceMethodsFiles)
        complexity_d = dict(map(lambda f: (f, list()), files_dict.keys()))
        statements_d = dict(map(lambda f: (f, list()), files_dict.keys()))
        depth_d = dict(map(lambda f: (f, list()), files_dict.keys()))
        calls_d = dict(map(lambda f: (f, list()), files_dict.keys()))
        for row in c.execute('select File_Name, Complexity, Statements, Maximum_Depth, Calls from SourcemethodsFix'):
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


