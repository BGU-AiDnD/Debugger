__author__ = 'amir'
import os
from datetime import datetime
import tempfile
import wekaMethods.issuesExtract.python_bugzilla

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

conf = None

def globalConfig(confFile):
    lines =[x.split("\n")[0] for x in open(confFile,"r").readlines()]
    current_dir = os.path.dirname(os.path.realpath(__file__))
    utilsPath = os.path.realpath(os.path.join(current_dir, "../utils"))
    docletPath = os.path.join(utilsPath, "xml-doclet-1.0.4-jar-with-dependencies.jar")
    sourceMonitorEXE = "C:\Program Files (x86)\SourceMonitor\SourceMonitor.exe"
    checkStyle57 = os.path.join(utilsPath, "checkstyle-5.7-all.jar")
    checkStyle68 = os.path.join(utilsPath, "checkstyle-6.8-SNAPSHOT-all.jar")
    allchecks = os.path.join(utilsPath, "allChecks.xml")
    methodsNamesXML = os.path.join(utilsPath, "methodNameLines.xml")
    wekaJar = os.path.join(utilsPath, "weka.jar")
    RemoveBat = os.path.join(utilsPath, "../removeBat.bat")
    for x in lines:
        if x.startswith("sourceMonitorEXE"):
            v=x.split("=")[1]
            sourceMonitorEXE=v
    return docletPath,sourceMonitorEXE,checkStyle57,checkStyle68,allchecks,methodsNamesXML,wekaJar,RemoveBat,utilsPath


def configure(confFile):
    lines =[x.split("\n")[0] for x in open(confFile,"r").readlines()]
    vers, gitPath,bugzilla_url, bugzilla_product, workingDir="","","","",""
    for x in lines:
        if x.startswith("workingDir"):
            v=x.split("=")[1]
            workingDir=v
        if x.startswith("git"):
            v=x.split("=")[1]
            gitPath=v
        if x.startswith("bugzilla_product"):
            v=x.split("=")[1]
            bugzilla_product=v
        if x.startswith("bugzilla_url"):
            v=x.split("=")[1]
            bugzilla_url=v
        if x.startswith("vers"):
            v=x.split("=")[1]
            v=v.split("(")[1]
            v=v.split(")")[0]
            vers=v.split(",")
    init_configuration(workingDir)
    bugs = tempfile.mkstemp(suffix=".csv")[1]
    wekaMethods.issuesExtract.python_bugzilla.write_bugs_csv(bugs, bugzilla_url, bugzilla_product)
    return [v.lstrip() for v in vers], gitPath,bugs, workingDir


def configureExperiments(confFile):
    lines =[x.split("\n")[0] for x in open(confFile,"r").readlines()]
    vers, gitPath,bugs, workingDir="","","",""
    for x in lines:
        if x.startswith("workingDir"):
            v=x.split("=")[1]
            workingDir=v
        if x.startswith("git"):
            v=x.split("=")[1]
            gitPath=v
        if x.startswith("bugs"):
            v=x.split("=")[1]
            bugs=v
        if x.startswith("vers"):
            v=x.split("=")[1]
            v=v.split("(")[1]
            v=v.split(")")[0]
            vers=v.split(",")
    return [v.lstrip() for v in vers], gitPath,bugs, workingDir

class Configuration:
    def __init__(self, workingDir):
        self.markers_dir = os.path.join(workingDir,"markers")

    def get_marker_path(self, marker):
        return os.path.join(self.markers_dir, marker)

    def get_marker(self, marker):
        return Marker(self.get_marker_path(marker))

class Marker:
    def __init__(self, path):
        self.marker_path = path

    def is_exists(self):
        os.path.isfile(self.marker_path)

    def start(self):
        with open(self.marker_path, "wb") as f:
            f.write("start time: " + str(datetime.now()) + "\n")

    def finish(self):
        with open(self.marker_path, "ab") as f:
            f.write("finish time: " + str(datetime.now()) + "\n")

def init_configuration(workingDir):
    global conf
    assert(conf is None)
    conf = Configuration(workingDir)

def get_configuration():
    return conf

def marker_decorator(marker):
    """
    run function if marker doesnt exists
    """
    def decorator(func):
        def f(*args, **kwargs):
            ans = None
            if not get_configuration().get_marker(marker).is_exists():
                get_configuration().get_marker(marker).start()
                ans = func(*args, **kwargs)
                get_configuration().get_marker(marker).finish()
            return ans
        return f
    return decorator