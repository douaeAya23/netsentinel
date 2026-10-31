"""Noms des features, dans l'ordre du vecteur (lus dans le rapport de sélection)."""

from pathlib import Path

import pandas as pd


def load_feature_names(selection_report: Path) -> tuple[str, ...]:
    report = pd.read_csv(selection_report)
    return tuple(report.loc[report["status"] == "kept", "feature"])