from sympy.functions.elementary.trigonometric import sec
from wekaMethods import wekaAccuracy

__author__ = 'Amir-pc'

import arff

from wekaMethods.buildDB import *
from wekaMethods.commentedCodeDetector import *
import features.process as process
import features.haelstead as haelstead
import features.OO as OO
import features.OOFamilies as OOFamilies
import features.sourceMonitor as sourceMonitor
import features.checkStyle as checkStyle
import features.blame as blame
import features.processFamilies as processFamilies
import features.analyzeComms as analyzeComms
import features.analyzeLast as analyzeLast
import featuresMethods.processMethods as processMethods
import featuresMethods.haelsteadMethods as haelsteadMethods
import featuresMethods.OOMethods as OOMethods
import featuresMethods.OOFamiliesMethods as OOFamiliesMethods
import featuresMethods.sourceMonitorMethods as sourceMonitorMethods
import featuresMethods.checkStyleMethods as checkStyleMethods
import featuresMethods.blameMethods as blameMethods
import featuresMethods.analyzeCommsMethods as analyzeCommsMethods
import featuresMethods.analyzeLastMethods as analyzeLastMethods
import featuresMethods.processMethodsFamilies as processMethodsFamilies
import Agent.pathTopack

# for %%l in (1,2,3,4,5,6,7,8,9,10,11,12) do (
# java -classpath ../weka/weka.jar weka.classifiers.trees.J48  -t TRAINING_%%l.arff -x 10 -d MOEDL_%%l.model
# java -classpath ../weka/weka.jar weka.classifiers.trees.J48  -l MOEDL_%%l.model -T TEST_WILD%%l.arff -p 0 > WEKA_%%l.txt  )

BUG_QUERIES = {"Method": {
    "All": 'select distinct methodDir,"bugged"  from commitedMethods '
           'where bugId<>0 and '
           'methodDir like "%.java%" and '
           'methodDir not like "%test%" and '
           'commiter_date>="STARTDATE" and '
           'commiter_date<="ENDDATE" '
           'group by methodDir',
    "Most": 'select CommitedMethods.methodDir,"bugged"  from CommitedMethods , '
            '(select max(lines) as l, bugId from CommitedMethods '
            'where methodDir like "%.java%" and '
            'methodDir not like "%test%" and '
            'commiter_date>="STARTDATE"  and '
            'commiter_date<="ENDDATE" and '
            'bugId<>0 '
            'group by bugId) as T '
            'where CommitedMethods.lines=T.l and '
            'CommitedMethods.bugId=T.bugId group by methodDir '
},
    "File": {
        "All": 'select distinct name,"bugged"  from commitedfiles '
               'where bugId<>0 and '
               'name like "%.java" and '
               'name not like "%test%" and '
               'commiter_date>="STARTDATE" and '
               'commiter_date<="ENDDATE" and '
               'not exists (select comments.commitid,comments.name from comments where comments.commitid=Commitedfiles.commitid and comments.name=Commitedfiles.name) '
               'group by name',
        "Most": 'select distinct name,"bugged" from '
                '(select Commitedfiles.bugId as bugId,Commitedfiles.name as name  from Commitedfiles , '
                '(select max(lines) as l, Commitedfiles.bugId as bugId from Commitedfiles '
                'where Commitedfiles.name like "%.java" and '
                'name not like "%test%" and '
                'commiter_date>="STARTDATE" and '
                'commiter_date<="ENDDATE" and '
                'not exists (select comments.commitid,comments.name from comments where comments.commitid=Commitedfiles.commitid and comments.name=Commitedfiles.name) '
                'group by bugId) as T '
                'where Commitedfiles.lines=T.l and '
                'Commitedfiles.bugId=T.bugId) '
                'where bugId<>0 '
                'group by name'}}
COMPONENTS_QUERIES = {
    "Method": 'select methodDir from '
              '(select distinct methodDir, sum(is_deleted_file) as deleted from commitedMethods '
              'where commitedMethods.commiter_date<="ENDDATE" '
              'group by methodDir) where deleted=0',
    "File": 'select name from '
            '(select distinct name, sum(is_deleted_file) as deleted from '
            'commitedFiles '
            'where Commitedfiles.commiter_date <="ENDDATE" '
            'group by name) '
            'where deleted=0'}
PACKAGES = {'Method': ["lastProcessMethods", "simpleProcessArticlesMethods", "simpleProcessAddedMethods"],
            'File': ["haelstead", "methodsArticles", "methodsAdded", "hirarcy", "fieldsArticles", "fieldsAdded",
                     "constructorsArticles", "constructorsAdded", "lastProcess", "simpleProcessArticles",
                     "simpleProcessAdded", "bugs", "sourceMonitor", "checkStyle"]}


def arff_build(attributes, data, description, relation):
    dict = {}
    dict['attributes'] = attributes
    dict['data'] = data
    dict['description'] = description
    dict['relation'] = relation
    return dict


def write_to_arff(data, filename):
    with open(filename, 'w') as f:
        f.write(arff.dumps(data))


def load_arff(filename):
    with open(filename, 'r') as f:
        return arff.loads(f.read())


def GitVersInfo():
    r = git.Repo(utilsConf.get_configuration().gitPath)
    wanted = [x.commit for x in r.tags if x.name in utilsConf.get_configuration().vers]
    dates = [datetime.datetime.fromtimestamp(x.committed_date).strftime('%Y-%m-%d %H:%M:%S') for x in wanted]
    return dates


def sqlToAttributes(basicAtt, c, files_dict, first):
    Att_dict = {}
    for f in files_dict.keys():
        Att_dict[f] = list(basicAtt)
    for row in c.execute(first):
        name = Agent.pathTopack.pathToPack(row[0])
        if (name in Att_dict):
            Att_dict[name] = list(row[1:])
    for f in Att_dict:
        files_dict[f] = files_dict[f] + Att_dict[f]


def sqlToAttributesBest(basicAtt, c, files_dict, first, best):
    Att_dict = {}
    for f in files_dict.keys():
        Att_dict[f] = list(basicAtt)
    for row in c.execute(first):
        name = Agent.pathTopack.pathToPack(row[0])
        if (name in Att_dict):
            ret = []
            all = list(row[1:])
            for i in range(len(all)):
                if i + 1 in best:
                    ret.append(all[i])
            Att_dict[name] = ret
    for f in Att_dict:
        files_dict[f] = files_dict[f] + Att_dict[f]


def get_arff_class(dbpath, start_date, end_date, bug_query, component_query):
    with utilsConf.use_sqllite(dbpath) as conn:
        c = conn.cursor()
        files_hasBug = {}
        for row in c.execute(component_query.replace("STARTDATE", str(start_date)).replace("ENDDATE", str(end_date))):
            files_hasBug[Agent.pathTopack.pathToPack(row[0])] = ["valid"]
        for row in c.execute(bug_query.replace("STARTDATE", str(start_date)).replace("ENDDATE", str(end_date))):
            name = Agent.pathTopack.pathToPack(row[0])
            if name in files_hasBug:
                files_hasBug[name] = ["bugged"]
        return files_hasBug


def arffCreateForTag(dbpath, prev_date, start_date, end_date, objects, bug_query, component_query):
    conn = sqlite3.connect(dbpath)
    print dbpath
    conn.text_factory = str
    c = conn.cursor()
    files_dict = {}
    for row in c.execute(component_query.replace("STARTDATE", str(start_date)).replace("ENDDATE", str(end_date))):
        name = Agent.pathTopack.pathToPack(row[0])
        files_dict[name] = []
    conn.close()
    for o in objects:
        conn = sqlite3.connect(dbpath)
        conn.text_factory = str
        c = conn.cursor()
        o.get_features(c, files_dict, prev_date, start_date, end_date)
        conn.close()
    files_hasBug = get_arff_class(dbpath, start_date, end_date, bug_query, component_query)
    for f in files_hasBug:
        files_dict[f] = files_dict[f] + files_hasBug[f]
    return files_dict.values(), files_dict.keys()


def objectsAttr(objects):
    attr = []
    for o in objects:
        attr.extend(o.get_attributes())
    attr.append(("hasBug", ["bugged", "valid"]))
    return attr


def writeFile(allNames, arffExtension, namesFile, attr, data, name, outPath):
    arff_data = arff_build(attr, data, str([]), "base")
    path_join = os.path.join(outPath, str(name + arffExtension))
    write_to_arff(arff_data, path_join)
    if namesFile != "":
        path_join = os.path.join(outPath, str(name + namesFile))
        f = open(path_join, "wb")
        writer = csv.writer(f)
        writer.writerows([[a] for a in allNames])
        f.close()
    # f.writelines(allNames)


def writeArff(allNames, arffName, namesFile, attr, data):
    arff_data = arff_build(attr, data, str([]), "base")
    write_to_arff(arff_data, arffName)
    if namesFile != "":
        with open(namesFile, "wb") as f:
            writer = csv.writer(f)
            writer.writerows([[a] for a in allNames])


def arffCreate(basicPath, objects, names, dates, bug_query, component_query, trainingFile, testingFile, NamesFile):
    data = []
    i = 0
    attr = objectsAttr(objects)
    while (i + 1 < len(names)):
        dbpath = os.path.join(basicPath, str(names[i] + ".db"))
        prev_date, start_date, end_date = dates[i: i + 3]
        tag, allNames = arffCreateForTag(dbpath, prev_date, start_date, end_date, objects, bug_query, component_query)
        arff_names = "_{0}_{1}".format(names[i], names[i + 1])
        writeArff(allNames, testingFile.replace(".arff", arff_names + ".arff"),
                  NamesFile.replace(".csv", arff_names + ".csv"), attr, tag)
        data = data + tag
        if i == len(names) - 3:
            writeArff([], trainingFile, "", attr, data)
        if i == len(names) - 2:
            writeArff(allNames, testingFile, NamesFile, attr, tag)
        i = i + 1
    return data


def attributeSelect(sourceFile, outFile, inds):
    source = load_arff(sourceFile)
    attributes = []
    ind = 0
    last = len(source['attributes']) - 1
    for x in source['attributes']:
        if ind in inds or ind == last:
            attributes.append(x)
        ind = ind + 1
    data = []
    for x in source['data']:
        ind = 0
        d = []
        for y in x:
            if ind in inds or ind == last:
                d.append(y)
            ind = ind + 1
        if (d != []):
            data.append(d)
    arff_data = arff_build(attributes, data, str([]), "selected")
    write_to_arff(arff_data, outFile)


def featuresMethodsPacksToClasses(packs):
    l = []
    names = []
    if "bugsMethods" in packs:
        l.append(processMethodsFamilies.processMethodsFamilies("bugsMethods"))
        names.append("bugsMethods")
    if "processMethods" in packs:
        l.append(processMethods.processMethods())
        names.append("processMethods")
    if "haelsteadMethods" in packs:
        l.append(haelsteadMethods.haelsteadMethods())
        names.append("haelsteadMethods")
    if "OOMethods" in packs:
        l.append(OOMethods.OOMethods())
        names.append("OOMethods")
    if "g2Methods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("g2Methods"))
        names.append("g2Methods")
    if "g3Methods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("g3Methods"))
        names.append("g3Methods")
    if "g4Methods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("g4Methods"))
        names.append("g4Methods")
    if "methodsMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("methodsMethods"))
        names.append("methodsMethods")
    if "methodsArticlesMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("methodsArticlesMethods"))
        names.append("methodsArticlesMethods")
    if "methodsAddedMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("methodsAddedMethods"))
        names.append("methodsAddedMethods")
    if "hirarcyMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("hirarcyMethods"))
        names.append("hirarcyMethods")
    if "fieldsMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("fieldsMethods"))
        names.append("fieldsMethods")
    if "fieldsArticlesMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("fieldsArticlesMethods"))
        names.append("fieldsArticlesMethods")
    if "fieldsAddedMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("fieldsAddedMethods"))
        names.append("fieldsAddedMethods")
    if "constructorsMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("constructorsMethods"))
        names.append("constructorsMethods")
    if "constructorsArticlesMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("constructorsArticlesMethods"))
        names.append("constructorsArticlesMethods")
    if "constructorsAddedMethods" in packs:
        l.append(OOFamiliesMethods.OOFamiliesMethods("constructorsAddedMethods"))
        names.append("constructorsAddedMethods")
    if "lastProcessMethods" in packs:
        l.append(processMethodsFamilies.processMethodsFamilies("lastProcessMethods"))
        names.append("lastProcessMethods")
    if "simpleProcessArticlesMethods" in packs:
        l.append(processMethodsFamilies.processMethodsFamilies("simpleProcessArticlesMethods"))
        names.append("simpleProcessArticlesMethods")
    if "simpleProcessAddedMethods" in packs:
        l.append(processMethodsFamilies.processMethodsFamilies("simpleProcessAddedMethods"))
        names.append("simpleProcessAddedMethods")
    if "sourceMonitorMethods" in packs:
        l.append(sourceMonitorMethods.sourceMonitorMethods())
        names.append("sourceMonitorMethods")
    if "checkStyleMethods" in packs:
        l.append(checkStyleMethods.checkStyleMethods())
        names.append("checkStyleMethods")
    if "blameMethods" in packs:
        l.append(blameMethods.blameMethods())
        names.append("blameMethods")
    if "analyzeCommsMethods" in packs:
        l.append(analyzeCommsMethods.analyzeCommsMethods())
        names.append("analyzeCommsMethods")
    if "analyzeLastMethods" in packs:
        l.append(analyzeLastMethods.analyzeLastMethods())
        names.append("analyzeLastMethods")
    return l, names


def featuresPacksToClasses(packs):
    l = []
    names = []
    if "process" in packs:
        l.append(process.process())
        names.append("process")
    if "haelstead" in packs:
        l.append(haelstead.haelstead())
        names.append("haelstead")
    if "OO" in packs:
        l.append(OO.OO())
        names.append("OO")
    if "g2" in packs:
        l.append(OOFamilies.OOFamilies("g2"))
        names.append("g2")
    if "g3" in packs:
        l.append(OOFamilies.OOFamilies("g3"))
        names.append("g3")
    if "g4" in packs:
        l.append(OOFamilies.OOFamilies("g4"))
        names.append("g4")
    if "methods" in packs:
        l.append(OOFamilies.OOFamilies("methods"))
        names.append("methods")
    if "methodsArticles" in packs:
        l.append(OOFamilies.OOFamilies("methodsArticles"))
        names.append("methodsArticles")
    if "methodsAdded" in packs:
        l.append(OOFamilies.OOFamilies("methodsAdded"))
        names.append("methodsAdded")
    if "hirarcy" in packs:
        l.append(OOFamilies.OOFamilies("hirarcy"))
        names.append("hirarcy")
    if "fields" in packs:
        l.append(OOFamilies.OOFamilies("fields"))
        names.append("fields")
    if "fieldsArticles" in packs:
        l.append(OOFamilies.OOFamilies("fieldsArticles"))
        names.append("fieldsArticles")
    if "fieldsAdded" in packs:
        l.append(OOFamilies.OOFamilies("fieldsAdded"))
        names.append("fieldsAdded")
    if "constructors" in packs:
        l.append(OOFamilies.OOFamilies("constructors"))
        names.append("constructors")
    if "constructorsArticles" in packs:
        l.append(OOFamilies.OOFamilies("constructorsArticles"))
        names.append("constructorsArticles")
    if "constructorsAdded" in packs:
        l.append(OOFamilies.OOFamilies("constructorsAdded"))
        names.append("constructorsAdded")
    if "lastProcess" in packs:
        l.append(processFamilies.processFamilies("lastProcess"))
        names.append("lastProcess")
    if "simpleProcessArticles" in packs:
        l.append(processFamilies.processFamilies("simpleProcessArticles"))
        names.append("simpleProcessArticles")
    if "simpleProcessAdded" in packs:
        l.append(processFamilies.processFamilies("simpleProcessAdded"))
        names.append("simpleProcessAdded")
    if "bugs" in packs:
        l.append(processFamilies.processFamilies("bugs"))
        names.append("bugs")
    if "sourceMonitor" in packs:
        l.append(sourceMonitor.sourceMonitor())
        names.append("sourceMonitor")
    if "checkStyle" in packs:
        l.append(checkStyle.checkStyle())
        names.append("checkStyle")
    if "blame" in packs:
        l.append(blame.blame())
        names.append("blame")
    if "analyzeComms" in packs:
        l.append(analyzeComms.analyzeComms())
        names.append("analyzeComms")
    if "analyzeLast" in packs:
        l.append(analyzeLast.analyzeLast())
        names.append("analyzeLast")
    return l, names


class arffGenerator(object):
    def __init__(self, buggedType, granularity):
        self.buggedType = buggedType
        self.granularity = granularity
        self.bug_query = BUG_QUERIES[granularity][buggedType]
        self.component_query = COMPONENTS_QUERIES[granularity]

    def get_files(self, out_dir):
        trainingFile = os.path.join(out_dir, self.buggedType + "_training_" + self.granularity + ".arff")
        testingFile = os.path.join(out_dir, self.buggedType + "_testing_" + self.granularity + ".arff")
        NamesFile = os.path.join(out_dir, self.buggedType + "_names_" + self.granularity + ".csv")
        outCsv = os.path.join(out_dir, self.buggedType + "_out_" + self.granularity + ".csv")
        return trainingFile, testingFile, NamesFile, outCsv

    def generate_features(self, out_dir, packages):
        trainingFile, testingFile, NamesFile, outCsv = self.get_files(out_dir)
        FeaturesClasses, Featuresnames = self.names_to_classes(packages)
        arffCreate(utilsConf.get_configuration().db_dir, FeaturesClasses, utilsConf.get_configuration().vers_dirs,
                   [datetime.datetime(1900, 1, 1, 0, 0).strftime(
                       '%Y-%m-%d %H:%M:%S')] + utilsConf.get_configuration().dates, self.bug_query,
                   self.component_query,
                   trainingFile, testingFile, NamesFile)
        return trainingFile, testingFile, NamesFile, outCsv

    def names_to_classes(self, packages):
        if self.granularity == 'File':
            return featuresPacksToClasses(packages)
        elif self.granularity == 'Method':
            return featuresMethodsPacksToClasses(packages)
        assert False

    def BuildWekaModel(self, out_dir):
        wekaJar = utilsConf.to_short_path(utilsConf.get_configuration().wekaJar)
        trainingFile, testingFile, NamesFile, outCsv = self.get_files(out_dir)
        name = "_{0}_{1}".format(self.buggedType, self.granularity)
        algorithm = "weka.classifiers.trees.RandomForest -I 1000 -K 0 -S 1 -num-slots 1 "
        os.system("cd /d  " + utilsConf.to_short_path(
            utilsConf.get_configuration().weka_path) + " & java -Xmx2024m  -cp " + utilsConf.to_short_path(
            wekaJar) + " weka.Run " + algorithm + " -x 10 -d .\\model.model -t " + trainingFile + " > training" + name + ".txt")
        algorithm = "weka.classifiers.trees.RandomForest "
        os.system("cd /d  " + utilsConf.to_short_path(
            utilsConf.get_configuration().weka_path) + " & java -Xmx2024m  -cp " + utilsConf.to_short_path(
            wekaJar) + " weka.Run " + algorithm + " -l .\\model.model -T " + testingFile + " -classifications \"weka.classifiers.evaluation.output.prediction.CSV -file testing" + name + ".csv\" ")
        os.system("cd /d  " + utilsConf.to_short_path(
            utilsConf.get_configuration().weka_path) + " & java -Xmx2024m  -cp " + utilsConf.to_short_path(
            wekaJar) + " weka.Run " + algorithm + " -l .\\model.model -T " + testingFile + " > testing" + name + ".txt ")
        wekaCsv = os.path.join(utilsConf.to_short_path(utilsConf.get_configuration().weka_path),
                               "testing" + name + ".csv")
        wekaAccuracy.priorsCreation(NamesFile, wekaCsv, outCsv)
