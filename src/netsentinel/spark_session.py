"""Fabrique de SparkSession (responsabilité unique : construire la session)."""

from pyspark.sql import SparkSession

from netsentinel.config import SparkConfig


def build_spark_session(config: SparkConfig) -> SparkSession:
    """Crée (ou récupère) une SparkSession à partir de la configuration fournie."""
    return (
        SparkSession.builder.appName(config.app_name)
        .master(config.master)
        .config("spark.sql.shuffle.partitions", config.shuffle_partitions)
        .config("spark.driver.memory", config.driver_memory)
        .getOrCreate()
    )