__author__ = 'amir'
import numpy as np
from sklearn.metrics import precision_recall_fscore_support,classification_report,confusion_matrix
import csv





def BuildWekaModel(training,testing,name,wekaJar):
    algorithm="weka.classifiers.trees.RandomForest -I 1000 -K 0 -S 1 -num-slots 1 "
    #os.system("cd /d  "+weka +" & java -Xmx2024m  -cp \"C:\\Program Files\\Weka-3-7\\weka.jar\" weka.Run " +algorithm+ " -x 10 -d .\\model.model -t "+training+" > training"+name+".txt")
    print("java -Xmx2024m  -cp "+wekaJar+" weka.Run " +algorithm+ " -x 10 -d .\\model.model -t "+training+" > training"+name+".txt")
    #os.system("cd /d  "+weka +" & java -Xmx2024m  -cp "+wekaJar+" weka.Run " +algorithm+ " -l .\\model.model -T "+testing+" -classifications \"weka.classifiers.evaluation.output.prediction.CSV -file testing"+name+".csv\" ")
    print("java -Xmx2024m  -cp "+wekaJar+" weka.Run " +algorithm+ " -l .\\model.model -T "+testing+" > testing"+name+".txt ")


BuildWekaModel("TRAIN","TEST","NAME","JAR")

def properties(file):
    f=open(file,"r")
    reader=csv.reader(f)
    y_true=[]
    y_pred=[]
    x=0
    for line in reader:
        x=x+1
        if x==1:
            continue
        if line==[]:
            break
        actual=line[2]
        prediction=line[3]
        y_true.append(actual)
        y_pred.append(prediction)

    return np.array(y_true),np.array(y_pred)



#y_true = np.array(['cat', 'dog', 'pig', 'cat', 'dog', 'pig'])
#y_pred = np.array(['cat', 'pig', 'dog', 'cat', 'cat', 'dog'])

y_true, y_pred=properties("E:\\Amir\\All_out_files.csv")
print y_pred
print precision_recall_fscore_support(y_true, y_pred, average='macro')
print classification_report(y_true, y_pred)
print confusion_matrix(y_true, y_pred)

#(0.22..., 0.33..., 0.26..., None)
print precision_recall_fscore_support(y_true, y_pred, average='micro')

#(0.33..., 0.33..., 0.33..., None)
print precision_recall_fscore_support(y_true, y_pred, average='weighted')
#(0.22..., 0.33..., 0.26..., None)

