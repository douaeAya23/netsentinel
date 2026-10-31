import numpy as np
import pytest

from netsentinel.evaluation.metrics import ClassificationEvaluator, build_report


def test_build_report_computes_per_class_metrics() -> None:
    matrix = np.array([[2, 1], [0, 1]])

    report = build_report(matrix, ("A", "B"))

    assert report.accuracy == pytest.approx(0.75)
    assert report.per_class.loc["A", "precision"] == pytest.approx(1.0)
    assert report.per_class.loc["A", "recall"] == pytest.approx(2 / 3)
    assert report.per_class.loc["B", "precision"] == pytest.approx(0.5)
    assert report.macro_f1 == pytest.approx((0.8 + 2 / 3) / 2)


def test_macro_f1_ignores_classes_absent_from_the_test_set() -> None:
    matrix = np.array([[3, 0, 0], [0, 2, 0], [0, 0, 0]])

    report = build_report(matrix, ("A", "B", "C"))

    assert report.macro_f1 == pytest.approx(1.0)


def test_evaluator_builds_the_confusion_matrix_from_predictions(spark) -> None:
    predictions = spark.createDataFrame(
        [(0.0, 0.0), (0.0, 0.0), (0.0, 1.0), (1.0, 1.0)], ["label", "prediction"]
    )

    report = ClassificationEvaluator("label", ("A", "B")).evaluate(predictions)

    assert report.confusion.loc["A", "B"] == 1
    assert report.accuracy == pytest.approx(0.75)