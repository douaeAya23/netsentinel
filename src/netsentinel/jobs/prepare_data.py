"""Job de préparation des données : CSV bruts -> nettoyage -> Parquet."""

import logging
from pathlib import Path

from netsentinel.cleaning.pipeline import build_default_pipeline
from netsentinel.config import load_config
from netsentinel.ingestion.reader import FlowCsvReader
from netsentinel.spark_session import build_spark_session
from netsentinel.storage import ParquetStore

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path("configs/config.yaml")


def main(config_path: Path = DEFAULT_CONFIG_PATH) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    config = load_config(config_path)
    spark = build_spark_session(config.spark)
    store = ParquetStore()
    output = config.paths.processed_dir / "flows"

    try:
        raw = FlowCsvReader(spark).read(config.paths.raw_dir)
        logger.info("Lignes brutes : %d", raw.count())

        store.write(build_default_pipeline().run(raw), output)
        logger.info("Lignes après nettoyage : %d", store.read(spark, output).count())
    finally:
        spark.stop()


if __name__ == "__main__":
    main()