"""Importance des features d'un modèle à base d'arbres."""

from collections.abc import Sequence
from typing import Any

import pandas as pd


def feature_importances(model: Any, names: Sequence[str]) -> pd.Series | None:
    """Importances triées, ou None si le modèle n'en expose pas (ex. régression logistique)."""
    importances = getattr(model, "featureImportances", None)
    if importances is None:
        return None
    return pd.Series(importances.toArray(), index=list(names)).sort_values(ascending=False)