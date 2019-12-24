import pandas as pd
import numpy as np
from operator import itemgetter
from copy import deepcopy
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn import preprocessing
from sklearn.model_selection import cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import json
import os
from itertools import product


class LearningClassify(object):
    PROBABILITY = {True: {True: 0, False: 1}, False: {True: 1, False: 0}}

    def __init__(self, training_set, testing_set, training_describe, testing_describe, cv_scores_path, prediction_path, classifier, additional_name=''):
        self.classifier = classifier
        self.training_set = training_set
        self.testing_set = testing_set
        self.training_describe, self.testing_describe = training_describe, testing_describe
        self.cv_scores_path = cv_scores_path
        self.prediction_path = prediction_path
        self.additional_name = additional_name
        self.cross_validation()
        self.describe()
        self.model = self.get_classifier().fit(self.get_training_featues(), self.get_training_labels())
        prediction_probabilities = self.model.predict_proba(self.get_testing_featues())
        prediction = self.model.predict(self.get_testing_featues())
        probabilities_index = LearningClassify.PROBABILITY[prediction_probabilities[0][0] >= 0.5][prediction[0]]
        self.prediction = zip(self.get_test_ids(), map(itemgetter(probabilities_index), prediction_probabilities))
        with open(self.prediction_path + self.get_name() + ".json", "wb") as f:
            json.dump(self.prediction, f)

    def get_name(self):
        return "learning_{0}_{1}".format(self.classifier.__class__.__name__, self.additional_name)

    def get_training_featues(self):
        train = pd.read_csv(self.training_set)
        train = LearningClassify.drop(train)
        train = train.drop('hasBug', axis=1)
        train_features = np.array(train)
        return train_features

    def get_testing_featues(self):
        test = pd.read_csv(self.testing_set)
        test = test.drop('hasBug', axis=1)
        test_features = np.array(LearningClassify.drop(test))
        return test_features

    def get_training_labels(self):
        train = pd.read_csv(self.training_set)
        return np.array(train['hasBug'])

    def get_classifier(self):
        return self.classifier

    def get_test_ids(self):
        test = pd.read_csv(self.testing_set)
        return test['component_name']

    def check_feature_importance(self):
        if not hasattr(self.get_classifier(), "feature_importances_"):
            return
        importances = self.get_classifier().feature_importances_
        std = np.std([tree.feature_importances_ for tree in self.get_classifier().estimators_], axis=0)
        indices = np.argsort(importances)[::-1]
        print("Feature ranking:")
        for f in range(X.shape[1]):
            print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    @staticmethod
    def get_all_classifers(trainingFile, testingFile, training_describe, testing_describe, cs_scores, prediction):
        from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.neural_network import MLPClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.svm import SVC
        from sklearn.naive_bayes import GaussianNB
        from sklearn.ensemble import ExtraTreesClassifier
        from sklearn.feature_selection import VarianceThreshold
        return [LearningClassify(trainingFile, testingFile, training_describe, testing_describe, cs_scores, prediction, RandomForestClassifier(n_estimators=10, random_state=42))]#,
                # LearningClassify(trainingFile, testingFile, training_describe, testing_describe, cs_scores, prediction, GradientBoostingClassifier()),
                # LearningClassify(trainingFile, testingFile, training_describe, testing_describe, cs_scores, prediction, DecisionTreeClassifier()),
                # LearningClassify(trainingFile, testingFile, training_describe, testing_describe, cs_scores, prediction, MLPClassifier(solver='adam', alpha=1e-5, activation='relu', max_iter=3000, hidden_layer_sizes=(30, 30, 30, 30, 30), random_state=13)),
                # LearningClassify(trainingFile, testingFile, training_describe, testing_describe, cs_scores, prediction, LogisticRegression()),
                # LearningClassify(trainingFile, testingFile, training_describe, testing_describe, cs_scores, prediction, KNeighborsClassifier())]
                # LearningClassify(trainingFile, testingFile, training_describe, testing_describe, cs_scores, prediction, SVC(probability=True)),
                # LearningClassify(trainingFile, testingFile, training_describe, testing_describe, cs_scores, prediction, GaussianNB()),
                # LearningClassify(trainingFile, testingFile, training_describe, testing_describe, cs_scores, prediction, ExtraTreesClassifier(n_estimators=100, random_state=0)),
                # LearningClassify(trainingFile, testingFile, training_describe, testing_describe, cs_scores, prediction, make_pipeline(VarianceThreshold(threshold=(.8 * (1 - .8))), DecisionTreeClassifier()), "VarianceThreshold"),
                # LearningClassify(trainingFile, testingFile, training_describe, testing_describe, cs_scores, prediction, make_pipeline(SelectKBest(chi2, k=10), DecisionTreeClassifier()), "SelectKBest_chi"),
                # LearningClassify(trainingFile, testingFile, training_describe, testing_describe, cs_scores, prediction, make_pipeline(SelectKBest(k=10), DecisionTreeClassifier()), "SelectKBest_f_classif")

    @staticmethod
    def drop(features):
        return features.drop('component_name', axis=1)

    def cross_validation(self):
        import sklearn.metrics as metrics
        from sklearn.metrics.scorer import get_scorer
        scores_names = ['accuracy', 'adjusted_mutual_info_score', 'adjusted_rand_score', 'average_precision', 'completeness_score',
         'f1', 'f1_macro', 'f1_micro', 'f1_weighted', 'fowlkes_mallows_score',
         'homogeneity_score', 'mutual_info_score', 'neg_log_loss', 'normalized_mutual_info_score', 'precision',
         'precision_macro', 'precision_micro', 'precision_weighted', 'recall',
         'recall_macro', 'recall_micro', 'recall_weighted', 'roc_auc', 'v_measure_score']
        metrics_functions = [metrics.cohen_kappa_score, metrics.hinge_loss,
                             metrics.matthews_corrcoef, metrics.accuracy_score,
                             metrics.f1_score, metrics.hamming_loss,
                             metrics.log_loss, metrics.precision_score, metrics.recall_score,
                             metrics.zero_one_loss, metrics.average_precision_score, metrics.roc_auc_score]

        def pr_auc_score(y_true, y_score):
            """
            Generates the Area Under the Curve for precision and recall.
            """
            precision, recall, thresholds = \
                metrics.precision_recall_curve(y_true, y_score[:, 1])
            return metrics.auc(recall, precision, reorder=True)

        pr_auc_scorer = metrics.make_scorer(pr_auc_score, greater_is_better=True,
                                    needs_proba=True)
        scoring = {x: get_scorer(x) for x in scores_names}
        scoring.update({x.__name__: metrics.make_scorer(x) for x in metrics_functions})
        scoring["pr_auc"] = pr_auc_scorer

        def tn(y_true, y_pred): return metrics.confusion_matrix(y_true, y_pred)[0, 0]

        def fp(y_true, y_pred): return metrics.confusion_matrix(y_true, y_pred)[0, 1]

        def fn(y_true, y_pred): return metrics.confusion_matrix(y_true, y_pred)[1, 0]

        def tp(y_true, y_pred): return metrics.confusion_matrix(y_true, y_pred)[1, 1]

        def cost(y_true, y_pred, fp_cost=1, fn_cost=1): return fp(y_true, y_pred) * fp_cost + fn(y_true, y_pred)*fn_cost

        def mean_squared_error_cost(true_value, pred_value, fp_cost=1, fn_cost=1):
            # fp is true_value=true and pred_value>0.5
            # fn is true_value=false and pred_value<0.5
            from numpy import mean
            squares = []
            for t,p in zip(true_value, pred_value):
                diff = (t-p) ** 2
                if t:
                    diff *= fp_cost
                else:
                    diff *= fn_cost
                squares.append(diff)
            return mean(squares)

        def mse(y_true, y_pred):
            return min(metrics.mean_squared_error([1 if x else 0 for x in y_true], map(lambda x: x[0][1 if x[1] else 0], zip(y_pred, y_true))), metrics.mean_squared_error([1 if x else 0 for x in y_true], map(lambda x: x[0][0 if x[1] else 1], zip(y_pred, y_true))))

        def mse_cost(y_true, y_pred, fp_cost=1, fn_cost=1):
            return min(mean_squared_error_cost([1 if x else 0 for x in y_true], map(lambda x: x[0][1 if x[1] else 0], zip(y_pred, y_true)), fp_cost=fp_cost, fn_cost=fn_cost),
                       mean_squared_error_cost([1 if x else 0 for x in y_true], map(lambda x: x[0][0 if x[1] else 1], zip(y_pred, y_true)), fp_cost=fp_cost, fn_cost=fn_cost))

        def mse1(y_true, y_pred):
            return max(metrics.mean_squared_error([1 if x else 0 for x in y_true], map(lambda x: x[0][1 if x[1] else 0], zip(y_pred, y_true))), metrics.mean_squared_error([1 if x else 0 for x in y_true], map(lambda x: x[0][0 if x[1] else 1], zip(y_pred, y_true))))

        def mse_cost1(y_true, y_pred, fp_cost=1, fn_cost=1):
            return max(mean_squared_error_cost([1 if x else 0 for x in y_true], map(lambda x: x[0][1 if x[1] else 0], zip(y_pred, y_true)), fp_cost=fp_cost, fn_cost=fn_cost),
                       mean_squared_error_cost([1 if x else 0 for x in y_true], map(lambda x: x[0][0 if x[1] else 1], zip(y_pred, y_true)), fp_cost=fp_cost, fn_cost=fn_cost))
        scoring.update({'tp': metrics.make_scorer(tp), 'tn': metrics.make_scorer(tn),
                        'fp': metrics.make_scorer(fp), 'fn': metrics.make_scorer(fn)})
        scoring.update({"cost_{0}_{1}".format(*x): metrics.make_scorer(cost, fp_cost=x[0], fn_cost=x[1]) for x in product(range(1,4), range(1,4))})
        scoring.update({"mse_cost_{0}_{1}".format(*x): metrics.make_scorer(mse_cost, fp_cost=x[0], fn_cost=x[1], needs_proba=True) for x in
                        product(range(1, 4), range(1, 4))})
        scoring.update({"mse1_cost_{0}_{1}".format(*x): metrics.make_scorer(mse_cost1, fp_cost=x[0], fn_cost=x[1], needs_proba=True) for x in
                        product(range(1, 4), range(1, 4))})
        scoring["mse"] = metrics.make_scorer(mse, needs_proba=True)
        scoring["mse1"] = metrics.make_scorer(mse1, needs_proba=True)
        scores = cross_validate(self.get_classifier(), self.get_training_featues(), self.get_training_labels(), cv=3, scoring=scoring, return_train_score=True)
        all_scores = dict()
        for score in scores:
            all_scores["{0}_mean".format(score)] = scores[score].mean()
            all_scores["{0}_std".format(score)] = scores[score].std()
        with open(self.cv_scores_path + self.get_name() + ".json", "wb") as f:
            json.dump(all_scores, f)

    def _describe_helper(self, array, csv_path):
        pd.DataFrame(array).describe().to_csv(csv_path)

    def describe(self):
        self._describe_helper(self.get_training_featues(), self.training_describe)
        self._describe_helper(self.get_testing_featues(), self.testing_describe)
