import json
from os import path

import cached_property

from wekaMethods.articles import Agent
from wekaMethods.features.features_extractor import FeaturesExtractor


class ProcessFeaturesExtractor(FeaturesExtractor):
    """"""

    @cached_property
    def features_object(self):
        with open(path.abspath(path.join(self.FEATURES_FOLDER, "proc_features.json")),
                  "r") as features_file:
            return json.load(features_file)

    @property
    def all_features(self):
        return self.features_object["all_features"]

    def get_attributes(self):
        return [(key, self.all_features[key]) for key in self.all_features]

    def get_features(self, prev_date, start_date, end_date):
        first = \
            'select name, count(*), sum(insertions),sum(deletions), ' \
            'Sum(case When insertions > 0 Then 1 Else 0 End),' \
            'Sum(case When deletions > 0 Then 1 Else 0 End),' \
            'avg(insertions),avg(deletions), ' \
            'avg(case When insertions > 0 Then insertions Else Null End),' \
            'avg(case When deletions > 0 Then deletions Else Null End),' \
            '(case When name not like "%test%" Then count(distinct bugId)-1 Else 0 End)  ' \
            'from commitedfiles where commiter_date<="{start_date}" ' \
            'and commiter_date<="{end_date}" ' \
            'group by name'.format(start_date=start_date, end_date=end_date)

        self.convert_sql_queries_to_attributes(["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                                               first)

        first_last_query = \
            'select name, count(*),  sum(insertions),sum(deletions),' \
            'Sum(case When insertions > 0 Then 1 Else 0 End),' \
            'Sum(case When deletions > 0 Then 1 Else 0 End),  ' \
            'avg(insertions),avg(deletions), ' \
            'avg(case When insertions > 0 Then insertions Else Null End),' \
            'avg(case When deletions > 0 Then deletions Else Null End),' \
            '(case When name not like "%test%" Then count(distinct bugId)-1 Else 0 End) ' \
            'from commitedfiles where commiter_date>="{prev_date}" ' \
            'and commiter_date<="{start_date}" ' \
            'group by name'.format(prev_date=prev_date, start_date=start_date)

        self.convert_sql_queries_to_attributes(["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                                               first_last_query)

        distinct_authors_current_commits_query = \
            'select name, count(distinct author) ' \
            'from commitedfiles, commits ' \
            'where commits.ID=commitedfiles.commitid ' \
            'and commits.commiter_date<="{start_date}" ' \
            'and commits.commiter_date<="{end_date}" ' \
            'group by Commitedfiles.name'.format(start_date=start_date, end_date=end_date)

        self.convert_sql_queries_to_attributes(["0"], distinct_authors_current_commits_query)

        distinct_authors_from_prev_commits_query = \
            'select name, count(distinct author) ' \
            'from commitedfiles, commits ' \
            'where commits.ID=commitedfiles.commitid ' \
            'and commits.commiter_date>="{prev_date}" and ' \
            'commits.commiter_date<="{start_date}" ' \
            'group by Commitedfiles.name'.format(prev_date=prev_date, start_date=start_date)

        self.convert_sql_queries_to_attributes(["0"], distinct_authors_from_prev_commits_query)

        last_commit_query = \
            'select name, julianday("{start_date}")-julianday(max(commiter_date)) ' \
            'from commitedfiles where commitedfiles.commiter_date<="{start_date}" ' \
            'and commitedfiles.commiter_date<="{end_date}" ' \
            'group by Commitedfiles.name'.format(start_date=start_date, end_date=end_date)

        self.convert_sql_queries_to_attributes(["0"], last_commit_query)

        last_bug_query = \
            'select name, julianday("{start_date}")-julianday(max(commiter_date)) ' \
            'from commitedfiles where bugId<>0 and name not like "%test%" and ' \
            'commitedfiles.commiter_date<="{start_date}" ' \
            'and commitedfiles.commiter_date<="{end_date}" ' \
            'group by Commitedfiles.name'.format(start_date=start_date, end_date=end_date)

        self.convert_sql_queries_to_attributes(["0"], last_bug_query)

        last_version_bug_query = \
            'select name, julianday("{start_date}")-julianday(max(commiter_date)) ' \
            'from commitedfiles where bugId<>0 and name not like "%test%" and ' \
            'commitedfiles.commiter_date>="{prev_date}" ' \
            'and commitedfiles.commiter_date<="{start_date}" ' \
            'group by Commitedfiles.name'.format(start_date=start_date, prev_date=prev_date)

        self.convert_sql_queries_to_attributes(["0"], last_version_bug_query)

        change_set_query = \
            'select A.name, count(distinct B.name) ' \
            'from Commitedfiles as A, Commitedfiles as B ' \
            'where A.commitid=B.commitid and A.commiter_date<="{start_date}" ' \
            'and A.commiter_date<="{end_date}" and B.commiter_date<="{start_date}" ' \
            'and B.commiter_date<="{end_date}" ' \
            'group by A.name'.format(start_date=start_date, end_date=end_date)

        self.convert_sql_queries_to_attributes(["0"], change_set_query)

        commit_age_query = \
            'select name, ' \
            'sum(julianday(commiter_date)*insertions) - sum(julianday(commiter_date)*deletions) ' \
            'from Commitedfiles  where commiter_date<="{start_date}" ' \
            'and commiter_date<="{end_date}" ' \
            'group by name'.format(start_date=start_date, end_date=end_date)
        self.convert_sql_queries_to_attributes(["0"], commit_age_query)

        commit_age_query = \
            'select name, julianday("{start_date}")*(sum(insertions)-sum(deletions)) - ' \
            'sum(julianday(commiter_date)*insertions) - sum(julianday(commiter_date)*deletions) ' \
            'from Commitedfiles  where commiter_date<="{start_date}" and ' \
            'commiter_date<="{end_date}" ' \
            'group by name'.format(start_date=start_date, end_date=end_date)
        self.convert_sql_queries_to_attributes(["0"], commit_age_query)

        first = \
            'select name, count(*), sum(insertions), sum(deletions),' \
            'Sum(case When insertions > 0 Then 1 Else 0 End),' \
            'Sum(case When deletions > 0 Then 1 Else 0 End), ' \
            'avg(insertions), avg(deletions), ' \
            'avg(case When insertions > 0 Then insertions Else Null End),' \
            'avg(case When deletions > 0 Then deletions Else Null End) ' \
            'from commitedfiles where bugId<>0 and name not like "%test%" ' \
            'and commiter_date<="{start_date}"  and commiter_date<="{end_date}" ' \
            'group by name'.format(start_date=start_date, end_date=end_date)

        self.convert_sql_queries_to_attributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"], first)

        for p in ['"P3"']:  # TODO: WHATTTTTTTTTTTTTTTTTTTTTTTTTTTTTT???????
            first = \
                'select name, count(*), sum(insertions), sum(deletions), ' \
                'Sum(case When insertions > 0 Then 1 Else 0 End), ' \
                'Sum(case When deletions > 0 Then 1 Else 0 End), ' \
                'avg(insertions), avg(deletions), ' \
                'avg(case When insertions > 0 Then insertions Else Null End), ' \
                'avg(case When deletions > 0 Then deletions Else Null End) ' \
                'from commitedfiles,bugs where commitedfiles.bugId=bugs.id and ' \
                'name not like "%test%" and bugs.Priority={p} ' \
                'and commiter_date<="{start_date}"  and commiter_date<="{end_date}" ' \
                'group by name'.format(start_date=start_date, end_date=end_date)

            self.convert_sql_queries_to_attributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"],
                                                   first)

        # Why are there so many variables named first?!?!
        # Is there no other name that might indicate what the query does????

        first = \
            'select name, ' \
            'avg((julianday(commitedfiles.commiter_date)-julianday(bugs.Submit_Date))) ' \
            'from commitedfiles,bugs where commitedfiles.bugId=bugs.id and ' \
            'name not like "%test%" group by name'

        self.convert_sql_queries_to_attributes(["0"], first)

        first = \
            'select name,' \
            'avg((julianday(commitedfiles.commiter_date)-julianday(bugs.Last_Modified))) ' \
            'from commitedfiles,bugs where commitedfiles.bugId=bugs.id and ' \
            'name not like "%test%" group by name'

        self.convert_sql_queries_to_attributes(["0"], first)

        first = \
            'select name, count(distinct OS) from commitedfiles,bugs ' \
            'where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'

        self.convert_sql_queries_to_attributes(["0"], first)

        first = \
            'select name, count(Distinct Assigned_To) ' \
            'from commitedfiles,bugs ' \
            'where commitedfiles.bugId=bugs.id and name not like "%test%"  group by name'

        self.convert_sql_queries_to_attributes(["0"], first)

        first = \
            'select name, count(Distinct Component) ' \
            'from commitedfiles,bugs ' \
            'where commitedfiles.bugId=bugs.id and name not like "%test%" group by name'

        self.convert_sql_queries_to_attributes(["0"], first)

        first = 'select name, avg(files) from commitedfiles,commits ' \
                'where commitedfiles.commitId=commits.id group by name'

        self.convert_sql_queries_to_attributes(["0"], first)

        first = 'select name, avg(files) from commitedfiles,commits ' \
                'where commitedfiles.commitId=commits.id and commitedfiles.bugId<>0 ' \
                'and name not like "%test%" group by name'

        self.convert_sql_queries_to_attributes(["0"], first)

        first = 'select name, avg(files) from commitedfiles,commits ' \
                'where commitedfiles.commitId=commits.id and commitedfiles.bugId=0 ' \
                'and name not like "%test%" group by name'

        self.convert_sql_queries_to_attributes(["0"], first)
