"""Fabriques de classifieurs (Open/Closed : un nouveau modèle = une nouvelle classe)."""

from abc import ABC, abstractmethod

from pyspark.ml import Estimator
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier

from netsentinel.features.vectorizer import FEATURES_COLUMN


class ClassifierFactory(ABC):
    name: str

    @abstractmethod
    def create(self, label_column: str) -> Estimator:
        """Construit un classifieur non entraîné pour la colonne cible donnée."""


class LogisticRegressionFactory(ClassifierFactory):
    name = "logistic_regression"

    def __init__(self, max_iter: int) -> None:
        self._max_iter = max_iter

    def create(self, label_column: str) -> Estimator:
        return LogisticRegression(
            featuresCol=FEATURES_COLUMN, labelCol=label_column, maxIter=self._max_iter
        )


class RandomForestFactory(ClassifierFactory):
    name = "random_forest"

    def __init__(self, num_trees: int, max_depth: int, seed: int) -> None:
        self._num_trees = num_trees
        self._max_depth = max_depth
        self._seed = seed

    def create(self, label_column: str) -> Estimator:
        return RandomForestClassifier(
            featuresCol=FEATURES_COLUMN,
            labelCol=label_column,
            numTrees=self._num_trees,
            maxDepth=self._max_depth,
            seed=self._seed,
        )