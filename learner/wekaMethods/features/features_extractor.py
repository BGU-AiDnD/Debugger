"""A module that creates an interface for all the extraction modules of the package."""
from abc import ABC, abstractmethod

from wekaMethods.articles import Agent


class FeaturesExtractor(ABC):
    """Interface for all he features extractors in the package."""

    FEATURES_FOLDER = "features_descriptions"

    def __init__(self, cursor_object, files_map):
        super(FeaturesExtractor, self).__init__()
        self.cursor_object = cursor_object
        self.files_map = files_map

    @abstractmethod
    def features_object(self):
        pass

    @property
    def all_features(self):
        return self.features_object["all_features"]

    @property
    def best_features_indexes(self):
        return self.features_object.get("best_features", [])

    def get_attributes(self):
        pass

    @abstractmethod
    def get_features(self, prev_date, start_date, end_date):
        pass

    def convert_sql_queries_to_attributes(self, basic_attributes, query):
        """"""
        attributes = {}
        for file_name in self.files_map:
            attributes[file_name] = list(basic_attributes)

        for result_row in self.cursor_object.execute(query):
            title = Agent.pathTopack.pathToPack(result_row[0])
            try:
                attributes[title] = [column if column is not None else 0 for column in
                                     result_row[1:]]
            except:
                pass  # TODO: LOG this

        for attribute in attributes:
            self.files_map[attribute] += attributes[attribute]

    def convert_sql_queries_to_best_attributes(self, basic_attributes, query):
        """"""
        attributes = {}
        for file_name in self.files_map:
            attributes[file_name] = list(basic_attributes)

        for result_row in self.cursor_object.execute(query):
            file_title = Agent.pathTopack.pathToPack(result_row[0])
            if file_title in attributes:
                query_attributes = list(result_row[1:])
                attribute_items = []
                for index, query_attribute in enumerate(query_attributes, 1):
                    if index in self.best_features_indexes:
                        attribute_items.append(query_attribute)

                attributes[file_title] = attribute_items

        for file_name in attributes:
            self.files_map[file_name] += attributes[file_name]




