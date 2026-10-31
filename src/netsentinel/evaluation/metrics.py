"""Métriques de classification (responsabilité unique : mesurer des prédictions)."""

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd
from pyspark.sql import DataFrame


@dataclass(frozen=True)
class EvaluationReport:
    per_class: pd.DataFrame  # index : classe ; colonnes : precision, recall, f1, support
    confusion: pd.DataFrame  # lignes : classe réelle ; colonnes : classe prédite
    accuracy: float
    macro_f1: float


def build_report(matrix: np.ndarray, class_names: Sequence[str]) -> EvaluationReport:
    """Construit le rapport depuis une matrice de confusion (réel x prédit)."""
    true_positives = np.diag(matrix).astype(float)
    support = matrix.sum(axis=1)
    predicted = matrix.sum(axis=0)

    precision = _safe_divide(true_positives, predicted)
    recall = _safe_divide(true_positives, support)
    f1 = _safe_divide(2 * precision * recall, precision + recall)

    per_class = pd.DataFrame(
        {"precision": precision, "recall": recall, "f1": f1, "support": support},
        index=list(class_names),
    )
    return EvaluationReport(
        per_class=per_class,
        confusion=pd.DataFrame(matrix, index=list(class_names), columns=list(class_names)),
        accuracy=float(true_positives.sum() / matrix.sum()),
        # Les classes absentes du jeu de test ne comptent pas dans la moyenne
        macro_f1=float(per_class.loc[per_class["support"] > 0, "f1"].mean()),
    )


def _safe_divide(numerator: np.ndarray, denominator: np.ndarray) -> np.ndarray:
    return np.divide(
        numerator.astype(float),
        denominator.astype(float),
        out=np.zeros(len(numerator), dtype=float),
        where=denominator > 0,
    )


class ClassificationEvaluator:
    def __init__(self, label_column: str, class_names: Sequence[str]) -> None:
        self._label_column = label_column
        self._class_names = tuple(class_names)

    def evaluate(self, predictions: DataFrame) -> EvaluationReport:
        """Évalue un DataFrame contenant la colonne cible et la colonne `prediction`."""
        counts = predictions.groupBy(self._label_column, "prediction").count().collect()
        size = len(self._class_names)
        matrix = np.zeros((size, size), dtype=np.int64)
        for row in counts:
            matrix[int(row[0]), int(row[1])] += row[2]
        return build_report(matrix, self._class_names)