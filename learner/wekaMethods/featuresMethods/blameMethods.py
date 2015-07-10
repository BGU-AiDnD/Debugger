__author__ = 'amir'

from wekaMethods.articles import *
#from wekaMethods.articles import sqlToAttributes
best_features=[1,3,5,6,7,8,12,14,15,17,21,22,23,27,32,34,36,37,43,44,45,47,49,50,52,56,57,58,62,64,67,69,71,72,78,88]

class blameMethods:
    def get_attributesOld(self):
        return [("diff_commits" , "NUMERIC") ,("diff_commits_lastver" , "NUMERIC") ,("groups" , "NUMERIC") ,("committers" , "NUMERIC") ,
    ("avg_date" , "NUMERIC") ,("median_date" , "NUMERIC" ) ,("max_date" , "NUMERIC") ,("numBlobs" , "NUMERIC") ,("numPatchs" , "NUMERIC") ,("numCommits" , "NUMERIC" )
    ]

    def get_featuresOld(self, c, files_dict,prev_date,start_date,end_date):
        blame='select name ,diff_commits  ,diff_commits_lastver  ,groups   ,committers  ,julianday("'+ str(start_date)+'")-julianday(avg_date)  ,julianday("'+ str(start_date)+'")-julianday(median_date)   ,julianday("'+ str(start_date)+'")-julianday(max_date)  ,numBlobs  , numPatchs  ,numCommits    from blame group by name'
        sqlToAttributes(["0","0","0","0","0","0","0","0","0","0"], c, files_dict, blame)

    def get_attributes(self):
        all= [("diff_commits" ,"NUMERIC") ,("diff_commits_lastver" ,"NUMERIC") ,("diff_commitsApproved" ,"NUMERIC") ,("diff_commits_lastverApproved" ,"NUMERIC") ,("numBlobs" ,"NUMERIC") ,("numPatchs" ,"NUMERIC") ,("numCommits" ,"NUMERIC") ,
("len_times" ,"NUMERIC") ,("mean_times" ,"NUMERIC") ,("median_times" ,"NUMERIC") ,("var_times" ,"NUMERIC") ,("max_times" ,"NUMERIC") ,("min_times" ,"NUMERIC") ,("p01_times" ,"NUMERIC") ,("p02_times" ,"NUMERIC") ,("p05_times" ,"NUMERIC") ,("mx1_times" ,"NUMERIC") ,("max_min_times" ,"NUMERIC") ,
("ones_times" ,"NUMERIC") ,("twos_times" ,"NUMERIC") ,("less5_times" ,"NUMERIC") ,("less10_times" ,"NUMERIC") ,
("len_difftimes" ,"NUMERIC") ,("mean_difftimes" ,"NUMERIC") ,("median_difftimes" ,"NUMERIC") ,("var_difftimes" ,"NUMERIC") ,("max_difftimes" ,"NUMERIC") ,("min_difftimes" ,"NUMERIC") ,("p01_difftimes" ,"NUMERIC") ,("p02_difftimes" ,"NUMERIC") ,("p05_difftimes" ,"NUMERIC") ,("mx1_difftimes" ,"NUMERIC") ,("max_min_difftimes" ,"NUMERIC") ,
("ones_difftimes" ,"NUMERIC") ,("twos_difftimes" ,"NUMERIC") ,("less5_difftimes" ,"NUMERIC") ,("less10_difftimes" ,"NUMERIC") ,
("len_committers" ,"NUMERIC") ,("p01_committers" ,"NUMERIC") ,("p02_committers" ,"NUMERIC") ,("p05_committers" ,"NUMERIC") ,("mx1_committers" ,"NUMERIC") ,
("len_timesApproved" ,"NUMERIC") ,("mean_timesApproved" ,"NUMERIC") ,("median_timesApproved" ,"NUMERIC") ,("var_timesApproved" ,"NUMERIC") ,("max_timesApproved" ,"NUMERIC") ,("min_timesApproved" ,"NUMERIC") ,("p01_timesApproved" ,"NUMERIC") ,("p02_timesApproved" ,"NUMERIC") ,("p05_timesApproved" ,"NUMERIC") ,("mx1_timesApproved" ,"NUMERIC") ,("max_min_timesApproved" ,"NUMERIC") ,
("ones_timesApproved" ,"NUMERIC") ,("twos_timesApproved" ,"NUMERIC") ,("less5_timesApproved" ,"NUMERIC") ,("less10_timesApproved" ,"NUMERIC") ,
("len_difftimesApproved" ,"NUMERIC") ,("mean_difftimesApproved" ,"NUMERIC") ,("median_difftimesApproved" ,"NUMERIC") ,("var_difftimesApproved" ,"NUMERIC") ,("max_difftimesApproved" ,"NUMERIC") ,("min_difftimesApproved" ,"NUMERIC") ,("p01_difftimesApproved" ,"NUMERIC") ,("p02_difftimesApproved" ,"NUMERIC") ,("p05_difftimesApproved" ,"NUMERIC") ,("mx1__difftimesApproved" ,"NUMERIC") ,("max_min_difftimesApproved" ,"NUMERIC") ,
("ones_difftimesApproved" ,"NUMERIC") ,("twos_difftimesApproved" ,"NUMERIC") ,("less5_difftimesApproved" ,"NUMERIC") ,("less10_difftimesApproved" ,"NUMERIC") ,
("len_committersApproved" ,"NUMERIC") ,("p01_committersApproved" ,"NUMERIC") ,("p02_committersApproved" ,"NUMERIC") ,("p05_committersApproved" ,"NUMERIC") ,("mx1_committersApproved" ,"NUMERIC") ,
("len_groups" ,"NUMERIC") ,("mean_groups" ,"NUMERIC") ,("median_groups" ,"NUMERIC") ,("var_groups" ,"NUMERIC") ,("max_groups" ,"NUMERIC") ,("min_groups" ,"NUMERIC") ,("p01_groups" ,"NUMERIC") ,("p02_groups" ,"NUMERIC") ,("p05_groups" ,"NUMERIC") ,("mx1_groups" ,"NUMERIC") ,
("len_groupsApproved" ,"NUMERIC") ,("mean_groupsApproved" ,"NUMERIC") ,("median_groupsApproved" ,"NUMERIC") ,("var_groupsApproved" ,"NUMERIC") ,("max_groupsApproved" ,"NUMERIC") ,("min_groupsApproved" ,"NUMERIC") ,("p01_groupsApproved" ,"NUMERIC") ,("p02_groupsApproved" ,"NUMERIC") ,("p05_groupsApproved" ,"NUMERIC") ,("mx1_groupsApproved",  "NUMERIC")
    ]
        ret=[]
        for i in range(len(all)):
            if i+1 in best_features:
                ret.append(all[i])
        return ret



    def get_features(self, c, files_dict,prev_date,start_date,end_date):
        blame='''select name ,diff_commits ,diff_commits_lastver ,diff_commitsApproved ,diff_commits_lastverApproved ,numBlobs , numPatchs ,numCommits ,
len_times ,julianday("'''+ str(start_date)+'''")-julianday(mean_times) ,julianday("'''+ str(start_date)+'''")-julianday(median_times) ,var_times ,julianday("'''+ str(start_date)+'''")-julianday(max_times) ,julianday("'''+ str(start_date)+'''")-julianday(min_times) ,p01_times  ,p02_times  ,p05_times  ,mx1_times  , max_min_times ,
ones_times , twos_times ,less5_times ,less10_times ,
len_difftimes ,julianday("'''+ str(start_date)+'''")-julianday(mean_difftimes) ,julianday("'''+ str(start_date)+'''")-julianday(median_difftimes) ,var_difftimes ,julianday("'''+ str(start_date)+'''")-julianday(max_difftimes) ,julianday("'''+ str(start_date)+'''")-julianday(min_difftimes) ,p01_difftimes ,p02_difftimes ,p05_difftimes ,mx1_difftimes  , max_min_difftimes ,
ones_difftimes , twos_difftimes ,less5_difftimes ,less10_difftimes ,
len_committers ,p01_committers  ,p02_committers  ,p05_committers  ,mx1_committers  ,
len_timesApproved ,julianday("'''+ str(start_date)+'''")-julianday(mean_timesApproved) ,julianday("'''+ str(start_date)+'''")-julianday(median_timesApproved) ,var_timesApproved ,julianday("'''+ str(start_date)+'''")-julianday(max_timesApproved) ,julianday("'''+ str(start_date)+'''")-julianday(min_timesApproved) ,p01_timesApproved  ,p02_timesApproved  ,p05_timesApproved  ,mx1_timesApproved  , max_min_timesApproved ,
ones_timesApproved , twos_timesApproved ,less5_timesApproved ,less10_timesApproved ,
len_difftimesApproved ,julianday("'''+ str(start_date)+'''")-julianday(mean_difftimesApproved) ,julianday("'''+ str(start_date)+'''")-julianday(median_difftimesApproved) ,var_difftimesApproved ,julianday("'''+ str(start_date)+'''")-julianday(max_difftimesApproved) ,julianday("'''+ str(start_date)+'''")-julianday(min_difftimesApproved) ,p01_difftimesApproved ,p02_difftimesApproved ,p05_difftimesApproved ,mx1__difftimesApproved  , max_min_difftimesApproved ,
ones_difftimesApproved , twos_difftimesApproved ,less5_difftimesApproved ,less10_difftimesApproved ,
len_committersApproved ,p01_committersApproved  ,p02_committersApproved  ,p05_committersApproved  ,mx1_committersApproved  ,
len_groups ,mean_groups ,median_groups ,var_groups ,max_groups ,min_groups ,p01_groups  ,p02_groups  ,p05_groups  ,mx1_groups  ,
len_groupsApproved ,mean_groupsApproved ,median_groupsApproved ,var_groupsApproved ,max_groupsApproved ,min_groupsApproved ,p01_groupsApproved  ,p02_groupsApproved  ,p05_groupsApproved  ,mx1_groupsApproved   from blameExtends group by name'''
        sqlToAttributesBest(["0" for x in best_features], c, files_dict, blame,best_features)

