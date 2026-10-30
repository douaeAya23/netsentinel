"""Contrat commun des étapes de nettoyage."""

from abc import ABC, abstractmethod

from pyspark.sql import DataFrame


class CleaningStep(ABC):
    @abstractmethod
    def apply(self, df: DataFrame) -> DataFrame:
        """Transforme un DataFrame en un autre DataFrame."""