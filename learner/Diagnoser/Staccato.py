__author__ = 'amir'


import St_Strip

L = 50

class Staccato():
    def __init__(self):
        self.calls=0

    def ochiai(self,M_matrix, e_vector, strip):
        result = {}
        for i in range(len(M_matrix[0])):
            result[i]  = strip.get_ochiai_rank(M_matrix, e_vector, i)
        return result


    def rank(self, M_matrix, e_vector,  strip):
        M = len(M_matrix[0])#No. of components
        result = []
        ochiai_vector = self.ochiai(M_matrix, e_vector, strip)

        ranks =[]
        for i in range(M):
            if (ochiai_vector[i] > 0):#!!!!!!!!!!!!!!!!!!!!!!!
                ranks.append((i, ochiai_vector[i]))

        sorted_by_second = sorted(ranks, key=lambda tup: tup[1])
        for comp,rank in sorted_by_second:
            result.append(comp)

        return result

    def is_in_all_conflicts(self, M_matrix, e_vector,  comp,  strip):
        #declare vars
        result =True

        #get unstripped true conflicts
        conflicts = strip.get_conflic_list(e_vector)
        #process

        #rule out stripped components
        if (strip.is_comp_stripped(comp)):
            result = False

        #scan all true conflicts
        for x in conflicts:
            if result == False:
                break
            if (M_matrix[x][comp] != 1 ):
                result = False

        return result


    def join(self, diagnosis,  comp):
        result = []
        i = 0
        while(i < len(diagnosis) and diagnosis[i] <= comp ):
            result.append(diagnosis[i])
            i=i+1

        result.append(comp)

        while(i < len(diagnosis)):
            result.append(diagnosis[i])
            i=i+1


        return result

    def is_subsumed(self,diagnoses, candidate):

        result = False
        current_d=[]
        ##start process
        for current_d in diagnoses:
            if result==True:
                break
        #	#first, check cardinality
            if (len(candidate) >= len(current_d)):
                combined=[x for x in current_d if x in candidate]
                if len(combined)==len(current_d):
                    result=True
                    break
        return result

    def runStrip(self, M_matrix, e_vector, strip):
        self.calls=self.calls+1
        if (self.calls > L):
            return []
        #declare vars
        diagnoses = []
        diagnoses_tag=[]
        ranking = [] #rank vector
        temp_d=[] #temporary diagnosis
        temp_strip=None

        #process
        ranking = self.rank(M_matrix, e_vector, strip) #rank components

        unstripped_comps = strip.unstripped_comps_array_Func()

        if (unstripped_comps != []):
            for comp in unstripped_comps:
                if (self.is_in_all_conflicts(M_matrix, e_vector, comp, strip)):
                    #insert component as a single fault diagnosis
                    temp_d = []
                    temp_d.append(comp)
                    diagnoses.append(temp_d)

                    #"remove" this component from matrix
                    strip.strip_comp(comp)
                #end if
            #end for

        #generate rest of diagnoses
        i = 0
        while(i < len(ranking)):
            #make sure component hasn't been striped
            j = ranking[i]
            if (strip.is_comp_stripped(j)):
                i=i+1
                continue
            #strip (if in limits)
            if (self.calls <= L):
                temp_strip = strip.clone()
                temp_strip.strip(M_matrix, e_vector, j)
                diagnoses_tag = self.runStrip(M_matrix, e_vector, temp_strip)
            else:
                break

            #scan "tag" diagnoses
            for  tag_diag in  diagnoses_tag:
                temp_d = self.join(tag_diag,j)
                if ( not self.is_subsumed(diagnoses, temp_d)):
                    diagnoses.append(temp_d)
            #end inner loop

            i=i+1
        #end outer loop
        return diagnoses

    def run(self, M_matrix,  e_vector):
        #for debug
        self.calls = 0

        N = len(M_matrix)
        M = len(M_matrix[0])

        strip =St_Strip.St_Strip(M, N)


        result = self.runStrip(M_matrix, e_vector, strip)

        return result

	















