import os
import sqlite3
from contextlib import contextmanager

ALL_FILES_BUGS_QUERY = 'select bugId,name from Commitedfiles where bugId<>0  and name like "%.java" and commiter_date>="{START_DATE}" and commiter_date<="{END_DATE}" order by bugId'
ALL_METHODS_BUGS_QUERY = 'select bugId,methodDir from CommitedMethods where bugId<>0  and methodDir like "%.java%" and commiter_date>="{START_DATE}" and commiter_date<="{END_DATE}" order by bugId'
MOST_MODIFIED_FILES_BUGS_QUERY = 'select Commitedfiles.bugId,Commitedfiles.name  from Commitedfiles , (select max(lines) as l, bugId from Commitedfiles where name like "%.java" and commiter_date>="{START_DATE}" and commiter_date<="{END_DATE}" group by bugId) as T where Commitedfiles.lines=T.l and Commitedfiles.bugId=T.bugId'
MOST_MODIFIED_METHODS_BUGS_QUERY = 'select CommitedMethods.bugId,CommitedMethods.methodDir  from CommitedMethods , (select max(lines) as l, bugId from CommitedMethods where methodDir like "%.java%" and commiter_date>="{START_DATE}" and commiter_date<="{END_DATE}" group by bugId) as T where CommitedMethods.lines=T.l and CommitedMethods.bugId=T.bugId'


class Bug(object):
    def __init__(self, bug_id, all_files, most_files, all_methods, most_methods):
        self.bug_id = bug_id
        self.all_files = all_files
        self.most_files = most_files
        self.all_methods = all_methods
        self.most_methods = most_methods
        self.components = {'files': {'all': self.all_files, 'most': self.most_files},
                           'methods': {'all': self.all_methods, 'most': self.most_methods}}

    def get_buggy_components(self, granularity, bugged_type):
        return self.components[granularity][bugged_type]



@contextmanager
def use_sql_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.text_factory = str
    yield conn.cursor()
    conn.commit()
    conn.close()


def get_bugs_from_db(db_path, start_date, end_date):
    def get_bug_comps(cursor, query):
        comps = {}
        for bug_id, name in cursor.execute(query.format(START_DATE=start_date, END_DATE=end_date)):
            comps.setdefault(bug_id, []).append(name.replace(os.path.sep, '.').replace('.java', '').replace('$', '@').lower())
        return comps
    bugs = []
    with use_sql_db(db_path) as cursor:
        all_files = get_bug_comps(cursor, ALL_FILES_BUGS_QUERY)
        most_files = get_bug_comps(cursor, MOST_MODIFIED_FILES_BUGS_QUERY)
        all_methods = get_bug_comps(cursor, ALL_METHODS_BUGS_QUERY)
        most_methods = get_bug_comps(cursor, MOST_MODIFIED_METHODS_BUGS_QUERY)
    for bug_id in set(all_files.keys() + most_files.keys() + all_methods.keys() + most_methods.keys()):
        bugs.append(Bug(bug_id, all_files.get(bug_id, []), most_files.get(bug_id, []), all_methods.get(bug_id, []), most_methods.get(bug_id, [])))
    return bugs