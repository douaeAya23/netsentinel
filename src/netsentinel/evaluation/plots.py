"""Figures d'évaluation (responsabilité unique : dessiner et sauvegarder)."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_confusion_matrix(confusion: pd.DataFrame, output: Path) -> Path:
    """Matrice de confusion normalisée par ligne : chaque ligne représente 100 % d'une classe."""
    normalized = confusion.div(confusion.sum(axis=1).replace(0, 1), axis=0)
    fig, ax = plt.subplots(figsize=(8, 7))
    image = ax.imshow(normalized.values, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(len(confusion.columns)), labels=confusion.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(confusion.index)), labels=confusion.index)
    for row in range(len(confusion.index)):
        for col in range(len(confusion.columns)):
            value = normalized.iat[row, col]
            ax.text(
                col, row, f"{value:.2f}", ha="center", va="center",
                color="white" if value > 0.5 else "black",
            )
    fig.colorbar(image, ax=ax, label="Part de la classe réelle")
    ax.set_xlabel("Classe prédite")
    ax.set_ylabel("Classe réelle")
    ax.set_title("Matrice de confusion (jeu de test, distribution réelle)")
    return _save(fig, output)


def plot_feature_importance(importances: pd.Series, output: Path, top: int = 15) -> Path:
    best = importances.head(top).iloc[::-1]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(best.index, best.values)
    ax.set_xlabel("Importance (Random Forest)")
    ax.set_title(f"Les {len(best)} features les plus importantes")
    return _save(fig, output)


def _save(fig: plt.Figure, output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)
    return output