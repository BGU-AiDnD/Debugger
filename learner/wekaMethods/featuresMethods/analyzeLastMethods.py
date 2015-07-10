__author__ = 'amir'

from wekaMethods.articles import *
#from wekaMethods.articles import sqlToAttributes
best_features=[1,2,4,7,8,10,11,14,15,16,18,19,21,22,24,25,28,42,43,44,46,49,56,60,65,76,79,80,81,83,84,86,87,88,90,91,93,94,95,96,97,98,100,101,102,104,105,107,108,109,111,112,114,115,116,118,119,121,122,123,125,126,128,129,130,132,133,145,146,148,150,151,152,154,155,158,159,160,161,162,163,164,165,166,168,169,171,172,173,175,176,186,187,188,190,191,192,193,194,196,197,199,200,201,202,203,204,206,208,209,217,218,220,223,224,226,230,231,232,234,237,238,240,244,245,247,259,265,266,268,272,273,275,289,290,292,295,296,298,299,302,303,304,306,307,309,310,312,313,316,317,320,330,331,334,337,344,348,353,362,367,368,370,371,374,375,376,378,379,381,382,384,385,388,389,390,391,392,402,403,404,406,407,409,410,412,413,416,417,418,419,420,436,439,440,443,446,447,448,450,451,453,454,456,457,460,461,462,464,474,475,476,478,479,481,482,485,488,489,490,492,506,511,512,514,518,519,520,522,523,525,526,528,532,533,535,546,547,550,553,554,556,560,561,563]
class analyzeLastMethods:
    def get_attributes(self):
        all= [ ("NCSS_AnalyzeLast_sum",  "NUMERIC"),("FileLen_AnalyzeLast_sum",  "NUMERIC"),("sum_fors_AnalyzeLast_sum",  "NUMERIC"),("sum_ifs_AnalyzeLast_sum",  "NUMERIC"),
("sum_tries_AnalyzeLast_sum",  "NUMERIC"),("len_mccab_AnalyzeLast_sum",  "NUMERIC"),("sum_mccab_AnalyzeLast_sum",  "NUMERIC"),("mean_mccab_AnalyzeLast_sum",  "NUMERIC"),
("median_mccab_AnalyzeLast_sum",  "NUMERIC"),("var_mccab_AnalyzeLast_sum",  "NUMERIC"),("max_mccab_AnalyzeLast_sum",  "NUMERIC"),("min_mccab_AnalyzeLast_sum",  "NUMERIC"),
(" len_fanOut_AnalyzeLast_sum",  "NUMERIC"),("sum_fanOut_AnalyzeLast_sum",  "NUMERIC"),("mean_fanOut_AnalyzeLast_sum",  "NUMERIC"),("median_fanOut_AnalyzeLast_sum",  "NUMERIC"),
("var_fanOut_AnalyzeLast_sum",  "NUMERIC"),("max_fanOut_AnalyzeLast_sum",  "NUMERIC"),("min_fanOut_AnalyzeLast_sum",  "NUMERIC"),(" len_NPath_AnalyzeLast_sum",  "NUMERIC"),
("sum_NPath_AnalyzeLast_sum",  "NUMERIC"),("mean_NPath_AnalyzeLast_sum",  "NUMERIC"),("median_NPath_AnalyzeLast_sum",  "NUMERIC"),("var_NPath_AnalyzeLast_sum",  "NUMERIC"),
("max_NPath_AnalyzeLast_sum",  "NUMERIC"),("min_NPath_AnalyzeLast_sum",  "NUMERIC"),(" len_JavaNCSSmet_AnalyzeLast_sum",  "NUMERIC"),("sum_JavaNCSSmet_AnalyzeLast_sum",  "NUMERIC"),
("mean_JavaNCSSmet_AnalyzeLast_sum",  "NUMERIC"),("median_JavaNCSSmet_AnalyzeLast_sum",  "NUMERIC"),("var_JavaNCSSmet_AnalyzeLast_sum",  "NUMERIC"),("max_JavaNCSSmet_AnalyzeLast_sum",  "NUMERIC"),
("min_JavaNCSSmet_AnalyzeLast_sum",  "NUMERIC"),(" len_thorwsSTM_AnalyzeLast_sum",  "NUMERIC"),("sum_thorwsSTM_AnalyzeLast_sum",  "NUMERIC"),("mean_thorwsSTM_AnalyzeLast_sum",  "NUMERIC"),
("median_thorwsSTM_AnalyzeLast_sum",  "NUMERIC"),("var_thorwsSTM_AnalyzeLast_sum",  "NUMERIC"),("max_thorwsSTM_AnalyzeLast_sum",  "NUMERIC"),("min_thorwsSTM_AnalyzeLast_sum",  "NUMERIC"),
(" len_coupl_AnalyzeLast_sum",  "NUMERIC"),("sum_coupl_AnalyzeLast_sum",  "NUMERIC"),("mean_coupl_AnalyzeLast_sum",  "NUMERIC"),("median_coupl_AnalyzeLast_sum",  "NUMERIC"),
("var_coupl_AnalyzeLast_sum",  "NUMERIC"),("max_coupl_AnalyzeLast_sum",  "NUMERIC"),("min_coupl_AnalyzeLast_sum",  "NUMERIC"),(" len_executables_AnalyzeLast_sum",  "NUMERIC"),
("sum_executables_AnalyzeLast_sum",  "NUMERIC"),("mean_executables_AnalyzeLast_sum",  "NUMERIC"),("median_executables_AnalyzeLast_sum",  "NUMERIC"),("var_executables_AnalyzeLast_sum",  "NUMERIC"),
("max_executables_AnalyzeLast_sum",  "NUMERIC"),("min_executables_AnalyzeLast_sum",  "NUMERIC"),(" len_lens_AnalyzeLast_sum",  "NUMERIC"),
("sum_lens_AnalyzeLast_sum",  "NUMERIC"),("mean_lens_AnalyzeLast_sum",  "NUMERIC"),("median_lens_AnalyzeLast_sum",  "NUMERIC"),("var_lens_AnalyzeLast_sum",  "NUMERIC"),
("max_lens_AnalyzeLast_sum",  "NUMERIC"),("min_lens_AnalyzeLast_sum",  "NUMERIC"),(" publics_AnalyzeLast_sum",  "NUMERIC"),("protecteds_AnalyzeLast_sum",  "NUMERIC"),
("privates_AnalyzeLast_sum",  "NUMERIC"),("totals _AnalyzeLast_sum",  "NUMERIC"),("len_params_AnalyzeLast_sum",  "NUMERIC"),("sum_params_AnalyzeLast_sum",  "NUMERIC"),
("mean_params_AnalyzeLast_sum",  "NUMERIC"),("median_params_AnalyzeLast_sum",  "NUMERIC"),("var_params_AnalyzeLast_sum",  "NUMERIC"),("max_params_AnalyzeLast_sum",  "NUMERIC"),
("min_params_AnalyzeLast_sum",  "NUMERIC"),("NCSS_AnalyzeLast_avg",  "NUMERIC"),("FileLen_AnalyzeLast_avg",  "NUMERIC"),("sum_fors_AnalyzeLast_avg",  "NUMERIC"),("sum_ifs_AnalyzeLast_avg",  "NUMERIC"),
("sum_tries_AnalyzeLast_avg",  "NUMERIC"),("len_mccab_AnalyzeLast_avg",  "NUMERIC"),("sum_mccab_AnalyzeLast_avg",  "NUMERIC"),("mean_mccab_AnalyzeLast_avg",  "NUMERIC"),
("median_mccab_AnalyzeLast_avg",  "NUMERIC"),("var_mccab_AnalyzeLast_avg",  "NUMERIC"),("max_mccab_AnalyzeLast_avg",  "NUMERIC"),("min_mccab_AnalyzeLast_avg",  "NUMERIC"),
(" len_fanOut_AnalyzeLast_avg",  "NUMERIC"),("sum_fanOut_AnalyzeLast_avg",  "NUMERIC"),("mean_fanOut_AnalyzeLast_avg",  "NUMERIC"),("median_fanOut_AnalyzeLast_avg",  "NUMERIC"),
("var_fanOut_AnalyzeLast_avg",  "NUMERIC"),("max_fanOut_AnalyzeLast_avg",  "NUMERIC"),("min_fanOut_AnalyzeLast_avg",  "NUMERIC"),(" len_NPath_AnalyzeLast_avg",  "NUMERIC"),
("sum_NPath_AnalyzeLast_avg",  "NUMERIC"),("mean_NPath_AnalyzeLast_avg",  "NUMERIC"),("median_NPath_AnalyzeLast_avg",  "NUMERIC"),("var_NPath_AnalyzeLast_avg",  "NUMERIC"),
("max_NPath_AnalyzeLast_avg",  "NUMERIC"),("min_NPath_AnalyzeLast_avg",  "NUMERIC"),(" len_JavaNCSSmet_AnalyzeLast_avg",  "NUMERIC"),("sum_JavaNCSSmet_AnalyzeLast_avg",  "NUMERIC"),
("mean_JavaNCSSmet_AnalyzeLast_avg",  "NUMERIC"),("median_JavaNCSSmet_AnalyzeLast_avg",  "NUMERIC"),("var_JavaNCSSmet_AnalyzeLast_avg",  "NUMERIC"),("max_JavaNCSSmet_AnalyzeLast_avg",  "NUMERIC"),
("min_JavaNCSSmet_AnalyzeLast_avg",  "NUMERIC"),(" len_thorwsSTM_AnalyzeLast_avg",  "NUMERIC"),("sum_thorwsSTM_AnalyzeLast_avg",  "NUMERIC"),("mean_thorwsSTM_AnalyzeLast_avg",  "NUMERIC"),
("median_thorwsSTM_AnalyzeLast_avg",  "NUMERIC"),("var_thorwsSTM_AnalyzeLast_avg",  "NUMERIC"),("max_thorwsSTM_AnalyzeLast_avg",  "NUMERIC"),("min_thorwsSTM_AnalyzeLast_avg",  "NUMERIC"),
(" len_coupl_AnalyzeLast_avg",  "NUMERIC"),("sum_coupl_AnalyzeLast_avg",  "NUMERIC"),("mean_coupl_AnalyzeLast_avg",  "NUMERIC"),("median_coupl_AnalyzeLast_avg",  "NUMERIC"),
("var_coupl_AnalyzeLast_avg",  "NUMERIC"),("max_coupl_AnalyzeLast_avg",  "NUMERIC"),("min_coupl_AnalyzeLast_avg",  "NUMERIC"),(" len_executables_AnalyzeLast_avg",  "NUMERIC"),
("sum_executables_AnalyzeLast_avg",  "NUMERIC"),("mean_executables_AnalyzeLast_avg",  "NUMERIC"),("median_executables_AnalyzeLast_avg",  "NUMERIC"),("var_executables_AnalyzeLast_avg",  "NUMERIC"),
("max_executables_AnalyzeLast_avg",  "NUMERIC"),("min_executables_AnalyzeLast_avg",  "NUMERIC"),(" len_lens_AnalyzeLast_avg",  "NUMERIC"),
("sum_lens_AnalyzeLast_avg",  "NUMERIC"),("mean_lens_AnalyzeLast_avg",  "NUMERIC"),("median_lens_AnalyzeLast_avg",  "NUMERIC"),("var_lens_AnalyzeLast_avg",  "NUMERIC"),
("max_lens_AnalyzeLast_avg",  "NUMERIC"),("min_lens_AnalyzeLast_avg",  "NUMERIC"),(" publics_AnalyzeLast_avg",  "NUMERIC"),("protecteds_AnalyzeLast_avg",  "NUMERIC"),
("privates_AnalyzeLast_avg",  "NUMERIC"),("totals _AnalyzeLast_avg",  "NUMERIC"),("len_params_AnalyzeLast_avg",  "NUMERIC"),("sum_params_AnalyzeLast_avg",  "NUMERIC"),
("mean_params_AnalyzeLast_avg",  "NUMERIC"),("median_params_AnalyzeLast_avg",  "NUMERIC"),("var_params_AnalyzeLast_avg",  "NUMERIC"),("max_params_AnalyzeLast_avg",  "NUMERIC"),
("min_params_AnalyzeLast_avg",  "NUMERIC"),
("NCSS_AnalyzeLast_countPos",  "NUMERIC"),("FileLen_AnalyzeLast_countPos",  "NUMERIC"),("sum_fors_AnalyzeLast_countPos",  "NUMERIC"),("sum_ifs_AnalyzeLast_countPos",  "NUMERIC"),
("sum_tries_AnalyzeLast_countPos",  "NUMERIC"),("len_mccab_AnalyzeLast_countPos",  "NUMERIC"),("sum_mccab_AnalyzeLast_countPos",  "NUMERIC"),("mean_mccab_AnalyzeLast_countPos",  "NUMERIC"),
("median_mccab_AnalyzeLast_countPos",  "NUMERIC"),("var_mccab_AnalyzeLast_countPos",  "NUMERIC"),("max_mccab_AnalyzeLast_countPos",  "NUMERIC"),("min_mccab_AnalyzeLast_countPos",  "NUMERIC"),
(" len_fanOut_AnalyzeLast_countPos",  "NUMERIC"),("sum_fanOut_AnalyzeLast_countPos",  "NUMERIC"),("mean_fanOut_AnalyzeLast_countPos",  "NUMERIC"),("median_fanOut_AnalyzeLast_countPos",  "NUMERIC"),
("var_fanOut_AnalyzeLast_countPos",  "NUMERIC"),("max_fanOut_AnalyzeLast_countPos",  "NUMERIC"),("min_fanOut_AnalyzeLast_countPos",  "NUMERIC"),(" len_NPath_AnalyzeLast_countPos",  "NUMERIC"),
("sum_NPath_AnalyzeLast_countPos",  "NUMERIC"),("mean_NPath_AnalyzeLast_countPos",  "NUMERIC"),("median_NPath_AnalyzeLast_countPos",  "NUMERIC"),("var_NPath_AnalyzeLast_countPos",  "NUMERIC"),
("max_NPath_AnalyzeLast_countPos",  "NUMERIC"),("min_NPath_AnalyzeLast_countPos",  "NUMERIC"),(" len_JavaNCSSmet_AnalyzeLast_countPos",  "NUMERIC"),("sum_JavaNCSSmet_AnalyzeLast_countPos",  "NUMERIC"),
("mean_JavaNCSSmet_AnalyzeLast_countPos",  "NUMERIC"),("median_JavaNCSSmet_AnalyzeLast_countPos",  "NUMERIC"),("var_JavaNCSSmet_AnalyzeLast_countPos",  "NUMERIC"),("max_JavaNCSSmet_AnalyzeLast_countPos",  "NUMERIC"),
("min_JavaNCSSmet_AnalyzeLast_countPos",  "NUMERIC"),(" len_thorwsSTM_AnalyzeLast_countPos",  "NUMERIC"),("sum_thorwsSTM_AnalyzeLast_countPos",  "NUMERIC"),("mean_thorwsSTM_AnalyzeLast_countPos",  "NUMERIC"),
("median_thorwsSTM_AnalyzeLast_countPos",  "NUMERIC"),("var_thorwsSTM_AnalyzeLast_countPos",  "NUMERIC"),("max_thorwsSTM_AnalyzeLast_countPos",  "NUMERIC"),("min_thorwsSTM_AnalyzeLast_countPos",  "NUMERIC"),
(" len_coupl_AnalyzeLast_countPos",  "NUMERIC"),("sum_coupl_AnalyzeLast_countPos",  "NUMERIC"),("mean_coupl_AnalyzeLast_countPos",  "NUMERIC"),("median_coupl_AnalyzeLast_countPos",  "NUMERIC"),
("var_coupl_AnalyzeLast_countPos",  "NUMERIC"),("max_coupl_AnalyzeLast_countPos",  "NUMERIC"),("min_coupl_AnalyzeLast_countPos",  "NUMERIC"),(" len_executables_AnalyzeLast_countPos",  "NUMERIC"),
("sum_executables_AnalyzeLast_countPos",  "NUMERIC"),("mean_executables_AnalyzeLast_countPos",  "NUMERIC"),("median_executables_AnalyzeLast_countPos",  "NUMERIC"),("var_executables_AnalyzeLast_countPos",  "NUMERIC"),
("max_executables_AnalyzeLast_countPos",  "NUMERIC"),("min_executables_AnalyzeLast_countPos",  "NUMERIC"),(" len_lens_AnalyzeLast_countPos",  "NUMERIC"),
("sum_lens_AnalyzeLast_countPos",  "NUMERIC"),("mean_lens_AnalyzeLast_countPos",  "NUMERIC"),("median_lens_AnalyzeLast_countPos",  "NUMERIC"),("var_lens_AnalyzeLast_countPos",  "NUMERIC"),
("max_lens_AnalyzeLast_countPos",  "NUMERIC"),("min_lens_AnalyzeLast_countPos",  "NUMERIC"),(" publics_AnalyzeLast_countPos",  "NUMERIC"),("protecteds_AnalyzeLast_countPos",  "NUMERIC"),
("privates_AnalyzeLast_countPos",  "NUMERIC"),("totals _AnalyzeLast_countPos",  "NUMERIC"),("len_params_AnalyzeLast_countPos",  "NUMERIC"),("sum_params_AnalyzeLast_countPos",  "NUMERIC"),
("mean_params_AnalyzeLast_countPos",  "NUMERIC"),("median_params_AnalyzeLast_countPos",  "NUMERIC"),("var_params_AnalyzeLast_countPos",  "NUMERIC"),("max_params_AnalyzeLast_countPos",  "NUMERIC"),
("min_params_AnalyzeLast_countPos",  "NUMERIC"),("NCSS_AnalyzeLast_countNeg",  "NUMERIC"),("FileLen_AnalyzeLast_countNeg",  "NUMERIC"),("sum_fors_AnalyzeLast_countNeg",  "NUMERIC"),("sum_ifs_AnalyzeLast_countNeg",  "NUMERIC"),
("sum_tries_AnalyzeLast_countNeg",  "NUMERIC"),("len_mccab_AnalyzeLast_countNeg",  "NUMERIC"),("sum_mccab_AnalyzeLast_countNeg",  "NUMERIC"),("mean_mccab_AnalyzeLast_countNeg",  "NUMERIC"),
("median_mccab_AnalyzeLast_countNeg",  "NUMERIC"),("var_mccab_AnalyzeLast_countNeg",  "NUMERIC"),("max_mccab_AnalyzeLast_countNeg",  "NUMERIC"),("min_mccab_AnalyzeLast_countNeg",  "NUMERIC"),
(" len_fanOut_AnalyzeLast_countNeg",  "NUMERIC"),("sum_fanOut_AnalyzeLast_countNeg",  "NUMERIC"),("mean_fanOut_AnalyzeLast_countNeg",  "NUMERIC"),("median_fanOut_AnalyzeLast_countNeg",  "NUMERIC"),
("var_fanOut_AnalyzeLast_countNeg",  "NUMERIC"),("max_fanOut_AnalyzeLast_countNeg",  "NUMERIC"),("min_fanOut_AnalyzeLast_countNeg",  "NUMERIC"),(" len_NPath_AnalyzeLast_countNeg",  "NUMERIC"),
("sum_NPath_AnalyzeLast_countNeg",  "NUMERIC"),("mean_NPath_AnalyzeLast_countNeg",  "NUMERIC"),("median_NPath_AnalyzeLast_countNeg",  "NUMERIC"),("var_NPath_AnalyzeLast_countNeg",  "NUMERIC"),
("max_NPath_AnalyzeLast_countNeg",  "NUMERIC"),("min_NPath_AnalyzeLast_countNeg",  "NUMERIC"),(" len_JavaNCSSmet_AnalyzeLast_countNeg",  "NUMERIC"),("sum_JavaNCSSmet_AnalyzeLast_countNeg",  "NUMERIC"),
("mean_JavaNCSSmet_AnalyzeLast_countNeg",  "NUMERIC"),("median_JavaNCSSmet_AnalyzeLast_countNeg",  "NUMERIC"),("var_JavaNCSSmet_AnalyzeLast_countNeg",  "NUMERIC"),("max_JavaNCSSmet_AnalyzeLast_countNeg",  "NUMERIC"),
("min_JavaNCSSmet_AnalyzeLast_countNeg",  "NUMERIC"),(" len_thorwsSTM_AnalyzeLast_countNeg",  "NUMERIC"),("sum_thorwsSTM_AnalyzeLast_countNeg",  "NUMERIC"),("mean_thorwsSTM_AnalyzeLast_countNeg",  "NUMERIC"),
("median_thorwsSTM_AnalyzeLast_countNeg",  "NUMERIC"),("var_thorwsSTM_AnalyzeLast_countNeg",  "NUMERIC"),("max_thorwsSTM_AnalyzeLast_countNeg",  "NUMERIC"),("min_thorwsSTM_AnalyzeLast_countNeg",  "NUMERIC"),
(" len_coupl_AnalyzeLast_countNeg",  "NUMERIC"),("sum_coupl_AnalyzeLast_countNeg",  "NUMERIC"),("mean_coupl_AnalyzeLast_countNeg",  "NUMERIC"),("median_coupl_AnalyzeLast_countNeg",  "NUMERIC"),
("var_coupl_AnalyzeLast_countNeg",  "NUMERIC"),("max_coupl_AnalyzeLast_countNeg",  "NUMERIC"),("min_coupl_AnalyzeLast_countNeg",  "NUMERIC"),(" len_executables_AnalyzeLast_countNeg",  "NUMERIC"),
("sum_executables_AnalyzeLast_countNeg",  "NUMERIC"),("mean_executables_AnalyzeLast_countNeg",  "NUMERIC"),("median_executables_AnalyzeLast_countNeg",  "NUMERIC"),("var_executables_AnalyzeLast_countNeg",  "NUMERIC"),
("max_executables_AnalyzeLast_countNeg",  "NUMERIC"),("min_executables_AnalyzeLast_countNeg",  "NUMERIC"),(" len_lens_AnalyzeLast_countNeg",  "NUMERIC"),
("sum_lens_AnalyzeLast_countNeg",  "NUMERIC"),("mean_lens_AnalyzeLast_countNeg",  "NUMERIC"),("median_lens_AnalyzeLast_countNeg",  "NUMERIC"),("var_lens_AnalyzeLast_countNeg",  "NUMERIC"),
("max_lens_AnalyzeLast_countNeg",  "NUMERIC"),("min_lens_AnalyzeLast_countNeg",  "NUMERIC"),(" publics_AnalyzeLast_countNeg",  "NUMERIC"),("protecteds_AnalyzeLast_countNeg",  "NUMERIC"),
("privates_AnalyzeLast_countNeg",  "NUMERIC"),("totals _AnalyzeLast_countNeg",  "NUMERIC"),("len_params_AnalyzeLast_countNeg",  "NUMERIC"),("sum_params_AnalyzeLast_countNeg",  "NUMERIC"),
("mean_params_AnalyzeLast_countNeg",  "NUMERIC"),("median_params_AnalyzeLast_countNeg",  "NUMERIC"),("var_params_AnalyzeLast_countNeg",  "NUMERIC"),("max_params_AnalyzeLast_countNeg",  "NUMERIC"),
("min_params_AnalyzeLast_countNeg",  "NUMERIC"),("NCSS_AnalyzeLast_sumPos",  "NUMERIC"),("FileLen_AnalyzeLast_sumPos",  "NUMERIC"),("sum_fors_AnalyzeLast_sumPos",  "NUMERIC"),("sum_ifs_AnalyzeLast_sumPos",  "NUMERIC"),
("sum_tries_AnalyzeLast_sumPos",  "NUMERIC"),("len_mccab_AnalyzeLast_sumPos",  "NUMERIC"),("sum_mccab_AnalyzeLast_sumPos",  "NUMERIC"),("mean_mccab_AnalyzeLast_sumPos",  "NUMERIC"),
("median_mccab_AnalyzeLast_sumPos",  "NUMERIC"),("var_mccab_AnalyzeLast_sumPos",  "NUMERIC"),("max_mccab_AnalyzeLast_sumPos",  "NUMERIC"),("min_mccab_AnalyzeLast_sumPos",  "NUMERIC"),
(" len_fanOut_AnalyzeLast_sumPos",  "NUMERIC"),("sum_fanOut_AnalyzeLast_sumPos",  "NUMERIC"),("mean_fanOut_AnalyzeLast_sumPos",  "NUMERIC"),("median_fanOut_AnalyzeLast_sumPos",  "NUMERIC"),
("var_fanOut_AnalyzeLast_sumPos",  "NUMERIC"),("max_fanOut_AnalyzeLast_sumPos",  "NUMERIC"),("min_fanOut_AnalyzeLast_sumPos",  "NUMERIC"),(" len_NPath_AnalyzeLast_sumPos",  "NUMERIC"),
("sum_NPath_AnalyzeLast_sumPos",  "NUMERIC"),("mean_NPath_AnalyzeLast_sumPos",  "NUMERIC"),("median_NPath_AnalyzeLast_sumPos",  "NUMERIC"),("var_NPath_AnalyzeLast_sumPos",  "NUMERIC"),
("max_NPath_AnalyzeLast_sumPos",  "NUMERIC"),("min_NPath_AnalyzeLast_sumPos",  "NUMERIC"),(" len_JavaNCSSmet_AnalyzeLast_sumPos",  "NUMERIC"),("sum_JavaNCSSmet_AnalyzeLast_sumPos",  "NUMERIC"),
("mean_JavaNCSSmet_AnalyzeLast_sumPos",  "NUMERIC"),("median_JavaNCSSmet_AnalyzeLast_sumPos",  "NUMERIC"),("var_JavaNCSSmet_AnalyzeLast_sumPos",  "NUMERIC"),("max_JavaNCSSmet_AnalyzeLast_sumPos",  "NUMERIC"),
("min_JavaNCSSmet_AnalyzeLast_sumPos",  "NUMERIC"),(" len_thorwsSTM_AnalyzeLast_sumPos",  "NUMERIC"),("sum_thorwsSTM_AnalyzeLast_sumPos",  "NUMERIC"),("mean_thorwsSTM_AnalyzeLast_sumPos",  "NUMERIC"),
("median_thorwsSTM_AnalyzeLast_sumPos",  "NUMERIC"),("var_thorwsSTM_AnalyzeLast_sumPos",  "NUMERIC"),("max_thorwsSTM_AnalyzeLast_sumPos",  "NUMERIC"),("min_thorwsSTM_AnalyzeLast_sumPos",  "NUMERIC"),
(" len_coupl_AnalyzeLast_sumPos",  "NUMERIC"),("sum_coupl_AnalyzeLast_sumPos",  "NUMERIC"),("mean_coupl_AnalyzeLast_sumPos",  "NUMERIC"),("median_coupl_AnalyzeLast_sumPos",  "NUMERIC"),
("var_coupl_AnalyzeLast_sumPos",  "NUMERIC"),("max_coupl_AnalyzeLast_sumPos",  "NUMERIC"),("min_coupl_AnalyzeLast_sumPos",  "NUMERIC"),(" len_executables_AnalyzeLast_sumPos",  "NUMERIC"),
("sum_executables_AnalyzeLast_sumPos",  "NUMERIC"),("mean_executables_AnalyzeLast_sumPos",  "NUMERIC"),("median_executables_AnalyzeLast_sumPos",  "NUMERIC"),("var_executables_AnalyzeLast_sumPos",  "NUMERIC"),
("max_executables_AnalyzeLast_sumPos",  "NUMERIC"),("min_executables_AnalyzeLast_sumPos",  "NUMERIC"),(" len_lens_AnalyzeLast_sumPos",  "NUMERIC"),
("sum_lens_AnalyzeLast_sumPos",  "NUMERIC"),("mean_lens_AnalyzeLast_sumPos",  "NUMERIC"),("median_lens_AnalyzeLast_sumPos",  "NUMERIC"),("var_lens_AnalyzeLast_sumPos",  "NUMERIC"),
("max_lens_AnalyzeLast_sumPos",  "NUMERIC"),("min_lens_AnalyzeLast_sumPos",  "NUMERIC"),(" publics_AnalyzeLast_sumPos",  "NUMERIC"),("protecteds_AnalyzeLast_sumPos",  "NUMERIC"),
("privates_AnalyzeLast_sumPos",  "NUMERIC"),("totals _AnalyzeLast_sumPos",  "NUMERIC"),("len_params_AnalyzeLast_sumPos",  "NUMERIC"),("sum_params_AnalyzeLast_sumPos",  "NUMERIC"),
("mean_params_AnalyzeLast_sumPos",  "NUMERIC"),("median_params_AnalyzeLast_sumPos",  "NUMERIC"),("var_params_AnalyzeLast_sumPos",  "NUMERIC"),("max_params_AnalyzeLast_sumPos",  "NUMERIC"),
("min_params_AnalyzeLast_sumPos",  "NUMERIC"),("NCSS_AnalyzeLast_sumNeg",  "NUMERIC"),("FileLen_AnalyzeLast_sumNeg",  "NUMERIC"),("sum_fors_AnalyzeLast_sumNeg",  "NUMERIC"),("sum_ifs_AnalyzeLast_sumNeg",  "NUMERIC"),
("sum_tries_AnalyzeLast_sumNeg",  "NUMERIC"),("len_mccab_AnalyzeLast_sumNeg",  "NUMERIC"),("sum_mccab_AnalyzeLast_sumNeg",  "NUMERIC"),("mean_mccab_AnalyzeLast_sumNeg",  "NUMERIC"),
("median_mccab_AnalyzeLast_sumNeg",  "NUMERIC"),("var_mccab_AnalyzeLast_sumNeg",  "NUMERIC"),("max_mccab_AnalyzeLast_sumNeg",  "NUMERIC"),("min_mccab_AnalyzeLast_sumNeg",  "NUMERIC"),
(" len_fanOut_AnalyzeLast_sumNeg",  "NUMERIC"),("sum_fanOut_AnalyzeLast_sumNeg",  "NUMERIC"),("mean_fanOut_AnalyzeLast_sumNeg",  "NUMERIC"),("median_fanOut_AnalyzeLast_sumNeg",  "NUMERIC"),
("var_fanOut_AnalyzeLast_sumNeg",  "NUMERIC"),("max_fanOut_AnalyzeLast_sumNeg",  "NUMERIC"),("min_fanOut_AnalyzeLast_sumNeg",  "NUMERIC"),(" len_NPath_AnalyzeLast_sumNeg",  "NUMERIC"),
("sum_NPath_AnalyzeLast_sumNeg",  "NUMERIC"),("mean_NPath_AnalyzeLast_sumNeg",  "NUMERIC"),("median_NPath_AnalyzeLast_sumNeg",  "NUMERIC"),("var_NPath_AnalyzeLast_sumNeg",  "NUMERIC"),
("max_NPath_AnalyzeLast_sumNeg",  "NUMERIC"),("min_NPath_AnalyzeLast_sumNeg",  "NUMERIC"),(" len_JavaNCSSmet_AnalyzeLast_sumNeg",  "NUMERIC"),("sum_JavaNCSSmet_AnalyzeLast_sumNeg",  "NUMERIC"),
("mean_JavaNCSSmet_AnalyzeLast_sumNeg",  "NUMERIC"),("median_JavaNCSSmet_AnalyzeLast_sumNeg",  "NUMERIC"),("var_JavaNCSSmet_AnalyzeLast_sumNeg",  "NUMERIC"),("max_JavaNCSSmet_AnalyzeLast_sumNeg",  "NUMERIC"),
("min_JavaNCSSmet_AnalyzeLast_sumNeg",  "NUMERIC"),(" len_thorwsSTM_AnalyzeLast_sumNeg",  "NUMERIC"),("sum_thorwsSTM_AnalyzeLast_sumNeg",  "NUMERIC"),("mean_thorwsSTM_AnalyzeLast_sumNeg",  "NUMERIC"),
("median_thorwsSTM_AnalyzeLast_sumNeg",  "NUMERIC"),("var_thorwsSTM_AnalyzeLast_sumNeg",  "NUMERIC"),("max_thorwsSTM_AnalyzeLast_sumNeg",  "NUMERIC"),("min_thorwsSTM_AnalyzeLast_sumNeg",  "NUMERIC"),
(" len_coupl_AnalyzeLast_sumNeg",  "NUMERIC"),("sum_coupl_AnalyzeLast_sumNeg",  "NUMERIC"),("mean_coupl_AnalyzeLast_sumNeg",  "NUMERIC"),("median_coupl_AnalyzeLast_sumNeg",  "NUMERIC"),
("var_coupl_AnalyzeLast_sumNeg",  "NUMERIC"),("max_coupl_AnalyzeLast_sumNeg",  "NUMERIC"),("min_coupl_AnalyzeLast_sumNeg",  "NUMERIC"),(" len_executables_AnalyzeLast_sumNeg",  "NUMERIC"),
("sum_executables_AnalyzeLast_sumNeg",  "NUMERIC"),("mean_executables_AnalyzeLast_sumNeg",  "NUMERIC"),("median_executables_AnalyzeLast_sumNeg",  "NUMERIC"),("var_executables_AnalyzeLast_sumNeg",  "NUMERIC"),
("max_executables_AnalyzeLast_sumNeg",  "NUMERIC"),("min_executables_AnalyzeLast_sumNeg",  "NUMERIC"),(" len_lens_AnalyzeLast_sumNeg",  "NUMERIC"),
("sum_lens_AnalyzeLast_sumNeg",  "NUMERIC"),("mean_lens_AnalyzeLast_sumNeg",  "NUMERIC"),("median_lens_AnalyzeLast_sumNeg",  "NUMERIC"),("var_lens_AnalyzeLast_sumNeg",  "NUMERIC"),
("max_lens_AnalyzeLast_sumNeg",  "NUMERIC"),("min_lens_AnalyzeLast_sumNeg",  "NUMERIC"),(" publics_AnalyzeLast_sumNeg",  "NUMERIC"),("protecteds_AnalyzeLast_sumNeg",  "NUMERIC"),
("privates_AnalyzeLast_sumNeg",  "NUMERIC"),("totals _AnalyzeLast_sumNeg",  "NUMERIC"),("len_params_AnalyzeLast_sumNeg",  "NUMERIC"),("sum_params_AnalyzeLast_sumNeg",  "NUMERIC"),
("mean_params_AnalyzeLast_sumNeg",  "NUMERIC"),("median_params_AnalyzeLast_sumNeg",  "NUMERIC"),("var_params_AnalyzeLast_sumNeg",  "NUMERIC"),("max_params_AnalyzeLast_sumNeg",  "NUMERIC"),
("min_params_AnalyzeLast_sumNeg",  "NUMERIC"),("NCSS_AnalyzeLast_avgPos",  "NUMERIC"),("FileLen_AnalyzeLast_avgPos",  "NUMERIC"),("sum_fors_AnalyzeLast_avgPos",  "NUMERIC"),("sum_ifs_AnalyzeLast_avgPos",  "NUMERIC"),
("sum_tries_AnalyzeLast_avgPos",  "NUMERIC"),("len_mccab_AnalyzeLast_avgPos",  "NUMERIC"),("sum_mccab_AnalyzeLast_avgPos",  "NUMERIC"),("mean_mccab_AnalyzeLast_avgPos",  "NUMERIC"),
("median_mccab_AnalyzeLast_avgPos",  "NUMERIC"),("var_mccab_AnalyzeLast_avgPos",  "NUMERIC"),("max_mccab_AnalyzeLast_avgPos",  "NUMERIC"),("min_mccab_AnalyzeLast_avgPos",  "NUMERIC"),
(" len_fanOut_AnalyzeLast_avgPos",  "NUMERIC"),("sum_fanOut_AnalyzeLast_avgPos",  "NUMERIC"),("mean_fanOut_AnalyzeLast_avgPos",  "NUMERIC"),("median_fanOut_AnalyzeLast_avgPos",  "NUMERIC"),
("var_fanOut_AnalyzeLast_avgPos",  "NUMERIC"),("max_fanOut_AnalyzeLast_avgPos",  "NUMERIC"),("min_fanOut_AnalyzeLast_avgPos",  "NUMERIC"),(" len_NPath_AnalyzeLast_avgPos",  "NUMERIC"),
("sum_NPath_AnalyzeLast_avgPos",  "NUMERIC"),("mean_NPath_AnalyzeLast_avgPos",  "NUMERIC"),("median_NPath_AnalyzeLast_avgPos",  "NUMERIC"),("var_NPath_AnalyzeLast_avgPos",  "NUMERIC"),
("max_NPath_AnalyzeLast_avgPos",  "NUMERIC"),("min_NPath_AnalyzeLast_avgPos",  "NUMERIC"),(" len_JavaNCSSmet_AnalyzeLast_avgPos",  "NUMERIC"),("sum_JavaNCSSmet_AnalyzeLast_avgPos",  "NUMERIC"),
("mean_JavaNCSSmet_AnalyzeLast_avgPos",  "NUMERIC"),("median_JavaNCSSmet_AnalyzeLast_avgPos",  "NUMERIC"),("var_JavaNCSSmet_AnalyzeLast_avgPos",  "NUMERIC"),("max_JavaNCSSmet_AnalyzeLast_avgPos",  "NUMERIC"),
("min_JavaNCSSmet_AnalyzeLast_avgPos",  "NUMERIC"),(" len_thorwsSTM_AnalyzeLast_avgPos",  "NUMERIC"),("sum_thorwsSTM_AnalyzeLast_avgPos",  "NUMERIC"),("mean_thorwsSTM_AnalyzeLast_avgPos",  "NUMERIC"),
("median_thorwsSTM_AnalyzeLast_avgPos",  "NUMERIC"),("var_thorwsSTM_AnalyzeLast_avgPos",  "NUMERIC"),("max_thorwsSTM_AnalyzeLast_avgPos",  "NUMERIC"),("min_thorwsSTM_AnalyzeLast_avgPos",  "NUMERIC"),
(" len_coupl_AnalyzeLast_avgPos",  "NUMERIC"),("sum_coupl_AnalyzeLast_avgPos",  "NUMERIC"),("mean_coupl_AnalyzeLast_avgPos",  "NUMERIC"),("median_coupl_AnalyzeLast_avgPos",  "NUMERIC"),
("var_coupl_AnalyzeLast_avgPos",  "NUMERIC"),("max_coupl_AnalyzeLast_avgPos",  "NUMERIC"),("min_coupl_AnalyzeLast_avgPos",  "NUMERIC"),(" len_executables_AnalyzeLast_avgPos",  "NUMERIC"),
("sum_executables_AnalyzeLast_avgPos",  "NUMERIC"),("mean_executables_AnalyzeLast_avgPos",  "NUMERIC"),("median_executables_AnalyzeLast_avgPos",  "NUMERIC"),("var_executables_AnalyzeLast_avgPos",  "NUMERIC"),
("max_executables_AnalyzeLast_avgPos",  "NUMERIC"),("min_executables_AnalyzeLast_avgPos",  "NUMERIC"),(" len_lens_AnalyzeLast_avgPos",  "NUMERIC"),
("sum_lens_AnalyzeLast_avgPos",  "NUMERIC"),("mean_lens_AnalyzeLast_avgPos",  "NUMERIC"),("median_lens_AnalyzeLast_avgPos",  "NUMERIC"),("var_lens_AnalyzeLast_avgPos",  "NUMERIC"),
("max_lens_AnalyzeLast_avgPos",  "NUMERIC"),("min_lens_AnalyzeLast_avgPos",  "NUMERIC"),(" publics_AnalyzeLast_avgPos",  "NUMERIC"),("protecteds_AnalyzeLast_avgPos",  "NUMERIC"),
("privates_AnalyzeLast_avgPos",  "NUMERIC"),("totals _AnalyzeLast_avgPos",  "NUMERIC"),("len_params_AnalyzeLast_avgPos",  "NUMERIC"),("sum_params_AnalyzeLast_avgPos",  "NUMERIC"),
("mean_params_AnalyzeLast_avgPos",  "NUMERIC"),("median_params_AnalyzeLast_avgPos",  "NUMERIC"),("var_params_AnalyzeLast_avgPos",  "NUMERIC"),("max_params_AnalyzeLast_avgPos",  "NUMERIC"),
("min_params_AnalyzeLast_avgPos",  "NUMERIC"),("NCSS_AnalyzeLast_avgNeg",  "NUMERIC"),("FileLen_AnalyzeLast_avgNeg",  "NUMERIC"),("sum_fors_AnalyzeLast_avgNeg",  "NUMERIC"),("sum_ifs_AnalyzeLast_avgNeg",  "NUMERIC"),
("sum_tries_AnalyzeLast_avgNeg",  "NUMERIC"),("len_mccab_AnalyzeLast_avgNeg",  "NUMERIC"),("sum_mccab_AnalyzeLast_avgNeg",  "NUMERIC"),("mean_mccab_AnalyzeLast_avgNeg",  "NUMERIC"),
("median_mccab_AnalyzeLast_avgNeg",  "NUMERIC"),("var_mccab_AnalyzeLast_avgNeg",  "NUMERIC"),("max_mccab_AnalyzeLast_avgNeg",  "NUMERIC"),("min_mccab_AnalyzeLast_avgNeg",  "NUMERIC"),
(" len_fanOut_AnalyzeLast_avgNeg",  "NUMERIC"),("sum_fanOut_AnalyzeLast_avgNeg",  "NUMERIC"),("mean_fanOut_AnalyzeLast_avgNeg",  "NUMERIC"),("median_fanOut_AnalyzeLast_avgNeg",  "NUMERIC"),
("var_fanOut_AnalyzeLast_avgNeg",  "NUMERIC"),("max_fanOut_AnalyzeLast_avgNeg",  "NUMERIC"),("min_fanOut_AnalyzeLast_avgNeg",  "NUMERIC"),(" len_NPath_AnalyzeLast_avgNeg",  "NUMERIC"),
("sum_NPath_AnalyzeLast_avgNeg",  "NUMERIC"),("mean_NPath_AnalyzeLast_avgNeg",  "NUMERIC"),("median_NPath_AnalyzeLast_avgNeg",  "NUMERIC"),("var_NPath_AnalyzeLast_avgNeg",  "NUMERIC"),
("max_NPath_AnalyzeLast_avgNeg",  "NUMERIC"),("min_NPath_AnalyzeLast_avgNeg",  "NUMERIC"),(" len_JavaNCSSmet_AnalyzeLast_avgNeg",  "NUMERIC"),("sum_JavaNCSSmet_AnalyzeLast_avgNeg",  "NUMERIC"),
("mean_JavaNCSSmet_AnalyzeLast_avgNeg",  "NUMERIC"),("median_JavaNCSSmet_AnalyzeLast_avgNeg",  "NUMERIC"),("var_JavaNCSSmet_AnalyzeLast_avgNeg",  "NUMERIC"),("max_JavaNCSSmet_AnalyzeLast_avgNeg",  "NUMERIC"),
("min_JavaNCSSmet_AnalyzeLast_avgNeg",  "NUMERIC"),(" len_thorwsSTM_AnalyzeLast_avgNeg",  "NUMERIC"),("sum_thorwsSTM_AnalyzeLast_avgNeg",  "NUMERIC"),("mean_thorwsSTM_AnalyzeLast_avgNeg",  "NUMERIC"),
("median_thorwsSTM_AnalyzeLast_avgNeg",  "NUMERIC"),("var_thorwsSTM_AnalyzeLast_avgNeg",  "NUMERIC"),("max_thorwsSTM_AnalyzeLast_avgNeg",  "NUMERIC"),("min_thorwsSTM_AnalyzeLast_avgNeg",  "NUMERIC"),
(" len_coupl_AnalyzeLast_avgNeg",  "NUMERIC"),("sum_coupl_AnalyzeLast_avgNeg",  "NUMERIC"),("mean_coupl_AnalyzeLast_avgNeg",  "NUMERIC"),("median_coupl_AnalyzeLast_avgNeg",  "NUMERIC"),
("var_coupl_AnalyzeLast_avgNeg",  "NUMERIC"),("max_coupl_AnalyzeLast_avgNeg",  "NUMERIC"),("min_coupl_AnalyzeLast_avgNeg",  "NUMERIC"),(" len_executables_AnalyzeLast_avgNeg",  "NUMERIC"),
("sum_executables_AnalyzeLast_avgNeg",  "NUMERIC"),("mean_executables_AnalyzeLast_avgNeg",  "NUMERIC"),("median_executables_AnalyzeLast_avgNeg",  "NUMERIC"),("var_executables_AnalyzeLast_avgNeg",  "NUMERIC"),
("max_executables_AnalyzeLast_avgNeg",  "NUMERIC"),("min_executables_AnalyzeLast_avgNeg",  "NUMERIC"),(" len_lens_AnalyzeLast_avgNeg",  "NUMERIC"),
("sum_lens_AnalyzeLast_avgNeg",  "NUMERIC"),("mean_lens_AnalyzeLast_avgNeg",  "NUMERIC"),("median_lens_AnalyzeLast_avgNeg",  "NUMERIC"),("var_lens_AnalyzeLast_avgNeg",  "NUMERIC"),
("max_lens_AnalyzeLast_avgNeg",  "NUMERIC"),("min_lens_AnalyzeLast_avgNeg",  "NUMERIC"),(" publics_AnalyzeLast_avgNeg",  "NUMERIC"),("protecteds_AnalyzeLast_avgNeg",  "NUMERIC"),
("privates_AnalyzeLast_avgNeg",  "NUMERIC"),("totals _AnalyzeLast_avgNeg",  "NUMERIC"),("len_params_AnalyzeLast_avgNeg",  "NUMERIC"),("sum_params_AnalyzeLast_avgNeg",  "NUMERIC"),
("mean_params_AnalyzeLast_avgNeg",  "NUMERIC"),("median_params_AnalyzeLast_avgNeg",  "NUMERIC"),("var_params_AnalyzeLast_avgNeg",  "NUMERIC"),("max_params_AnalyzeLast_avgNeg",  "NUMERIC"),
("min_params_AnalyzeLast_avgNeg",  "NUMERIC")
]
        ret=[]
        for i in range(len(all)):
            if i+1 in best_features:
                ret.append(all[i])
        return all


    def sqlToAttributesBest(self,basicAtt, c, files_dict, first,best):
        Att_dict = {}
        for f in files_dict.keys():
            Att_dict[f] = list(basicAtt)
        for row in c.execute(first):
            name = Agent.pathTopack.pathToPack(row[0])
            if (name in Att_dict):
                ret=[]
                all=list([ x if x!=None else 0 for x in  row[1:]  ])
                for i in range(len(all)):
                        if i in best:
                            ret.append(all[i])
                if len(ret)!=len(best):
                    print "len ", len(ret)
                Att_dict[name] = ret
        for f in Att_dict:
            files_dict[f] = files_dict[f] + Att_dict[f]


    def get_features(self, c, files_dict,prev_date,start_date,end_date):
        analyze='''select name , sum( NCSS ), sum(FileLen ), sum(sum_fors ), sum(sum_ifs ), sum(sum_tries ), sum(
		len_mccab ), sum(sum_mccab ), sum(mean_mccab ), sum(median_mccab ), sum(var_mccab ), sum(max_mccab ), sum(min_mccab ), sum(
		len_fanOut ), sum(sum_fanOut ), sum(mean_fanOut ), sum(median_fanOut ), sum(var_fanOut ), sum(max_fanOut ), sum(min_fanOut ), sum(
		len_NPath ), sum(sum_NPath ), sum(mean_NPath ), sum(median_NPath ), sum(var_NPath ), sum(max_NPath ), sum(min_NPath ), sum(
		len_JavaNCSSmet ), sum(sum_JavaNCSSmet ), sum(mean_JavaNCSSmet ), sum(median_JavaNCSSmet ), sum(var_JavaNCSSmet ), sum(max_JavaNCSSmet ), sum(min_JavaNCSSmet ), sum(
		len_thorwsSTM ), sum(sum_thorwsSTM ), sum(mean_thorwsSTM ), sum(median_thorwsSTM ), sum(var_thorwsSTM ), sum(max_thorwsSTM ), sum(min_thorwsSTM ), sum(
		len_coupl ), sum(sum_coupl ), sum(mean_coupl ), sum(median_coupl ), sum(var_coupl ), sum(max_coupl ), sum(min_coupl ), sum(
		len_executables ), sum(sum_executables ), sum(mean_executables ), sum(median_executables ), sum(var_executables ), sum(max_executables ), sum(min_executables ), sum(
		len_lens ), sum(sum_lens ), sum(mean_lens ), sum(median_lens ), sum(var_lens ), sum(max_lens ), sum(min_lens ), sum(
		publics ), sum(protecteds ), sum(privates ), sum(totals  ), sum(len_params ), sum(sum_params ), sum(mean_params ), sum(median_params ), sum(var_params ), sum(max_params ), sum(min_params)
		from checkStyleAnalyzeExtends,commits where  checkStyleAnalyzeExtends.commitid=commits.ID and commits.commiter_date>="''' + str(prev_date)+ '''"''' + '''  and commits.commiter_date<="''' + str(start_date)+'''" group by checkStyleAnalyzeExtends.name'''
        lst=[0,1,3,6,7,9,10,13,14,15,17,18,20,21,23,24,27,41,42,43,45,48,55,59,64]
        lst=range(72)
        self.sqlToAttributesBest(["0" for x in lst], c, files_dict, analyze,lst)
        analyze='''select name , avg( NCSS ), avg(FileLen ), avg(sum_fors ), avg(sum_ifs ), avg(sum_tries ), avg(
		len_mccab ), avg(sum_mccab ), avg(mean_mccab ), avg(median_mccab ), avg(var_mccab ), avg(max_mccab ), avg(min_mccab ), avg(
		len_fanOut ), avg(sum_fanOut ), avg(mean_fanOut ), avg(median_fanOut ), avg(var_fanOut ), avg(max_fanOut ), avg(min_fanOut ), avg(
		len_NPath ), avg(sum_NPath ), avg(mean_NPath ), avg(median_NPath ), avg(var_NPath ), avg(max_NPath ), avg(min_NPath ), avg(
		len_JavaNCSSmet ), avg(sum_JavaNCSSmet ), avg(mean_JavaNCSSmet ), avg(median_JavaNCSSmet ), avg(var_JavaNCSSmet ), avg(max_JavaNCSSmet ), avg(min_JavaNCSSmet ), avg(
		len_thorwsSTM ), avg(sum_thorwsSTM ), avg(mean_thorwsSTM ), avg(median_thorwsSTM ), avg(var_thorwsSTM ), avg(max_thorwsSTM ), avg(min_thorwsSTM ), avg(
		len_coupl ), avg(sum_coupl ), avg(mean_coupl ), avg(median_coupl ), avg(var_coupl ), avg(max_coupl ), avg(min_coupl ), avg(
		len_executables ), avg(sum_executables ), avg(mean_executables ), avg(median_executables ), avg(var_executables ), avg(max_executables ), avg(min_executables ), avg(
		len_lens ), avg(sum_lens ), avg(mean_lens ), avg(median_lens ), avg(var_lens ), avg(max_lens ), avg(min_lens ), avg(
		publics ), avg(protecteds ), avg(privates ), avg(totals  ), avg(len_params ), avg(sum_params ), avg(mean_params ), avg(median_params ), avg(var_params ), avg(max_params ), avg(min_params)
		from checkStyleAnalyzeExtends,commits where  checkStyleAnalyzeExtends.commitid=commits.ID and commits.commiter_date>="''' + str(prev_date)+ '''"''' + '''  and commits.commiter_date<="''' + str(start_date)+'''" group by checkStyleAnalyzeExtends.name'''
        lst=[3,6,7,8,10,11,13,14,15,17,18,20,21,22,23,24,25,27,28,29,31,32,34,35,36,38,39,41,42,43,45,46,48,49,50,52,53,55,56,57,59,60]
        lst=range(72)
        self.sqlToAttributesBest(["0" for x in lst], c, files_dict, analyze,lst)
        analyze='''select name , Sum(case When	NCSS 	> 0 Then 1 Else 0 End),Sum(case When	FileLen 	> 0 Then 1 Else 0 End),Sum(case When	sum_fors 	> 0 Then 1 Else 0 End),
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
Sum(case When	max_params 	> 0 Then 1 Else 0 End),Sum(case When	min_params	> 0 Then 1 Else 0 End) from checkStyleAnalyzeExtends,commits where  checkStyleAnalyzeExtends.commitid=commits.ID and commits.commiter_date>="''' + str(prev_date)+ '''"''' + '''  and commits.commiter_date<="''' + str(start_date)+'''" group by checkStyleAnalyzeExtends.name'''
        lst=[0,1,3,5,6,7,9,10,13,14,15,16,17,18,19,20,21,23,24,26,27,28,30,31,41,42,43,45,46,47,48,49,51,52,54,55,56,57,58,59,61,63,64]
        lst=range(72)
        self.sqlToAttributesBest(["0" for x in lst ], c, files_dict, analyze,lst)
        analyze='''select name , Sum(case When	NCSS 	< 0 Then 1 Else 0 End),Sum(case When	FileLen 	< 0 Then 1 Else 0 End),Sum(case When	sum_fors 	< 0 Then 1 Else 0 End),
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
Sum(case When	max_params 	< 0 Then 1 Else 0 End),Sum(case When	min_params	< 0 Then 1 Else 0 End) from checkStyleAnalyzeExtends,commits where  checkStyleAnalyzeExtends.commitid=commits.ID and commits.commiter_date>="''' + str(prev_date)+ '''"''' + '''  and commits.commiter_date<="''' + str(start_date)+'''" group by checkStyleAnalyzeExtends.name'''
        lst=[0,1,3,6,7,9,13,14,15,17,20,21,23,27,28,30,42,48,49,51,55,56,58]
        lst=range(72)
        self.sqlToAttributesBest(["0" for x in lst], c, files_dict, analyze,lst)
        analyze='''select name , Sum(case When	NCSS 	> 0 Then 	NCSS 	Else 0 End),Sum(case When	FileLen 	> 0 Then 	FileLen 	Else 0 End),Sum(case When	sum_fors 	> 0 Then 	sum_fors 	Else 0 End),
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
from checkStyleAnalyzeExtends,commits where  checkStyleAnalyzeExtends.commitid=commits.ID and commits.commiter_date>="''' + str(prev_date)+ '''"''' + '''  and commits.commiter_date<="''' + str(start_date)+'''" group by checkStyleAnalyzeExtends.name'''
        lst=[0,1,3,6,7,9,10,13,14,15,17,18,20,21,23,24,27,28,31,41,42,45,48,55,59,64]
        lst=range(72)
        self.sqlToAttributesBest(["0" for x in lst], c, files_dict, analyze,lst)
        analyze='''select name , Sum(case When	NCSS 	< 0 Then 	NCSS 	Else 0 End),Sum(case When	FileLen 	< 0 Then 	FileLen 	Else 0 End),Sum(case When	sum_fors 	< 0 Then 	sum_fors 	Else 0 End),
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
from checkStyleAnalyzeExtends,commits where  checkStyleAnalyzeExtends.commitid=commits.ID and commits.commiter_date>="''' + str(prev_date)+ '''"''' + '''  and commits.commiter_date<="''' + str(start_date)+'''" group by checkStyleAnalyzeExtends.name'''
        lst=[1,6,7,9,10,13,14,15,17,18,20,21,23,24,27,28,29,30,31,41,42,43,45,46,48,49,51,52,55,56,57,58,59]
        lst=range(72)
        self.sqlToAttributesBest(["0" for x in lst], c, files_dict, analyze,lst)
        analyze='''select name , avg(case When	NCSS 	> 0 Then 	NCSS 	Else null End),avg(case When	FileLen 	> 0 Then 	FileLen 	Else null End),avg(case When	sum_fors 	> 0 Then 	sum_fors 	Else null End),
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
from checkStyleAnalyzeExtends,commits where  checkStyleAnalyzeExtends.commitid=commits.ID and commits.commiter_date>="''' + str(prev_date)+ '''"''' + '''  and commits.commiter_date<="''' + str(start_date)+'''" group by checkStyleAnalyzeExtends.name'''
        lst=[3,6,7,10,13,14,15,17,18,20,21,23,24,27,28,29,31,41,42,43,45,46,48,49,52,55,56,57,59]
        lst=range(72)
        self.sqlToAttributesBest(["0" for x in lst], c, files_dict, analyze,lst)
        analyze='''select name , avg(case When	NCSS 	< 0 Then 	NCSS 	Else null End),avg(case When	FileLen 	< 0 Then 	FileLen 	Else null End),avg(case When	sum_fors 	< 0 Then 	sum_fors 	Else null End),
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
from checkStyleAnalyzeExtends,commits where  checkStyleAnalyzeExtends.commitid=commits.ID and commits.commiter_date>="''' + str(prev_date)+ '''"''' + '''  and commits.commiter_date<="''' + str(start_date)+'''" group by checkStyleAnalyzeExtends.name'''
        lst=[1,6,7,9,13,14,15,17,18,20,21,23,27,28,30,41,42,45,48,49,51,55,56,58]
        lst=range(72)
        self.sqlToAttributesBest(["0" for x in lst], c, files_dict, analyze,lst)
