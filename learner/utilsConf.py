__author__ = 'amir'
import datetime
import shutil
import git
import os
import subprocess
import traceback
import sys
import github3
from datetime import datetime
import logging

LONG_PATH_MAGIC = u"\\\\?\\"
# markers names:
VERSIONS_MARKER = "versions"
VERSION_TEST_MARKER = "test_version"
FEATURES_MARKER = "features"
DB_BUILD_MARKER = "db"
ML_MODELS_MARKER = "ml"
COMPLEXITY_FEATURES_MARKER = "complexity_features"
OO_OLD_FEATURES_MARKER = "old_oo_features"
OO_FEATURES_MARKER = "oo_features"
COMMENTS_SPACES_MARKER = "comments_spaces_features"
PATCHS_FEATURES_MARKER = "patchs_features"
SOURCE_MONITOR_FEATURES_MARKER = "source_monitor_features"
BLAME_FEATURES_MARKER = "blame_features"
TEST_DB_MARKER = "test_db_features"
PACKS_FILE_MARKER = "packs_file_features"
LEARNER_PHASE_FILE = "learner_phase_file"
ISSUE_TRACKER_FILE = "issue_tracker_file"
ERROR_FILE = "error_file"

conf = None

USE_LONG_PATHS = True

def globalConfig():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    utilsPath = os.path.realpath(os.path.join(current_dir, "../utils"))
    docletPath = os.path.join(utilsPath, "xml-doclet-1.0.4-jar-with-dependencies.jar")
    sourceMonitorEXE = os.path.join(utilsPath, "SourceMonitor.exe")
    checkStyle57 = os.path.join(utilsPath, "checkstyle-5.7-all.jar")
    checkStyle68 = os.path.join(utilsPath, "checkstyle-6.8-SNAPSHOT-all.jar")
    allchecks = os.path.join(utilsPath, "allChecks.xml")
    methodsNamesXML = os.path.join(utilsPath, "methodNameLines.xml")
    wekaJar = os.path.join(utilsPath, "weka.jar")
    RemoveBat = os.path.join(utilsPath, "../removeBat.bat")
    return docletPath,sourceMonitorEXE,checkStyle57,checkStyle68,allchecks,methodsNamesXML,wekaJar,RemoveBat,utilsPath


def to_long_path(path):
    drive_letter, other_path = os.path.splitdrive(path)
    if USE_LONG_PATHS:
        return os.path.join(LONG_PATH_MAGIC + drive_letter, other_path)
    else:
        return path


def to_short_path(path):
    return path.replace(LONG_PATH_MAGIC, "")


def versions_info(repoPath, vers):
    r = git.Repo(repoPath)
    if vers==[]:
        wanted = [x.commit for x in r.tags]
        vers=r.tags
    else:
        wanted = [x.commit for x in r.tags if x.name in vers]
    commits = [int("".join(list(x.hexsha)[:7]), 16) for x in wanted]
    dates = [datetime.fromtimestamp(x.committed_date).strftime('%Y-%m-%d %H:%M:%S') for x in wanted]
    paths = [os.path.join(ver, "repo") for ver in vers]
    return vers, paths, dates, commits


def CopyDirs(gitPath, versPath, versions):
    for version in versions:
        path=os.path.join(versPath, version_to_dir_name(version), "repo")
        if not os.path.exists(path):
            run_commands = ["git", "clone", to_short_path(gitPath), 'repo']
            proc = open_subprocess(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                   cwd=to_short_path(os.path.join(versPath, version_to_dir_name(version))))
            (out, err) = proc.communicate()


def GitRevert(versPath,vers):
    def run_cmd(path, args):
        run_commands = ["git", "-C", path] + args
        proc = open_subprocess(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

    for version in vers:
        repo_path = os.path.join(versPath, version_to_dir_name(version), "repo")
        run_cmd(repo_path, ["clean", "-fd", version])
        run_cmd(repo_path, ["checkout", '-f', version])
        run_cmd(repo_path, ["clean", "-fd", version])


def versionsCreate(gitPath, vers, versPath, workingDir):
    CopyDirs(gitPath, versPath, vers)
    GitRevert(versPath, vers)
    run_commands = ["git", "clone", to_short_path(gitPath), 'repo']
    proc = open_subprocess(run_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=to_short_path(workingDir))
    (out, err) = proc.communicate()
    proc.returncode


def configure(confFile):
    lines = []
    full_configure_file = ""
    with open(confFile,"r") as conf:
        lines =[x.split("\n")[0] for x in conf.readlines()]
        conf.seek(0)
        full_configure_file = conf.read()
    versions, gitPath,issue_tracker_url, issue_tracker_product, workingDir="","","","",""
    issue_tracker = "bugzilla"
    for x in lines:
        if x.startswith("workingDir"):
            workingDir = to_long_path(x.split("=")[1])
        if x.startswith("git"):
            gitPath = to_long_path(x.split("=")[1])
        if x.startswith("issue_tracker_product_name"):
            issue_tracker_product = x.split("=")[1]
        if x.startswith("issue_tracker_url"):
            issue_tracker_url = x.split("=")[1]
        if x.startswith("issue_tracker"):
            issue_tracker = x.split("=")[1]
        if x.startswith("vers"):
            v=x.split("=")[1]
            v=v.split("(")[1]
            v=v.split(")")[0]
            versions = v.split(",")
    versions = [v.strip() for v in versions]
    init_configuration(workingDir, versions)
    configuration = get_configuration()
    db_dir = os.path.join(workingDir, "dbAdd")
    versPath = os.path.join(workingDir, "vers")
    vers, paths, dates, commits = versions_info(gitPath, versions)
    docletPath, sourceMonitorEXE, checkStyle57, checkStyle68, allchecks, methodsNamesXML, wekaJar, RemoveBat, utilsPath = globalConfig()
    bugsPath = os.path.join(workingDir, "bugs.csv")
    vers_dirs = map(version_to_dir_name, vers)
    vers_paths = map(lambda ver: os.path.join(versPath, ver), vers_dirs)
    LocalGitPath = os.path.join(workingDir, "repo")
    mkOneDir(LocalGitPath)
    weka_path = to_short_path(os.path.join(workingDir, "weka"))
    web_prediction_results = to_short_path(os.path.join(workingDir, "web_prediction_results"))
    MethodsParsed = os.path.join(os.path.join(LocalGitPath, "commitsFiles"), "CheckStyle.txt")
    changeFile = os.path.join(os.path.join(LocalGitPath, "commitsFiles"), "Ins_dels.txt")
    debugger_base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    try:
        repo = git.Repo(debugger_base_path)
        logging.info('Debugger HEAD is on commit {0}'.format(str(repo.head.commit)))
        repo.close()
        repo = git.Repo(gitPath)
        remotes_urls = reduce(list.__add__, map(lambda r: list(r.urls), repo.remotes))
        logging.info('remote git at urls {0} and HEAD is on commit {1}'.format(str(remotes_urls),str(repo.head.commit)))
        repo.close()
    except:
        pass
    names_values = [("versPath", versPath), ("db_dir", db_dir), ("vers", vers), ("paths", paths), ("dates", dates),
                    ("commits", commits), ("docletPath", docletPath), ("sourceMonitorEXE", sourceMonitorEXE),
                    ("checkStyle57", checkStyle57), ("checkStyle68", checkStyle68), ("allchecks", allchecks),
                    ("methodsNamesXML", methodsNamesXML), ("wekaJar", wekaJar), ("RemoveBat", RemoveBat),
                    ("utilsPath", utilsPath), ("versions", versions), ("gitPath", gitPath), ("issue_tracker", issue_tracker),
                    ("issue_tracker_url", issue_tracker_url), ("issue_tracker_product", issue_tracker_product),
                    ("workingDir", workingDir), ("bugsPath", bugsPath), ("vers_dirs", vers_dirs), ("vers_paths", vers_paths),
                    ("LocalGitPath", LocalGitPath), ("weka_path", weka_path), ("MethodsParsed", MethodsParsed),
                    ("changeFile", changeFile), ("debugger_base_path", debugger_base_path),
                    ("web_prediction_results", web_prediction_results), ("full_configure_file", full_configure_file)]
    map(lambda name_val: setattr(configuration, name_val[0], name_val[1]), names_values)
    Mkdirs(workingDir)
    versionsCreate(gitPath, vers, versPath, workingDir)
    return versions, gitPath,issue_tracker, issue_tracker_url, issue_tracker_product, workingDir, versPath, db_dir


def version_to_dir_name(version):
    return version.replace("\\", "_").replace("/", "_").replace("-", "_").replace(".", "_")


def mkOneDir(dir):
    if not os.path.isdir(dir):
            os.mkdir(dir)


def Mkdirs(workingDir):
    mkOneDir(workingDir)
    map(lambda dir_name: mkOneDir(os.path.join(workingDir, dir_name)), ["", "vers", "experiments", "experiments_known",
                                                                        "dbAdd", "testedVer", "weka", "web_prediction_results", "markers"])
    versPath=os.path.join(workingDir,"vers")
    mkOneDir(versPath)
    checkAll=os.path.join(versPath,"checkAll")
    mkOneDir(checkAll)
    checkAllMethodsData=os.path.join(versPath,"checkAllMethodsData")
    mkOneDir(checkAllMethodsData)
    for v in get_configuration().vers:
        version=os.path.join(versPath, version_to_dir_name(v))
        mkOneDir(version)
        blame=os.path.join(version,"blame")
        mkOneDir(blame)
        Jdoc2=os.path.join(version,"Jdoc2")
        mkOneDir(Jdoc2)
    return versPath

class Configuration(object):
    def __init__(self, workingDir, versions):
        self.markers_dir = os.path.join(workingDir,"markers")
        self.versions = versions
        mkOneDir(workingDir)
        log_path = os.path.join(to_short_path(workingDir), "log.log")
        if os.path.exists(log_path):
            os.remove(log_path)
        logging.basicConfig(filename=log_path, level=logging.DEBUG)

    def get_marker_path(self, marker):
        return os.path.join(self.markers_dir, marker)

    def get_marker(self, marker):
        return Marker(self.get_marker_path(marker))

def open_subprocess(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None,
                    close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False,
                    startupinfo=None, creationflags=0):
    logging.info('running new process with cmdline {0}'.format(" ".join(args)))
    return subprocess.Popen(args, bufsize=bufsize, executable=executable, stdin=stdin, stdout=stdout, stderr=stderr,
                            preexec_fn=preexec_fn, close_fds=close_fds, shell=shell, cwd=cwd, env=env,
                            universal_newlines=universal_newlines, startupinfo=startupinfo, creationflags=creationflags)

class Marker(object):
    def __init__(self, path):
        self.marker_path = path

    def is_done(self):
        if os.path.isfile(self.marker_path):
            with open(self.marker_path) as f:
                if "finish" in f.read():
                    return True
        return False

    def start(self):
        with open(self.marker_path, "wb") as f:
            log_line = "start time: " + str(datetime.now()) + "\n"
            f.write(log_line)
            logging.info('writing to %s: %s', self.marker_path, log_line)

    def error(self, error_msg):
        with open(self.marker_path, "ab") as f:
            f.write("failed\n")
            f.write("error msg : {0}\n".format(error_msg))
            logging.exception("error msg : {0}\n".format(error_msg))

    def finish(self):
        with open(self.marker_path, "ab") as f:
            log_line = "finish time: " + str(datetime.now()) + "\n"
            f.write(log_line)
            logging.info('writing to %s: %s', self.marker_path ,log_line)


def init_configuration(workingDir, versions):
    global conf
    assert(conf is None)
    conf = Configuration(workingDir, versions)


def get_configuration():
    return conf


def post_bug_to_github(etype, value, tb):
    # try to post bug to github
    try:
        gh = github3.login('DebuggerIssuesReport', password='DebuggerIssuesReport1') # DebuggerIssuesReport@mail.com
        repo = gh.repository('amir9979', 'Debugger')
        issue_body = "\n".join(["An Exception occurred while running Debugger:\n", "command line is {0}\n\n".format(" ".join(sys.argv))])\
                     + "".join(['Traceback (most recent call last):\n'] + traceback.format_tb(tb) + traceback.format_exception_only(etype, value))
        issue = repo.create_issue(title='An Exception occurred : {0}'.format(value.message), body=issue_body, assignee='amir9979')
        configuration = get_configuration()
        issue.create_comment(body="Configuration is : \n" + "\n".join(map(str, configuration.__dict__.items())))
        with open(logging.root.handlers[0].baseFilename) as logger:
            issue.create_comment(body=logger.read())
    except:
        pass


def marker_decorator(marker):
    """
    run function if marker doesnt exists
    """
    def decorator(func):
        def f(*args, **kwargs):
            ans = None
            if not get_configuration().get_marker(marker).is_done():
                get_configuration().get_marker(marker).start()
                try:
                    ans = func(*args, **kwargs)
                    get_configuration().get_marker(marker).finish()
                except Exception as e:
                    get_configuration().get_marker(marker).error(e.message)
                    etype, value, tb = sys.exc_info()
                    traceback.print_exc()
                    post_bug_to_github(etype, value, tb)
                    raise
            return ans
        return f
    return decorator
