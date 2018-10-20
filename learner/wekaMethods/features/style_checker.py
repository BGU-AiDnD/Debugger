""""""
import json
from os import path

from wekaMethods.features.features_extractor import FeaturesExtractor


class StyleChecker(FeaturesExtractor):
    """"""

    @cached_property
    def features_object(self):
        with open(path.abspath(path.join(self.FEATURES_FOLDER, "style_checker_features.json")),
                  "r") as features_file:
            return json.load(features_file)

    def get_attributes(self):
        attributes = []
        for feature_index, feature_key, feature_type in enumerate(self.all_features.items(), 1):
            if feature_index in self.best_features_indexes:
                attributes.append((feature_key, feature_type))

        return attributes

    def get_features(self, prev_date, start_date, end_date):
        style_query = 'select * from checkStyleExtends group by name'
        # TODO: WHAT THE HELL "0" FOR X IN BEST_FEATURES???? why???
        self.convert_sql_queries_to_best_attributes(["0" for x in best_features], style_query)
