from netsentinel.cleaning.steps import (
    ColumnNameNormalizer,
    DuplicateRemover,
    InfiniteValueReplacer,
    LabelNormalizer,
    NullRowDropper,
)


def test_column_name_normalizer_converts_to_snake_case(spark) -> None:
    df = spark.createDataFrame([(1, 2)], [" Flow Bytes/s", "Fwd Header Length.1"])

    result = ColumnNameNormalizer().apply(df)

    assert result.columns == ["flow_bytes_s", "fwd_header_length_1"]


def test_label_normalizer_fixes_encoding_and_whitespace(spark) -> None:
    df = spark.createDataFrame([("Web Attack \ufffd Brute Force",), (" BENIGN",)], ["label"])

    result = LabelNormalizer().apply(df)

    assert [row.label for row in result.collect()] == ["Web Attack - Brute Force", "BENIGN"]


def test_infinite_value_replacer_turns_invalid_values_into_null(spark) -> None:
    df = spark.createDataFrame([(1.0,), (float("inf"),), (float("nan"),)], ["x"])

    result = InfiniteValueReplacer().apply(df)

    assert [row.x for row in result.collect()] == [1.0, None, None]


def test_null_row_dropper_removes_rows_with_missing_values(spark) -> None:
    df = spark.createDataFrame([(1.0,), (None,)], ["x"])

    assert NullRowDropper().apply(df).count() == 1


def test_duplicate_remover_keeps_one_copy(spark) -> None:
    df = spark.createDataFrame([(1, "a"), (1, "a"), (2, "b")], ["x", "y"])

    assert DuplicateRemover().apply(df).count() == 2