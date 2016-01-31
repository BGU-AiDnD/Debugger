__author__ = 'amir'



class Bar_TF:


    def __init__(self):
        M_matrix=[]
        skinny_M=[]
        e_vector=[]
        diagnosis=[]

        compilation=[]
        flip=[]

    def setup(self,matrix,e,d):
        self.M_matrix = matrix
        self.e_vector = e
        self.diagnosis = d

        ##compile
        self.compile()

    def build_skinny_M(self):
        self.skinny_M = []

        for row in range(len(self.e_vector)):
            for col in range(len(self.diagnosis)):
                if (self.M_matrix[row][self.diagnosis[col]] == 1):
                    self.skinny_M[row][col] = 1
                else :
                    self.skinny_M[row][col] = 0

    def compile(self):
        #initialize compilation
        self.compilation = [[] for x in self.M_matrix]

        self.flip = [False for x in self.M_matrix]

        #build skinny M
        self.build_skinny_M()

        #process skinny M
        for i in range(len(self.skinny_M)):
            for j in range(len(self.skinny_M[0])):
                if (self.skinny_M[i][j] == 1):
                    self.compilation[i].append(j)


            if (self.e_vector[i] == 1):
                self.flip[i] = True
    
    
    def compute(self, params):
        #initialize
        result = 1.0
        temp = 1.0
        #interpret compilation
        for i in range(len(self.compilation)):

            temp = 1
            for j in self.compilation[i]:
                temp =temp* params[j]

            if (self.flip[i]):
                temp = 1 - temp

            result =result * temp

        #wrap
        return -result #as a convention, optimizers are looking for minimum!

