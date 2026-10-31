import pytest
from pyspark.ml.linalg import Vectors

from netsentinel.modeling.feature_names import load_feature_names
from netsentinel.modeling.feature_subset import FeatureSubset
from netsentinel.modeling.sampling import ClassCapSampler


def test_sampler_caps_large_classes_and_keeps_small_ones(spark) -> None:
    rows = [("A",)] * 1000 + [("B",)] * 10
    df = spark.createDataFrame(rows, ["family"])

    sampled = ClassCapSampler("family", {}, default_cap=100, seed=42).apply(df)

    assert sampled.filter("family = 'A'").count() < 250
    assert sampled.filter("family = 'B'").count() == 10


def test_sampler_uses_per_class_caps(spark) -> None:
    rows = [("A",)] * 1000 + [("B",)] * 1000
    df = spark.createDataFrame(rows, ["family"])

    sampled = ClassCapSampler("family", {"A": 900}, default_cap=50, seed=42).apply(df)

    assert sampled.filter("family = 'A'").count() > sampled.filter("family = 'B'").count()


def test_feature_subset_drops_the_requested_features(spark) -> None:
    df = spark.createDataFrame([(Vectors.dense([1.0, 2.0, 3.0]),)], ["features"])
    subset = FeatureSubset(("a", "b", "c"), dropped=("b",))

    result = subset.apply(df).first().features

    assert subset.kept_names == ("a", "c")
    assert list(result) == [1.0, 3.0]


def test_feature_subset_rejects_unknown_features() -> None:
    with pytest.raises(ValueError, match="zzz"):
        FeatureSubset(("a", "b"), dropped=("zzz",))


def test_load_feature_names_keeps_only_kept_features_in_order(tmp_path) -> None:
    report = tmp_path / "selection.csv"
    report.write_text(
        "feature,status,reason\na,kept,\nb,kept,\nc,dropped,CorrelationFilter\n", encoding="utf-8"
    )

    assert load_feature_names(report) == ("a", "b")