__author__ = 'Amir-pc'


def packsFroMets(mets):
    f = open(mets)
    lines=f.readlines()
    f.close()
    packs=set()
    for i in lines:
        p= i.split("(")[0]
        p= p.split(".")
        #p=p[:len(p)-2]
        p= ".".join(p)
        packs.add(p)
    return packs

def methsTest(packs):
    tests=[]
    for i in packs:
        p= i.split(".")
        p=p[len(p)-1]
        if "test" in p:
            tests=tests+[i]
    return tests


def paksInstOtTests(packs):
    inst=[]
    test=[]
    for i in packs:
        if "test" in i:
            test=test+[i]
        else:
            inst=inst+[i]
    return test,inst

def dirEntries(packs,dirfile):
    f= open(dirfile)
    lines=f.readlines()
    target=[i.split("\n")[0]  for i in lines if "target\\classes\\" in i]
    tarPacks=[i.split("target\\classes\\")[1] for i in target]
    tarPacks=[".".join(i.split("\\")) for i in tarPacks]
    ans=[]
    for i in range(len(tarPacks)):
        if tarPacks[i] in packs:
            ans=ans+[target[i].split("target\\classes\\")[0]+"target\\classes"]
            #ans=ans+[target[i]]
    return list(set(ans))

def dirRepo(file):
    f= open(file)
    lines=f.readlines()
    target=[i.split("\n")[0]  for i in lines if ".jar" in i]
    ans=[]
    for i in target:
        a=i.split("\\")
        a="\\".join(a[:len(a)-1])
        ans=ans+[a]
    f.close()
    return list(set(ans))

def compiliedTests(tests,dirs):
    t=open(tests)
    tes=t.readlines()
    tes=[i.split("\n")[0] for i in tes]
    reduced=tes#[".".join(i.split(".")[:4]) for i in tes]
    t.close()
    d=open(dirs)
    dir1=d.readlines()
    d.close()
    dir1=dir1[:len(dir1)-1]
    dir1=[i.split("\\")[6] for i in dir1]
    #dir1=[".".join(i.split(".")[:4]) for i in dir1]
    ans=[]
    for i in range(len(reduced)):
        if (reduced[i] in dir1) :
            ans=ans+[tes[i]]
    return ans


comp= compiliedTests("C:\\GitHub\\Gzoltar\\tests.txt","C:\\GitHub\\Gzoltar\\dirs2.txt")
print (comp)
#exit()
f=open("C:\\GitHub\\Gzoltar\\tests3.txt","wb")
f.writelines("\n".join([i for i in comp]))
f.close()

exit()
rep=dirRepo("C:\\GitHub\\Gzoltar\\dir.txt")
f=open("C:\\GitHub\\Gzoltar\\dir_Gzoltar.txt","wb")
f.writelines("\n".join([i for i in rep]))
f.close()

exit()
packs = list(packsFroMets("C:\\GitHub\\backkup\\meths_names.txt"))
#print([i for i in packs])
t= methsTest(packs)
f=open("C:\\GitHub\\backkup\\meths_Gzoltar.txt","wb")
f.writelines("\n".join([i for i in t]))
f.close()
exit()
mets = open("C:\\Users\\Amir-pc\\Documents\\GitHub\\backkup\\AllPacks.txt","r")
x= paksInstOtTests([i.split("\n")[0] for i in mets.readlines()])
mets.close()
#print len(x[0])
#print len(x[1])
dirs= dirEntries(x[0]+x[1],"C:\\Users\\Amir-pc\\Documents\\GitHub\\backkup\\CDT_8_1_2\\org.eclipse.cdt\\dir3.txt")
f=open("C:\\Users\\Amir-pc\\Documents\\GitHub\\Gzoltar\pakcs.txt","wb")
#f.writelines("\n".join(x[1]))
f.close()
f=open("C:\\Users\\Amir-pc\\Documents\\GitHub\\Gzoltar\\tests.txt","wb")
#f.writelines("\n".join(x[0]))
f.close()
f=open("C:\\Users\\Amir-pc\\Documents\\GitHub\\Gzoltar\\dirs2.txt","wb")
#f.writelines("\n".join(dirs))
f.close()