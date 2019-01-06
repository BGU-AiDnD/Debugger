CREATE_ALL_METHODS_SQL_TABLE = ("CREATE TABLE AllMethods (methodDir text, fileName text, methodName text, beginLine INT , endLine INT )")

CREATE_COMMITTED_METHODS_SQL_TABLE_COMMAND = ("CREATE TABLE commitedMethods (commit_sha text , methodDir text, fileName text, methodName text, deletions INT , insertions INT , lines INT, bugId INT, commiter_date DateTime,commitID INT)")

CREATE_BUG_FIX_COMMITS_SQL_TABLE_COMMAND = ("CREATE TABLE bugsFix (ID INT,Product text,Component text,Assigned_To text,Status text,Resolution text,Reporter text,Last_Modified DateTime ,Version text,Milestone text,Hardware text,OS text,Priority text,Severity text,Summary text,Keywords text,Submit_Date DateTime ,Blocks text,Depends_On text,Duplicate_Of INT,CC text)")

CREATE_COMMITS_SQL_TABLE_COMMAND = ("CREATE TABLE commits (ID INT, bugId INT, commiter_date DateTime , commiter text,author_date DateTime , author text  , size INT, parentID INT, message text,commit_sha text )")

CREATE_COMMITED_FILES_SQL_TABLE_COMMAMD = ("CREATE TABLE Commitedfiles (id INT,name text,commit_sha text,lines INT,deletions INT,insertions INT, bugId INT, commiter_date DateTime, commitid INT)")

CREATE_FILES_SQL_TABLE_COMMAND = "CREATE TABLE files (id INT,name text)"

CREATE_COMPLEX_FILES_SQL_TABLE_COMMAND = "CREATE TABLE Complexyfiles (name text, complex INT)"

CREATE_HALSTEAD_FILES_SQL_TABLE_COMMAND = ("CREATE TABLE haelsTfiles (name text, Operators_count INT, Distinct_operators INT, Operands_count INT, Distinct_operands INT, Program_length INT, Program_vocabulary INT,Volume float, Difficulty INT, Effort float)")

CREATE_BUGS_SQL_TABLE_COMMAND = ("CREATE TABLE bugs (ID INT,Product text,Component text,Assigned_To text,Status text,Resolution text,Reporter text,Last_Modified DateTime ,Version text,Milestone text,Hardware text,OS text,Priority text,Severity text,Summary text,Keywords text,Submit_Date DateTime ,Blocks text,Depends_On text,Duplicate_Of INT,CC text)")

STATEMENTS_AT_BLOCK_LEVEL_X_COLUMNS = ["Statements_at_block_level_{level} INT".format(level=level)
                                       for level in range(10)]

CREATE_JAVA_FILES_SQL_TABLE_COMMAND = ("CREATE TABLE JAVAfiles (name text, Lines INT, "
                                       "Statements INT, Percent_Branch_Statements INT,"
                                       "Method_Call_Statements INT, Percent_Lines_with_Comments INT,"
                                       "Classes_and_Interfaces INT, Methods_per_Class float,"
                                       "Average_Statements_per_Method float,"
                                       "Line_Number_of_Most_Complex_Method INT, "
                                       "Name_of_Most_Complex_Method text, "
                                       "Maximum_Complexity INT, Line_Number_of_Deepest_Block INT,"
                                       "Maximum_Block_Depth INT, Average_Block_Depth float, "
                                       "Average_Complexity float, {})".format(",".join(
										STATEMENTS_AT_BLOCK_LEVEL_X_COLUMNS)))

CREATE_SOURCE_METHODS_SQL_TABLE_COMMAND = ("CREATE TABLE JAVAfiles (name text,Lines INT,	Statements INT,	Percent_Branch_Statements INT,Method_Call_Statements INT,Percent_Lines_with_Comments INT,Classes_and_Interfaces INT,Methods_per_Class float,Average_Statements_per_Method float,Line_Number_of_Most_Complex_Method 	INT, Name_of_Most_Complex_Method 	text, Maximum_Complexity INT,Line_Number_of_Deepest_Block INT,Maximum_Block_Depth INT,Average_Block_Depth	float, Average_Complexity	float, Statements_at_block_level_0 INT,Statements_at_block_level_1 INT,Statements_at_block_level_2 INT,Statements_at_block_level_3 INT,Statements_at_block_level_4 INT,Statements_at_block_level_5 INT,Statements_at_block_level_6 INT,Statements_at_block_level_7 INT,Statements_at_block_level_8 INT,Statements_at_block_level_9 INT)")

CREATE_CLASSES_SQL_TABLE_COMMAND = ("CREATE TABLE classes (Dirpath text,superClass text,exception text, name text,externalizable text ,abstract text ,path text ,error text   ,included text ,scope text   ,serializable text)")

CREATE_CONSTRUCTORS_SQL_TABLE_COMMAND = ("CREATE TABLE constructors (Dirpath text ,className text , name text , synchronized text, varArgs text,  classPath text ,static text, signature text, included text, scope text, final text,  native text,  Num_params text)")

CREATE_METHODS_SQL_TABLE_COMMAND = ("CREATE TABLE methods (Dirpath text,className text, name text , synchronized text, abstract text , varArgs text, classPath text , static text, signature text , included text , scope text  , final text  , native text   ,return text,Num_params text)")

CREATE_FIELDS_SQL_TABLE_COMMAND = ("CREATE TABLE fields (Dirpath text,className text,static text, name text, classPath text, transient text,volatile text,scope text,    final text, type text)")

CREATE_CHECKSTYLE_SQL_TABLE_COMMAND = ("CREATE TABLE checkStyle (name text,McCabe REAL,fanOut REAL,NPath REAL,FileLen INT, NCSS INT, outer INT, publicMethods INT, totalMethods INT,thorwsSTM INT,Coupling INT,Executables INT, depthFor INT,depthIf INT)")

CREATE_COMMENTS_SQL_TABLE_COMMAND = "CREATE TABLE comments (name text, commitid INT)"

CREATE_TABLE_BLAME_EXTENDED_SQL_COMMAND = \
	'''CREATE TABLE blameExtends (name text, diff_commits INT, diff_commits_lastver INT,
	diff_commitsApproved INT, diff_commits_lastverApproved INT, numBlobs INT, numPatchs INT,
	numCommits INT, len_times INT, mean_times DateTime,median_times DateTime,var_times float,max_times DateTime,min_times DateTime,p01_times  float,p02_times  float,p05_times  float,mx1_times  float, max_min_times INT,
	ones_times float, twos_times float,less5_times float,less10_times float,
	len_difftimes INT,mean_difftimes DateTime,median_difftimes DateTime,var_difftimes float,max_difftimes DateTime,min_difftimes DateTime,p01_difftimes float,p02_difftimes float,p05_difftimes float,mx1_difftimes  float, max_min_difftimes INT,
	ones_difftimes float, twos_difftimes float,less5_difftimes float,less10_difftimes float,
	len_committers INT,p01_committers  float,p02_committers  float,p05_committers  float,mx1_committers  float,
	len_timesApproved INT,mean_timesApproved DateTime,median_timesApproved DateTime,var_timesApproved float,max_timesApproved DateTime,min_timesApproved DateTime,p01_timesApproved  float,p02_timesApproved  float,p05_timesApproved  float,mx1_timesApproved  float, max_min_timesApproved INT,
	ones_timesApproved float, twos_timesApproved float,less5_timesApproved float,less10_timesApproved float,
	len_difftimesApproved INT,mean_difftimesApproved DateTime,median_difftimesApproved DateTime,var_difftimesApproved float,max_difftimesApproved DateTime,min_difftimesApproved DateTime,p01_difftimesApproved float,p02_difftimesApproved float,p05_difftimesApproved float,mx1__difftimesApproved  float, max_min_difftimesApproved INT,
	ones_difftimesApproved float, twos_difftimesApproved float,less5_difftimesApproved float,less10_difftimesApproved float,
	len_committersApproved INT,p01_committersApproved  float,p02_committersApproved  float,p05_committersApproved  float,mx1_committersApproved  float,
	len_groups INT,mean_groups float,median_groups float,var_groups float,max_groups float,min_groups float,p01_groups  float,p02_groups  float,p05_groups  float,mx1_groups  float,
	len_groupsApproved INT,mean_groupsApproved float,median_groupsApproved float,var_groupsApproved float,max_groupsApproved float,min_groupsApproved float,p01_groupsApproved  float,p02_groupsApproved  float,p05_groupsApproved  float,mx1_groupsApproved  float)'''

CREATE_CHECKSTYLE_EXTENDED_SQL_TABLE_COMMAND = \
	'''CREATE TABLE checkStyleExtends (name text, NCSS INT,FileLen INT,sum_fors REAL,sum_ifs REAL,sum_tries REAL,
	len_mccab REAL,sum_mccab REAL,mean_mccab REAL,median_mccab REAL,var_mccab REAL,max_mccab REAL,min_mccab REAL, oneElement_mccab text,
	len_fanOut REAL,sum_fanOut REAL,mean_fanOut REAL,median_fanOut REAL,var_fanOut REAL,max_fanOut REAL,min_fanOut REAL, oneElement_fanOut text,
	len_NPath REAL,sum_NPath REAL,mean_NPath REAL,median_NPath REAL,var_NPath REAL,max_NPath REAL,min_NPath REAL, oneElement_NPath text,
	len_JavaNCSSmet REAL,sum_JavaNCSSmet REAL,mean_JavaNCSSmet REAL,median_JavaNCSSmet REAL,var_JavaNCSSmet REAL,max_JavaNCSSmet REAL,min_JavaNCSSmet REAL, oneElement_JavaNCSSmet text,
	len_thorwsSTM REAL,sum_thorwsSTM REAL,mean_thorwsSTM REAL,median_thorwsSTM REAL,var_thorwsSTM REAL,max_thorwsSTM REAL,min_thorwsSTM REAL, oneElement_thorwsSTM text,
	len_coupl REAL,sum_coupl REAL,mean_coupl REAL,median_coupl REAL,var_coupl REAL,max_coupl REAL,min_coupl REAL, oneElement_coupl text,
	len_executables REAL,sum_executables REAL,mean_executables REAL,median_executables REAL,var_executables REAL,max_executables REAL,min_executables REAL, oneElement_executables text,
	len_lens REAL,sum_lens REAL,mean_lens REAL,median_lens REAL,var_lens REAL,max_lens REAL,min_lens REAL, oneElement_lens text
	)'''

CREATE_JAVA_FILE_FIX_SQL_TABLE_COMMAND = \
	("CREATE TABLE JAVAfilesFix (name text,Lines INT, Statements INT, "
	 "Percent_Branch_Statements INT, Method_Call_Statements INT, Percent_Lines_with_Comments INT,"
	 "Classes_and_Interfaces INT, Methods_per_Class float, Average_Statements_per_Method float,"
	 "Line_Number_of_Most_Complex_Method INT, Name_of_Most_Complex_Method text, "
	 "Maximum_Complexity INT, Line_Number_of_Deepest_Block INT,"
	 "Maximum_Block_Depth INT,Average_Block_Depth float, Average_Complexity float,"
	 " {})".format(",".join(STATEMENTS_AT_BLOCK_LEVEL_X_COLUMNS)))

CREATE_SOURCE_METHODS_FIX_SQL_TABLE_COMMMAD = \
	("CREATE TABLE SourcemethodsFix (File_Name text, Method text ,Complexity INT, Statements INT, "
	 "Maximum_Depth	INT, Calls INT)")

JAVA_TABLES_CREATION_COMMANDS = [CREATE_SOURCE_METHODS_FIX_SQL_TABLE_COMMMAD,
                                 CREATE_JAVA_FILE_FIX_SQL_TABLE_COMMAND,
                                 CREATE_CHECKSTYLE_EXTENDED_SQL_TABLE_COMMAND,
                                 CREATE_TABLE_BLAME_EXTENDED_SQL_COMMAND,
                                 CREATE_COMMENTS_SQL_TABLE_COMMAND,
                                 CREATE_CHECKSTYLE_SQL_TABLE_COMMAND,
                                 CREATE_FIELDS_SQL_TABLE_COMMAND,
                                 CREATE_METHODS_SQL_TABLE_COMMAND,
                                 CREATE_CONSTRUCTORS_SQL_TABLE_COMMAND,
                                 CREATE_CLASSES_SQL_TABLE_COMMAND,
                                 CREATE_SOURCE_METHODS_SQL_TABLE_COMMAND,
                                 CREATE_JAVA_FILES_SQL_TABLE_COMMAND,
                                 CREATE_BUGS_SQL_TABLE_COMMAND,
                                 CREATE_HALSTEAD_FILES_SQL_TABLE_COMMAND,
                                 CREATE_COMPLEX_FILES_SQL_TABLE_COMMAND,
                                 CREATE_FILES_SQL_TABLE_COMMAND,
                                 CREATE_COMMITED_FILES_SQL_TABLE_COMMAMD,
                                 CREATE_COMMITS_SQL_TABLE_COMMAND,
                                 CREATE_BUG_FIX_COMMITS_SQL_TABLE_COMMAND,
                                 CREATE_COMMITTED_METHODS_SQL_TABLE_COMMAND]
