import os

os.environ.setdefault("MPLBACKEND", "Agg")  # figures sans interface graphique

import pytest  # noqa: E402
from pyspark.sql import SparkSession  # noqa: E402


@pytest.fixture(scope="session")
def spark():
    session = (
        SparkSession.builder.master("local[1]")
        .appName("netsentinel-tests")
        .config("spark.sql.shuffle.partitions", 1)
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield session
    session.stop()