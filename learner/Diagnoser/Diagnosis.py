__author__ = 'amir'


class Diagnosis:
    def __init__(self):
        self.diagnosis = []
        self.probability = 0.0

    def clone(self):
        res=Diagnosis()
        res.diagnosis = list(self.diagnosis)
        res.probability = self.get_prob()
        return res

    def get_diag(self):
        return self.diagnosis

    def get_prob(self):
        return self.probability

    def __str__(self):
        return str(self.diagnosis)+" P: "+str(self.probability)

    def __repr__(self):
        return str(self.diagnosis)+" P: "+str(self.probability)






