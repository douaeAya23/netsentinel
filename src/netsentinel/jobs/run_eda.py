"""Job d'analyse exploratoire : Parquet nettoyé -> tables et figures."""

import logging
from pathlib import Path

from netsentinel.config import load_config
from netsentinel.eda.key_features import KEY_FEATURES
from netsentinel.eda.plots import (
    plot_class_distribution,
    plot_class_signatures,
    plot_correlation_heatmap,
)
from netsentinel.eda.statistics import class_distribution, correlation_matrix, median_by_class
from netsentinel.spark_session import build_spark_session
from netsentinel.storage import ParquetStore

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path("configs/config.yaml")


def main(config_path: Path = DEFAULT_CONFIG_PATH) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    config = load_config(config_path)
    figures_dir = config.paths.reports_dir / "figures"
    tables_dir = config.paths.reports_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    spark = build_spark_session(config.spark)
    try:
        df = ParquetStore().read(spark, config.paths.processed_dir / "flows").cache()

        distribution = class_distribution(df)
        distribution.to_csv(tables_dir / "class_distribution.csv", index=False)
        plot_class_distribution(distribution, figures_dir / "class_distribution.png")
        logger.info("Distribution des classes :\n%s", distribution.to_string(index=False))

        medians = median_by_class(df, KEY_FEATURES)
        medians.to_csv(tables_dir / "median_by_class.csv")
        plot_class_signatures(medians, figures_dir / "class_signatures.png")

        correlation = correlation_matrix(df, KEY_FEATURES)
        plot_correlation_heatmap(correlation, figures_dir / "correlation_heatmap.png")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()