"""Chargement et typage de la configuration (responsabilité unique : config)."""

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class PathsConfig:
    raw_dir: Path
    processed_dir: Path
    reports_dir: Path


@dataclass(frozen=True)
class SparkConfig:
    app_name: str
    master: str
    shuffle_partitions: int
    driver_memory: str


@dataclass(frozen=True)
class FeaturesConfig:
    train_fraction: float
    random_seed: int
    correlation_threshold: float
    excluded_columns: tuple[str, ...]


@dataclass(frozen=True)
class ModelingConfig:
    random_seed: int
    benign_cap: int
    attack_cap: int
    logistic_max_iter: int
    forest_num_trees: int
    forest_max_depth: int
    suspect_features: tuple[str, ...]


@dataclass(frozen=True)
class AppConfig:
    paths: PathsConfig
    spark: SparkConfig
    features: FeaturesConfig
    modeling: ModelingConfig


def load_config(path: Path) -> AppConfig:
    """Lit un fichier YAML et retourne une configuration immuable et typée."""
    with path.open(encoding="utf-8") as file:
        raw = yaml.safe_load(file)

    return AppConfig(
        paths=PathsConfig(**{key: Path(value) for key, value in raw["paths"].items()}),
        spark=SparkConfig(**raw["spark"]),
        features=_load_features(raw["features"]),
        modeling=_load_modeling(raw["modeling"]),
    )


def _load_features(raw: dict) -> FeaturesConfig:
    return FeaturesConfig(**{**raw, "excluded_columns": tuple(raw["excluded_columns"])})


def _load_modeling(raw: dict) -> ModelingConfig:
    return ModelingConfig(**{**raw, "suspect_features": tuple(raw["suspect_features"])})