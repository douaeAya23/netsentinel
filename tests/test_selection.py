from netsentinel.features.selection import (
    ConstantFeatureFilter,
    CorrelationFilter,
    ExcludedColumnsFilter,
    SelectionPipeline,
)


def test_excluded_columns_filter_removes_listed_columns(spark) -> None:
    df = spark.createDataFrame([(1.0, 2.0)], ["a", "b"])

    assert ExcludedColumnsFilter(["b"]).select(df, ["a", "b"]) == ["a"]


def test_constant_feature_filter_removes_zero_variance_columns(spark) -> None:
    df = spark.createDataFrame([(1.0, 5.0), (2.0, 5.0)], ["a", "b"])

    assert ConstantFeatureFilter().select(df, ["a", "b"]) == ["a"]


def test_correlation_filter_drops_later_column_of_a_correlated_pair(spark) -> None:
    df = spark.createDataFrame(
        [(1.0, 2.0, 1.0), (2.0, 4.0, 3.0), (3.0, 6.0, 2.0), (4.0, 8.0, 4.0)], ["x", "y", "z"]
    )

    assert CorrelationFilter(0.95).select(df, ["x", "y", "z"]) == ["x", "z"]


def test_selection_pipeline_records_why_each_column_was_dropped(spark) -> None:
    df = spark.createDataFrame(
        [(1.0, 2.0, 5.0), (2.0, 4.0, 5.0), (3.0, 6.0, 5.0), (4.0, 8.0, 5.0)], ["x", "y", "c"]
    )
    pipeline = SelectionPipeline([ConstantFeatureFilter(), CorrelationFilter(0.95)])

    result = pipeline.run(df, ["x", "y", "c"])

    assert result.kept == ("x",)
    assert result.dropped == {"c": "ConstantFeatureFilter", "y": "CorrelationFilter"}