"""Colonnes cibles et regroupement des labels en familles d'attaque."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

LABEL_COLUMN = "label"
FAMILY_COLUMN = "family"
FAMILY_INDEX_COLUMN = "family_index"
BINARY_LABEL_COLUMN = "is_attack"
TARGET_COLUMNS = (LABEL_COLUMN, FAMILY_COLUMN, FAMILY_INDEX_COLUMN, BINARY_LABEL_COLUMN)

BENIGN_FAMILY = "BENIGN"
# L'ordre fixe l'indice de classe : 0 = BENIGN, 1 = DoS, etc. (déterministe, documenté)
FAMILIES: tuple[str, ...] = (
    BENIGN_FAMILY, "DoS", "DDoS", "PortScan", "BruteForce", "WebAttack", "Bot", "Rare",
)

LABEL_TO_FAMILY: dict[str, str] = {
    "BENIGN": BENIGN_FAMILY,
    "DoS Hulk": "DoS",
    "DoS GoldenEye": "DoS",
    "DoS slowloris": "DoS",
    "DoS Slowhttptest": "DoS",
    "DDoS": "DDoS",
    "PortScan": "PortScan",
    "FTP-Patator": "BruteForce",
    "SSH-Patator": "BruteForce",
    "Web Attack - Brute Force": "WebAttack",
    "Web Attack - XSS": "WebAttack",
    "Web Attack - Sql Injection": "WebAttack",
    "Bot": "Bot",
    "Infiltration": "Rare",
    "Heartbleed": "Rare",
}


def feature_columns(df: DataFrame) -> list[str]:
    """Toutes les colonnes qui ne sont pas des cibles."""
    return [name for name in df.columns if name not in TARGET_COLUMNS]


class LabelGrouper:
    """Ajoute la famille d'attaque, son indice et la cible binaire normal/attaque."""

    def apply(self, df: DataFrame) -> DataFrame:
        self._check_known_labels(df)
        family_map = F.create_map(*[F.lit(x) for pair in LABEL_TO_FAMILY.items() for x in pair])
        index_map = F.create_map(
            *[F.lit(x) for i, family in enumerate(FAMILIES) for x in (family, float(i))]
        )
        return (
            df.withColumn(FAMILY_COLUMN, family_map.getItem(F.col(LABEL_COLUMN)))
            .withColumn(FAMILY_INDEX_COLUMN, index_map.getItem(F.col(FAMILY_COLUMN)))
            .withColumn(
                BINARY_LABEL_COLUMN,
                F.when(F.col(FAMILY_COLUMN) == BENIGN_FAMILY, 0.0).otherwise(1.0),
            )
        )

    @staticmethod
    def _check_known_labels(df: DataFrame) -> None:
        present = {row[LABEL_COLUMN] for row in df.select(LABEL_COLUMN).distinct().collect()}
        unknown = present - LABEL_TO_FAMILY.keys()
        if unknown:
            raise ValueError(f"Labels inconnus : {sorted(unknown)}")