"""Tableau comparatif des expériences (responsabilité unique : résumer)."""

from collections.abc import Sequence

import pandas as pd

from netsentinel.modeling.experiment import ExperimentResult


def summarize(results: Sequence[ExperimentResult]) -> pd.DataFrame:
    rows = [
        {
            "experiment": result.spec.name,
            "task": result.spec.task.name,
            "model": result.spec.factory.name,
            "features": len(result.feature_names),
            "accuracy": result.report.accuracy,
            "macro_f1": result.report.macro_f1,
            "fit_seconds": result.fit_seconds,
        }
        for result in results
    ]
    return pd.DataFrame(rows)