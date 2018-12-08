"""This module analyzes the commits the users uploaded."""
from wekaMethods.articles import *
from wekaMethods.features.features_analyzer import FeatureAnalyzer


class CommitsAnalyzer(FeatureAnalyzer):
	"""Class to analyze the commits posted to the work-flow tool."""

	def __init__(self):
		super(CommitsAnalyzer, self).__init__("commits_static_data.json")

	def get_attributes(self):
		return self.get_best_attributes()

	def get_features(self, c, files_dict, prev_date, start_date, end_date):
		analyze = '''select name , sum( NCSS ), sum(FileLen ), sum(sum_fors ), sum(sum_ifs ), sum(sum_tries ), sum(
		len_mccab ), sum(sum_mccab ), sum(mean_mccab ), sum(median_mccab ), sum(var_mccab ), sum(max_mccab ), sum(min_mccab ), sum(
		len_fanOut ), sum(sum_fanOut ), sum(mean_fanOut ), sum(median_fanOut ), sum(var_fanOut ), sum(max_fanOut ), sum(min_fanOut ), sum(
		len_NPath ), sum(sum_NPath ), sum(mean_NPath ), sum(median_NPath ), sum(var_NPath ), sum(max_NPath ), sum(min_NPath ), sum(
		len_JavaNCSSmet ), sum(sum_JavaNCSSmet ), sum(mean_JavaNCSSmet ), sum(median_JavaNCSSmet ), sum(var_JavaNCSSmet ), sum(max_JavaNCSSmet ), sum(min_JavaNCSSmet ), sum(
		len_thorwsSTM ), sum(sum_thorwsSTM ), sum(mean_thorwsSTM ), sum(median_thorwsSTM ), sum(var_thorwsSTM ), sum(max_thorwsSTM ), sum(min_thorwsSTM ), sum(
		len_coupl ), sum(sum_coupl ), sum(mean_coupl ), sum(median_coupl ), sum(var_coupl ), sum(max_coupl ), sum(min_coupl ), sum(
		len_executables ), sum(sum_executables ), sum(mean_executables ), sum(median_executables ), sum(var_executables ), sum(max_executables ), sum(min_executables ), sum(
		len_lens ), sum(sum_lens ), sum(mean_lens ), sum(median_lens ), sum(var_lens ), sum(max_lens ), sum(min_lens ), sum(
		publics ), sum(protecteds ), sum(privates ), sum(totals  ), sum(len_params ), sum(sum_params ), sum(mean_params ), sum(median_params ), sum(var_params ), sum(max_params ), sum(min_params)
		from checkStyleAnalyzeExtends group by name'''
		lst = [0, 1, 3, 6, 7, 9, 10, 13, 14, 15, 17, 18, 20, 21, 23, 24, 27, 41, 42, 43, 45, 48, 55,
			   59, 64]
		self.convert_sql_query_to_attributes(["0" for x in lst], c, files_dict, analyze, lst)
		analyze = '''select name , avg( NCSS ), avg(FileLen ), avg(sum_fors ), avg(sum_ifs ), avg(sum_tries ), avg(
		len_mccab ), avg(sum_mccab ), avg(mean_mccab ), avg(median_mccab ), avg(var_mccab ), avg(max_mccab ), avg(min_mccab ), avg(
		len_fanOut ), avg(sum_fanOut ), avg(mean_fanOut ), avg(median_fanOut ), avg(var_fanOut ), avg(max_fanOut ), avg(min_fanOut ), avg(
		len_NPath ), avg(sum_NPath ), avg(mean_NPath ), avg(median_NPath ), avg(var_NPath ), avg(max_NPath ), avg(min_NPath ), avg(
		len_JavaNCSSmet ), avg(sum_JavaNCSSmet ), avg(mean_JavaNCSSmet ), avg(median_JavaNCSSmet ), avg(var_JavaNCSSmet ), avg(max_JavaNCSSmet ), avg(min_JavaNCSSmet ), avg(
		len_thorwsSTM ), avg(sum_thorwsSTM ), avg(mean_thorwsSTM ), avg(median_thorwsSTM ), avg(var_thorwsSTM ), avg(max_thorwsSTM ), avg(min_thorwsSTM ), avg(
		len_coupl ), avg(sum_coupl ), avg(mean_coupl ), avg(median_coupl ), avg(var_coupl ), avg(max_coupl ), avg(min_coupl ), avg(
		len_executables ), avg(sum_executables ), avg(mean_executables ), avg(median_executables ), avg(var_executables ), avg(max_executables ), avg(min_executables ), avg(
		len_lens ), avg(sum_lens ), avg(mean_lens ), avg(median_lens ), avg(var_lens ), avg(max_lens ), avg(min_lens ), avg(
		publics ), avg(protecteds ), avg(privates ), avg(totals  ), avg(len_params ), avg(sum_params ), avg(mean_params ), avg(median_params ), avg(var_params ), avg(max_params ), avg(min_params)
		from checkStyleAnalyzeExtends group by name'''
		lst = [3, 6, 7, 8, 10, 11, 13, 14, 15, 17, 18, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32,
			   34, 35, 36, 38, 39,
			   41, 42, 43, 45, 46, 48, 49, 50, 52, 53, 55, 56, 57, 59, 60]
		self.convert_sql_query_to_attributes(["0" for x in lst], c, files_dict, analyze, lst)
		analyze = '''select name , Sum(case When	NCSS 	> 0 Then 1 Else 0 End),Sum(case When	FileLen 	> 0 Then 1 Else 0 End),Sum(case When	sum_fors 	> 0 Then 1 Else 0 End),
Sum(case When	sum_ifs 	> 0 Then 1 Else 0 End),Sum(case When	sum_tries 	> 0 Then 1 Else 0 End),Sum(case When	len_mccab 	> 0 Then 1 Else 0 End),
Sum(case When	sum_mccab 	> 0 Then 1 Else 0 End),Sum(case When	mean_mccab 	> 0 Then 1 Else 0 End),Sum(case When	median_mccab 	> 0 Then 1 Else 0 End),
Sum(case When	var_mccab 	> 0 Then 1 Else 0 End),Sum(case When	max_mccab 	> 0 Then 1 Else 0 End),Sum(case When	min_mccab 	> 0 Then 1 Else 0 End),
Sum(case When	 len_fanOut 	> 0 Then 1 Else 0 End),Sum(case When	sum_fanOut 	> 0 Then 1 Else 0 End),Sum(case When	mean_fanOut 	> 0 Then 1 Else 0 End),
Sum(case When	median_fanOut 	> 0 Then 1 Else 0 End),Sum(case When	var_fanOut 	> 0 Then 1 Else 0 End),Sum(case When	max_fanOut 	> 0 Then 1 Else 0 End),
Sum(case When	min_fanOut 	> 0 Then 1 Else 0 End),Sum(case When	 len_NPath 	> 0 Then 1 Else 0 End),Sum(case When	sum_NPath 	> 0 Then 1 Else 0 End),
Sum(case When	mean_NPath 	> 0 Then 1 Else 0 End),Sum(case When	median_NPath 	> 0 Then 1 Else 0 End),Sum(case When	var_NPath 	> 0 Then 1 Else 0 End),
Sum(case When	max_NPath 	> 0 Then 1 Else 0 End),Sum(case When	min_NPath 	> 0 Then 1 Else 0 End),Sum(case When	 len_JavaNCSSmet 	> 0 Then 1 Else 0 End),
Sum(case When	sum_JavaNCSSmet 	> 0 Then 1 Else 0 End),Sum(case When	mean_JavaNCSSmet 	> 0 Then 1 Else 0 End),Sum(case When	median_JavaNCSSmet 	> 0 Then 1 Else 0 End),
Sum(case When	var_JavaNCSSmet 	> 0 Then 1 Else 0 End),Sum(case When	max_JavaNCSSmet 	> 0 Then 1 Else 0 End),Sum(case When	min_JavaNCSSmet 	> 0 Then 1 Else 0 End),
Sum(case When	 len_thorwsSTM 	> 0 Then 1 Else 0 End),Sum(case When	sum_thorwsSTM 	> 0 Then 1 Else 0 End),Sum(case When	mean_thorwsSTM 	> 0 Then 1 Else 0 End),
Sum(case When	median_thorwsSTM 	> 0 Then 1 Else 0 End),Sum(case When	var_thorwsSTM 	> 0 Then 1 Else 0 End),Sum(case When	max_thorwsSTM 	> 0 Then 1 Else 0 End),
Sum(case When	min_thorwsSTM 	> 0 Then 1 Else 0 End),Sum(case When	 len_coupl 	> 0 Then 1 Else 0 End),Sum(case When	sum_coupl 	> 0 Then 1 Else 0 End),
Sum(case When	mean_coupl 	> 0 Then 1 Else 0 End),Sum(case When	median_coupl 	> 0 Then 1 Else 0 End),Sum(case When	var_coupl 	> 0 Then 1 Else 0 End),
Sum(case When	max_coupl 	> 0 Then 1 Else 0 End),Sum(case When	min_coupl 	> 0 Then 1 Else 0 End),Sum(case When	 len_executables 	> 0 Then 1 Else 0 End),
Sum(case When	sum_executables 	> 0 Then 1 Else 0 End),Sum(case When	mean_executables 	> 0 Then 1 Else 0 End),Sum(case When	median_executables 	> 0 Then 1 Else 0 End),
Sum(case When	var_executables 	> 0 Then 1 Else 0 End),
Sum(case When	max_executables 	> 0 Then 1 Else 0 End),Sum(case When	min_executables 	> 0 Then 1 Else 0 End),Sum(case When	 len_lens 	> 0 Then 1 Else 0 End),
Sum(case When	sum_lens 	> 0 Then 1 Else 0 End),Sum(case When	mean_lens 	> 0 Then 1 Else 0 End),Sum(case When	median_lens 	> 0 Then 1 Else 0 End),
Sum(case When	var_lens 	> 0 Then 1 Else 0 End),Sum(case When	max_lens 	> 0 Then 1 Else 0 End),Sum(case When	min_lens 	> 0 Then 1 Else 0 End),
Sum(case When	 publics 	> 0 Then 1 Else 0 End),Sum(case When	protecteds 	> 0 Then 1 Else 0 End),Sum(case When	privates 	> 0 Then 1 Else 0 End),
Sum(case When	totals  	> 0 Then 1 Else 0 End),Sum(case When	len_params 	> 0 Then 1 Else 0 End),Sum(case When	sum_params 	> 0 Then 1 Else 0 End),
Sum(case When	mean_params 	> 0 Then 1 Else 0 End),Sum(case When	median_params 	> 0 Then 1 Else 0 End),Sum(case When	var_params 	> 0 Then 1 Else 0 End),
Sum(case When	max_params 	> 0 Then 1 Else 0 End),Sum(case When	min_params	> 0 Then 1 Else 0 End) from checkStyleAnalyzeExtends group by name'''
		lst = [0, 1, 3, 5, 6, 7, 9, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 26, 27, 28, 30,
			   31, 41, 42, 43, 45,
			   46, 47, 48, 49, 51, 52, 54, 55, 56, 57, 58, 59, 61, 63, 64]
		self.convert_sql_query_to_attributes(["0" for x in lst], c, files_dict, analyze, lst)
		analyze = '''select name , Sum(case When	NCSS 	< 0 Then 1 Else 0 End),Sum(case When	FileLen 	< 0 Then 1 Else 0 End),Sum(case When	sum_fors 	< 0 Then 1 Else 0 End),
Sum(case When	sum_ifs 	< 0 Then 1 Else 0 End),Sum(case When	sum_tries 	< 0 Then 1 Else 0 End),Sum(case When	len_mccab 	< 0 Then 1 Else 0 End),
Sum(case When	sum_mccab 	< 0 Then 1 Else 0 End),Sum(case When	mean_mccab 	< 0 Then 1 Else 0 End),Sum(case When	median_mccab 	< 0 Then 1 Else 0 End),
Sum(case When	var_mccab 	< 0 Then 1 Else 0 End),Sum(case When	max_mccab 	< 0 Then 1 Else 0 End),Sum(case When	min_mccab 	< 0 Then 1 Else 0 End),
Sum(case When	 len_fanOut 	< 0 Then 1 Else 0 End),Sum(case When	sum_fanOut 	< 0 Then 1 Else 0 End),Sum(case When	mean_fanOut 	< 0 Then 1 Else 0 End),
Sum(case When	median_fanOut 	< 0 Then 1 Else 0 End),Sum(case When	var_fanOut 	< 0 Then 1 Else 0 End),Sum(case When	max_fanOut 	< 0 Then 1 Else 0 End),
Sum(case When	min_fanOut 	< 0 Then 1 Else 0 End),Sum(case When	 len_NPath 	< 0 Then 1 Else 0 End),Sum(case When	sum_NPath 	< 0 Then 1 Else 0 End),
Sum(case When	mean_NPath 	< 0 Then 1 Else 0 End),Sum(case When	median_NPath 	< 0 Then 1 Else 0 End),Sum(case When	var_NPath 	< 0 Then 1 Else 0 End),
Sum(case When	max_NPath 	< 0 Then 1 Else 0 End),Sum(case When	min_NPath 	< 0 Then 1 Else 0 End),Sum(case When	 len_JavaNCSSmet 	< 0 Then 1 Else 0 End),
Sum(case When	sum_JavaNCSSmet 	< 0 Then 1 Else 0 End),Sum(case When	mean_JavaNCSSmet 	< 0 Then 1 Else 0 End),Sum(case When	median_JavaNCSSmet 	< 0 Then 1 Else 0 End),
Sum(case When	var_JavaNCSSmet 	< 0 Then 1 Else 0 End),Sum(case When	max_JavaNCSSmet 	< 0 Then 1 Else 0 End),Sum(case When	min_JavaNCSSmet 	< 0 Then 1 Else 0 End),
Sum(case When	 len_thorwsSTM 	< 0 Then 1 Else 0 End),Sum(case When	sum_thorwsSTM 	< 0 Then 1 Else 0 End),Sum(case When	mean_thorwsSTM 	< 0 Then 1 Else 0 End),
Sum(case When	median_thorwsSTM 	< 0 Then 1 Else 0 End),Sum(case When	var_thorwsSTM 	< 0 Then 1 Else 0 End),Sum(case When	max_thorwsSTM 	< 0 Then 1 Else 0 End),
Sum(case When	min_thorwsSTM 	< 0 Then 1 Else 0 End),Sum(case When	 len_coupl 	< 0 Then 1 Else 0 End),Sum(case When	sum_coupl 	< 0 Then 1 Else 0 End),
Sum(case When	mean_coupl 	< 0 Then 1 Else 0 End),Sum(case When	median_coupl 	< 0 Then 1 Else 0 End),Sum(case When	var_coupl 	< 0 Then 1 Else 0 End),
Sum(case When	max_coupl 	< 0 Then 1 Else 0 End),Sum(case When	min_coupl 	< 0 Then 1 Else 0 End),Sum(case When	 len_executables 	< 0 Then 1 Else 0 End),
Sum(case When	sum_executables 	< 0 Then 1 Else 0 End),Sum(case When	mean_executables 	< 0 Then 1 Else 0 End),Sum(case When	median_executables 	< 0 Then 1 Else 0 End),
Sum(case When	var_executables 	< 0 Then 1 Else 0 End),
Sum(case When	max_executables 	< 0 Then 1 Else 0 End),Sum(case When	min_executables 	< 0 Then 1 Else 0 End),Sum(case When	 len_lens 	< 0 Then 1 Else 0 End),
Sum(case When	sum_lens 	< 0 Then 1 Else 0 End),Sum(case When	mean_lens 	< 0 Then 1 Else 0 End),Sum(case When	median_lens 	< 0 Then 1 Else 0 End),
Sum(case When	var_lens 	< 0 Then 1 Else 0 End),Sum(case When	max_lens 	< 0 Then 1 Else 0 End),Sum(case When	min_lens 	< 0 Then 1 Else 0 End),
Sum(case When	 publics 	< 0 Then 1 Else 0 End),Sum(case When	protecteds 	< 0 Then 1 Else 0 End),Sum(case When	privates 	< 0 Then 1 Else 0 End),
Sum(case When	totals  	< 0 Then 1 Else 0 End),Sum(case When	len_params 	< 0 Then 1 Else 0 End),Sum(case When	sum_params 	< 0 Then 1 Else 0 End),
Sum(case When	mean_params 	< 0 Then 1 Else 0 End),Sum(case When	median_params 	< 0 Then 1 Else 0 End),Sum(case When	var_params 	< 0 Then 1 Else 0 End),
Sum(case When	max_params 	< 0 Then 1 Else 0 End),Sum(case When	min_params	< 0 Then 1 Else 0 End) from checkStyleAnalyzeExtends group by name'''
		lst = [0, 1, 3, 6, 7, 9, 13, 14, 15, 17, 20, 21, 23, 27, 28, 30, 42, 48, 49, 51, 55, 56, 58]
		self.convert_sql_query_to_attributes(["0" for x in lst], c, files_dict, analyze, lst)
		analyze = '''select name , Sum(case When	NCSS 	> 0 Then 	NCSS 	Else 0 End),Sum(case When	FileLen 	> 0 Then 	FileLen 	Else 0 End),Sum(case When	sum_fors 	> 0 Then 	sum_fors 	Else 0 End),
Sum(case When	sum_ifs 	> 0 Then 	sum_ifs 	Else 0 End),Sum(case When	sum_tries 	> 0 Then 	sum_tries 	Else 0 End),Sum(case When	len_mccab 	> 0 Then 	len_mccab 	Else 0 End),
Sum(case When	sum_mccab 	> 0 Then 	sum_mccab 	Else 0 End),Sum(case When	mean_mccab 	> 0 Then 	mean_mccab 	Else 0 End),Sum(case When	median_mccab 	> 0 Then 	median_mccab 	Else 0 End),
Sum(case When	var_mccab 	> 0 Then 	var_mccab 	Else 0 End),Sum(case When	max_mccab 	> 0 Then 	max_mccab 	Else 0 End),Sum(case When	min_mccab 	> 0 Then 	min_mccab 	Else 0 End),
Sum(case When	 len_fanOut 	> 0 Then 	 len_fanOut 	Else 0 End),Sum(case When	sum_fanOut 	> 0 Then 	sum_fanOut 	Else 0 End),Sum(case When	mean_fanOut 	> 0 Then 	mean_fanOut 	Else 0 End),
Sum(case When	median_fanOut 	> 0 Then 	median_fanOut 	Else 0 End),Sum(case When	var_fanOut 	> 0 Then 	var_fanOut 	Else 0 End),Sum(case When	max_fanOut 	> 0 Then 	max_fanOut 	Else 0 End),
Sum(case When	min_fanOut 	> 0 Then 	min_fanOut 	Else 0 End),Sum(case When	 len_NPath 	> 0 Then 	 len_NPath 	Else 0 End),Sum(case When	sum_NPath 	> 0 Then 	sum_NPath 	Else 0 End),
Sum(case When	mean_NPath 	> 0 Then 	mean_NPath 	Else 0 End),Sum(case When	median_NPath 	> 0 Then 	median_NPath 	Else 0 End),Sum(case When	var_NPath 	> 0 Then 	var_NPath 	Else 0 End),
Sum(case When	max_NPath 	> 0 Then 	max_NPath 	Else 0 End),Sum(case When	min_NPath 	> 0 Then 	min_NPath 	Else 0 End),Sum(case When	 len_JavaNCSSmet 	> 0 Then 	 len_JavaNCSSmet 	Else 0 End),
Sum(case When	sum_JavaNCSSmet 	> 0 Then 	sum_JavaNCSSmet 	Else 0 End),Sum(case When	mean_JavaNCSSmet 	> 0 Then 	mean_JavaNCSSmet 	Else 0 End),Sum(case When	median_JavaNCSSmet 	> 0 Then 	median_JavaNCSSmet 	Else 0 End),
Sum(case When	var_JavaNCSSmet 	> 0 Then 	var_JavaNCSSmet 	Else 0 End),Sum(case When	max_JavaNCSSmet 	> 0 Then 	max_JavaNCSSmet 	Else 0 End),Sum(case When	min_JavaNCSSmet 	> 0 Then 	min_JavaNCSSmet 	Else 0 End),
Sum(case When	 len_thorwsSTM 	> 0 Then 	 len_thorwsSTM 	Else 0 End),Sum(case When	sum_thorwsSTM 	> 0 Then 	sum_thorwsSTM 	Else 0 End),Sum(case When	mean_thorwsSTM 	> 0 Then 	mean_thorwsSTM 	Else 0 End),
Sum(case When	median_thorwsSTM 	> 0 Then 	median_thorwsSTM 	Else 0 End),Sum(case When	var_thorwsSTM 	> 0 Then 	var_thorwsSTM 	Else 0 End),Sum(case When	max_thorwsSTM 	> 0 Then 	max_thorwsSTM 	Else 0 End),
Sum(case When	min_thorwsSTM 	> 0 Then 	min_thorwsSTM 	Else 0 End),Sum(case When	 len_coupl 	> 0 Then 	 len_coupl 	Else 0 End),Sum(case When	sum_coupl 	> 0 Then 	sum_coupl 	Else 0 End),
Sum(case When	mean_coupl 	> 0 Then 	mean_coupl 	Else 0 End),Sum(case When	median_coupl 	> 0 Then 	median_coupl 	Else 0 End),Sum(case When	var_coupl 	> 0 Then 	var_coupl 	Else 0 End),
Sum(case When	max_coupl 	> 0 Then 	max_coupl 	Else 0 End),Sum(case When	min_coupl 	> 0 Then 	min_coupl 	Else 0 End),Sum(case When	 len_executables 	> 0 Then 	 len_executables 	Else 0 End),
Sum(case When	sum_executables 	> 0 Then 	sum_executables 	Else 0 End),Sum(case When	mean_executables 	> 0 Then 	mean_executables 	Else 0 End),Sum(case When	median_executables 	> 0 Then 	median_executables 	Else 0 End),
Sum(case When	var_executables 	> 0 Then 	var_executables 	Else 0 End),Sum(case When	max_executables 	> 0 Then 	max_executables 	Else 0 End),Sum(case When	min_executables 	> 0 Then 	min_executables 	Else 0 End),
Sum(case When	 len_lens 	> 0 Then 	 len_lens 	Else 0 End),Sum(case When	sum_lens 	> 0 Then 	sum_lens 	Else 0 End),Sum(case When	mean_lens 	> 0 Then 	mean_lens 	Else 0 End),Sum(case When	median_lens 	> 0 Then 	median_lens 	Else 0 End),
Sum(case When	var_lens 	> 0 Then 	var_lens 	Else 0 End),Sum(case When	max_lens 	> 0 Then 	max_lens 	Else 0 End),Sum(case When	min_lens 	> 0 Then 	min_lens 	Else 0 End),
Sum(case When	 publics 	> 0 Then 	 publics 	Else 0 End),Sum(case When	protecteds 	> 0 Then 	protecteds 	Else 0 End),Sum(case When	privates 	> 0 Then 	privates 	Else 0 End),
Sum(case When	totals  	> 0 Then 	totals  	Else 0 End),Sum(case When	len_params 	> 0 Then 	len_params 	Else 0 End),Sum(case When	sum_params 	> 0 Then 	sum_params 	Else 0 End),
Sum(case When	mean_params 	> 0 Then 	mean_params 	Else 0 End),Sum(case When	median_params 	> 0 Then 	median_params 	Else 0 End),Sum(case When	var_params 	> 0 Then 	var_params 	Else 0 End),
Sum(case When	max_params 	> 0 Then 	max_params 	Else 0 End),Sum(case When	min_params	> 0 Then 	min_params	Else 0 End)
from checkStyleAnalyzeExtends group by name'''
		lst = [0, 1, 3, 6, 7, 9, 10, 13, 14, 15, 17, 18, 20, 21, 23, 24, 27, 28, 31, 41, 42, 45, 48,
			   55, 59, 64]
		self.convert_sql_query_to_attributes(["0" for x in lst], c, files_dict, analyze, lst)
		analyze = '''select name , Sum(case When	NCSS 	< 0 Then 	NCSS 	Else 0 End),Sum(case When	FileLen 	< 0 Then 	FileLen 	Else 0 End),Sum(case When	sum_fors 	< 0 Then 	sum_fors 	Else 0 End),
Sum(case When	sum_ifs 	< 0 Then 	sum_ifs 	Else 0 End),Sum(case When	sum_tries 	< 0 Then 	sum_tries 	Else 0 End),Sum(case When	len_mccab 	< 0 Then 	len_mccab 	Else 0 End),
Sum(case When	sum_mccab 	< 0 Then 	sum_mccab 	Else 0 End),Sum(case When	mean_mccab 	< 0 Then 	mean_mccab 	Else 0 End),Sum(case When	median_mccab 	< 0 Then 	median_mccab 	Else 0 End),
Sum(case When	var_mccab 	< 0 Then 	var_mccab 	Else 0 End),Sum(case When	max_mccab 	< 0 Then 	max_mccab 	Else 0 End),Sum(case When	min_mccab 	< 0 Then 	min_mccab 	Else 0 End),
Sum(case When	 len_fanOut 	< 0 Then 	 len_fanOut 	Else 0 End),Sum(case When	sum_fanOut 	< 0 Then 	sum_fanOut 	Else 0 End),Sum(case When	mean_fanOut 	< 0 Then 	mean_fanOut 	Else 0 End),
Sum(case When	median_fanOut 	< 0 Then 	median_fanOut 	Else 0 End),Sum(case When	var_fanOut 	< 0 Then 	var_fanOut 	Else 0 End),Sum(case When	max_fanOut 	< 0 Then 	max_fanOut 	Else 0 End),
Sum(case When	min_fanOut 	< 0 Then 	min_fanOut 	Else 0 End),Sum(case When	 len_NPath 	< 0 Then 	 len_NPath 	Else 0 End),Sum(case When	sum_NPath 	< 0 Then 	sum_NPath 	Else 0 End),
Sum(case When	mean_NPath 	< 0 Then 	mean_NPath 	Else 0 End),Sum(case When	median_NPath 	< 0 Then 	median_NPath 	Else 0 End),Sum(case When	var_NPath 	< 0 Then 	var_NPath 	Else 0 End),
Sum(case When	max_NPath 	< 0 Then 	max_NPath 	Else 0 End),Sum(case When	min_NPath 	< 0 Then 	min_NPath 	Else 0 End),Sum(case When	 len_JavaNCSSmet 	< 0 Then 	 len_JavaNCSSmet 	Else 0 End),
Sum(case When	sum_JavaNCSSmet 	< 0 Then 	sum_JavaNCSSmet 	Else 0 End),Sum(case When	mean_JavaNCSSmet 	< 0 Then 	mean_JavaNCSSmet 	Else 0 End),Sum(case When	median_JavaNCSSmet 	< 0 Then 	median_JavaNCSSmet 	Else 0 End),
Sum(case When	var_JavaNCSSmet 	< 0 Then 	var_JavaNCSSmet 	Else 0 End),Sum(case When	max_JavaNCSSmet 	< 0 Then 	max_JavaNCSSmet 	Else 0 End),Sum(case When	min_JavaNCSSmet 	< 0 Then 	min_JavaNCSSmet 	Else 0 End),
Sum(case When	 len_thorwsSTM 	< 0 Then 	 len_thorwsSTM 	Else 0 End),Sum(case When	sum_thorwsSTM 	< 0 Then 	sum_thorwsSTM 	Else 0 End),Sum(case When	mean_thorwsSTM 	< 0 Then 	mean_thorwsSTM 	Else 0 End),
Sum(case When	median_thorwsSTM 	< 0 Then 	median_thorwsSTM 	Else 0 End),Sum(case When	var_thorwsSTM 	< 0 Then 	var_thorwsSTM 	Else 0 End),Sum(case When	max_thorwsSTM 	< 0 Then 	max_thorwsSTM 	Else 0 End),
Sum(case When	min_thorwsSTM 	< 0 Then 	min_thorwsSTM 	Else 0 End),Sum(case When	 len_coupl 	< 0 Then 	 len_coupl 	Else 0 End),Sum(case When	sum_coupl 	< 0 Then 	sum_coupl 	Else 0 End),
Sum(case When	mean_coupl 	< 0 Then 	mean_coupl 	Else 0 End),Sum(case When	median_coupl 	< 0 Then 	median_coupl 	Else 0 End),Sum(case When	var_coupl 	< 0 Then 	var_coupl 	Else 0 End),
Sum(case When	max_coupl 	< 0 Then 	max_coupl 	Else 0 End),Sum(case When	min_coupl 	< 0 Then 	min_coupl 	Else 0 End),Sum(case When	 len_executables 	< 0 Then 	 len_executables 	Else 0 End),
Sum(case When	sum_executables 	< 0 Then 	sum_executables 	Else 0 End),Sum(case When	mean_executables 	< 0 Then 	mean_executables 	Else 0 End),Sum(case When	median_executables 	< 0 Then 	median_executables 	Else 0 End),
Sum(case When	var_executables 	< 0 Then 	var_executables 	Else 0 End),Sum(case When	max_executables 	< 0 Then 	max_executables 	Else 0 End),Sum(case When	min_executables 	< 0 Then 	min_executables 	Else 0 End),
Sum(case When	 len_lens 	< 0 Then 	 len_lens 	Else 0 End),Sum(case When	sum_lens 	< 0 Then 	sum_lens 	Else 0 End),Sum(case When	mean_lens 	< 0 Then 	mean_lens 	Else 0 End),Sum(case When	median_lens 	< 0 Then 	median_lens 	Else 0 End),
Sum(case When	var_lens 	< 0 Then 	var_lens 	Else 0 End),Sum(case When	max_lens 	< 0 Then 	max_lens 	Else 0 End),Sum(case When	min_lens 	< 0 Then 	min_lens 	Else 0 End),
Sum(case When	 publics 	< 0 Then 	 publics 	Else 0 End),Sum(case When	protecteds 	< 0 Then 	protecteds 	Else 0 End),Sum(case When	privates 	< 0 Then 	privates 	Else 0 End),
Sum(case When	totals  	< 0 Then 	totals  	Else 0 End),Sum(case When	len_params 	< 0 Then 	len_params 	Else 0 End),Sum(case When	sum_params 	< 0 Then 	sum_params 	Else 0 End),
Sum(case When	mean_params 	< 0 Then 	mean_params 	Else 0 End),Sum(case When	median_params 	< 0 Then 	median_params 	Else 0 End),Sum(case When	var_params 	< 0 Then 	var_params 	Else 0 End),
Sum(case When	max_params 	< 0 Then 	max_params 	Else 0 End),Sum(case When	min_params	< 0 Then 	min_params	Else 0 End)
from checkStyleAnalyzeExtends group by name'''
		lst = [1, 6, 7, 9, 10, 13, 14, 15, 17, 18, 20, 21, 23, 24, 27, 28, 29, 30, 31, 41, 42, 43,
			   45, 46, 48, 49, 51,
			   52, 55, 56, 57, 58, 59]
		self.convert_sql_query_to_attributes(["0" for x in lst], c, files_dict, analyze, lst)
		analyze = '''select name , avg(case When	NCSS 	> 0 Then 	NCSS 	Else null End),avg(case When	FileLen 	> 0 Then 	FileLen 	Else null End),avg(case When	sum_fors 	> 0 Then 	sum_fors 	Else null End),
avg(case When	sum_ifs 	> 0 Then 	sum_ifs 	Else null End),avg(case When	sum_tries 	> 0 Then 	sum_tries 	Else null End),avg(case When	len_mccab 	> 0 Then 	len_mccab 	Else null End),
avg(case When	sum_mccab 	> 0 Then 	sum_mccab 	Else null End),avg(case When	mean_mccab 	> 0 Then 	mean_mccab 	Else null End),avg(case When	median_mccab 	> 0 Then 	median_mccab 	Else null End),
avg(case When	var_mccab 	> 0 Then 	var_mccab 	Else null End),avg(case When	max_mccab 	> 0 Then 	max_mccab 	Else null End),avg(case When	min_mccab 	> 0 Then 	min_mccab 	Else null End),
avg(case When	 len_fanOut 	> 0 Then 	 len_fanOut 	Else null End),avg(case When	sum_fanOut 	> 0 Then 	sum_fanOut 	Else null End),avg(case When	mean_fanOut 	> 0 Then 	mean_fanOut 	Else null End),
avg(case When	median_fanOut 	> 0 Then 	median_fanOut 	Else null End),avg(case When	var_fanOut 	> 0 Then 	var_fanOut 	Else null End),avg(case When	max_fanOut 	> 0 Then 	max_fanOut 	Else null End),
avg(case When	min_fanOut 	> 0 Then 	min_fanOut 	Else null End),avg(case When	 len_NPath 	> 0 Then 	 len_NPath 	Else null End),avg(case When	sum_NPath 	> 0 Then 	sum_NPath 	Else null End),
avg(case When	mean_NPath 	> 0 Then 	mean_NPath 	Else null End),avg(case When	median_NPath 	> 0 Then 	median_NPath 	Else null End),avg(case When	var_NPath 	> 0 Then 	var_NPath 	Else null End),
avg(case When	max_NPath 	> 0 Then 	max_NPath 	Else null End),avg(case When	min_NPath 	> 0 Then 	min_NPath 	Else null End),avg(case When	 len_JavaNCSSmet 	> 0 Then 	 len_JavaNCSSmet 	Else null End),
avg(case When	sum_JavaNCSSmet 	> 0 Then 	sum_JavaNCSSmet 	Else null End),avg(case When	mean_JavaNCSSmet 	> 0 Then 	mean_JavaNCSSmet 	Else null End),avg(case When	median_JavaNCSSmet 	> 0 Then 	median_JavaNCSSmet 	Else null End),
avg(case When	var_JavaNCSSmet 	> 0 Then 	var_JavaNCSSmet 	Else null End),avg(case When	max_JavaNCSSmet 	> 0 Then 	max_JavaNCSSmet 	Else null End),avg(case When	min_JavaNCSSmet 	> 0 Then 	min_JavaNCSSmet 	Else null End),
avg(case When	 len_thorwsSTM 	> 0 Then 	 len_thorwsSTM 	Else null End),avg(case When	sum_thorwsSTM 	> 0 Then 	sum_thorwsSTM 	Else null End),avg(case When	mean_thorwsSTM 	> 0 Then 	mean_thorwsSTM 	Else null End),
avg(case When	median_thorwsSTM 	> 0 Then 	median_thorwsSTM 	Else null End),avg(case When	var_thorwsSTM 	> 0 Then 	var_thorwsSTM 	Else null End),avg(case When	max_thorwsSTM 	> 0 Then 	max_thorwsSTM 	Else null End),
avg(case When	min_thorwsSTM 	> 0 Then 	min_thorwsSTM 	Else null End),avg(case When	 len_coupl 	> 0 Then 	 len_coupl 	Else null End),avg(case When	sum_coupl 	> 0 Then 	sum_coupl 	Else null End),
avg(case When	mean_coupl 	> 0 Then 	mean_coupl 	Else null End),avg(case When	median_coupl 	> 0 Then 	median_coupl 	Else null End),avg(case When	var_coupl 	> 0 Then 	var_coupl 	Else null End),
avg(case When	max_coupl 	> 0 Then 	max_coupl 	Else null End),avg(case When	min_coupl 	> 0 Then 	min_coupl 	Else null End),avg(case When	 len_executables 	> 0 Then 	 len_executables 	Else null End),
avg(case When	sum_executables 	> 0 Then 	sum_executables 	Else null End),avg(case When	mean_executables 	> 0 Then 	mean_executables 	Else null End),avg(case When	median_executables 	> 0 Then 	median_executables 	Else null End),
avg(case When	var_executables 	> 0 Then 	var_executables 	Else null End),avg(case When	max_executables 	> 0 Then 	max_executables 	Else null End),avg(case When	min_executables 	> 0 Then 	min_executables 	Else null End),
avg(case When	 len_lens 	> 0 Then 	 len_lens 	Else null End),avg(case When	sum_lens 	> 0 Then 	sum_lens 	Else null End),avg(case When	mean_lens 	> 0 Then 	mean_lens 	Else null End),
avg(case When	median_lens 	> 0 Then 	median_lens 	Else null End),avg(case When	var_lens 	> 0 Then 	var_lens 	Else null End),avg(case When	max_lens 	> 0 Then 	max_lens 	Else null End),
avg(case When	min_lens 	> 0 Then 	min_lens 	Else null End),avg(case When	 publics 	> 0 Then 	 publics 	Else null End),avg(case When	protecteds 	> 0 Then 	protecteds 	Else null End),
avg(case When	privates 	> 0 Then 	privates 	Else null End),avg(case When	totals  	> 0 Then 	totals  	Else null End),avg(case When	len_params 	> 0 Then 	len_params 	Else null End),
avg(case When	sum_params 	> 0 Then 	sum_params 	Else null End),avg(case When	mean_params 	> 0 Then 	mean_params 	Else null End),avg(case When	median_params 	> 0 Then 	median_params 	Else null End),
avg(case When	var_params 	> 0 Then 	var_params 	Else null End),avg(case When	max_params 	> 0 Then 	max_params 	Else null End),avg(case When	min_params	> 0 Then 	min_params	Else null End)
from checkStyleAnalyzeExtends group by name'''
		lst = [3, 6, 7, 10, 13, 14, 15, 17, 18, 20, 21, 23, 24, 27, 28, 29, 31, 41, 42, 43, 45, 46,
			   48, 49, 52, 55, 56,
			   57, 59]
		self.convert_sql_query_to_attributes(["0" for x in lst], c, files_dict, analyze, lst)
		analyze = '''select name , avg(case When	NCSS 	< 0 Then 	NCSS 	Else null End),avg(case When	FileLen 	< 0 Then 	FileLen 	Else null End),avg(case When	sum_fors 	< 0 Then 	sum_fors 	Else null End),
avg(case When	sum_ifs 	< 0 Then 	sum_ifs 	Else null End),avg(case When	sum_tries 	< 0 Then 	sum_tries 	Else null End),avg(case When	len_mccab 	< 0 Then 	len_mccab 	Else null End),
avg(case When	sum_mccab 	< 0 Then 	sum_mccab 	Else null End),avg(case When	mean_mccab 	< 0 Then 	mean_mccab 	Else null End),avg(case When	median_mccab 	< 0 Then 	median_mccab 	Else null End),
avg(case When	var_mccab 	< 0 Then 	var_mccab 	Else null End),avg(case When	max_mccab 	< 0 Then 	max_mccab 	Else null End),avg(case When	min_mccab 	< 0 Then 	min_mccab 	Else null End),
avg(case When	 len_fanOut 	< 0 Then 	 len_fanOut 	Else null End),avg(case When	sum_fanOut 	< 0 Then 	sum_fanOut 	Else null End),avg(case When	mean_fanOut 	< 0 Then 	mean_fanOut 	Else null End),
avg(case When	median_fanOut 	< 0 Then 	median_fanOut 	Else null End),avg(case When	var_fanOut 	< 0 Then 	var_fanOut 	Else null End),avg(case When	max_fanOut 	< 0 Then 	max_fanOut 	Else null End),
avg(case When	min_fanOut 	< 0 Then 	min_fanOut 	Else null End),avg(case When	 len_NPath 	< 0 Then 	 len_NPath 	Else null End),avg(case When	sum_NPath 	< 0 Then 	sum_NPath 	Else null End),
avg(case When	mean_NPath 	< 0 Then 	mean_NPath 	Else null End),avg(case When	median_NPath 	< 0 Then 	median_NPath 	Else null End),avg(case When	var_NPath 	< 0 Then 	var_NPath 	Else null End),
avg(case When	max_NPath 	< 0 Then 	max_NPath 	Else null End),avg(case When	min_NPath 	< 0 Then 	min_NPath 	Else null End),avg(case When	 len_JavaNCSSmet 	< 0 Then 	 len_JavaNCSSmet 	Else null End),
avg(case When	sum_JavaNCSSmet 	< 0 Then 	sum_JavaNCSSmet 	Else null End),avg(case When	mean_JavaNCSSmet 	< 0 Then 	mean_JavaNCSSmet 	Else null End),avg(case When	median_JavaNCSSmet 	< 0 Then 	median_JavaNCSSmet 	Else null End),
avg(case When	var_JavaNCSSmet 	< 0 Then 	var_JavaNCSSmet 	Else null End),avg(case When	max_JavaNCSSmet 	< 0 Then 	max_JavaNCSSmet 	Else null End),avg(case When	min_JavaNCSSmet 	< 0 Then 	min_JavaNCSSmet 	Else null End),
avg(case When	 len_thorwsSTM 	< 0 Then 	 len_thorwsSTM 	Else null End),avg(case When	sum_thorwsSTM 	< 0 Then 	sum_thorwsSTM 	Else null End),avg(case When	mean_thorwsSTM 	< 0 Then 	mean_thorwsSTM 	Else null End),
avg(case When	median_thorwsSTM 	< 0 Then 	median_thorwsSTM 	Else null End),avg(case When	var_thorwsSTM 	< 0 Then 	var_thorwsSTM 	Else null End),avg(case When	max_thorwsSTM 	< 0 Then 	max_thorwsSTM 	Else null End),
avg(case When	min_thorwsSTM 	< 0 Then 	min_thorwsSTM 	Else null End),avg(case When	 len_coupl 	< 0 Then 	 len_coupl 	Else null End),avg(case When	sum_coupl 	< 0 Then 	sum_coupl 	Else null End),
avg(case When	mean_coupl 	< 0 Then 	mean_coupl 	Else null End),avg(case When	median_coupl 	< 0 Then 	median_coupl 	Else null End),avg(case When	var_coupl 	< 0 Then 	var_coupl 	Else null End),
avg(case When	max_coupl 	< 0 Then 	max_coupl 	Else null End),avg(case When	min_coupl 	< 0 Then 	min_coupl 	Else null End),avg(case When	 len_executables 	< 0 Then 	 len_executables 	Else null End),
avg(case When	sum_executables 	< 0 Then 	sum_executables 	Else null End),avg(case When	mean_executables 	< 0 Then 	mean_executables 	Else null End),avg(case When	median_executables 	< 0 Then 	median_executables 	Else null End),
avg(case When	var_executables 	< 0 Then 	var_executables 	Else null End),avg(case When	max_executables 	< 0 Then 	max_executables 	Else null End),avg(case When	min_executables 	< 0 Then 	min_executables 	Else null End),
avg(case When	 len_lens 	< 0 Then 	 len_lens 	Else null End),avg(case When	sum_lens 	< 0 Then 	sum_lens 	Else null End),avg(case When	mean_lens 	< 0 Then 	mean_lens 	Else null End),
avg(case When	median_lens 	< 0 Then 	median_lens 	Else null End),avg(case When	var_lens 	< 0 Then 	var_lens 	Else null End),avg(case When	max_lens 	< 0 Then 	max_lens 	Else null End),
avg(case When	min_lens 	< 0 Then 	min_lens 	Else null End),avg(case When	 publics 	< 0 Then 	 publics 	Else null End),avg(case When	protecteds 	< 0 Then 	protecteds 	Else null End),
avg(case When	privates 	< 0 Then 	privates 	Else null End),avg(case When	totals  	< 0 Then 	totals  	Else null End),avg(case When	len_params 	< 0 Then 	len_params 	Else null End),
avg(case When	sum_params 	< 0 Then 	sum_params 	Else null End),avg(case When	mean_params 	< 0 Then 	mean_params 	Else null End),avg(case When	median_params 	< 0 Then 	median_params 	Else null End),
avg(case When	var_params 	< 0 Then 	var_params 	Else null End),avg(case When	max_params 	< 0 Then 	max_params 	Else null End),avg(case When	min_params	< 0 Then 	min_params	Else null End)
from checkStyleAnalyzeExtends group by name'''
		lst = [1, 6, 7, 9, 13, 14, 15, 17, 18, 20, 21, 23, 27, 28, 30, 41, 42, 45, 48, 49, 51, 55,
			   56, 58]
		self.convert_sql_query_to_attributes(["0" for x in lst], c, files_dict, analyze, lst)
