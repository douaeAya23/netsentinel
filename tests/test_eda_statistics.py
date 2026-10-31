import pytest

from netsentinel.eda.statistics import class_distribution, correlation_matrix, median_by_class


def test_class_distribution_counts_and_percentages(spark) -> None:
    df = spark.createDataFrame([("A",), ("A",), ("B",)], ["label"])

    result = class_distribution(df)

    assert result["label"].tolist() == ["A", "B"]
    assert result["count"].tolist() == [2, 1]
    assert result["percent"].iloc[0] == pytest.approx(66.667, abs=1e-3)


def test_median_by_class_returns_one_row_per_class(spark) -> None:
    df = spark.createDataFrame(
        [("A", 1.0), ("A", 3.0), ("A", 5.0), ("B", 10.0)], ["label", "x"]
    )

    result = median_by_class(df, ["x"])

    assert result.loc["A", "x"] == 3.0
    assert result.loc["B", "x"] == 10.0


def test_correlation_matrix_detects_positive_and_negative_links(spark) -> None:
    df = spark.createDataFrame(
        [(1.0, 2.0, 4.0), (2.0, 4.0, 3.0), (3.0, 6.0, 2.0), (4.0, 8.0, 1.0)],
        ["x", "y", "z"],
    )

    result = correlation_matrix(df, ["x", "y", "z"])

    assert result.loc["x", "y"] == pytest.approx(1.0)
    assert result.loc["x", "z"] == pytest.approx(-1.0)