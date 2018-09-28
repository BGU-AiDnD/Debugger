import os

#import learner.wekaMethods
#import learner.utilsConf

current_dir = os.path.dirname(os.path.abspath(__file__))
utilsPath = os.path.realpath(os.path.join(current_dir, "../utils"))

#mycomp:
#wekaJar = 'C:\\Users\\USER\\Documents\\Debugger\\Debugger\\utils\\weka.jar'#os.path.join(utilsPath, "weka.jar")

#server:
wekaJar = 'C:\\Users\\inbalros\\PycharmProjects\\Debugger\\utils\\weka.jar'


def mkOneDir(dir):
    if not os.path.isdir(dir):
            os.mkdir(dir)


def createBuildMLModels(weka,workingDir):
    for buggedType in ["All", "Most"]:
        trainingFile, testingFile, NamesFile, outCsv=BuildMLFiles(weka,buggedType,"files")
        BuildWekaModel(weka,trainingFile,testingFile,"files_"+buggedType,wekaJar)
        trainingFile, testingFile, NamesFile, outCsv=BuildMLFiles(weka,buggedType,"methods")
        BuildWekaModel(weka,trainingFile,testingFile,NamesFile,outCsv,"methods_"+buggedType,wekaJar)


def BuildMLFiles(outDir, buggedType, component):
    trainingFile=os.path.join(outDir,buggedType+"_training_"+component+".arff")
    testingFile=os.path.join(outDir,buggedType+"_testing_"+component+".arff")
    NamesFile=os.path.join(outDir,buggedType+"_names_"+component+".csv")
    outCsv=os.path.join(outDir,buggedType+"_out_"+component+".csv")
    return trainingFile, testingFile , NamesFile, outCsv


def BuildWekaModel(weka, training, testing, name, wekaJar):
    algorithm="weka.classifiers.trees.RandomForest -I 1000 -K 0 -S 1 -num-slots 1 "
    os.system("cd /d "+ weka +" & java -Xmx2024m  -cp "+(wekaJar)+" weka.Run " +algorithm+ " -x 10 -d .\\model"+name+".model -t "+training+" > training"+name+".txt")
    algorithm="weka.classifiers.trees.RandomForest"
    os.system("cd /d  "+ (weka) +" & java -Xmx2024m  -cp "+ (wekaJar) +" weka.Run " +algorithm+ " -l .\\model"+name+".model -T "+testing+" -classifications \"weka.classifiers.evaluation.output.prediction.CSV -file testing"+name+".csv\" ")
    os.system("cd /d  "+ (weka) +" & java -Xmx2024m  -cp "+ (wekaJar) +" weka.Run " +algorithm+ " -l .\\model"+name+".model -T "+testing+" > testing"+name+".txt ")


def RunTestingFiles(weka, testing, name, wekaJar):
    algorithm="weka.classifiers.trees.RandomForest"
    #os.system("cd /d  "+ (weka) +" & java -Xmx2024m  -cp "+ (wekaJar) +" weka.Run " +algorithm+ " -l .\\model"+name+".model -T "+testing+" -classifications \"weka.classifiers.evaluation.output.prediction.CSV -file testing"+name+".csv\" ")
    os.system("cd /d  "+ (weka) +" & java -Xmx2024m  -cp "+ (wekaJar) +" weka.Run " +algorithm+ " -l .\\bestModel.model -T "+testing+" > "+name+".txt ")

def buildAllModels():
    directory = "C:\\amirelm\\projects"
    for filename in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, filename)) and filename[-2:]=="_c":
            directoriesWekaModel = os.path.join(directory, filename)
            print(directoriesWekaModel)
            for wekaFile in os.listdir(directoriesWekaModel):
                if wekaFile == 'weka':
                    weka = os.path.join(directoriesWekaModel, wekaFile)
                    print(weka)
                    #here we have the weka file - find all the arff file:
                    createBuildMLModels(weka,directoriesWekaModel )


def runOnBestModel():
    directory = "D:\Debbuger\ZBestM"
    for filename in os.listdir(directory):
           if filename.endswith('.arff'):
               testingWeka = os.path.join(directory, filename)
               print(testingWeka)
               print(filename)
               RunTestingFiles(directory,testingWeka,filename,wekaJar)


buildAllModels()