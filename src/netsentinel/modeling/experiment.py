"""Exécution d'une expérience : préparer, entraîner, prédire, évaluer."""

import time
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from pyspark import StorageLevel
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from netsentinel.evaluation.metrics import ClassificationEvaluator, EvaluationReport
from netsentinel.features.labels import FAMILY_COLUMN
from netsentinel.modeling.factories import ClassifierFactory
from netsentinel.modeling.feature_subset import FeatureSubset
from netsentinel.modeling.sampling import ClassCapSampler
from netsentinel.modeling.tasks import ClassificationTask


@dataclass(frozen=True)
class ExperimentSpec:
    name: str
    task: ClassificationTask
    factory: ClassifierFactory
    dropped_features: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExperimentResult:
    spec: ExperimentSpec
    report: EvaluationReport
    model: Any
    feature_names: tuple[str, ...]
    fit_seconds: float


class ExperimentRunner:
    def __init__(
        self,
        train: DataFrame,
        test: DataFrame,
        feature_names: Sequence[str],
        sampler: ClassCapSampler,
    ) -> None:
        self._train = train
        self._test = test
        self._feature_names = tuple(feature_names)
        self._sampler = sampler

    def run(self, spec: ExperimentSpec) -> ExperimentResult:
        task = spec.task
        subset = FeatureSubset(self._feature_names, spec.dropped_features)

        train = subset.apply(self._sampler.apply(self._restrict(self._train, task)))
        train = train.persist(StorageLevel.MEMORY_AND_DISK)
        test = subset.apply(self._restrict(self._test, task))

        try:
            started = time.perf_counter()
            model = spec.factory.create(task.label_column).fit(train)
            fit_seconds = time.perf_counter() - started

            report = ClassificationEvaluator(task.label_column, task.class_names).evaluate(
                model.transform(test)
            )
        finally:
            train.unpersist()

        return ExperimentResult(spec, report, model, subset.kept_names, fit_seconds)

    @staticmethod
    def _restrict(df: DataFrame, task: ClassificationTask) -> DataFrame:
        if not task.excluded_families:
            return df
        return df.filter(~F.col(FAMILY_COLUMN).isin(*task.excluded_families))