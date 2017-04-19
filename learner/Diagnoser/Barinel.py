__author__ = 'amir'

import Staccato
import Diagnosis

import math
import TF
import random
import csv
import sys

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
            prob *= self.prior_probs[comps[i]]
        return prob

    def generate_probs(self):
        new_diagnoses = []
        probs_sum = 0.0
        for diag in self.diagnoses:
            dk = 0.0
            if (self.prior_probs == []):
                dk = math.pow(prior_p,len(diag.get_diag())) #assuming same prior prob. for every component.
            else:
                dk = self.non_uniform_prior(diag)
            tf = TF.TF(self.M_matrix,self.e_vector,diag.get_diag())
            e_dk = tf.maximize()
            diag.probability=e_dk * dk #temporary probability
            probs_sum += diag.probability
        for diag in self.diagnoses:
            temp_prob = diag.get_prob() / probs_sum
            diag.probability=temp_prob
            new_diagnoses.append(diag)
        self.diagnoses = new_diagnoses


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

def load_file_with_header(file):
    with open(file,"r") as f:
        lines = list(csv.reader(f))
        probs=[float(x) for x in lines[0]]
        comps_num=len(probs)
        tests = lines[1:]
        erorr_vector = [int(t[comps_num]) for t in  tests]
        Matrix = [[int(float(y)) for y in x[:comps_num]] for x in  tests]
        ans = Barinel()
        ans.set_prior_probs(probs)
        ans.set_matrix_error(Matrix,erorr_vector)
        return ans



def main(matrix_file, out_file):
    bar = load_file_with_header(matrix_file)
    diags = bar.run()
    sorted_diags = sorted(diags, key=lambda d: d.probability, reverse=True)
    with open(out_file, "wb") as f:
        f.write(str(sorted_diags))

if __name__=="__main__":
    if len(sys.argv) != 3:
        print "Usage: Barinel.py matrix_file out_file"
        exit()
    main(sys.argv[1], sys.argv[2])


