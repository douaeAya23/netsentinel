"""Tâches de classification (responsabilité unique : décrire ce qu'on prédit)."""

from dataclasses import dataclass

from netsentinel.features.labels import (
    BINARY_LABEL_COLUMN,
    FAMILIES,
    FAMILY_INDEX_COLUMN,
)


@dataclass(frozen=True)
class ClassificationTask:
    name: str
    label_column: str
    class_names: tuple[str, ...]
    excluded_families: tuple[str, ...] = ()


BINARY_TASK = ClassificationTask("binary", BINARY_LABEL_COLUMN, ("BENIGN", "ATTACK"))

# "Rare" (Infiltration, Heartbleed : moins de 50 flux) est exclue : inévaluable seule.
# Elle est la dernière famille, donc les indices des 7 autres restent contigus.
FAMILY_TASK = ClassificationTask(
    "family", FAMILY_INDEX_COLUMN, FAMILIES[:-1], excluded_families=("Rare",)
)