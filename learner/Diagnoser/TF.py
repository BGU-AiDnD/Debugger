__author__ = 'amir'


class TF:
    def __init__(self):
        self.M_matrix=[]
        self.e_vector=[]
        self.diagnosis=[]

    def setup(self,matrix,e,d):
        self.M_matrix = matrix
        self.e_vector = e
        self.diagnosis = d

    def probabilty_TF(self,h): #should receive only diag comps
        h_dict={}
        for comp in range(len(self.M_matrix[0])):
            h_dict[comp]=0
        for comp,h_score in zip(self.diagnosis,h):
            h_dict[comp]=h_score
        #print("h_dict",h,h_dict,matrix[0])
        p_d=1.0
        all_s=""
        for activity_vec,e in zip(self.M_matrix,self.e_vector):
            p_e_d=1
            s=""
            for comp in self.diagnosis:
                if activity_vec[comp]==1:
                    p_e_d=p_e_d*h_dict[comp]
                    s=s+"h"+str(comp)
            if e==1:
                p_e_d=1-p_e_d
                s="1-"+s
            all_s=all_s+"("+s
            p_d=p_d*p_e_d
        #print(all_s)
        return -p_d

