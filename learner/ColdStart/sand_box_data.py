import pandas as pd
import xml.etree.ElementTree as et
from scipy.io import arff
from scipy.io.arff import loadarff
import os
import sklearn.metrics as metrics
import pickle
from imblearn.ensemble import BalancedRandomForestClassifier
import numpy as np
from decimal import *
import operator
not_to_enter = 'ZZZ'

#data = pickle.load(open(r'D:\Debbuger\our projects style promise\within_models_full_ours_f\within_models_full_ours_f.sav', "rb"))
delete_features = [
    "ImperativeAbstraction",
    "MultifacetedAbstraction",
    "UnnecessaryAbstraction",
    "UnutilizedAbstraction",
    "DeficientEncapsulation",
    "UnexploitedEncapsulation",
    "BrokenModularization",
    "Cyclic_DependentModularization",
    "InsufficientModularization",
    "Hub_likeModularization",
    "BrokenHierarchy",
    "CyclicHierarchy",
    "DeepHierarchy",
    "MissingHierarchy",
    "MultipathHierarchy",
    "RebelliousHierarchy",
    "WideHierarchy",

    "AbstractFunctionCallFromConstructor",
    "ComplexConditional",
    "ComplexMethod",
    "EmptyCatchClause",
    "LongIdentifier",
    "LongMethod_Designite",
    "LongParameterList_Designite",
    "LongStatement",
    "MagicNumber",
    "MissingDefault",

    "GodClass",
    "ClassDataShouldBePrivate",
    "ComplexClass",
    "LazyClass",
    "RefusedBequest",
    "SpaghettiCode",
    "SpeculativeGenerality",
    "DataClass",
    "BrainClass",
    "LargeClass",
    "SwissArmyKnife",
    "AntiSingleton",

    "FeatureEnvy",
    "LongMethod_Organic",
    "LongParameterList_Organic",
    "MessageChain",
    "DispersedCoupling",
    "IntensiveCoupling",
    "ShotgunSurgery",
    "BrainMethod",


"AnonymousInnerClassLength_count",
"AnonymousInnerClassLength_max",
"AnonymousInnerClassLength_mean",
"AnonymousInnerClassLength_min",
"AnonymousInnerClassLength_std",

"CyclomaticComplexity_Designite_count",
"CyclomaticComplexity_Designite_max",
"CyclomaticComplexity_Designite_mean",
"CyclomaticComplexity_Designite_min",
"CyclomaticComplexity_Designite_std",

"LOCMethod_count",
"LOCMethod_max",
"LOCMethod_mean",
"LOCMethod_min",
"LOCMethod_std",

"NestedForDepth_count",
"NestedForDepth_max",
"NestedForDepth_mean",
"NestedForDepth_min",
"NestedForDepth_std",

"NumberOfParameters_Designite_count",
"NumberOfParameters_Designite_max",
"NumberOfParameters_Designite_mean",
"NumberOfParameters_Designite_min",
"NumberOfParameters_Designite_std"

]
save_features = [
"AverageBlockDepth",
"AverageComplexity",
"AverageStatementsperMethod",
"BooleanExpressionComplexity_count",
"BooleanExpressionComplexity_max",
"BooleanExpressionComplexity_mean",
"BooleanExpressionComplexity_min",
"BooleanExpressionComplexity_std",
"Bugged",
"CBO_count",
"CBO_max",
"CBO_mean",
"CBO_min",
"CBO_std",
"Calls_count",
"Calls_max",
"Calls_mean",
"Calls_min",
"Calls_std",
"ClassDataAbstractionCoupling_count",
"ClassDataAbstractionCoupling_max",
"ClassDataAbstractionCoupling_mean",
"ClassDataAbstractionCoupling_min",
"ClassDataAbstractionCoupling_std",
"ClassFanOutComplexity_count",
"ClassFanOutComplexity_max",
"ClassFanOutComplexity_mean",
"ClassFanOutComplexity_min",
"ClassFanOutComplexity_std",
"ClassesandInterfaces",
"Complexity_count",
"Complexity_max",
"Complexity_mean",
"Complexity_min",
"Complexity_std",
"CyclomaticComplexity_count",
"CyclomaticComplexity_max",
"CyclomaticComplexity_mean",
"CyclomaticComplexity_min",
"CyclomaticComplexity_std",
"DepthOfInheritance",
"Difficulty",
"Effort",
"ExecutableStatementCount_count",
"ExecutableStatementCount_max",
"ExecutableStatementCount_mean",
"ExecutableStatementCount_min",
"ExecutableStatementCount_std",
"FANIN",
"FANOUT",
"FileLength_count",
"FileLength_max",
"FileLength_mean",
"FileLength_min",
"FileLength_std",
"IsConstructor_count",
"IsConstructor_freq",
"IsConstructor_top",
"IsConstructor_unique",
"LCOM",
"LOCMethod",
"LOCMethod_CK_count",
"LOCMethod_CK_max",
"LOCMethod_CK_mean",
"LOCMethod_CK_min",
"LOCMethod_CK_std",
"Length",
"MaxNumberOfNestedBlocks_count",
"MaxNumberOfNestedBlocks_max",
"MaxNumberOfNestedBlocks_mean",
"MaxNumberOfNestedBlocks_min",
"MaxNumberOfNestedBlocks_std",
"Maximum Depth_count",
"Maximum Depth_max",
"Maximum Depth_mean",
"Maximum Depth_min",
"Maximum Depth_std",
"MaximumBlockDepth",
"MaximumComplexity",
"MethodCallStatements",
"MethodLength_count",
"MethodLength_max",
"MethodLength_mean",
"MethodLength_min",
"MethodLength_std",
"MethodsperClass",
"NCSSForThisClass_count",
"NCSSForThisClass_max",
"NCSSForThisClass_mean",
"NCSSForThisClass_min",
"NCSSForThisClass_std",
"NCSSForThisFile_count",
"NCSSForThisFile_max",
"NCSSForThisFile_mean",
"NCSSForThisFile_min",
"NCSSForThisFile_std",
"NCSSForThisMethod_count",
"NCSSForThisMethod_max",
"NCSSForThisMethod_mean",
"NCSSForThisMethod_min",
"NCSSForThisMethod_std",
"NPathComplexity_count",
"NPathComplexity_max",
"NPathComplexity_mean",
"NPathComplexity_min",
"NPathComplexity_std",
"NestedIfElseDepth_count",
"NestedIfElseDepth_max",
"NestedIfElseDepth_mean",
"NestedIfElseDepth_min",
"NestedIfElseDepth_std",
"NestedTryDepth_count",
"NestedTryDepth_max",
"NestedTryDepth_mean",
"NestedTryDepth_min",
"NestedTryDepth_std",
"NumberOfAnonymousClasses_count",
"NumberOfAnonymousClasses_max",
"NumberOfAnonymousClasses_mean",
"NumberOfAnonymousClasses_min",
"NumberOfAnonymousClasses_std",
"NumberOfAssignments_count",
"NumberOfAssignments_max",
"NumberOfAssignments_mean",
"NumberOfAssignments_min",
"NumberOfAssignments_std",
"NumberOfChildren",
"NumberOfComparisons_count",
"NumberOfComparisons_max",
"NumberOfComparisons_mean",
"NumberOfComparisons_min",
"NumberOfComparisons_std",
"NumberOfDistinctOperands",
"NumberOfDistinctOperators",
"NumberOfFields",
"NumberOfInnerClasses_count",
"NumberOfInnerClasses_max",
"NumberOfInnerClasses_mean",
"NumberOfInnerClasses_min",
"NumberOfInnerClasses_std",
"NumberOfLambdas_count",
"NumberOfLambdas_max",
"NumberOfLambdas_mean",
"NumberOfLambdas_min",
"NumberOfLambdas_std",
"NumberOfLogStatements_count",
"NumberOfLogStatements_max",
"NumberOfLogStatements_mean",
"NumberOfLogStatements_min",
"NumberOfLogStatements_std",
"NumberOfLoops_count",
"NumberOfLoops_max",
"NumberOfLoops_mean",
"NumberOfLoops_min",
"NumberOfLoops_std",
"NumberOfMathOperations_count",
"NumberOfMathOperations_max",
"NumberOfMathOperations_mean",
"NumberOfMathOperations_min",
"NumberOfMathOperations_std",
"NumberOfMethods_Checkstyle_count",
"NumberOfMethods_Checkstyle_max",
"NumberOfMethods_Checkstyle_mean",
"NumberOfMethods_Checkstyle_min",
"NumberOfMethods_Checkstyle_std",
"NumberOfMethods_Designite",
"NumberOfModifiers_count",
"NumberOfModifiers_max",
"NumberOfModifiers_mean",
"NumberOfModifiers_min",
"NumberOfModifiers_std",
"NumberOfNumbers_count",
"NumberOfNumbers_max",
"NumberOfNumbers_mean",
"NumberOfNumbers_min",
"NumberOfNumbers_std",
"NumberOfPackageMethod_count",
"NumberOfPackageMethod_max",
"NumberOfPackageMethod_mean",
"NumberOfPackageMethod_min",
"NumberOfPackageMethod_std",
"NumberOfParameters_CK_count",
"NumberOfParameters_CK_max",
"NumberOfParameters_CK_mean",
"NumberOfParameters_CK_min",
"NumberOfParameters_CK_std",
"NumberOfParenthesizedExps_count",
"NumberOfParenthesizedExps_max",
"NumberOfParenthesizedExps_mean",
"NumberOfParenthesizedExps_min",
"NumberOfParenthesizedExps_std",
"NumberOfPrivateMethod_count",
"NumberOfPrivateMethod_max",
"NumberOfPrivateMethod_mean",
"NumberOfPrivateMethod_min",
"NumberOfPrivateMethod_std",
"NumberOfProtectedMethod_count",
"NumberOfProtectedMethod_max",
"NumberOfProtectedMethod_mean",
"NumberOfProtectedMethod_min",
"NumberOfProtectedMethod_std",
"NumberOfPublicFields",
"NumberOfPublicMethods_Checkstyle_count",
"NumberOfPublicMethods_Checkstyle_max",
"NumberOfPublicMethods_Checkstyle_mean",
"NumberOfPublicMethods_Checkstyle_min",
"NumberOfPublicMethods_Checkstyle_std",
"NumberOfPublicMethods_Designite",
"NumberOfStringLiterals_count",
"NumberOfStringLiterals_max",
"NumberOfStringLiterals_mean",
"NumberOfStringLiterals_min",
"NumberOfStringLiterals_std",
"NumberOfTryCatch_count",
"NumberOfTryCatch_max",
"NumberOfTryCatch_mean",
"NumberOfTryCatch_min",
"NumberOfTryCatch_std",
"NumberOfUniqueWords_count",
"NumberOfUniqueWords_max",
"NumberOfUniqueWords_mean",
"NumberOfUniqueWords_min",
"NumberOfUniqueWords_std",
"NumberOfVariables_count",
"NumberOfVariables_max",
"NumberOfVariables_mean",
"NumberOfVariables_min",
"NumberOfVariables_std",
"PercentLinesWithComments",
"RFC_count",
"RFC_max",
"RFC_mean",
"RFC_min",
"RFC_std",
"Returns_count",
"Returns_max",
"Returns_mean",
"Returns_min",
"Returns_std",
"SourceMonitorCalls",
"SourceMonitorFileStatements",
"Statements_count",
"Statements_max",
"Statements_mean",
"Statements_min",
"Statements_std",
"Statementsatblocklevel0",
"Statementsatblocklevel1",
"Statementsatblocklevel2",
"Statementsatblocklevel3",
"Statementsatblocklevel4",
"Statementsatblocklevel5",
"Statementsatblocklevel6",
"Statementsatblocklevel7",
"Statementsatblocklevel8",
"Statementsatblocklevel9",
"ThrowsCount_count",
"ThrowsCount_max",
"ThrowsCount_mean",
"ThrowsCount_min",
"ThrowsCount_std",
"TotalNumberOfOperands",
"TotalNumberOfOperators",
"Vocabulary",
"Volume",
"WMC_CK_count",
"WMC_CK_max",
"WMC_CK_mean",
"WMC_CK_min",
"WMC_CK_std",
"WMC_Designite"
]
lable_metric = 'Bugged'

def fit_model(data):
    model = BalancedRandomForestClassifier(n_estimators=1000, max_depth=5)
    x = data.drop(lable_metric, axis=1)
    y = data[lable_metric]
    num_of_bugs = data.loc[data[lable_metric] == 1].shape[0]
    if num_of_bugs == 0:
        print("NO BUGS")
        return None
    model.fit(x, y)
    return model
def preper_model_and_train_test(training_set, testing_set):
    training_set_f = training_set.copy()
    testing_set_f = testing_set.copy()
    #training_set_f = training_set_f.replace([np.inf, -np.inf], np.nan)
    #testing_set_f = testing_set_f.replace([np.inf, -np.inf], np.nan)
    #testing_set_f = testing_set_f.dropna()
    #training_set_f = training_set_f.dropna()
    save_features
    for column in training_set_f:
        #if any(name in column for name in ['25%', '50%', '75%']) or column in delete_features:
            #print(column)
         #   training_set_f = training_set_f.drop(column, axis=1)
         #   if column in testing_set_f:
         #       testing_set_f = testing_set_f.drop(column, axis=1)
        if column not in save_features:
            training_set_f = training_set_f.drop(column, axis=1)
            if column in testing_set_f:
               testing_set_f = testing_set_f.drop(column, axis=1)


    training_set_f[lable_metric] = training_set_f[lable_metric].map(
        {'true': 1, 'false': 0, 'True': 1, 'False': 0, 'TRUE': 1, 'FALSE': 0, False: 0, True: 1})
    testing_set_f[lable_metric] = testing_set_f[lable_metric].map(
        {'true': 1, 'false': 0, 'True': 1, 'False': 0, 'TRUE': 1, 'FALSE': 0, False: 0, True: 1})

    training_set_f = training_set_f.reindex(sorted(training_set_f.columns), axis=1)
    testing_set_f = testing_set_f.reindex(sorted(testing_set_f.columns), axis=1)
    cur_model = fit_model(training_set_f)
    if cur_model is None:
        return None, None, None

    return training_set_f, testing_set_f, cur_model
def save_dump(path,name,to_save):
    file_path = os.path.join(path, name)
    pickle.dump(to_save, open(file_path, 'wb'))


directory_path = r'D:\Debbuger\Cluster_projects'
data_set_path = r'D:\Debbuger\Cluster_projects\Z_DataSet'
dic_many = {}
dict_all_data = {}

for project_name in os.listdir(directory_path):
    folder = os.path.join(directory_path, project_name)
    if os.path.isdir(folder) and project_name not in ['ZZZ_bugged_versions','ZZZ_NOT_RELEVENT','z_system_features','Z_DataSet','fop']:
    #if os.path.isdir(folder) and project_name in ['Archiva']:
        project_name_dataset = os.listdir(os.path.join(folder,'dataset'))[0]
        new_dir_path = os.path.join(data_set_path,project_name)
        training_file_path = os.path.join(os.path.join(os.path.join(folder,'dataset'), project_name_dataset), r'classes\training.csv')
        testing_file_path = os.path.join(os.path.join(os.path.join(folder,'dataset'), project_name_dataset), r'classes\testing.csv')
        train_data = pd.read_csv(training_file_path,delimiter=';')
        test_data = pd.read_csv(testing_file_path,delimiter=';')
        print(project_name)

        #print("training: " + str(train_data.shape))
        #print("1: " + str(train_data[train_data['Bugged']==1].shape))
        #print("0: " + str(train_data[train_data['Bugged']==0].shape))
        #print((train_data[train_data['Bugged']==1].shape[0])/train_data.shape[0])
        #print("testing: "+ str(test_data.shape) )
        #print("1: " + str(test_data[test_data['Bugged'] == 1].shape))
        #print("0: " + str(test_data[test_data['Bugged'] == 0].shape))
        #print((test_data[test_data['Bugged']==1].shape[0])/test_data.shape[0])

        os.mkdir(new_dir_path)
        train_set,test_set,cur_model = preper_model_and_train_test(train_data,test_data)


        if train_set is not None:
            dict_all_data[project_name] = (cur_model, train_set, test_set)
            print("all done - preper")

        save_dump(new_dir_path,"model_within.sav",cur_model)
        train_set.to_csv(os.path.join(new_dir_path, "training.csv"),index=False)
        test_set.to_csv(os.path.join(new_dir_path, "testing.csv"),index=False)
        print("all done - saved")

        prediction_test = cur_model.predict(test_set.drop(lable_metric, axis=1))
        f_measure_bugged1 = metrics.f1_score(test_set[lable_metric].tolist(), prediction_test.tolist())
        f_measure_bugged2 = metrics.f1_score(test_set[lable_metric].tolist(), prediction_test.tolist(), pos_label=1, average='binary')
        print("prediction F1: ")
        print(f_measure_bugged1)
        print(f_measure_bugged2)

        print("  ")
        #print(train_set.dtypes)
        #print(train_set.isnull())
        print("training: " + str(train_set.shape[1]))
        print("testing: " + str(test_set.shape[1]))


        #train_data.to_csv(os.path.join(os.path.join(dir, proj_name_host), "testing.csv"), index=False)
        #testing_set_host.to_csv(os.path.join(os.path.join(dir, proj_name_host), "testing.csv"), index=False)

        #dic_many[project_name] = ((train_data[train_data['Bugged']==1].shape[0])/train_data.shape[0],(test_data[test_data['Bugged']==1].shape[0])/test_data.shape[0])

save_dump(data_set_path,"all_data_with_models.sav",dict_all_data)

#sorted_x = sorted(dic_many.items(), key=operator.itemgetter(1))
#print(sorted_x)
#for a,b in sorted_x:
#    print( str(a) +"  " +str(b))

'''
dir = r'D:\Debbuger\new_data\DATA-SET'
for proj_name_host, (model_host, training_set_host, testing_set_host) in data.items():
    print(proj_name_host)Random Forest
    print("trainng set shape: "+ str(training_set_host.shape))
    training_set_host.to_csv(os.path.join( os.path.join( dir ,proj_name_host) ,"training.csv"),index=False)
    print("testing set shape: "+ str(testing_set_host.shape))
    testing_set_host.to_csv(os.path.join( os.path.join( dir ,proj_name_host) ,"testing.csv"),index=False)


#model,cur_bookkeeper,_ = data['bookkeeper']
#cur_bookkeeper.to_csv(r'D:\Debbuger\our projects style promise\within_models_full_ours_f\data.csv',index=False)
#print(model.feature_importances_)
'''

