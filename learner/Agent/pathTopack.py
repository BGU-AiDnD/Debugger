__author__ = 'amir'

project="eclipse"

def pathToPack(path):
    return path.replace("/","\\")
    if project=="eclipse":
        name=path
        if( name.endswith(".java")):
            name=path.split(".java")[0]
            elem="\\"
            if("/"in name):
                elem="/"
            name=name.split(elem+"org"+elem)[1]
            name="org."+name
            name=name.replace(elem,".")
        return name
    else:
        name=path
        if( name.endswith(".java")):
            name=path.split(".java")[0]
            elem="\\"
            if("/"in name):
                elem="/"
            spl=name.split(elem)
            splInd=1
            if "org" in spl:
                splInd=spl.index("org")
            name=".".join(spl[splInd:])
            #name=name.replace(elem,".")
        #print name,path
        return name
