"""Assemblage et normalisation des features (responsabilité unique : vectoriser)."""

from collections.abc import Sequence

from pyspark.ml import Pipeline
from pyspark.ml.feature import StandardScaler, VectorAssembler

FEATURES_COLUMN = "features"
_RAW_COLUMN = "raw_features"


def build_vector_pipeline(columns: Sequence[str]) -> Pipeline:
    """Colonnes numériques -> vecteur -> vecteur centré-réduit.

    À ajuster (fit) sur le jeu d'entraînement uniquement, puis à appliquer au test.
    """
    assembler = VectorAssembler(inputCols=list(columns), outputCol=_RAW_COLUMN)
    scaler = StandardScaler(
        inputCol=_RAW_COLUMN, outputCol=FEATURES_COLUMN, withMean=True, withStd=True
    )
    return Pipeline(stages=[assembler, scaler])