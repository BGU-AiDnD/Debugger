__author__ = 'amir'

from wekaMethods.articles import *
import wekaMethods.articles
import featureExtractorBase

simple_features=[1,2,3,4,5,6,7,8,9,10,21,26,27,28,29,30,31,32,33,34,35,36,37]
simpleArticles_features=[1,2,3,4,5,6,7,8,9,10,21,26,27,28]
simpleAdded_features=[29,30,31,32,33,34,35,36,37]
last_features=[11,12,13,14,15,16,17,18,19,20,22,23,24,25]
bugs_features=[38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117,118]
class processMethodsFamilies(featureExtractorBase.FeatureExtractorBase):

    def __init__(self,fam):
        self.family=fam
        if self.family=="simpleProcessArticlesMethods":
            self.best=simpleArticles_features
        if self.family=="simpleProcessAddedMethods":
            self.best=simpleAdded_features
        if self.family=="lastProcessMethods":
            self.best=last_features
        if self.family=="bugsMethods":
            self.best=bugs_features


    def get_attributes(self):
        all= [( "tot_changes_Methods", "NUMERIC"), ( "sum_insert_Methods", "NUMERIC"),
                ( "sum_delets_Methods", "NUMERIC"),( "count_insert_Methods", "NUMERIC"),
                ( "count_delets_Methods", "NUMERIC"),( "avg_insert_Methods", "NUMERIC"),
                ( "avg_delets_Methods", "NUMERIC"),( "avg_insert_nonzero_Methods", "NUMERIC"),
                ( "avg_delets_nonzero_Methods", "NUMERIC"), ( "tot_bugs_Methods", "NUMERIC"),( "tot_changes_last_Methods", "NUMERIC"), ( "sum_insert_last_Methods", "NUMERIC"),
                ( "sum_delet_lasts_Methods", "NUMERIC"),( "count_insert_last_Methods", "NUMERIC"),
                ( "count_delets_last_Methods", "NUMERIC"),( "avg_insert_last_Methods", "NUMERIC"),
                ( "avg_delets_last_Methods", "NUMERIC"),( "avg_insert_nonzero_last_Methods", "NUMERIC"),
                ( "avg_delets_nonzero_last_Methods", "NUMERIC"), ( "tot_bugs_last_Methods", "NUMERIC"), ( "tot_developers_Methods", "NUMERIC"),
                  ( "lastVer_tot_developers_Methods", "NUMERIC"),( "last_commit_Methods", "NUMERIC"),( "last_bug_Methods", "NUMERIC"),( "last_bug_binary_Methods", "NUMERIC"),
                ( "change_set_Methods", "NUMERIC"), ( "age_Methods", "NUMERIC"),( "age2_Methods", "NUMERIC"),( "tot_changes_bugged_Methods", "NUMERIC"), ( "sum_insert_bugged_Methods", "NUMERIC"),
                ( "sum_delet_buggeds_Methods", "NUMERIC"),( "count_insert_bugged_Methods", "NUMERIC"),
                ( "count_delets_bugged_Methods", "NUMERIC"),( "avg_insert_bugged_Methods", "NUMERIC"),
                ( "avg_delets_bugged_Methods", "NUMERIC"),( "avg_insert_nonzero_bugged_Methods", "NUMERIC"),
                ( "avg_delets_nonzero_bugged_Methods", "NUMERIC"),

                ( "tot_changes_p3_Methods", "NUMERIC"), ( "sum_insert_p3_Methods", "NUMERIC"),
				( "sum_delet_p3s_Methods", "NUMERIC"),( "count_insert_p3_Methods", "NUMERIC"),
				( "count_delets_p3_Methods", "NUMERIC"),( "avg_insert_p3_Methods", "NUMERIC"),
				( "avg_delets_p3_Methods", "NUMERIC"),( "avg_insert_nonzero_p3_Methods", "NUMERIC"),
				( "avg_delets_nonzero_p3_Methods", "NUMERIC"),

                                ( "tot_changes_normal_Methods", "NUMERIC"), ( "sum_insert_normal_Methods", "NUMERIC"),
				( "sum_delet_normals_Methods", "NUMERIC"),( "count_insert_normal_Methods", "NUMERIC"),
				( "count_delets_normal_Methods", "NUMERIC"),( "avg_insert_normal_Methods", "NUMERIC"),
				( "avg_delets_normal_Methods", "NUMERIC"),( "avg_insert_nonzero_normal_Methods", "NUMERIC"),
				( "avg_delets_nonzero_normal_Methods", "NUMERIC"),

                                ( "tot_changes_enhancement_Methods", "NUMERIC"), ( "sum_insert_enhancement_Methods", "NUMERIC"),
				( "sum_delet_enhancements_Methods", "NUMERIC"),( "count_insert_enhancement_Methods", "NUMERIC"),
				( "count_delets_enhancement_Methods", "NUMERIC"),( "avg_insert_enhancement_Methods", "NUMERIC"),
				( "avg_delets_enhancement_Methods", "NUMERIC"),( "avg_insert_nonzero_enhancement_Methods", "NUMERIC"),
				( "avg_delets_nonzero_enhancement_Methods", "NUMERIC"),

                ( "tot_changes_major_Methods", "NUMERIC"), ( "sum_insert_major_Methods", "NUMERIC"),
				( "sum_delet_majors_Methods", "NUMERIC"),( "count_insert_major_Methods", "NUMERIC"),
				( "count_delets_major_Methods", "NUMERIC"),( "avg_insert_major_Methods", "NUMERIC"),
				( "avg_delets_major_Methods", "NUMERIC"),( "avg_insert_nonzero_major_Methods", "NUMERIC"),
				( "avg_delets_nonzero_major_Methods", "NUMERIC"),
                ( "tot_changes_Ranking_Methods", "NUMERIC"), ( "sum_insert_Ranking_Methods", "NUMERIC"),
				( "sum_delet_Rankings_Methods", "NUMERIC"),( "count_insert_Ranking_Methods", "NUMERIC"),
				( "count_delets_Ranking_Methods", "NUMERIC"),( "avg_insert_Ranking_Methods", "NUMERIC"),
				( "avg_delets_Ranking_Methods", "NUMERIC"),( "avg_insert_nonzero_Ranking_Methods", "NUMERIC"),
				( "avg_delets_nonzero_Ranking_Methods", "NUMERIC"),


                ( "avg_submit_Methods", "NUMERIC"),
                ( "avg_modify_Methods", "NUMERIC"),
                ( "distinct_OS_Methods", "NUMERIC"),
                ( "distinct_assignedTo_Methods", "NUMERIC"),
                ( "distinct_Hardware_Methods", "NUMERIC"),
                ( "distinct_Component_Methods", "NUMERIC"),
                ( "distinct_Version_Methods", "NUMERIC"),
                ( "count_Block_Methods", "NUMERIC"),
                ( "count_Depends_Methods", "NUMERIC"),

                 ( "p1_count_Methods", "NUMERIC"), ( "p2_count_Methods", "NUMERIC"), ( "p3_count_Methods", "NUMERIC"), ( "p4_count_Methods", "NUMERIC"), ( "p5_count_Methods", "NUMERIC") ,
                  ( "p1_count_perc_Methods", "NUMERIC"), ( "p2_count_perc_Methods", "NUMERIC"), ( "p3_count_perc_Methods", "NUMERIC"), ( "p4_count_perc_Methods", "NUMERIC"), ( "p5_count_perc_Methods", "NUMERIC") ,

                ( "minor_count_Methods", "NUMERIC"), ( "normal_count_Methods", "NUMERIC"), ( "major_count_Methods", "NUMERIC"), ( "enhancement_count_Methods", "NUMERIC"), ( "critical_count_Methods", "NUMERIC"), ( "blocker_count_Methods", "NUMERIC"), ( "trivial_count_Methods", "NUMERIC"),
                ( "minor_count_perc_Methods", "NUMERIC"), ( "normal_count_perc_Methods", "NUMERIC"), ( "major_count_perc_Methods", "NUMERIC"), ( "enhancement_count_perc_Methods", "NUMERIC"), ( "critical_count_perc_Methods", "NUMERIC"), ( "blocker_count_perc_Methods", "NUMERIC"), ( "trivial_count_perc_Methods", "NUMERIC"),

                ( "avg_commits_files_Methods", "NUMERIC"),
                ( "avg_commits_files_bugged_Methods", "NUMERIC"),
                ( "avg_commits_files_valid_Methods", "NUMERIC")
        ]
        ret=[]
        for i in range(len(all)):
            if i+1 in self.best:
                ret.append(all[i])
        return ret


    def sqlToAttributes(self,basicAtt, c, files_dict, first):
        Att_dict = {}
        for f in files_dict.keys():
            Att_dict[f] = list(basicAtt)
        for row in c.execute(first):
            methodDir = row[0]
            if (methodDir in Att_dict):
                Att_dict[methodDir] = list([x if x!=None else 0 for x in row[1:]])
        for f in Att_dict:
            files_dict[f] = files_dict[f] + Att_dict[f]

    def simple_get_features(self, c, files_dict,prev_date,start_date,end_date):
        first='select methodDir, count(*),  sum(insertions),sum(deletions), Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End),(case When methodDir not like "%test%" Then count(distinct bugId)-1 Else 0 End)  from commitedMethods where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by methodDir'
        self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)
        disAuthors='select methodDir,count(distinct author) from commitedMethods,commits where commits.ID=commitedMethods.commitid  and commits.commiter_date<="' + str(start_date)+ '"' + '  and commits.commiter_date<="' + str(end_date) + '" group by commitedMethods.methodDir'
        self.sqlToAttributes(["0"], c, files_dict, disAuthors)
        changeSet='select A.methodDir,count(distinct B.methodDir) from commitedMethods as A, commitedMethods as B where A.commitid=B.commitid and A.commiter_date<="' + str(start_date)+ '"' + '  and A.commiter_date<="' + str(end_date) + '" and B.commiter_date<="' + str(start_date)+ '"' + '  and B.commiter_date<="' + str(end_date) + '" group by A.methodDir'
        self.sqlToAttributes(["0"], c, files_dict, changeSet)

        age='select methodDir, sum( julianday(commiter_date)*insertions ) -sum( julianday(commiter_date)*deletions ) from commitedMethods  where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) +'" group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, age)

        age='select methodDir, julianday("'+ str(start_date)+'")*(sum(insertions)-sum(deletions))-sum( julianday(commiter_date)*insertions ) -sum( julianday(commiter_date)*deletions ) from commitedMethods  where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) +'" group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, age)

        first='select methodDir, count(*),  sum(insertions),sum(deletions),Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End) from commitedMethods where bugId<>0 and methodDir not like "%test%" and commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by methodDir'
        self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)


    def simpleArticles_get_features(self, c, files_dict,prev_date,start_date,end_date):
        first='select methodDir, count(*),  sum(insertions),sum(deletions), Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End),(case When methodDir not like "%test%" Then count(distinct bugId)-1 Else 0 End)  from commitedMethods where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by methodDir'
        self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)
        disAuthors='select methodDir,count(distinct author) from commitedMethods,commits where commits.ID=commitedMethods.commitid  and commits.commiter_date<="' + str(start_date)+ '"' + '  and commits.commiter_date<="' + str(end_date) + '" group by commitedMethods.methodDir'
        self.sqlToAttributes(["0"], c, files_dict, disAuthors)
        changeSet='select A.methodDir,count(distinct B.methodDir) from commitedMethods as A, commitedMethods as B where A.commitid=B.commitid and A.commiter_date<="' + str(start_date)+ '"' + '  and A.commiter_date<="' + str(end_date) + '" and B.commiter_date<="' + str(start_date)+ '"' + '  and B.commiter_date<="' + str(end_date) + '" group by A.methodDir'
        self.sqlToAttributes(["0"], c, files_dict, changeSet)

        age='select methodDir, sum( julianday(commiter_date)*insertions ) -sum( julianday(commiter_date)*deletions ) from commitedMethods  where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) +'" group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, age)

        age='select methodDir, julianday("'+ str(start_date)+'")*(sum(insertions)-sum(deletions))-sum( julianday(commiter_date)*insertions ) -sum( julianday(commiter_date)*deletions ) from commitedMethods  where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) +'" group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, age)


    def simpleAdded_get_features(self, c, files_dict,prev_date,start_date,end_date):

        first='select methodDir, count(*),  sum(insertions),sum(deletions),Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End) from commitedMethods where bugId<>0 and methodDir not like "%test%" and commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by methodDir'
        self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)



    def last_get_features(self,c, files_dict,prev_date,start_date,end_date):
        first_last='select methodDir, count(*),  sum(insertions),sum(deletions),Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End),(case When methodDir not like "%test%" Then count(distinct bugId)-1 Else 0 End)  from commitedMethods where commiter_date>="' + str(prev_date)+ '"' + '  and commiter_date<="' + str(start_date) + '" group by methodDir'
        self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first_last)
        disAuthors_last='select methodDir,count(distinct author) from commitedMethods,commits where commits.ID=commitedMethods.commitid  and commits.commiter_date>="' + str(prev_date)+ '"' + '  and commits.commiter_date<="' + str(start_date) + '" group by commitedMethods.methodDir'
        self.sqlToAttributes(["0"], c, files_dict, disAuthors_last)

        last_commit='select methodDir,julianday("'+ str(start_date)+'")-julianday(max(commiter_date)) from commitedMethods  where commitedMethods.commiter_date<="' + str(start_date)+ '"' + '  and commitedMethods.commiter_date<="' + str(end_date) + '" group by commitedMethods.methodDir'
        self.sqlToAttributes(["0"], c, files_dict, last_commit)

        last_bug='select methodDir,julianday("'+ str(start_date)+'")-julianday(max(commiter_date)) from commitedMethods  where bugId<>0 and methodDir not like "%test%" and commitedMethods.commiter_date<="' + str(start_date)+ '"' + '  and commitedMethods.commiter_date<="' + str(end_date) + '" group by commitedMethods.methodDir'
        self.sqlToAttributes(["0"], c, files_dict, last_bug)

        last_ver_bug='select methodDir,julianday("'+ str(start_date)+'")-julianday(max(commiter_date)) from commitedMethods  where bugId<>0 and methodDir not like "%test%" and commitedMethods.commiter_date>="' + str(prev_date)+ '"' + '  and commitedMethods.commiter_date<="' + str(start_date) + '" group by commitedMethods.methodDir'
        self.sqlToAttributes(["0"], c, files_dict, last_ver_bug)

    def bugs_get_features(self, c, files_dict,prev_date,start_date,end_date):
        for p in ['"P3"']:
            first='select methodDir, count(*),  sum(insertions),sum(deletions),Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%" and bugs.Priority='+p+' and commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by methodDir'
            self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)
        Priorities=['"P1"','"P2"','"P3"','"P4"','"P5"']
        ranks=[1.0,2.0,3.0,4.0,5.0]
        case="(case "
        for p, r in zip(Priorities,ranks):
            case=case+ " When Priority= "+p + " Then "+str(r)+"*metric "
        case=case+" Else 0.0 End)"
        first='select methodDir, count('+case.replace('metric','1')+') ,  sum('+case.replace('metric','insertions')+') ,sum('+case.replace('metric','deletions')+') ,Sum(case When insertions > 0 Then '+case.replace('metric','1')+' Else 0 End) ,Sum(case When deletions > 0 Then '+case.replace('metric','1')+' Else 0 End) ,  avg('+case.replace('metric','insertions')+') ,avg('+case.replace('metric','deletions')+') , avg(case When insertions > 0 Then '+case.replace('metric','insertions')+' Else Null End) ,avg(case When deletions > 0 Then '+case.replace('metric','deletions')+' Else Null End) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%"  and commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by methodDir'
        print first
        self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)

        for p in ['"normal"','"enhancement"','"major"']:
            first='select methodDir, count(*),  sum(insertions),sum(deletions),Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%" and bugs.Severity='+p+' and commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by methodDir'
            self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)

        first='select methodDir,avg((julianday(commitedMethods.commiter_date)-julianday(bugs.Submit_Date))) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%" group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select methodDir,avg((julianday(commitedMethods.commiter_date)-julianday(bugs.Last_Modified))) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%" group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, first)

        first='select methodDir,count(distinct OS) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%" group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select methodDir,count(Distinct Assigned_To) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%"  group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select methodDir,count(Distinct Hardware) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%"  group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select methodDir,count(Distinct Component) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%" group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select methodDir,count(Distinct Version) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%" group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select methodDir,count(case When Blocks <> \'\' Then Blocks Else Null End) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%" group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select methodDir,count(case When Depends_On <> \'\' Then Depends_On Else Null End) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%" group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, first)

        first='select methodDir,Sum(case When Priority= "P1" Then 1 Else 0 End),Sum(case When Priority= "P2" Then 1 Else 0 End),Sum(case When Priority= "P3" Then 1 Else 0 End),Sum(case When Priority= "P4" Then 1 Else 0 End),Sum(case When Priority= "P5" Then 1 Else 0 End) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%" group by methodDir'
        self.sqlToAttributes(["0","0","0","0","0"], c, files_dict, first)
        first='select methodDir,Sum(case When Priority= "P1" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Priority= "P2" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Priority= "P3" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Priority= "P4" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Priority= "P5" Then 1 Else 0 End)/(1.0*count(*)) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%" group by methodDir'
        self.sqlToAttributes(["0","0","0","0","0"], c, files_dict, first)
        first='select methodDir,Sum(case When Severity= "minor" Then 1 Else 0 End),Sum(case When Severity= "normal" Then 1 Else 0 End),Sum(case When Severity= "major" Then 1 Else 0 End),Sum(case When Severity= "enhancement" Then 1 Else 0 End),Sum(case When Severity= "critical" Then 1 Else 0 End),Sum(case When Severity= "blocker" Then 1 Else 0 End),Sum(case When Severity= "trivial" Then 1 Else 0 End) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%" group by methodDir'
        self.sqlToAttributes(["0","0","0","0","0","0","0"], c, files_dict, first)
        first='select methodDir,Sum(case When Severity= "minor" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Severity= "normal" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Severity= "major" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Severity= "enhancement" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Severity= "critical" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Severity= "blocker" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Severity= "trivial" Then 1 Else 0 End)/(1.0*count(*)) from commitedMethods,bugs where commitedMethods.bugId=bugs.id and methodDir not like "%test%" group by methodDir'
        self.sqlToAttributes(["0","0","0","0","0","0","0"], c, files_dict, first)
        first='select methodDir,avg(files) from commitedMethods,commits where commitedMethods.commitId=commits.id group by methodDir'
        first='select methodDir,avg(comms.files) from commitedMethods,(select commits.Id as Id,count(methodDir) as files from commits,commitedMethods where commits.Id=commitedMethods.commitid group by commits.Id) as comms where commitedMethods.commitId=comms.id group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select methodDir,avg(comms.files) from commitedMethods,(select commits.Id as Id,count(methodDir) as files from commits,commitedMethods where commits.Id=commitedMethods.commitid group by commits.Id) as comms where commitedMethods.commitId=comms.id and commitedMethods.bugId<>0 and methodDir not like "%test%" group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select methodDir,avg(comms.files) from commitedMethods,(select commits.Id as Id,count(methodDir) as files from commits,commitedMethods where commits.Id=commitedMethods.commitid group by commits.Id) as comms where commitedMethods.commitId=comms.id and commitedMethods.bugId=0 and methodDir not like "%test%" group by methodDir'
        self.sqlToAttributes(["0"], c, files_dict, first)


    def get_features(self, c, files_dict,prev_date,start_date,end_date):
        ',  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End)'
        'case When and methodDir not like "%test%" Then count(distinct bugId)-1 Else 0'
        if self.family=="simpleProcessMethods":
            self.simple_get_features(c, files_dict,prev_date,start_date,end_date)
        if self.family=="simpleProcessArticlesMethods":
            self.simpleArticles_get_features(c, files_dict,prev_date,start_date,end_date)
        if self.family=="simpleProcessAddedMethods":
            self.simpleAdded_get_features(c, files_dict,prev_date,start_date,end_date)

        if self.family=="lastProcessMethods":
            self.last_get_features(c, files_dict,prev_date,start_date,end_date)
        if self.family=="bugsMethods":
            self.bugs_get_features(c, files_dict,prev_date,start_date,end_date)








