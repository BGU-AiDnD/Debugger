""""""
import json
from os import path

from wekaMethods.features.features_extractor import FeaturesExtractor


class HaelsteadFeaturesExtractor(FeaturesExtractor):
    """"""

    @cached_property
    def features_object(self):
        with open(path.abspath(path.join(self.FEATURES_FOLDER, "object_oriented_features.json")),
                  "r") as features_file:
            return json.load(features_file)

    def get_attributes(self):
        return [(attribute, attribute_type) for attribute, attribute_type in self.all_features]

    def get_features(self, prev_date, start_date, end_date):
        haelstead_features_query = 'select   name, Operators_count, Operandscount, ' \
                                   'Distinct_operators, Distinct_operands, Program_length, ' \
                                   'Program_vocabulary, Volume, Difficulty, Effort ' \
                                   'from haelsTfiles group by name'

        self.convert_sql_queries_to_attributes(["0", "0", "0", "0", "0", "0", "0", "0", "0"],
                                               haelstead_features_query)

        complex_haelstead_query = 'select * from Complexyfiles group by name'

        self.convert_sql_queries_to_attributes(["0"], complex_haelstead_query)
