__author__ = 'amir'


import arff

def arff_build(attributes, data,desc,relation):
    dict={}
    dict['attributes']=attributes
    dict['data']=data
    dict['description']=desc
    dict['relation']=relation
    return dict


def write_to_arff(data,filename):
    f = open(filename, 'w')
    f.write(arff.dumps(data))
    f.close()

def load_arff(filename):
    f = open(filename, 'r')
    arf= arff.loads(f.read())
    f.close()
    return arf

