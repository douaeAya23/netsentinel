import numpy as np
import pandas as pd

from netsentinel.evaluation.metrics import build_report
from netsentinel.evaluation.plots import plot_confusion_matrix, plot_feature_importance
from netsentinel.evaluation.reporting import summarize
from netsentinel.modeling.experiment import ExperimentResult, ExperimentSpec
from netsentinel.modeling.factories import LogisticRegressionFactory
from netsentinel.modeling.tasks import BINARY_TASK


def test_summarize_builds_one_row_per_experiment() -> None:
    report = build_report(np.array([[2, 0], [0, 2]]), ("A", "B"))
    spec = ExperimentSpec("binary_lr", BINARY_TASK, LogisticRegressionFactory(1))
    result = ExperimentResult(spec, report, None, ("a", "b"), 1.5)

    table = summarize([result])

    assert table.loc[0, "experiment"] == "binary_lr"
    assert table.loc[0, "features"] == 2
    assert table.loc[0, "macro_f1"] == 1.0


def test_plot_confusion_matrix_writes_a_file(tmp_path) -> None:
    confusion = pd.DataFrame([[2, 1], [0, 3]], index=["A", "B"], columns=["A", "B"])

    assert plot_confusion_matrix(confusion, tmp_path / "confusion.png").exists()


def test_plot_feature_importance_writes_a_file(tmp_path) -> None:
    importances = pd.Series([0.7, 0.3], index=["a", "b"])

    assert plot_feature_importance(importances, tmp_path / "importance.png").exists()