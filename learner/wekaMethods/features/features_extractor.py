"""A module that creates an interface for all the extraction modules of the package."""
from abc import ABC, abstractmethod


class FeaturesExtractor(ABC):
    """Interface for all he features extractors in the package."""

    FEATURES_FOLDER = "features_descriptions"

    @abstractmethod
    def features_object(self):
        pass

    @property
    @abstractmethod
    def all_features(self):
        pass



