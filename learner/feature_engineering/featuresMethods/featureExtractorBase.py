
class FeatureExtractorBase(object):
    def get_attributes(self):
        """
        return attributes names and weka types
        """
        raise NotImplementedError()

    def get_features(self, cursor, files_dict, prev_date, start_date, end_date):
        """
        extract features for files and add them to files_dict
        :param cursor: cursor of the version db
        :param files_dict: dict (file_names -> features). The extracted features added to this dict
        :param prev_date: release date of previous version
        :param start_date: release date of current version
        :param end_date: release date of next version
        """
        raise NotImplementedError()