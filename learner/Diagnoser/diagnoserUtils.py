import Diagnoser.ExperimentInstance

__author__ = 'amir'

import csv
import Barinel
import sys
import os


class FullMatrix:
    def __init__(self):
        self.matrix=[] # matrix size define the num of tests
        self.probabilities=[] # probabilities size define the num of components
        self.error=[]

    def convetTodynamicSpectrum(self):
        ans=dynamicSpectrum()
        ans.probabilities=self.probabilities
        ans.error=list(self.error)
        testsD=[[y[0] for y in enumerate(x) if y[1]==1] for x in self.matrix]
        ans.TestsComponents=testsD
        return ans

    def diagnose(self):
        bar=Barinel.Barinel()
        bar.set_matrix_error(self.matrix,self.error)
        bar.set_prior_probs(self.probabilities)
        return bar.run()

    def save_to_csv_file(self, out_file):
        import csv
        lines = [self.probabilities] + map(lambda x : x[0] + [x[1]] ,zip(self.matrix, self.error))
        with open(out_file, "wb") as f:
            writer = csv.writer(f)
            writer.writerows(lines)

    # optimization: remove unreachable components & components that pass all their tests
    # return: optimized FullMatrix, chosen_components( indices)
    @staticmethod
    def optimize_FullMatrix(fullMatrix):
        chosen=[]
        UnusedComps=range(len(fullMatrix.probabilities))
        for test,err in zip(fullMatrix.matrix,fullMatrix.error):
            if err==0:
                continue
            for comp in list(UnusedComps):
                if test[comp]==1:
                    chosen.append(comp)
                    UnusedComps.remove(comp)
        optimizedMatrix=FullMatrix()
        optimizedMatrix.probabilities=[x[1] for x in enumerate(fullMatrix.probabilities) if x[0] in chosen]
        newErr=[]
        newMatrix=[]
        for test,err in zip(fullMatrix.matrix,fullMatrix.error):
            newTest=[x[1] for x in enumerate(test) if x[0] in chosen]
            if 1 in newTest: ## optimization could remove all comps of a test
                newMatrix.append(newTest)
                newErr.append(err)
        optimizedMatrix.matrix=newMatrix
        optimizedMatrix.error=newErr
        return optimizedMatrix,sorted(chosen)


class dynamicSpectrum:
    def __init__(self):
        self.TestsComponents=[] # TestsComponents size define the num of tests
        self.probabilities=[] # probabilities size define the num of components
        self.error=[]

    def convertToFullMatrix(self):
        ans=FullMatrix()
        ans.probabilities=list(self.probabilities)
        ans.error=list(self.error)
        ans.matrix=[[1 if i in x else 0 for i in range(len(self.probabilities)) ] for x in self.TestsComponents]
        return ans

    #return diagnoses
    def diagnose(self):
        fullM,chosen=FullMatrix.optimize_FullMatrix(self.convertToFullMatrix())
        chosenDict=dict(enumerate(chosen))
        Opt_diagnoses=fullM.diagnose()
        diagnoses=[]
        for diag in Opt_diagnoses:
            diag=diag.clone()
            diag_comps=[chosenDict[x] for x in diag.diagnosis]
            diag.diagnosis=list(diag_comps)
            diagnoses.append(diag)
        return diagnoses


def readMatrixWithProbabilitiesFile(fileName):
    reader=csv.reader(open(fileName,"r"))
    lines=[x for x in reader]
    probabilies=[float(x) for x in  lines[0][:-1]]
    matrix=[]
    error=[]
    lines=[[int(y) for y in x ] for x in lines[1:]]
    for line in lines:
        error.append(line[-1])
        matrix.append(line[:-1])
    ans=FullMatrix()
    ans.probabilities=probabilies
    ans.matrix=matrix
    ans.error=error
    return ans

def readPlanningFile(fileName):
    lines=open(fileName,"r").readlines()
    lines=[x.replace("\n","") for x in lines]
    sections=["[Priors]","[Bugs]","[InitialTests]","[TestDetails]"]
    sections=[lines.index(x) for x in sections]
    priorsStr,BugsStr,InitialsStr,TestDetailsStr=tuple([lines[x[0]+1:x[1]] for x in zip(sections,sections[1:]+[len(lines)])])
    priors=eval(priorsStr[0].replace("\n",""))
    bugs=[eval(x) for x in BugsStr]
    initials=[eval(x) for x in InitialsStr]
    testsPool=[]
    error=[]
    for td in TestDetailsStr:
        ind,actualTrace,guessTrace,err=tuple(td.split(";"))
        actualTrace=eval(actualTrace)
        err=int(err)
        testsPool.append(actualTrace)
        error.append(err)
    Diagnoser.ExperimentInstance.set_values(priors, bugs, testsPool)
    return Diagnoser.ExperimentInstance.ExperimentInstance(initials, error)


def diagnoseTests():
    full = readMatrixWithProbabilitiesFile("C:\GitHub\matrix\OPT__Rand.csv")
    print "full",[x.diagnosis for x in full.diagnose()]
    ds = full.convetTodynamicSpectrum()
    matrix_ = ds.convertToFullMatrix()
    print "matrix",[x.diagnosis for x in matrix_.diagnose()]
    Fullm,chosen=FullMatrix.optimize_FullMatrix(matrix_)
    print "matrixOPT",[x.diagnosis for x in Fullm.diagnose()] ## should result wrong comps!!
    print [x.diagnosis for x in ds.diagnose()]




def readMatrixTest():
    global full, ds
    full = readMatrixWithProbabilitiesFile("C:\GitHub\matrix\OPT__Rand.csv")
    print full.probabilities, len(full.probabilities)
    print full.error[0]
    print full.matrix[0]
    ds = full.convetTodynamicSpectrum()
    print ds.probabilities
    print ds.error[0]
    print ds.TestsComponents[0]
    matrix_ = ds.convertToFullMatrix()
    print matrix_.probabilities
    opt = FullMatrix.optimize_FullMatrix(matrix_)
    print opt.probabilities
    print len(opt.error), len(matrix_.error)



def readPlannerTest():
    global instance
    print "planner"
    file="C:\projs\\40_uniform_9.txt"
    instance = readPlanningFile(file)
    # print instance.priors
    # print instance.error
    # print instance.bugs
    # print instance.initial_tests
    # print instance.pool[0]
    instance.initial_tests=range(len(instance.error))
    instance.diagnose()
    print [x.diagnosis for x in instance.diagnoses]
    ds=instance.initials_to_DS()
    print [x.diagnosis for x in ds.diagnose()]
    fm=ds.convertToFullMatrix()
    print [x.diagnosis for x in fm.diagnose()]

    # print fm.error
    # for i in range(len(fm.error)):
    #     print fm.matrix[i]

def write_diagnoses_file(out_file):
    pass


def calc_result_fo_planning_file(planning_file, out_file):
    global instance
    instance = readPlanningFile(planning_file)
    precision, recall = instance.calc_precision_recall()
    csv_output = [["precision", "recall"], [precision, recall]]
    print instance.count_different_cases() , precision, recall
    with open(out_file, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(csv_output)


def dll_diagnosis(matrix_file_name="dll_diagnosis.txt", result_file_name="dll_diagnosis_result.txt"):
    for dir_name in ["CVE-2016-7531", "CVE-2016-7533", "CVE-2016-7535", "CVE-2016-7906", "CVE-2016-8866",
                     "CVE-2016-9556", "CVE-2017-5506", "CVE-2017-5508", "CVE-2017-5509", "CVE-2017-5510",
                     "CVE-2017-5511"]:
        fuzzing_dir = os.path.join(r"C:\vulnerabilities\ImageMagick_exploited", dir_name, "fuzzing")
        planning_file = os.path.join(fuzzing_dir, matrix_file_name)
        out_file = os.path.join(fuzzing_dir, result_file_name)
        print planning_file
        try:
            calc_result_fo_planning_file(planning_file, out_file)
        except:
            print "failed"


if __name__=="__main__":
    dll_diagnosis("function_diagnosis_matrix.txt", "function_diagnosis_result.csv")
