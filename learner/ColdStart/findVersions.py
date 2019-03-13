
import os

import pandas as pd

directory = r"C:\Users\USER\Desktop\allFiles"
for filename in os.listdir(directory):
     if filename.endswith("csv"):
         progVersionsFull = os.path.join(directory, filename)
         df = pd.read_csv(progVersionsFull)
         sortedByDate = df.sort_values('version_date')
         sortedByDate['precent'] = sortedByDate['#bugged files in version'] / sortedByDate['#files in version']






#df = pd.read_csv(r"C:\Users\USER\Desktop\allFiles\accumulo.csv")
#sortedByDate = df.sort_values('version_date')
#sortedByDate['precent'] = sortedByDate['#bugged files in version']/sortedByDate['#files in version']

#print (df)
#print (sortedByDate)
#print (df.describe())