__author__ = 'amir'

from weka.articles import *
#from weka.articles import sqlToAttributes
simple_features=[1,2,3,4,5,6,7,8,9,10,21,26,27,28,29,30,31,32,33,34,35,36,37]
simpleArticles_features=[1,2,3,4,5,6,7,8,9,10,21,26,27,28]
simpleAdded_features=[29,30,31,32,33,34,35,36,37]
last_features=[11,12,13,14,15,16,17,18,19,20,22,23,24,25]
bugs_features=[38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117,118]
class processFamilies:

    def __init__(self,fam):
        self.family=fam
        if self.family=="simpleProcessArticles":
            self.best=simpleArticles_features
        if self.family=="simpleProcessAdded":
            self.best=simpleAdded_features
        if self.family=="lastProcess":
            self.best=last_features
        if self.family=="bugs":
            self.best=bugs_features


    def get_attributes(self):
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
        for i in range(len(all)):
            if i+1 in self.best:
                ret.append(all[i])
        return ret


    def sqlToAttributes(self,basicAtt, c, files_dict, first):
        Att_dict = {}
        for f in files_dict.keys():
            Att_dict[f] = list(basicAtt)
        for row in c.execute(first):
            name = Agent.pathTopack.pathToPack(row[0])
            if (name in Att_dict):
                Att_dict[name] = list([x if x!=None else 0 for x in row[1:]])
        for f in Att_dict:
            files_dict[f] = files_dict[f] + Att_dict[f]

    def simple_get_features(self, c, files_dict,prev_date,start_date,end_date):
        first='select name, count(*),  sum(insertions),sum(deletions), Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End),(case When name not like "%test%" Then count(distinct bugId)-1 Else 0 End)  from commitedfiles where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by name'
        self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)
        disAuthors='select name,count(distinct author) from commitedfiles,commits where commits.ID=commitedfiles.commitid  and commits.commiter_date<="' + str(start_date)+ '"' + '  and commits.commiter_date<="' + str(end_date) + '" group by Commitedfiles.name'
        self.sqlToAttributes(["0"], c, files_dict, disAuthors)
        changeSet='select A.name,count(distinct B.name) from Commitedfiles as A, Commitedfiles as B where A.commitid=B.commitid and A.commiter_date<="' + str(start_date)+ '"' + '  and A.commiter_date<="' + str(end_date) + '" and B.commiter_date<="' + str(start_date)+ '"' + '  and B.commiter_date<="' + str(end_date) + '" group by A.name'
        self.sqlToAttributes(["0"], c, files_dict, changeSet)

        age='select name, sum( julianday(commiter_date)*insertions ) -sum( julianday(commiter_date)*deletions ) from Commitedfiles  where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) +'" group by name'
        self.sqlToAttributes(["0"], c, files_dict, age)

        age='select name, julianday("'+ str(start_date)+'")*(sum(insertions)-sum(deletions))-sum( julianday(commiter_date)*insertions ) -sum( julianday(commiter_date)*deletions ) from Commitedfiles  where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) +'" group by name'
        self.sqlToAttributes(["0"], c, files_dict, age)

        first='select name, count(*),  sum(insertions),sum(deletions),Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End) from commitedfiles where bugId<>0 and name not like "%test%" and commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by name'
        self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)


    def simpleArticles_get_features(self, c, files_dict,prev_date,start_date,end_date):
        first='select name, count(*),  sum(insertions),sum(deletions), Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End),(case When name not like "%test%" Then count(distinct bugId)-1 Else 0 End)  from commitedfiles where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by name'
        self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)
        disAuthors='select name,count(distinct author) from commitedfiles,commits where commits.ID=commitedfiles.commitid  and commits.commiter_date<="' + str(start_date)+ '"' + '  and commits.commiter_date<="' + str(end_date) + '" group by Commitedfiles.name'
        self.sqlToAttributes(["0"], c, files_dict, disAuthors)
        changeSet='select A.name,count(distinct B.name) from Commitedfiles as A, Commitedfiles as B where A.commitid=B.commitid and A.commiter_date<="' + str(start_date)+ '"' + '  and A.commiter_date<="' + str(end_date) + '" and B.commiter_date<="' + str(start_date)+ '"' + '  and B.commiter_date<="' + str(end_date) + '" group by A.name'
        self.sqlToAttributes(["0"], c, files_dict, changeSet)

        age='select name, sum( julianday(commiter_date)*insertions ) -sum( julianday(commiter_date)*deletions ) from Commitedfiles  where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) +'" group by name'
        self.sqlToAttributes(["0"], c, files_dict, age)

        age='select name, julianday("'+ str(start_date)+'")*(sum(insertions)-sum(deletions))-sum( julianday(commiter_date)*insertions ) -sum( julianday(commiter_date)*deletions ) from Commitedfiles  where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) +'" group by name'
        self.sqlToAttributes(["0"], c, files_dict, age)


    def simpleAdded_get_features(self, c, files_dict,prev_date,start_date,end_date):

        first='select name, count(*),  sum(insertions),sum(deletions),Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End) from commitedfiles where bugId<>0 and name not like "%test%" and commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by name'
        self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)



    def last_get_features(self,c, files_dict,prev_date,start_date,end_date):
        first_last='select name, count(*),  sum(insertions),sum(deletions),Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End),(case When name not like "%test%" Then count(distinct bugId)-1 Else 0 End)  from commitedfiles where commiter_date>="' + str(prev_date)+ '"' + '  and commiter_date<="' + str(start_date) + '" group by name'
        self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first_last)
        disAuthors_last='select name,count(distinct author) from commitedfiles,commits where commits.ID=commitedfiles.commitid  and commits.commiter_date>="' + str(prev_date)+ '"' + '  and commits.commiter_date<="' + str(start_date) + '" group by Commitedfiles.name'
        self.sqlToAttributes(["0"], c, files_dict, disAuthors_last)

        last_commit='select name,julianday("'+ str(start_date)+'")-julianday(max(commiter_date)) from commitedfiles  where commitedfiles.commiter_date<="' + str(start_date)+ '"' + '  and commitedfiles.commiter_date<="' + str(end_date) + '" group by Commitedfiles.name'
        self.sqlToAttributes(["0"], c, files_dict, last_commit)

        last_bug='select name,julianday("'+ str(start_date)+'")-julianday(max(commiter_date)) from commitedfiles  where bugId<>0 and name not like "%test%" and commitedfiles.commiter_date<="' + str(start_date)+ '"' + '  and commitedfiles.commiter_date<="' + str(end_date) + '" group by Commitedfiles.name'
        self.sqlToAttributes(["0"], c, files_dict, last_bug)

        last_ver_bug='select name,julianday("'+ str(start_date)+'")-julianday(max(commiter_date)) from commitedfiles  where bugId<>0 and name not like "%test%" and commitedfiles.commiter_date>="' + str(prev_date)+ '"' + '  and commitedfiles.commiter_date<="' + str(start_date) + '" group by Commitedfiles.name'
        self.sqlToAttributes(["0"], c, files_dict, last_ver_bug)

    def bugs_get_features(self, c, files_dict,prev_date,start_date,end_date):
        for p in ['"P3"']:
            first='select name, count(*),  sum(insertions),sum(deletions),Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" and bugs.Priority='+p+' and commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by name'
            self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)
        Priorities=['"P1"','"P2"','"P3"','"P4"','"P5"']
        ranks=[1.0,2.0,3.0,4.0,5.0]
        case="(case "
        for p, r in zip(Priorities,ranks):
            case=case+ " When Priority= "+p + " Then "+str(r)+"*metric "
        case=case+" Else 0.0 End)"
        first='select name, count('+case.replace('metric','1')+') ,  sum('+case.replace('metric','insertions')+') ,sum('+case.replace('metric','deletions')+') ,Sum(case When insertions > 0 Then '+case.replace('metric','1')+' Else 0 End) ,Sum(case When deletions > 0 Then '+case.replace('metric','1')+' Else 0 End) ,  avg('+case.replace('metric','insertions')+') ,avg('+case.replace('metric','deletions')+') , avg(case When insertions > 0 Then '+case.replace('metric','insertions')+' Else Null End) ,avg(case When deletions > 0 Then '+case.replace('metric','deletions')+' Else Null End) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%"  and commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by name'
        print first
        self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)

        for p in ['"normal"','"enhancement"','"major"']:
            first='select name, count(*),  sum(insertions),sum(deletions),Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" and bugs.Severity='+p+' and commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by name'
            self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)

        first='select name,avg((julianday(commitedfiles.commiter_date)-julianday(bugs.Submit_Date))) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,avg((julianday(commitedfiles.commiter_date)-julianday(bugs.Last_Modified))) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)

        first='select name,count(distinct OS) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,count(Distinct Assigned_To) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%"  group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,count(Distinct Hardware) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%"  group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,count(Distinct Component) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,count(Distinct Version) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,count(case When Blocks <> \'\' Then Blocks Else Null End) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,count(case When Depends_On <> \'\' Then Depends_On Else Null End) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)

        first='select name,Sum(case When Priority= "P1" Then 1 Else 0 End),Sum(case When Priority= "P2" Then 1 Else 0 End),Sum(case When Priority= "P3" Then 1 Else 0 End),Sum(case When Priority= "P4" Then 1 Else 0 End),Sum(case When Priority= "P5" Then 1 Else 0 End) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'
        self.sqlToAttributes(["0","0","0","0","0"], c, files_dict, first)
        first='select name,Sum(case When Priority= "P1" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Priority= "P2" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Priority= "P3" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Priority= "P4" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Priority= "P5" Then 1 Else 0 End)/(1.0*count(*)) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'
        self.sqlToAttributes(["0","0","0","0","0"], c, files_dict, first)
        first='select name,Sum(case When Severity= "minor" Then 1 Else 0 End),Sum(case When Severity= "normal" Then 1 Else 0 End),Sum(case When Severity= "major" Then 1 Else 0 End),Sum(case When Severity= "enhancement" Then 1 Else 0 End),Sum(case When Severity= "critical" Then 1 Else 0 End),Sum(case When Severity= "blocker" Then 1 Else 0 End),Sum(case When Severity= "trivial" Then 1 Else 0 End) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'
        self.sqlToAttributes(["0","0","0","0","0","0","0"], c, files_dict, first)
        first='select name,Sum(case When Severity= "minor" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Severity= "normal" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Severity= "major" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Severity= "enhancement" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Severity= "critical" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Severity= "blocker" Then 1 Else 0 End)/(1.0*count(*)),Sum(case When Severity= "trivial" Then 1 Else 0 End)/(1.0*count(*)) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'
        self.sqlToAttributes(["0","0","0","0","0","0","0"], c, files_dict, first)
        first='select name,avg(comms.files) from commitedfiles,(select commits.Id as Id,count(name) as files from commits,Commitedfiles where commits.Id=Commitedfiles.commitid group by commits.Id) as comms where commitedfiles.commitId=comms.id group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,avg(comms.files) from commitedfiles,(select commits.Id as Id,count(name) as files from commits,Commitedfiles where commits.Id=Commitedfiles.commitid group by commits.Id) as comms where commitedfiles.commitId=comms.id  and commitedfiles.bugId<>0 and name not like "%test%" group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,avg(comms.files) from commitedfiles,(select commits.Id as Id,count(name) as files from commits,Commitedfiles where commits.Id=Commitedfiles.commitid group by commits.Id) as comms where commitedfiles.commitId=comms.id  and commitedfiles.bugId=0 and name not like "%test%" group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)


    def get_features(self, c, files_dict,prev_date,start_date,end_date):
        ',  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End)'
        'case When and name not like "%test%" Then count(distinct bugId)-1 Else 0'
        if self.family=="simpleProcess":
            self.simple_get_features(c, files_dict,prev_date,start_date,end_date)
        if self.family=="simpleProcessArticles":
            self.simpleArticles_get_features(c, files_dict,prev_date,start_date,end_date)
        if self.family=="simpleProcessAdded":
            self.simpleAdded_get_features(c, files_dict,prev_date,start_date,end_date)

        if self.family=="lastProcess":
            self.last_get_features(c, files_dict,prev_date,start_date,end_date)
        if self.family=="bugs":
            self.bugs_get_features(c, files_dict,prev_date,start_date,end_date)








