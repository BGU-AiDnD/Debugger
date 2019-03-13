import weka_parser
import os
import csv

badWords = ['ZRESULTS']

class ProjectDetails:
    def __init__(self, ProjectName=None,TestBuges=None,TestAll=None):
        self.ProjectName = ProjectName
        self.TestBuges = TestBuges
        self.TestAll = TestAll
        self.AllProjectModel = {}

    def isFilled(self):
        if self.TestAll:
            return True
        else:
            return False

    def fillDetailsTest(self,TestBuges,TestAll):
        self.TestBuges = TestBuges
        self.TestAll = TestAll
        self.TestPrecent= float(TestBuges) / float(TestAll)

    def fillDetailsTrain(self, TrainBuges, TrainAll):
        self.TrainBuges = TrainBuges
        self.TrainAll = TrainAll
        self.TrainPrecent = float(TrainBuges) / float(TrainAll)

    def bestForIt(self):
        index= max(self.AllProjectModel, key=lambda i: self.AllProjectModel[i])
        if self.AllProjectModel[index] == 0:
            return self.ProjectName,0
        else:
            return index,self.AllProjectModel[index]

    def calculateF2Bugs(self,precision,recall,modelName):
        if ((4 * precision) + recall) != 0:
            F2BUGS = (5 * ((precision * recall) / ((4 * precision) + recall)))
        else:
            F2BUGS = 0
        self.AllProjectModel[modelName] = F2BUGS
        return F2BUGS

    def insertToProjects(self,measure,modelName):
        self.AllProjectModel[modelName] = measure
        return measure

def createResults():
    directory = "D:\Debbuger\BestModel"
    for ModelHost in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, ModelHost)):
            dirModelHost = os.path.join(directory, ModelHost)
            print(dirModelHost)
            allDict={}
            mostDict={}
            for result in os.listdir(dirModelHost):
                if result.endswith("_cfiles_All.txt"):
                    txtFile = open(os.path.join(dirModelHost, result), "wb")
                    parsedResult =weka_parser.parse_WEKA_scores(txtFile.read())
                    prebu = float(parsedResult['test']['accuracy by class']['bugged']['precision'])
                    recbu = float(parsedResult['test']['accuracy by class']['bugged']['recall'])
                    preva = float(parsedResult['test']['accuracy by class']['valid']['precision'])
                    recva = float(parsedResult['test']['accuracy by class']['valid']['recall'])
                    preav = float(parsedResult['test']['accuracy by class']['weighted avg']['precision'])
                    recav = float(parsedResult['test']['accuracy by class']['weighted avg']['recall'])

                    pre = (prebu+preva)/2
                    rec = (recbu+recva)/2

                    F2mav = 5*((preav*recav)/((4*preav)+recav))
                    F2m = 5 * ((pre * rec) / ((4 * pre) + rec))
                    allDict[result[:-15]] = (preav,recav,F2mav,pre,rec,F2m)

                if result.endswith("_cfiles_most.txt"):
                    txtFile = open(os.path.join(dirModelHost, result), "wb")
                    parsedResult = weka_parser.parse_WEKA_scores(txtFile.read())
                    prebu = float(parsedResult['test']['accuracy by class']['bugged']['precision'])
                    recbu = float(parsedResult['test']['accuracy by class']['bugged']['recall'])
                    preva = float(parsedResult['test']['accuracy by class']['valid']['precision'])
                    recva = float(parsedResult['test']['accuracy by class']['valid']['recall'])
                    preav = float(parsedResult['test']['accuracy by class']['weighted avg']['precision'])
                    recav = float(parsedResult['test']['accuracy by class']['weighted avg']['recall'])

                    pre = (prebu + preva) / 2
                    rec = (recbu + recva) / 2

                    F2mav = 5 * ((preav * recav) / ((4 * preav) + recav))
                    F2m = 5 * ((pre * rec) / ((4 * pre) + rec))
                    mostDict[result[:-16]] = (preav, recav, F2mav, pre, rec, F2m)

            #creating the csv of "all" used to be 'wb'
            with open(os.path.join(r'D:\Debbuger\BestModel\ZRESULTS\allFiles','resultAllFiles.csv'), 'ab') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([" "])
                filewriter.writerow([" "])
                filewriter.writerow([ModelHost])
                filewriter.writerow([" "])
                filewriter.writerow(['projectName', 'precision_W_avg','recall_W_avg','F2_W_avg','precision_avg','recall_avg','F2_avg'])
                for key, value in allDict.iteritems():
                    filewriter.writerow(
                        [key, str(value[0]), str(value[1]), str(value[2]), str(value[3]), str(value[4]),
                         str(value[5])])

            #creating the csv of "most"
            with open(os.path.join(r'D:\Debbuger\BestModel\ZRESULTS\mostFiles','resultMostFiles.csv'), 'ab') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([" "])
                filewriter.writerow([" "])
                filewriter.writerow([ModelHost])
                filewriter.writerow([" "])
                filewriter.writerow(['projectName', 'precision_W_avg','recall_W_avg','F2_W_avg','precision_avg','recall_avg','F2_avg'])
                for key, value in allDict.iteritems():
                    filewriter.writerow(
                        [key, str(value[0]), str(value[1]), str(value[2]), str(value[3]), str(value[4]),
                         str(value[5])])

            print("writing completed")

def findBestOfBreed(dic):
    index = max(dic, key=lambda i: dic[i])
    return index, dic[index]

def createResultsBasedOnBuges():
    directory = "D:\Debbuger\BestModel"
    allDict = {}
    bestOfBreedAll={}
    mostDict = {}
    bestOfBreedMost = {}

    for ModelHost in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, ModelHost)) and (ModelHost[:-2] not in badWords)and (ModelHost not in badWords):
            dirModelHost = os.path.join(directory, ModelHost)
            print(dirModelHost)
            numOfProjAll = 0
            numOfProjMost = 0
            modelHostName = ModelHost[:-2]
            bestOfBreedAll[modelHostName] = 0
            bestOfBreedMost[modelHostName] = 0

            for result in os.listdir(dirModelHost):

                if result.endswith("_cfiles_All.txt") and (result[:-15] not in badWords):
                    numOfProjAll = numOfProjAll  + 1
                    projectName = result[:-15]
                    if projectName not in allDict:
                        allDict[projectName] =ProjectDetails(projectName)

                    txtFile = open(os.path.join(dirModelHost, result), "r")
                    parsedResult =weka_parser.parse_WEKA_scores(txtFile.read())

                    if not allDict[projectName].isFilled():
                        allDict[projectName].fillDetailsTest(
                            parsedResult['test']['confusion matrix']['bugged']['bugged'] +
                            parsedResult['test']['confusion matrix']['bugged']['valid'],
                            parsedResult['test']['confusion matrix']['bugged']['bugged'] +
                            parsedResult['test']['confusion matrix']['bugged']['valid'] +
                            parsedResult['test']['confusion matrix']['valid']['bugged'] +
                            parsedResult['test']['confusion matrix']['valid']['valid'])

                    prebu = float(parsedResult['test']['accuracy by class']['bugged']['precision'])
                    recbu = float(parsedResult['test']['accuracy by class']['bugged']['recall'])

                    F2m = allDict[projectName].calculateF2Bugs(prebu,recbu,modelHostName)
                    bestOfBreedAll[modelHostName] =bestOfBreedAll[modelHostName]+ F2m

                if result.endswith("_cfiles_most.txt") and (result[:-16] not in badWords):
                    numOfProjMost = numOfProjMost + 1
                    projectName = result[:-16]
                    if projectName not in mostDict:
                        mostDict[projectName] = ProjectDetails(projectName)

                    txtFile = open(os.path.join(dirModelHost, result), "r")
                    parsedResult = weka_parser.parse_WEKA_scores(txtFile.read())

                    if not mostDict[projectName].isFilled():
                        mostDict[projectName].fillDetailsTest(parsedResult['test']['confusion matrix']['bugged']['bugged'] +
                                                         parsedResult['test']['confusion matrix']['bugged']['valid'],
                                                         parsedResult['test']['confusion matrix']['bugged']['bugged'] +
                                                         parsedResult['test']['confusion matrix']['bugged']['valid'] +
                                                         parsedResult['test']['confusion matrix']['valid']['bugged'] +
                                                         parsedResult['test']['confusion matrix']['valid']['valid'])

                    prebu = float(parsedResult['test']['accuracy by class']['bugged']['precision'])
                    recbu = float(parsedResult['test']['accuracy by class']['bugged']['recall'])

                    F2m = mostDict[projectName].calculateF2Bugs(prebu, recbu, modelHostName)
                    bestOfBreedMost[modelHostName] =bestOfBreedMost[modelHostName] + F2m

            bestOfBreedMost[modelHostName] = bestOfBreedMost[modelHostName]/numOfProjMost
            bestOfBreedAll[modelHostName] = bestOfBreedAll[modelHostName]/numOfProjAll

    bestOfBreedAllProjectName,notImportent = findBestOfBreed(bestOfBreedAll)
    bestOfBreedMostProjectName, notImportent = findBestOfBreed(bestOfBreedMost)

    directory = "D:\Debbuger\Try"
    for projectname in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, projectname)) and (projectname[:-2] not in badWords):
            directoriesWekaModel = os.path.join(directory, projectname)
            theProjectName = projectname[:-2]
            print(directoriesWekaModel)
            for wekaFile in os.listdir(directoriesWekaModel):
                if wekaFile == 'weka':
                    weka = os.path.join(directoriesWekaModel, wekaFile)
                    trainingFileAll = os.path.join(weka, "trainingfiles_All.txt")
                    trainingFileMost = os.path.join(weka, "trainingfiles_Most.txt")

                    txtFile = open(trainingFileAll, "r")
                    parsedResultAll = weka_parser.parse_WEKA_scores(txtFile.read())

                    txtFile = open(trainingFileMost, "r")
                    parsedResultMost = weka_parser.parse_WEKA_scores(txtFile.read())

                    allDict[theProjectName].fillDetailsTrain(parsedResultAll['training']['confusion matrix']['bugged']['bugged'] +
                                                             parsedResultAll['training']['confusion matrix']['bugged']['valid'],
                                                             parsedResultAll['training']['confusion matrix']['bugged']['bugged'] +
                                                             parsedResultAll['training']['confusion matrix']['bugged']['valid'] +
                                                             parsedResultAll['training']['confusion matrix']['valid']['bugged'] +
                                                             parsedResultAll['training']['confusion matrix']['valid']['valid'])

                    mostDict[theProjectName].fillDetailsTrain(parsedResultMost['training']['confusion matrix']['bugged']['bugged'] +
                                                              parsedResultMost['training']['confusion matrix']['bugged']['valid'],
                                                              parsedResultMost['training']['confusion matrix']['bugged']['bugged'] +
                                                              parsedResultMost['training']['confusion matrix']['bugged']['valid'] +
                                                              parsedResultMost['training']['confusion matrix']['valid']['bugged'] +
                                                              parsedResultMost['training']['confusion matrix']['valid']['valid'])



    #creating the csv of "all" used to be 'wb'
    with open(os.path.join(r'D:\Debbuger\BestModel\ZRESULTS','resultsBugsAllFiles.csv'), 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['projectName', 'F2 on itself','F2 best of breed','best of breed project name',
                             'F2 best for it','best fot it project name',
                             '% bugs in train','# bugs in train','% bugs in test','# bugs in test',
                             '% bugs in train- best of breed','# bugs in train- best of breed','% bugs in test- best of breed','# bugs in test - best of breed',
                             '% bugs in train- best for it','# bugs in train- best for it','% bugs in test- best for it','# bugs in test - best for it'])

        for projextName, ProjectDetail in allDict.iteritems():
            bestforItProjectName, bestforItF2m = ProjectDetail.bestForIt()
            filewriter.writerow(
                [projextName, ProjectDetail.AllProjectModel[projextName],ProjectDetail.AllProjectModel[bestOfBreedAllProjectName],bestOfBreedAllProjectName,
                 bestforItF2m,bestforItProjectName,
                 ProjectDetail.TrainPrecent,ProjectDetail.TrainBuges,ProjectDetail.TestPrecent,ProjectDetail.TestBuges,
                 allDict[bestOfBreedAllProjectName].TrainPrecent, allDict[bestOfBreedAllProjectName].TrainBuges, allDict[bestOfBreedAllProjectName].TestPrecent,allDict[bestOfBreedAllProjectName].TestBuges,
                 allDict[bestforItProjectName].TrainPrecent, allDict[bestforItProjectName].TrainBuges,allDict[bestforItProjectName].TestPrecent, allDict[bestforItProjectName].TestBuges])


    with open(os.path.join(r'D:\Debbuger\BestModel\ZRESULTS','resultsBugsMostFiles.csv'), 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['projectName', 'F2 on itself','F2 best of breed','best of breed project name',
                             'F2 best for it','best fot it project name',
                             '% bugs in train','# bugs in train','% bugs in test','# bugs in test',
                             '% bugs in train- best of breed','# bugs in train- best of breed','% bugs in test- best of breed','# bugs in test - best of breed',
                             '% bugs in train- best for it','# bugs in train- best for it','% bugs in test- best for it','# bugs in test - best for it'])

        for projextName, ProjectDetail in mostDict.iteritems():
            bestforItProjectName, bestforItF2m = ProjectDetail.bestForIt()
            filewriter.writerow(
                [projextName, ProjectDetail.AllProjectModel[projextName],ProjectDetail.AllProjectModel[bestOfBreedMostProjectName],bestOfBreedMostProjectName,
                 bestforItF2m,bestforItProjectName,
                 ProjectDetail.TrainPrecent,ProjectDetail.TrainBuges,ProjectDetail.TestPrecent,ProjectDetail.TestBuges,
                 mostDict[bestOfBreedMostProjectName].TrainPrecent, mostDict[bestOfBreedMostProjectName].TrainBuges, mostDict[bestOfBreedMostProjectName].TestPrecent,mostDict[bestOfBreedMostProjectName].TestBuges,
                 mostDict[bestforItProjectName].TrainPrecent, mostDict[bestforItProjectName].TrainBuges,mostDict[bestforItProjectName].TestPrecent, mostDict[bestforItProjectName].TestBuges])



    print("writing completed")

def createResultsBasedOnPRC():
    directory = "D:\Debbuger\BestModel"
    allDict = {}
    bestOfBreedAll={}
    mostDict = {}
    bestOfBreedMost = {}

    for ModelHost in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, ModelHost)) and (ModelHost[:-2] not in badWords)and (ModelHost not in badWords):
            dirModelHost = os.path.join(directory, ModelHost)
            print(dirModelHost)
            numOfProjAll = 0
            numOfProjMost = 0
            modelHostName = ModelHost[:-2]
            bestOfBreedAll[modelHostName] = 0
            bestOfBreedMost[modelHostName] = 0

            for result in os.listdir(dirModelHost):

                if result.endswith("_cfiles_All.txt") and (result[:-15] not in badWords):
                    numOfProjAll = numOfProjAll  + 1
                    projectName = result[:-15]
                    if projectName not in allDict:
                        allDict[projectName] =ProjectDetails(projectName)

                    txtFile = open(os.path.join(dirModelHost, result), "r")
                    parsedResult =weka_parser.parse_WEKA_scores(txtFile.read())

                    if not allDict[projectName].isFilled():
                        allDict[projectName].fillDetailsTest(
                            parsedResult['test']['confusion matrix']['bugged']['bugged'] +
                            parsedResult['test']['confusion matrix']['bugged']['valid'],
                            parsedResult['test']['confusion matrix']['bugged']['bugged'] +
                            parsedResult['test']['confusion matrix']['bugged']['valid'] +
                            parsedResult['test']['confusion matrix']['valid']['bugged'] +
                            parsedResult['test']['confusion matrix']['valid']['valid'])

                    if(parsedResult['test']['accuracy by class']['bugged']['PRC Area']=='?'):
                        prcArea = 0
                    else:
                        prcArea = float(parsedResult['test']['accuracy by class']['bugged']['PRC Area'])

                    allDict[projectName].insertToProjects(prcArea,modelHostName)
                    bestOfBreedAll[modelHostName] =bestOfBreedAll[modelHostName] + prcArea

                if result.endswith("_cfiles_most.txt") and (result[:-16] not in badWords):
                    numOfProjMost = numOfProjMost + 1
                    projectName = result[:-16]
                    if projectName not in mostDict:
                        mostDict[projectName] = ProjectDetails(projectName)

                    txtFile = open(os.path.join(dirModelHost, result), "r")
                    parsedResult = weka_parser.parse_WEKA_scores(txtFile.read())

                    if not mostDict[projectName].isFilled():
                        mostDict[projectName].fillDetailsTest(parsedResult['test']['confusion matrix']['bugged']['bugged'] +
                                                         parsedResult['test']['confusion matrix']['bugged']['valid'],
                                                         parsedResult['test']['confusion matrix']['bugged']['bugged'] +
                                                         parsedResult['test']['confusion matrix']['bugged']['valid'] +
                                                         parsedResult['test']['confusion matrix']['valid']['bugged'] +
                                                         parsedResult['test']['confusion matrix']['valid']['valid'])

                    if (parsedResult['test']['accuracy by class']['bugged']['PRC Area'] == '?'):
                        prcArea = 0
                    else:
                        prcArea = float(parsedResult['test']['accuracy by class']['bugged']['PRC Area'])

                    mostDict[projectName].insertToProjects(prcArea, modelHostName)
                    bestOfBreedMost[modelHostName] =bestOfBreedMost[modelHostName] + prcArea

            bestOfBreedMost[modelHostName] = bestOfBreedMost[modelHostName]/numOfProjMost
            bestOfBreedAll[modelHostName] = bestOfBreedAll[modelHostName]/numOfProjAll

    bestOfBreedAllProjectName,notImportent = findBestOfBreed(bestOfBreedAll)
    bestOfBreedMostProjectName, notImportent = findBestOfBreed(bestOfBreedMost)

    directory = "D:\Debbuger\Try"
    for projectname in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, projectname)) and (projectname[:-2] not in badWords):
            directoriesWekaModel = os.path.join(directory, projectname)
            theProjectName = projectname[:-2]
            print(directoriesWekaModel)
            for wekaFile in os.listdir(directoriesWekaModel):
                if wekaFile == 'weka':
                    weka = os.path.join(directoriesWekaModel, wekaFile)
                    trainingFileAll = os.path.join(weka, "trainingfiles_All.txt")
                    trainingFileMost = os.path.join(weka, "trainingfiles_Most.txt")

                    txtFile = open(trainingFileAll, "r")
                    parsedResultAll = weka_parser.parse_WEKA_scores(txtFile.read())

                    txtFile = open(trainingFileMost, "r")
                    parsedResultMost = weka_parser.parse_WEKA_scores(txtFile.read())

                    allDict[theProjectName].fillDetailsTrain(parsedResultAll['training']['confusion matrix']['bugged']['bugged'] +
                                                             parsedResultAll['training']['confusion matrix']['bugged']['valid'],
                                                             parsedResultAll['training']['confusion matrix']['bugged']['bugged'] +
                                                             parsedResultAll['training']['confusion matrix']['bugged']['valid'] +
                                                             parsedResultAll['training']['confusion matrix']['valid']['bugged'] +
                                                             parsedResultAll['training']['confusion matrix']['valid']['valid'])

                    mostDict[theProjectName].fillDetailsTrain(parsedResultMost['training']['confusion matrix']['bugged']['bugged'] +
                                                              parsedResultMost['training']['confusion matrix']['bugged']['valid'],
                                                              parsedResultMost['training']['confusion matrix']['bugged']['bugged'] +
                                                              parsedResultMost['training']['confusion matrix']['bugged']['valid'] +
                                                              parsedResultMost['training']['confusion matrix']['valid']['bugged'] +
                                                              parsedResultMost['training']['confusion matrix']['valid']['valid'])



    #creating the csv of "all" used to be 'wb'
    with open(os.path.join(r'D:\Debbuger\BestModel\ZRESULTS','resultsPRCAllFiles.csv'), 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['projectName', 'prcArea on itself','prcArea best of breed','best of breed project name',
                             'prcArea best for it','best for it project name',
                             '% bugs in train','# bugs in train','% bugs in test','# bugs in test',
                             '% bugs in train- best of breed','# bugs in train- best of breed','% bugs in test- best of breed','# bugs in test - best of breed',
                             '% bugs in train- best for it','# bugs in train- best for it','% bugs in test- best for it','# bugs in test - best for it'])

        for projextName, ProjectDetail in allDict.iteritems():
            bestforItProjectName, bestforItF2m = ProjectDetail.bestForIt()
            filewriter.writerow(
                [projextName, ProjectDetail.AllProjectModel[projextName],ProjectDetail.AllProjectModel[bestOfBreedAllProjectName],bestOfBreedAllProjectName,
                 bestforItF2m,bestforItProjectName,
                 ProjectDetail.TrainPrecent,ProjectDetail.TrainBuges,ProjectDetail.TestPrecent,ProjectDetail.TestBuges,
                 allDict[bestOfBreedAllProjectName].TrainPrecent, allDict[bestOfBreedAllProjectName].TrainBuges, allDict[bestOfBreedAllProjectName].TestPrecent,allDict[bestOfBreedAllProjectName].TestBuges,
                 allDict[bestforItProjectName].TrainPrecent, allDict[bestforItProjectName].TrainBuges,allDict[bestforItProjectName].TestPrecent, allDict[bestforItProjectName].TestBuges])


    with open(os.path.join(r'D:\Debbuger\BestModel\ZRESULTS','resultsPRCMostFiles.csv'), 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['projectName', 'prcArea on itself','prcArea best of breed','best of breed project name',
                             'prcArea best for it','best for it project name',
                             '% bugs in train','# bugs in train','% bugs in test','# bugs in test',
                             '% bugs in train- best of breed','# bugs in train- best of breed','% bugs in test- best of breed','# bugs in test - best of breed',
                             '% bugs in train- best for it','# bugs in train- best for it','% bugs in test- best for it','# bugs in test - best for it'])

        for projextName, ProjectDetail in mostDict.iteritems():
            bestforItProjectName, bestforItF2m = ProjectDetail.bestForIt()
            filewriter.writerow(
                [projextName, ProjectDetail.AllProjectModel[projextName],ProjectDetail.AllProjectModel[bestOfBreedMostProjectName],bestOfBreedMostProjectName,
                 bestforItF2m,bestforItProjectName,
                 ProjectDetail.TrainPrecent,ProjectDetail.TrainBuges,ProjectDetail.TestPrecent,ProjectDetail.TestBuges,
                 mostDict[bestOfBreedMostProjectName].TrainPrecent, mostDict[bestOfBreedMostProjectName].TrainBuges, mostDict[bestOfBreedMostProjectName].TestPrecent,mostDict[bestOfBreedMostProjectName].TestBuges,
                 mostDict[bestforItProjectName].TrainPrecent, mostDict[bestforItProjectName].TrainBuges,mostDict[bestforItProjectName].TestPrecent, mostDict[bestforItProjectName].TestBuges])



    print("writing completed")



createResultsBasedOnPRC()

