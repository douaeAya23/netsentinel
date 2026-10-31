import pytest

from netsentinel.features.labels import LabelGrouper


def test_label_grouper_adds_family_index_and_binary_target(spark) -> None:
    df = spark.createDataFrame([("BENIGN",), ("DoS Hulk",), ("Heartbleed",)], ["label"])

    rows = {row.label: row for row in LabelGrouper().apply(df).collect()}

    assert rows["BENIGN"].family == "BENIGN"
    assert rows["BENIGN"].family_index == 0.0
    assert rows["BENIGN"].is_attack == 0.0
    assert rows["DoS Hulk"].family == "DoS"
    assert rows["DoS Hulk"].is_attack == 1.0
    assert rows["Heartbleed"].family == "Rare"


def test_label_grouper_rejects_unknown_labels(spark) -> None:
    df = spark.createDataFrame([("Mystery",)], ["label"])

    with pytest.raises(ValueError, match="Mystery"):
        LabelGrouper().apply(df)