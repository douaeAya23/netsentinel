"""Plafonnement des classes (responsabilité unique : limiter la taille par classe)."""

from collections.abc import Mapping

from pyspark.sql import DataFrame


class ClassCapSampler:
    """Garde au plus ~`cap` lignes par classe (échantillonnage stratifié avec graine).

    À appliquer au jeu d'entraînement uniquement : le test garde sa distribution réelle.
    """

    def __init__(self, column: str, caps: Mapping[str, int], default_cap: int, seed: int) -> None:
        self._column = column
        self._caps = dict(caps)
        self._default_cap = default_cap
        self._seed = seed

    def apply(self, df: DataFrame) -> DataFrame:
        counts = {
            row[self._column]: row["count"] for row in df.groupBy(self._column).count().collect()
        }
        fractions = {
            value: min(1.0, self._caps.get(value, self._default_cap) / count)
            for value, count in counts.items()
        }
        return df.sampleBy(self._column, fractions, self._seed)