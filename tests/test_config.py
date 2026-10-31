from pathlib import Path

from netsentinel.config import load_config


def test_load_config_returns_typed_values(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        "paths:\n"
        "  raw_dir: data/raw\n"
        "  processed_dir: data/processed\n"
        "  reports_dir: reports\n"
        "spark:\n"
        "  app_name: Test\n"
        "  master: 'local[1]'\n"
        "  shuffle_partitions: 2\n"
        "  driver_memory: 1g\n"
        "features:\n"
        "  train_fraction: 0.8\n"
        "  random_seed: 42\n"
        "  correlation_threshold: 0.95\n"
        "  excluded_columns: [destination_port]\n"
        "modeling:\n"
        "  random_seed: 42\n"
        "  benign_cap: 100\n"
        "  attack_cap: 50\n"
        "  logistic_max_iter: 10\n"
        "  forest_num_trees: 30\n"
        "  forest_max_depth: 5\n"
        "  suspect_features: [a]\n",
        encoding="utf-8",
    )

    config = load_config(config_file)

    assert config.paths.raw_dir == Path("data/raw")
    assert config.spark.shuffle_partitions == 2
    assert config.features.excluded_columns == ("destination_port",)
    assert config.modeling.forest_num_trees == 30