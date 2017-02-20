__author__ = 'amir'

from pyswarm import pso

def banana(x):
    x1 = x[0]
    x2 = x[1]
    return x1**4 - 2*x2*x1**2 + x2**2 + x1**2 - 2*x1 + 5

def con(x):
    x1 = x[0]
    x2 = x[1]
    return [-(x1 + 0.25)**2 + 0.75*x2]

lb = [-3, -1]
ub = [2, 6]

#xopt, fopt = pso(banana, lb, ub, f_ieqcons=con)

#print xopt, fopt



# usage for barinel

matrix=[]
error_vec=[]
d=[]
matrix.append([1,1,0])
matrix.append([0,1,1])
matrix.append([1,0,0])
matrix.append([1,0,1])
error_vec.extend([1,1,1,0])
d.extend([0,1])

def probabilty_TF(h): #should receive only diag comps
    h_dict={}
    for comp in range(len(matrix[0])):
        h_dict[comp]=0
    for comp,h_score in zip(d,h):
        h_dict[comp]=h_score
    #print("h_dict",h,h_dict,matrix[0])
    p_d=1.0
    all_s=""
    for activity_vec,e in zip(matrix,error_vec):
        p_e_d=1
        s=""
        for comp in d:
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

lb=[0 for _ in d]
# ub=[1 for _ in d]
#ub=[1 for x,ind in enumerate(matrix[0]) if ind ]


xopt, fopt = pso(probabilty_TF, lb, ub,swarmsize =1000,maxiter =10000000)
print -fopt


# print -probabilty_TF([0.47,0.19])
# print -probabilty_TF([0.41,0.5])
