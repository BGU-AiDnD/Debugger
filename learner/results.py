__author__ = 'Amir-pc'

import csv
import os.path


def get_diag(diagFile):
    diags=[]
    probs=[]
    with open(diagFile,"r") as f:
        reader =csv.reader(f)
        for i in reader:
            diags.append(i[:len(i)-2])
            probs.append(i[len(i)-1])
    return  (diags[:1],probs[:1])

def get_sen(diagFile):
    sen=open(diagFile).readlines()
    sen1=sen[0].split()
    sen=sen1[1:(len(sen1)-1)]
    ans=[]
    for s in sen1:
        if '[' in s:
            s=s.split('[')[1]
        if ',' in s:
            s=s.split(',')[0]
        if ']' in s:
            s=s.split(']')[0]
        ans=ans+[s]
    return ans

def yes_inds(fil):
    with open(fil, 'r') as f:
        reader = csv.reader(f)
        return [i for i in reader]


def results(basePath , yes_file):
    all=[]
    cov=[]
    for i in [5*t for t in range(16) if t!=0]:
        O=basePath+"\\results\\"+"i=_"+str(i)+".csv"
        writes=[["index","#comps","real bugs","algorithm","diagnosis","prob","fp","fn","tp","tn","accur","recall"]]
        for j in range(16):
            fi=yes_file+"i="+str(i)+"j="+str(j)+".csv"
            if not (os.path.isfile(fi)):
                continue
            Out2=basePath+"\\OPT__i=_"+str(i)+"j=_"+str(j)+"_.txt"
            diagRand=basePath+"\\out\\"+"\\DIFG_check_OPT__i=_"+str(i)+"j=_"+str(j)+"_Rand.csv.csv"
            diagUni=basePath+"\\out\\"+"\\DIFG_check_OPT__i=_"+str(i)+"j=_"+str(j)+"_Uni.csv.csv"
            diagWek=basePath+"\\out\\"+"\\DIFG_check_OPT__i=_"+str(i)+"j=_"+str(j)+"_Wek.csv.csv"
            if not (os.path.isfile(diagWek)):
                continue
            s = get_sen(Out2)
            yes=yes_inds(fi)[0]
            no=[str(i2) for i2 in range(len(s)) if str(i2) not in yes]
            s_no= [ttt for ttt in s if ttt in no]
            s_yes=[ttt for ttt in s if ttt in yes]
            if s_yes==[]:
                continue
            diags=[]
            probs=[]
            for t1 in [diagWek,diagRand,diagUni]:
                a,b=get_diag(t1)
                #a1=  [ [s[int(place1)] for place1 in place]    for place in a]
                diags=diags+[a]
                probs=probs+[b]
            algs=["Weka","Random","Uniform"]
            sen_num="i=_"+str(i)+"j=_"+str(j)+"_"
            nums=[sen_num,sen_num,sen_num]
            write1=[sen_num,len(s),s_yes]
            #writes=writes+[[sen_num,s_yes,len(s)]]
            for a,d,p in zip(algs,diags,probs):
                write2=[]
                if(len(d)!=0):
                    write2=write1+[a]
                    #writes=writes+[["","",a]]
                acc_avg=0.0
                recall_avg=0.0
                done=False
                fixed=[]
                fix_prob=0
                fix_count=0.0
                for dg,pr,orde in zip(d,p,[i3+1 for i3 in range(len(d))]):
                    if(not done):
                        fixed=fixed+dg
                        fix_prob=fix_prob+float(pr)
                        fix_count=fix_count+1
                        done= 0==len([amir for amir in s_yes if amir not in fixed])
                    fp=len([i1 for i1 in dg if i1 in s_no])
                    fn=len([i1 for i1 in s_yes if i1 not in dg])
                    tp=len([i1 for i1 in dg if i1 in s_yes])
                    all = all +[(float(tp)/len(s_yes),s_yes)]
                    tn=len([i1 for i1 in s_no if i1 not in dg])
                    if((tp+fp)==0):
                        accur="undef"
                    else:
                        accur=(tp+0.0)/float(tp+fp)
                        accur=accur*float(pr)
                        acc_avg=acc_avg+accur
                    if((tp+fn)==0):
                        recall="undef"
                    else:
                        recall=tp/float(tp+fn)
                        recall=recall*float(pr)
                        recall_avg=recall_avg+recall
                    #r=["","","",dg,pr,orde,fp,fn,tp,tn,accur,recall]
                    r=write2+[dg,pr,fp,fn,tp,tn,accur,recall]
                    writes=writes+[list(r)]
                if(len(d)!=0):
                    acc_avg=acc_avg/len(d)
                    recall_avg=recall_avg/len(d)
                    non_faulty=len([nony for nony in no if nony in [int(kk) for kk in fixed]])
                    cov=cov+[done]
                    #writes=writes+[["result:",acc_avg,recall_avg,done,fix_prob,fix_count,non_faulty]]
        with open(O, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(writes)
    all=[a for a in reversed(sorted([d[0] for d in all]))]





def sorted_comps(basePath , yes_file):
    arr=[]
    for i in [5*t for t in range(16) if t!=0]:
        for j in range(16):
            fi=yes_file+"i="+str(i)+"j="+str(j)+".csv"
            if not (os.path.isfile(fi)):
                continue
            Out2=basePath+"\\OPT__i=_"+str(i)+"j=_"+str(j)+"_.txt"
            diagWek=basePath+"\\DIFG_check_OPT__i=_"+str(i)+"j=_"+str(j)+"_Wek.csv.csv"
            if not (os.path.isfile(diagWek)):
                continue
            yes=yes_inds(fi)[0]
            if (yes==[]):
                continue
            s = get_sen(Out2)
            arr=arr+[(len(s),"i=_"+str(i)+"j=_"+str(j))]
    return sorted(arr,cmp=lambda d1,d2: d1[0]-d2[0])


dir="C:\Users\Amir-pc\Documents\GitHub\\tom\\"
if not (os.path.isdir(dir+"\\results\\")):
    os.mkdir(dir+"\\results\\")
print results(dir,dir+"\\yesInds")
#print sorted_comps(dir,dir+"\\yesInds")
