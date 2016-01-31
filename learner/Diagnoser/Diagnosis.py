__author__ = 'amir'


class Diagnosis:
    def __init__(self):
        self.diagnosis = []
        self.probability = 0.0
        self.h_list = []
        self.sorted = False

    def clone(self):
        res=Diagnosis()
        res.diagnosis = list(self.diagnosis)
        res.probability = self.get_prob()
        res.h_list = list(self.h_list)
        res.sorted = self.sorted
        return res

    def get_diag(self):
        return self.diagnosis

    def get_prob(self):
        return self.probability

    def __str__(self):
        return str(self.diagnosis)+" P: "+str(self.probability)






