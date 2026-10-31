"""Sous-ensemble de features d'un vecteur (utilisé pour l'ablation)."""

from collections.abc import Sequence

from pyspark.ml.feature import VectorSlicer
from pyspark.sql import DataFrame

from netsentinel.features.vectorizer import FEATURES_COLUMN

_SLICED = "sliced_features"


class FeatureSubset:
    def __init__(self, all_names: Sequence[str], dropped: Sequence[str]) -> None:
        unknown = set(dropped) - set(all_names)
        if unknown:
            raise ValueError(f"Features inconnues : {sorted(unknown)}")
        self._all_count = len(all_names)
        self._indices = [i for i, name in enumerate(all_names) if name not in set(dropped)]
        self.kept_names = tuple(all_names[i] for i in self._indices)

    def apply(self, df: DataFrame) -> DataFrame:
        if len(self._indices) == self._all_count:
            return df
        slicer = VectorSlicer(inputCol=FEATURES_COLUMN, outputCol=_SLICED, indices=self._indices)
        sliced = slicer.transform(df).drop(FEATURES_COLUMN)
        return sliced.withColumnRenamed(_SLICED, FEATURES_COLUMN)