"""Job de construction des features : Parquet nettoyé -> train/test vectorisés."""

import logging
from pathlib import Path

from pyspark import StorageLevel

from netsentinel.config import FeaturesConfig, load_config
from netsentinel.features.labels import FAMILY_COLUMN, TARGET_COLUMNS, LabelGrouper, feature_columns
from netsentinel.features.selection import (
    ConstantFeatureFilter,
    CorrelationFilter,
    ExcludedColumnsFilter,
    SelectionPipeline,
)
from netsentinel.features.splitting import StratifiedSplitter
from netsentinel.features.vectorizer import FEATURES_COLUMN, build_vector_pipeline
from netsentinel.spark_session import build_spark_session
from netsentinel.storage import ParquetStore

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path("configs/config.yaml")


def build_selection_pipeline(config: FeaturesConfig) -> SelectionPipeline:
    return SelectionPipeline(
        [
            ExcludedColumnsFilter(config.excluded_columns),
            ConstantFeatureFilter(),
            CorrelationFilter(config.correlation_threshold),
        ]
    )


def main(config_path: Path = DEFAULT_CONFIG_PATH) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    config = load_config(config_path)
    spark = build_spark_session(config.spark)
    store = ParquetStore()
    processed = config.paths.processed_dir

    try:
        labeled = LabelGrouper().apply(store.read(spark, processed / "flows"))

        splitter = StratifiedSplitter(
            FAMILY_COLUMN, config.features.train_fraction, config.features.random_seed
        )
        train, test = splitter.split(labeled)
        train = train.persist(StorageLevel.MEMORY_AND_DISK)

        candidates = feature_columns(labeled)
        selection = build_selection_pipeline(config.features).run(train, candidates)
        logger.info("%d features retenues sur %d", len(selection.kept), len(candidates))
        for name, reason in selection.dropped.items():
            logger.info("Retirée : %-35s par %s", name, reason)

        report = config.paths.reports_dir / "tables" / "feature_selection.csv"
        report.parent.mkdir(parents=True, exist_ok=True)
        selection.to_frame().to_csv(report, index=False)

        model = build_vector_pipeline(selection.kept).fit(train)
        for name, part in (("train", train), ("test", test)):
            vectors = model.transform(part).select(FEATURES_COLUMN, *TARGET_COLUMNS)
            store.write(vectors, processed / name)
            logger.info("%s : %d lignes", name, store.read(spark, processed / name).count())
    finally:
        spark.stop()


if __name__ == "__main__":
    main()