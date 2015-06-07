__author__ = 'Amir-pc'

import arff
import csv
import math
import os

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

data={
    u'attributes': [
        (u'outlook', [u'sunny', u'overcast', u'rainy']),
        (u'temperature', u'REAL'),
        (u'humidity', u'REAL'),
        (u'windy', [u'TRUE', u'FALSE']),
        (u'play', [u'yes', u'no'])],
    u'data': [
        [u'sunny', 85.0, 85.0, u'FALSE', u'no'],
        [u'sunny', 80.0, 90.0, u'TRUE', u'no'],
        [u'overcast', 83.0, 86.0, u'FALSE', u'yes'],
        [u'rainy', 70.0, 96.0, u'FALSE', u'yes'],
        [u'rainy', 68.0, 80.0, u'FALSE', u'yes'],
        [u'rainy', 65.0, 70.0, u'TRUE', u'no'],
        [u'overcast', 64.0, 65.0, u'TRUE', u'yes'],
        [u'sunny', 72.0, 95.0, u'FALSE', u'no'],
        [u'sunny', 69.0, 70.0, u'FALSE', u'yes'],
        [u'rainy', 75.0, 80.0, u'FALSE', u'yes'],
        [u'sunny', 75.0, 70.0, u'TRUE', u'yes'],
        [u'overcast', 72.0, 90.0, u'TRUE', u'yes'],
        [u'overcast', 81.0, 75.0, u'FALSE', u'yes'],
        [u'rainy', 71.0, 91.0, u'TRUE', u'no']
    ],
    u'description': u'',
    u'relation': u'weather'
}


attr = [( "filename", "STRING"), ( "tot_changes", "NUMERIC"), ( "sum_insert", "NUMERIC"),
                ( "sum_delets", "NUMERIC"), ( "tot_bugs", "NUMERIC"), ( "tot_developers", "NUMERIC"),
                ( "change_set", "NUMERIC"), ( "Operators_count", "NUMERIC"), ( "Operands_count", "NUMERIC"),
                ( "Distinct_operators", "NUMERIC"), ( "Distinct_operands", "NUMERIC")  ]


d= [['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\IMakeBuilderInfo.java', 0, None, None, 0, 0, 0, 116, 115, 10, 52, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\IMakeTarget.java', 0, None, None, 0, 0, 0, 80, 71, 8, 40, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\IMakeTargetListener.java', 0, None, None, 0, 0, 0, 12, 11, 8, 11, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\IMakeTargetManager.java', 0, None, None, 0, 0, 0, 75, 89, 11, 38, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\MakeBuilder.java', 1, 9, 5, 1, 1, 5, 1253, 745, 45, 202, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\MakeCorePlugin.java', 0, None, None, 0, 0, 0, 609, 408, 29, 131, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\MakeProjectNature.java', 0, None, None, 0, 0, 0, 524, 347, 29, 93, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\MakeScannerInfo.java', 0, None, None, 0, 0, 0, 308, 174, 30, 59, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\MakeScannerProvider.java', 0, None, None, 0, 0, 0, 774, 503, 28, 123, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\MakeTargetEvent.java', 0, None, None, 0, 0, 0, 99, 68, 14, 34, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\makefile\\IArchiveTarget.java', 0, None, None, 0, 0, 0, 14, 13, 9, 13, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\makefile\\IBadDirective.java', 0, None, None, 0, 0, 0, 9, 9, 5, 9, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\makefile\\ICommand.java', 0, None, None, 0, 0, 0, 82, 55, 18, 37, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\makefile\\IComment.java', 0, None, None, 0, 0, 0, 22, 18, 10, 16, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\makefile\\IDefaultRule.java', 0, None, None, 0, 0, 0, 9, 11, 5, 11, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\makefile\\IDirective.java', 0, None, None, 0, 0, 0, 23, 15, 8, 14, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\makefile\\IEmptyLine.java', 0, None, None, 0, 0, 0, 9, 11, 5, 11, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\makefile\\IIgnoreRule.java', 0, None, None, 0, 0, 0, 9, 11, 5, 11, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\makefile\\IInferenceRule.java', 0, None, None, 0, 0, 0, 9, 11, 5, 11, 1], ['build\\org.eclipse.cdt.make.core\\src\\org\\eclipse\\cdt\\make\\core\\makefile\\IMacroDefinition.java', 0, None, None, 0, 0, 0, 30, 25, 7, 21, 1]]
print arff.dumps(data)
write_to_arff(data,"C:\GitHub\weka\\try.arff")


exit()

os.system("python", shell=True)

print math.pow(0,0)
f=open("C:\GitHub\\agent\\allFiles.txt","r")
lines=[s.split("\n")[0] for s in f.readlines()]
packs=[".".join(s.split(".")[:5]) for s in lines]
packs=set(packs)
packs=list(packs)

out=open("C:\GitHub\\agent\\Packs.txt","wb")
out.writelines([p+"\n" for p in packs])
print packs

exit()
writer=csv.writer(open("C:\GitHub\\agent\\experiments2BugsTimes3\planner.csv","wb"))
for i in range(9000):
    writer.writerow([i,i])
