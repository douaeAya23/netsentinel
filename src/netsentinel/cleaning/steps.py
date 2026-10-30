"""Étapes de nettoyage : une classe = une règle."""

import re

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

from netsentinel.cleaning.base import CleaningStep


class ColumnNameNormalizer(CleaningStep):
    """Noms en snake_case : le CSV d'origine contient espaces, '/' et '.'."""

    def apply(self, df: DataFrame) -> DataFrame:
        return df.toDF(*[self._normalize(name) for name in df.columns])

    @staticmethod
    def _normalize(name: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")


class LabelNormalizer(CleaningStep):
    """Corrige les labels : caractères non ASCII (ex. 'Web Attack � XSS') et espaces."""

    def __init__(self, label_column: str = "label") -> None:
        self._label_column = label_column

    def apply(self, df: DataFrame) -> DataFrame:
        fixed = F.trim(F.regexp_replace(F.col(self._label_column), r"[^\x00-\x7F]+", "-"))
        return df.withColumn(self._label_column, fixed)


class InfiniteValueReplacer(CleaningStep):
    """Remplace +/-Infinity et NaN par null dans les colonnes décimales.

    À exécuter après ColumnNameNormalizer (les noms doivent être simples).
    """

    def apply(self, df: DataFrame) -> DataFrame:
        double_columns = {f.name for f in df.schema.fields if isinstance(f.dataType, DoubleType)}
        infinities = (float("inf"), float("-inf"))
        columns = [
            F.when(F.isnan(F.col(name)) | F.col(name).isin(*infinities), F.lit(None))
            .otherwise(F.col(name))
            .alias(name)
            if name in double_columns
            else F.col(name)
            for name in df.columns
        ]
        return df.select(*columns)


class NullRowDropper(CleaningStep):
    """Supprime les lignes contenant au moins une valeur manquante."""

    def apply(self, df: DataFrame) -> DataFrame:
        return df.dropna(how="any")


class DuplicateRemover(CleaningStep):
    """Supprime les lignes strictement identiques."""

    def apply(self, df: DataFrame) -> DataFrame:
        return df.dropDuplicates()