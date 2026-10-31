"""Sélecteurs de features composables : une classe = une règle de sélection."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from netsentinel.eda.statistics import correlation_matrix


@dataclass(frozen=True)
class SelectionResult:
    kept: tuple[str, ...]
    dropped: dict[str, str]  # colonne -> nom du sélecteur qui l'a retirée

    def to_frame(self) -> pd.DataFrame:
        rows = [{"feature": name, "status": "kept", "reason": ""} for name in self.kept]
        rows += [
            {"feature": name, "status": "dropped", "reason": reason}
            for name, reason in self.dropped.items()
        ]
        return pd.DataFrame(rows)


class FeatureSelector(ABC):
    @abstractmethod
    def select(self, df: DataFrame, columns: Sequence[str]) -> list[str]:
        """Retourne les colonnes à conserver, dans leur ordre d'origine."""


class ExcludedColumnsFilter(FeatureSelector):
    """Retire les colonnes exclues par configuration (ex. destination_port)."""

    def __init__(self, excluded: Sequence[str]) -> None:
        self._excluded = frozenset(excluded)

    def select(self, df: DataFrame, columns: Sequence[str]) -> list[str]:
        return [name for name in columns if name not in self._excluded]


class ConstantFeatureFilter(FeatureSelector):
    """Retire les colonnes de variance nulle, qui n'apportent aucune information."""

    def select(self, df: DataFrame, columns: Sequence[str]) -> list[str]:
        stats = df.agg(*[F.stddev(F.col(name)).alias(name) for name in columns]).first()
        return [name for name in columns if stats[name] is not None and stats[name] > 0]


class CorrelationFilter(FeatureSelector):
    """Pour chaque paire corrélée au-delà du seuil, retire la seconde colonne."""

    def __init__(self, threshold: float) -> None:
        self._threshold = threshold

    def select(self, df: DataFrame, columns: Sequence[str]) -> list[str]:
        if len(columns) < 2:
            return list(columns)
        matrix = correlation_matrix(df, columns).abs()
        upper = matrix.where(np.triu(np.ones(matrix.shape, dtype=bool), k=1))
        redundant = {name for name in upper.columns if (upper[name] > self._threshold).any()}
        return [name for name in columns if name not in redundant]


class SelectionPipeline:
    def __init__(self, selectors: Sequence[FeatureSelector]) -> None:
        self._selectors = tuple(selectors)

    def run(self, df: DataFrame, columns: Sequence[str]) -> SelectionResult:
        kept = list(columns)
        dropped: dict[str, str] = {}
        for selector in self._selectors:
            remaining = selector.select(df, kept)
            for name in kept:
                if name not in remaining:
                    dropped[name] = type(selector).__name__
            kept = remaining
        return SelectionResult(kept=tuple(kept), dropped=dropped)