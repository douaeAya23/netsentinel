from types import SimpleNamespace

import pandas as pd
from pyspark.ml.linalg import Vectors

from netsentinel.modeling.experiment import ExperimentRunner, ExperimentSpec
from netsentinel.modeling.factories import LogisticRegressionFactory
from netsentinel.modeling.importance import feature_importances
from netsentinel.modeling.sampling import ClassCapSampler
from netsentinel.modeling.tasks import BINARY_TASK


def _dataset(spark):
    rows = []
    for i in range(20):
        rows.append((Vectors.dense([float(i % 5), 0.0]), "BENIGN", 0.0, 0.0))
        rows.append((Vectors.dense([10.0 + i % 5, 1.0]), "DoS", 1.0, 1.0))
    return spark.createDataFrame(rows, ["features", "family", "family_index", "is_attack"])


def _runner(spark) -> ExperimentRunner:
    data = _dataset(spark)
    sampler = ClassCapSampler("family", {}, default_cap=1000, seed=42)
    return ExperimentRunner(data, data, ("a", "b"), sampler)


def test_runner_trains_and_evaluates_a_binary_model(spark) -> None:
    spec = ExperimentSpec("binary_lr", BINARY_TASK, LogisticRegressionFactory(20))

    result = _runner(spark).run(spec)

    assert result.report.accuracy > 0.9
    assert result.feature_names == ("a", "b")
    assert result.fit_seconds > 0


def test_runner_supports_feature_ablation(spark) -> None:
    spec = ExperimentSpec("ablation", BINARY_TASK, LogisticRegressionFactory(20), ("b",))

    result = _runner(spark).run(spec)

    assert result.feature_names == ("a",)


def test_feature_importances_returns_none_for_models_without_them() -> None:
    assert feature_importances(object(), ("a",)) is None


def test_feature_importances_sorts_values() -> None:
    stub = SimpleNamespace(featureImportances=Vectors.dense([0.1, 0.9]))

    result = feature_importances(stub, ("a", "b"))

    assert isinstance(result, pd.Series)
    assert list(result.index) == ["b", "a"]