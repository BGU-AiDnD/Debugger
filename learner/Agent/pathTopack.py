__author__ = 'amir'

RENAMED_FILES = None


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
                fix = lambda repl: re.sub(r"{[\.a-zA-Z_/\-0-9]* => [\.a-zA-Z_/\-0-9]*}", repl.strip(), file)
                src, dst = map(fix, [src, dst])
            else:
                # full path changed
                src, dst = map(lambda x: x.strip(), file.split("=>"))
            new_files[src] = dst
    return new_files


def set_renamed_files_for_repo(repo):
    global RENAMED_FILES
    if RENAMED_FILES:
        return
    renamed_mapping = {}
    for git_commit in repo.iter_commits():
        commit_renamed = get_renamed_files_for_commit(git_commit)
        for name in commit_renamed:
            if commit_renamed[name] in renamed_mapping:
                if renamed_mapping[commit_renamed[name]] == name:
                    # avoid double mapping
                    continue
            renamed_mapping[name] = commit_renamed[name]
    RENAMED_FILES = renamed_mapping


def fix_renamed_file(file_name):
    if RENAMED_FILES:
        found = True
        while found:
            found = False
            new_file = ""
            if file_name in RENAMED_FILES:
                new_file = RENAMED_FILES[file_name]
                found = True
                logging.info('found rename src: {0}, dst: {1}'.format(file_name, RENAMED_FILES[file_name]))
            else:
                new_file = file_name
            file_name = new_file
    return file_name


def pathToPack(path):
    return fix_renamed_file(path).replace("/","\\")
