__author__ = 'amir'

from weka.articles import *
#from weka.articles import sqlToAttributes

class processMethods:
    def get_attributes(self):
        return [( "tot_changes", "NUMERIC"), ( "sum_insert", "NUMERIC"),
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
                ( "avg_delets_nonzero_bugged", "NUMERIC"),( "tot_changes_p3", "NUMERIC"), ( "sum_insert_p3", "NUMERIC"),
				( "sum_delet_p3s", "NUMERIC"),( "count_insert_p3", "NUMERIC"),
				( "count_delets_p3", "NUMERIC"),( "avg_insert_p3", "NUMERIC"),
				( "avg_delets_p3", "NUMERIC"),( "avg_insert_nonzero_p3", "NUMERIC"),
				( "avg_delets_nonzero_p3", "NUMERIC"),
                ( "avg_submit", "NUMERIC"),
                ( "avg_modify", "NUMERIC"),
                ( "distinct_OS", "NUMERIC"),
                ( "distinct_assignedTo", "NUMERIC"),
                ( "distinct_Component", "NUMERIC"),
                ( "avg_commits_files", "NUMERIC"),
                ( "avg_commits_files_bugged", "NUMERIC"),
                ( "avg_commits_files_valid", "NUMERIC")
        ]

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


    def get_features(self, c, files_dict,prev_date,start_date,end_date):
        ',  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End)'
        'case When and name not like "%test%" Then count(distinct bugId)-1 Else 0'
        first='select name, count(*),  sum(insertions),sum(deletions), Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End),(case When name not like "%test%" Then count(distinct bugId)-1 Else 0 End)  from commitedfiles where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by name'
        self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)

        first_last='select name, count(*),  sum(insertions),sum(deletions),Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End),(case When name not like "%test%" Then count(distinct bugId)-1 Else 0 End)  from commitedfiles where commiter_date>="' + str(prev_date)+ '"' + '  and commiter_date<="' + str(start_date) + '" group by name'
        self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first_last)

        disAuthors='select name,count(distinct author) from commitedfiles,commits where commits.ID=commitedfiles.commitid  and commits.commiter_date<="' + str(start_date)+ '"' + '  and commits.commiter_date<="' + str(end_date) + '" group by Commitedfiles.name'
        self.sqlToAttributes(["0"], c, files_dict, disAuthors)

        disAuthors_last='select name,count(distinct author) from commitedfiles,commits where commits.ID=commitedfiles.commitid  and commits.commiter_date>="' + str(prev_date)+ '"' + '  and commits.commiter_date<="' + str(start_date) + '" group by Commitedfiles.name'
        self.sqlToAttributes(["0"], c, files_dict, disAuthors_last)

        last_commit='select name,julianday("'+ str(start_date)+'")-julianday(max(commiter_date)) from commitedfiles  where commitedfiles.commiter_date<="' + str(start_date)+ '"' + '  and commitedfiles.commiter_date<="' + str(end_date) + '" group by Commitedfiles.name'
        self.sqlToAttributes(["0"], c, files_dict, last_commit)

        last_bug='select name,julianday("'+ str(start_date)+'")-julianday(max(commiter_date)) from commitedfiles  where bugId<>0 and name not like "%test%" and commitedfiles.commiter_date<="' + str(start_date)+ '"' + '  and commitedfiles.commiter_date<="' + str(end_date) + '" group by Commitedfiles.name'
        self.sqlToAttributes(["0"], c, files_dict, last_bug)

        last_ver_bug='select name,julianday("'+ str(start_date)+'")-julianday(max(commiter_date)) from commitedfiles  where bugId<>0 and name not like "%test%" and commitedfiles.commiter_date>="' + str(prev_date)+ '"' + '  and commitedfiles.commiter_date<="' + str(start_date) + '" group by Commitedfiles.name'
        self.sqlToAttributes(["0"], c, files_dict, last_ver_bug)

        changeSet='select A.name,count(distinct B.name) from Commitedfiles as A, Commitedfiles as B where A.commitid=B.commitid and A.commiter_date<="' + str(start_date)+ '"' + '  and A.commiter_date<="' + str(end_date) + '" and B.commiter_date<="' + str(start_date)+ '"' + '  and B.commiter_date<="' + str(end_date) + '" group by A.name'
        self.sqlToAttributes(["0"], c, files_dict, changeSet)

        age='select name, sum( julianday(commiter_date)*insertions ) -sum( julianday(commiter_date)*deletions ) from Commitedfiles  where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) +'" group by name'
        self.sqlToAttributes(["0"], c, files_dict, age)

        age='select name, julianday("'+ str(start_date)+'")*(sum(insertions)-sum(deletions))-sum( julianday(commiter_date)*insertions ) -sum( julianday(commiter_date)*deletions ) from Commitedfiles  where commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) +'" group by name'
        self.sqlToAttributes(["0"], c, files_dict, age)

        first='select name, count(*),  sum(insertions),sum(deletions),Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End) from commitedfiles where bugId<>0 and name not like "%test%" and commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by name'
        self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)

        for p in ['"P3"']:
            first='select name, count(*),  sum(insertions),sum(deletions),Sum(case When insertions > 0 Then 1 Else 0 End),Sum(case When deletions > 0 Then 1 Else 0 End),  avg(insertions),avg(deletions), avg(case When insertions > 0 Then insertions Else Null End),avg(case When deletions > 0 Then deletions Else Null End) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" and bugs.Priority='+p+' and commiter_date<="' + str(start_date)+ '"' + '  and commiter_date<="' + str(end_date) + '" group by name'
            self.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, first)


        first='select name,avg((julianday(commitedfiles.commiter_date)-julianday(bugs.Submit_Date))) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,avg((julianday(commitedfiles.commiter_date)-julianday(bugs.Last_Modified))) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,count(distinct OS) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,count(Distinct Assigned_To) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%"  group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,count(Distinct Component) from commitedfiles,bugs where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,avg(files) from commitedfiles,commits where commitedfiles.commitId=commits.id group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,avg(files) from commitedfiles,commits where commitedfiles.commitId=commits.id and commitedfiles.bugId<>0 and name not like "%test%" group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)
        first='select name,avg(files) from commitedfiles,commits where commitedfiles.commitId=commits.id and commitedfiles.bugId=0 and name not like "%test%" group by name'
        self.sqlToAttributes(["0"], c, files_dict, first)





