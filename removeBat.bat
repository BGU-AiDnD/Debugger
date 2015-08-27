@echo off
REM bat <indices>  <inputTrain> <outputTrain> <inputTest> <outputTest> <model> <training> <testing>
call java -Xmx2024m  -cp "C:\Program Files\Weka-3-7\weka.jar" weka.filters.unsupervised.attribute.Remove -R  %1 -V -i %2 -o %3
call java -Xmx2024m  -cp "C:\Program Files\Weka-3-7\weka.jar" weka.filters.unsupervised.attribute.Remove -R  %1 -V -i %4 -o %5
call java -Xmx2024m  -cp "C:\Program Files\Weka-3-7\weka.jar" weka.Run weka.classifiers.trees.RandomForest -I 100 -K 0 -S 1 -num-slots 1  -t %3 -x 10 -d %6 > %7
call cmd.exe /x /c "java -Xmx4048m  -cp "C:\Program Files\Weka-3-7\weka.jar" weka.Run weka.classifiers.trees.RandomForest  -l %6 -T %5   > %8"
del /F %6