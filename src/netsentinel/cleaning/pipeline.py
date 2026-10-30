"""Enchaînement d'étapes de nettoyage (responsabilité unique : orchestrer)."""

import logging
from collections.abc import Sequence

from pyspark.sql import DataFrame

from netsentinel.cleaning.base import CleaningStep
from netsentinel.cleaning.steps import (
    ColumnNameNormalizer,
    DuplicateRemover,
    InfiniteValueReplacer,
    LabelNormalizer,
    NullRowDropper,
)

logger = logging.getLogger(__name__)


class CleaningPipeline:
    def __init__(self, steps: Sequence[CleaningStep]) -> None:
        self._steps = tuple(steps)

    def run(self, df: DataFrame) -> DataFrame:
        for step in self._steps:
            logger.info("Étape de nettoyage : %s", type(step).__name__)
            df = step.apply(df)
        return df


def build_default_pipeline() -> CleaningPipeline:
    """L'ordre compte : les noms de colonnes sont normalisés en premier."""
    return CleaningPipeline(
        [
            ColumnNameNormalizer(),
            LabelNormalizer(),
            InfiniteValueReplacer(),
            NullRowDropper(),
            DuplicateRemover(),
        ]
    )