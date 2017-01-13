__author__ = 'amir'

import Staccato
import Diagnosis

import math
import TF
import random
import scipy.optimize
import csv

prior_p = 0.05

class Barinel:

    def __init__(self):
        self.M_matrix = []
        self.e_vector = []
        self.prior_probs = []
        self.diagnoses = []


    def set_matrix_error(self,M,e):
        self.M_matrix = M
        self.e_vector = e

    def set_prior_probs(self, probs):
        self.prior_probs=probs


    def non_uniform_prior(self, diag):
        comps = diag.get_diag()
        prob = 1
        for i in range(len(comps)):
            prob =prob * self.prior_probs[comps[i]]
        return prob

    def generate_probs(self):
        #declare vars
        #temp_probs = new double[diagnoses.size()]
        new_set = []
        probs_sum = 0.0

        #start process
        for  temp_diagnosis in  self.diagnoses:
            #setup target function
            TargetFunc =TF.TF()
            TargetFunc.setup(self.M_matrix,self.e_vector,temp_diagnosis.get_diag())
            dim = len(temp_diagnosis.get_diag()) #deduce dimensions
            #optimize according to designated tehnique
            x = []
            e_dk = 0.0
            dk = 0.0
            lb=[0 for x in temp_diagnosis.get_diag()]
            ub=[1 for x in temp_diagnosis.get_diag()]
            initialGuess=[random.uniform(0, 1) for x in temp_diagnosis.get_diag()]
            boundsC=tuple(zip(lb,ub))
            res=scipy.optimize.minimize(TargetFunc.probabilty_TF,initialGuess,method="L-BFGS-B",bounds=boundsC,jac=False)
            x = res.x
            e_dk = -TargetFunc.probabilty_TF(x)

            dk=0
            if (self.prior_probs == []):
                dk = math.pow(prior_p,len(temp_diagnosis.get_diag())) #assuming same prior prob. for every component.

            else:
                dk = self.non_uniform_prior(temp_diagnosis)

            temp_diagnosis.probability=e_dk * dk #temporary probability

            #update probabilities sum
            probs_sum =probs_sum+ temp_diagnosis.probability

            #save h probabilities
            temp_diagnosis.h_list=x

        #normalize probabilities (and order them)
        temp_prob=0
        for  temp_diagnosis in self.diagnoses:
            #normalize
            temp_prob = temp_diagnosis.get_prob() / probs_sum

            #round

            #set
            temp_diagnosis.probability=temp_prob

            new_set.append(temp_diagnosis)

        self.diagnoses = new_set


    def run(self):
        #initialize
        self.diagnoses = []
        diags = Staccato.Staccato().run(self.M_matrix, self.e_vector)
        for  diag in diags:
            d=Diagnosis.Diagnosis()
            d.diagnosis=diag
            self.diagnoses.append(d)

        #generate probabilities
        self.generate_probs()

        return self.diagnoses

def load_file_with_header( file):
    reader=csv.reader(open(file,"r"))
    lines=[x for x in reader]
    ans= Barinel()
    probs=[float(x) for x in lines[0][:-1]]
    lines=lines[1:]
    comps_num=len(probs)
    erorr_vector=[int(x[comps_num]) for x in  lines]
    Matrix=[[int(y) for y in x[:comps_num]] for x in  lines]
    ans.set_matrix_error(Matrix,erorr_vector)
    ans.set_prior_probs(probs)
    return ans



if __name__=="__main__":
    matrix=[]
    error_vec=[]
    matrix.append([1,1,0])
    matrix.append([0,1,1])
    matrix.append([1,0,0])
    matrix.append([1,0,1])
    error_vec.extend([1,1,1,0])
    bar=Barinel()
    bar.set_matrix_error(matrix,error_vec)
    diags=bar.run()

    bar=load_file_with_header("C:\GitHub\matrix\OPT__Rand.csv")
