import git
import csv
import datetime
import wekaMethods.issuesExtract.python_bugzilla


class Commit(object):
    def __init__(self, git_commit, bug_id):
        self._git_commit = git_commit
        self._bug_id = bug_id
        self._commit_id = self._git_commit.hexsha
        self._files = self._git_commit.stats.files.keys()

    def to_list(self):
        return [self._commit_id, str(self._bug_id), ";".join(self._files)]


def bugs_data(BugsFile):
    bugsIds = []
    reader = csv.reader(open(BugsFile, "rb"))
    index = 0
    for row in reader:  # iterates the rows of the file in orders
        index = index + 1
        if (index == 1):
            continue
        bugsIds.append(row[0])
    return bugsIds


def clean_commit_message(commit_message):
    if "git-svn-id" in commit_message:
        return commit_message.split("git-svn-id")[0]
    return commit_message


def commits_and_Bugs(repo, bugsIds):
    def get_bug_num_from_comit_text(commit_text, bugsIds):
        s = commit_text.lower().replace(":", "").replace("#", "").replace("-", " ").replace("_", " ").split()
        for word in s:
            if word.isdigit():
                if word in bugsIds:
                    return word
        return "0"

    commits = []
    for git_commit in repo.iter_commits():
        commit_text = clean_commit_message(git_commit.message)
        print commit_text, get_bug_num_from_comit_text(commit_text, bugsIds)
        commits.append(Commit(git_commit, get_bug_num_from_comit_text(commit_text, bugsIds)))
    return commits


def get_data(gitPath, BugsFile):
    repo = git.Repo(gitPath)
    bugsIds = bugs_data(BugsFile)
    commits = commits_and_Bugs(repo, bugsIds)
    return commits


def data_to_csv(out_file, gitPath, BugsFile):
    commits = get_data(gitPath, BugsFile)
    with open(out_file, "wb") as f:
        writer = csv.writer(f)
        writer.writerows([c.to_list() for c in commits])


if __name__ == "__main__":
    import sys

    csv.field_size_limit(sys.maxsize)
    data_to_csv(r"C:\Temp\NLP.csv", r"C:\Users\User\Downloads\orientdb",
                r"C:\Users\User\AppData\Local\Temp\tmpwbfvow.csv")
