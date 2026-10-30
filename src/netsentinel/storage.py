"""Persistance au format Parquet (responsabilité unique : lire/écrire du Parquet)."""

from pathlib import Path

from pyspark.sql import DataFrame, SparkSession


class ParquetStore:
    def write(self, df: DataFrame, path: Path) -> None:
        df.write.mode("overwrite").parquet(str(path))

    def read(self, spark: SparkSession, path: Path) -> DataFrame:
        return spark.read.parquet(str(path))