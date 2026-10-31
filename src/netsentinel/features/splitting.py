"""Découpage train/test stratifié et reproductible (responsabilité unique : découper)."""

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F

_RANK = "_split_rank"


class StratifiedSplitter:
    def __init__(self, stratify_column: str, train_fraction: float, seed: int) -> None:
        if not 0.0 < train_fraction < 1.0:
            raise ValueError("train_fraction doit être strictement entre 0 et 1")
        self._stratify_column = stratify_column
        self._train_fraction = train_fraction
        self._seed = seed

    def split(self, df: DataFrame) -> tuple[DataFrame, DataFrame]:
        """Retourne (train, test) : chaque classe est répartie selon train_fraction."""
        content_hash = F.xxhash64(F.lit(self._seed), *[F.col(name) for name in df.columns])
        window = Window.partitionBy(self._stratify_column).orderBy(content_hash)
        ranked = df.withColumn(_RANK, F.percent_rank().over(window))
        train = ranked.filter(F.col(_RANK) < self._train_fraction).drop(_RANK)
        test = ranked.filter(F.col(_RANK) >= self._train_fraction).drop(_RANK)
        return train, test