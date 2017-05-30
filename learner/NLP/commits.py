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

    def to_csv(self):
        return [self._commit_id, str(self._bug_id), ";".join(self._files)]



def bugs_data(BugsFile):
    bugsIds=[]
    reader = csv.reader(open(BugsFile))
    index=0
    for row in reader:# iterates the rows of the file in orders
        index=index+1
        if(index==1):
            continue
        bugsIds.append(row[0])
    return bugsIds


def commits_and_Bugs(repo, bugsIds):
    def get_bug_num_from_comit_text(commit_text):
        s = commit_text.lower().replace(":", "").replace("#", "").replace("-", " ").replace("_", " ").split()
        for word in s:
            if word.isdigit():
                if (len(word) < 8 and len(word) > 4):
                    return word
        return "0"
    commits= []
    for git_commit in repo.iter_commits():
        commit_text = git_commit.summary
        commits.append(Commit(git_commit, get_bug_num_from_comit_text(commit_text)))
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
        writer.writerows([c.to_csv() for c in commits])

if __name__ == "__main__":
    data_to_csv(r"C:\Temp\AntNLP.csv", r"C:\Users\User\Downloads\antWorking5\repo", "C:\Temp\\AntBugs.csv")