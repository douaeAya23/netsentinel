"""Job d'entraînement : 5 expériences, comparaison et figures."""

import logging
from pathlib import Path

from netsentinel.config import AppConfig, load_config
from netsentinel.evaluation.plots import plot_confusion_matrix, plot_feature_importance
from netsentinel.evaluation.reporting import summarize
from netsentinel.features.labels import BENIGN_FAMILY, FAMILY_COLUMN
from netsentinel.modeling.experiment import ExperimentResult, ExperimentRunner, ExperimentSpec
from netsentinel.modeling.factories import LogisticRegressionFactory, RandomForestFactory
from netsentinel.modeling.feature_names import load_feature_names
from netsentinel.modeling.importance import feature_importances
from netsentinel.modeling.sampling import ClassCapSampler
from netsentinel.modeling.tasks import BINARY_TASK, FAMILY_TASK
from netsentinel.spark_session import build_spark_session
from netsentinel.storage import ParquetStore

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path("configs/config.yaml")
MAIN_EXPERIMENT = "family_random_forest"


def build_specs(config: AppConfig) -> list[ExperimentSpec]:
    modeling = config.modeling
    logistic = LogisticRegressionFactory(modeling.logistic_max_iter)
    forest = RandomForestFactory(
        modeling.forest_num_trees, modeling.forest_max_depth, modeling.random_seed
    )
    return [
        ExperimentSpec("binary_logistic_regression", BINARY_TASK, logistic),
        ExperimentSpec("binary_random_forest", BINARY_TASK, forest),
        ExperimentSpec("family_logistic_regression", FAMILY_TASK, logistic),
        ExperimentSpec(MAIN_EXPERIMENT, FAMILY_TASK, forest),
        ExperimentSpec(
            "family_random_forest_without_suspects", FAMILY_TASK, forest, modeling.suspect_features
        ),
    ]


def save_main_figures(results: list[ExperimentResult], figures_dir: Path, tables_dir: Path) -> None:
    main = next(result for result in results if result.spec.name == MAIN_EXPERIMENT)
    plot_confusion_matrix(main.report.confusion, figures_dir / "confusion_matrix_family.png")
    importances = feature_importances(main.model, main.feature_names)
    if importances is not None:
        importances.to_csv(tables_dir / "feature_importance.csv", header=["importance"])
        plot_feature_importance(importances, figures_dir / "feature_importance.png")


def main(config_path: Path = DEFAULT_CONFIG_PATH) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    config = load_config(config_path)
    processed = config.paths.processed_dir
    tables_dir = config.paths.reports_dir / "tables"
    figures_dir = config.paths.reports_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)

    spark = build_spark_session(config.spark)
    try:
        store = ParquetStore()
        sampler = ClassCapSampler(
            FAMILY_COLUMN,
            {BENIGN_FAMILY: config.modeling.benign_cap},
            config.modeling.attack_cap,
            config.modeling.random_seed,
        )
        runner = ExperimentRunner(
            store.read(spark, processed / "train"),
            store.read(spark, processed / "test"),
            load_feature_names(tables_dir / "feature_selection.csv"),
            sampler,
        )

        results = []
        for spec in build_specs(config):
            logger.info("Entraînement : %s", spec.name)
            result = runner.run(spec)
            logger.info(
                "%s : accuracy=%.4f, F1 macro=%.4f (%.0f s)",
                spec.name, result.report.accuracy, result.report.macro_f1, result.fit_seconds,
            )
            result.report.per_class.to_csv(
                tables_dir / f"per_class_{spec.name}.csv", float_format="%.4f"
            )
            results.append(result)

        summarize(results).to_csv(
            tables_dir / "model_comparison.csv", index=False, float_format="%.4f"
        )
        save_main_figures(results, figures_dir, tables_dir)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()