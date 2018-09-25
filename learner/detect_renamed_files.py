import re
import logging
from utilsConf import git_file_path_to_java_name
__author__ = 'amir'

def get_renamed_files_for_commit(commit):
    """
    fix the paths of renamed files.
    before : u'tika-core/src/test/resources/{org/apache/tika/fork => test-documents}/embedded_with_npe.xml'
    after:
    u'tika-core/src/test/resources/org/apache/tika/fork/embedded_with_npe.xml'
    u'tika-core/src/test/resources/test-documents/embedded_with_npe.xml'
    :param commit: git commit
    :return: mapping of {src : dst}
    """
    new_files = {}
    for file in commit.stats.files.keys():
        if "=>" in file:
            if "{" and "}" in file:
                # file moved
                src, dst = file.split("{")[1].split("}")[0].split("=>")
                fix = lambda repl: git_file_path_to_java_name(re.sub(r"{[\.a-zA-Z_/\-0-9]* => [\.a-zA-Z_/\-0-9]*}", repl.strip(), file))
                src, dst = map(fix, [src, dst])
            else:
                # full path changed
                src, dst = map(lambda x: git_file_path_to_java_name(x.strip()), file.split("=>"))
            new_files[src] = dst
    return new_files


def renamed_files_for_repo(repo):
    renamed_mapping = {}
    for git_commit in repo.iter_commits():
        commit_renamed = get_renamed_files_for_commit(git_commit)
        for name in commit_renamed:
            if commit_renamed[name] in renamed_mapping:
                if renamed_mapping[commit_renamed[name]] == name:
                    # avoid double mapping
                    continue
            renamed_mapping[name] = commit_renamed[name]
    return renamed_mapping


def fix_renamed_file(file_name, renamed_files):
    found = True
    file_name = git_file_path_to_java_name(file_name)
    while found:
        found = False
        new_file = ""
        if file_name in renamed_files:
            new_file = renamed_files[file_name]
            found = True
            logging.info('found rename src: {0}, dst: {1}'.format(file_name, renamed_files[file_name]))
        else:
            new_file = file_name
        file_name = new_file
    return file_name
