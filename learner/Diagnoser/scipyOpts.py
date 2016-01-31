__author__ = 'amir'


import scipy.optimize#.minimize
import random
from scipy.optimize import minimize, rosen, rosen_der


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

lb=[0 for x in d]
ub=[1 for x in d]
initialGuess=[random.uniform(0, 1) for x in d ]

for methodC in ["Nelder-Mead","Powell","CG","BFGS","L-BFGS-B","TNC","COBYLA","SLSQP"]:
    probs=[]
    for d in [[0,1],[0,2]]:
        res=scipy.optimize.minimize(probabilty_TF,initialGuess,method=methodC,jac=False)
        probs.append(-probabilty_TF(res.x))
    probs=[p/sum(probs) for p in probs]
    #print  -probabilty_TF(res.x),res.x,methodC
    print  probs,methodC
#exit()
for methodC in []:#["Newton-CG","dogleg","trust-ncg"]:
    res=scipy.optimize.minimize(probabilty_TF,initialGuess,method=methodC)
    print methodC ,-probabilty_TF(res.x),res.x

boundsC=tuple(zip(lb,ub))
for methodC in ["L-BFGS-B","TNC","SLSQP"]:
    probs=[]
    for d in [[0,1],[0,2]]:
        res=scipy.optimize.minimize(probabilty_TF,initialGuess,method=methodC,bounds=boundsC,jac=False)
        probs.append(-probabilty_TF(res.x))
    probs=[p/sum(probs) for p in probs]
    #print  -probabilty_TF(res.x),res.x,methodC
    print  probs,methodC

    #res=scipy.optimize.minimize(probabilty_TF,initialGuess,method=methodC,bounds=boundsC,jac=False)
    #print -probabilty_TF(res.x),res.x,"bound",methodC
exit()
res=scipy.optimize.minimize(probabilty_TF,initialGuess,method="TNC",bounds=tuple(zip(lb,ub)),jac=False)
#res=scipy.optimize.minimize(probabilty_TF,initialGuess,method="SLSQP",jac=False)
print res.x
print res["x"]
print "out" ,-probabilty_TF(res.x)
print "out" ,-probabilty_TF(initialGuess)


exit()
x0 = [1.3, 0.7, 0.8, 1.9, 1.2]
res = minimize(rosen, x0, method='Nelder-Mead')
print res.x

res = minimize(rosen, x0, method='BFGS', jac=rosen_der,options={'gtol': 1e-6, 'disp': True})
print res.x

fun = lambda x: (x[0] - 1)**2 + (x[1] - 2.5)**2

cons = ({'type': 'ineq', 'fun': lambda x:  x[0] - 2 * x[1] + 2},{'type': 'ineq', 'fun': lambda x: -x[0] - 2 * x[1] + 6},{'type': 'ineq', 'fun': lambda x: -x[0] + 2 * x[1] + 2})
bnds = ((0, None), (0, None))
res = minimize(fun, (2, 0), method='SLSQP', bounds=bnds,constraints=cons)
print res.x


