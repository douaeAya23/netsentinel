"""Statistiques exploratoires calculées avec Spark (responsabilité unique : calculer)."""

from collections.abc import Sequence

import pandas as pd
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.stat import Correlation
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

LABEL_COLUMN = "label"


def class_distribution(df: DataFrame) -> pd.DataFrame:
    """Nombre et pourcentage de flux par classe, de la plus fréquente à la plus rare."""
    total = df.count()
    counts = df.groupBy(LABEL_COLUMN).count().orderBy(F.desc("count")).toPandas()
    counts["percent"] = (counts["count"] / total * 100).round(3)
    return counts


def median_by_class(df: DataFrame, features: Sequence[str]) -> pd.DataFrame:
    """Médiane de chaque feature par classe.

    La médiane est préférée à la moyenne : les distributions réseau sont très
    asymétriques et quelques flux extrêmes fausseraient la moyenne.
    """
    aggregations = [F.percentile_approx(F.col(name), 0.5).alias(name) for name in features]
    return df.groupBy(LABEL_COLUMN).agg(*aggregations).toPandas().set_index(LABEL_COLUMN)


def correlation_matrix(df: DataFrame, features: Sequence[str]) -> pd.DataFrame:
    """Matrice de corrélation de Pearson, calculée en distribué par Spark MLlib."""
    names = list(features)
    assembled = VectorAssembler(
        inputCols=names, outputCol="features", handleInvalid="skip"
    ).transform(df)
    matrix = Correlation.corr(assembled, "features", "pearson").head()[0]
    return pd.DataFrame(matrix.toArray(), index=names, columns=names)