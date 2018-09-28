__author__ = 'amir'

from wekaMethods.articles import *
# from wekaMethods.articles import sqlToAttributes
import wekaMethods.articles


class haelstead:
    def get_attributes(self):
        return [("Operators_count", "NUMERIC"), ("Operands_count", "NUMERIC"),
                ("Distinct_operators", "NUMERIC"), ("Distinct_operands", "NUMERIC"), ("Program_length", "NUMERIC"),
                ("Program_vocabulary", "NUMERIC"), ("Volume", "NUMERIC"), ("Difficulty", "NUMERIC"),
                ("Effort", "NUMERIC"),
                ("complexity", "NUMERIC")]

    def get_features(self, c, files_dict, prev_date, start_date, end_date):
        hael = 'select   name,Operators_count, Operands_count , Distinct_operators  , Distinct_operands,Program_length , Program_vocabulary ,Volume , Difficulty , Effort from  haelsTfiles group by name'
        wekaMethods.articles.sqlToAttributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"], c, files_dict, hael)
        complex = 'select * from Complexyfiles group by name'
        wekaMethods.articles.sqlToAttributes(["0"], c, files_dict, complex)
