"""Lecture des CSV de flux réseau (responsabilité unique : lire, pas nettoyer)."""

from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType

from netsentinel.ingestion.schema import build_flow_schema


class FlowCsvReader:
    def __init__(self, spark: SparkSession, schema: StructType | None = None) -> None:
        self._spark = spark
        self._schema = schema or build_flow_schema()

    def read(self, directory: Path) -> DataFrame:
        if not any(directory.glob("*.csv")):
            raise FileNotFoundError(f"Aucun fichier CSV trouvé dans {directory}")
        return self._spark.read.csv(str(directory / "*.csv"), header=True, schema=self._schema)