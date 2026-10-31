"""Figures de l'EDA (responsabilité unique : dessiner et sauvegarder)."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_class_distribution(distribution: pd.DataFrame, output: Path) -> Path:
    """Barres horizontales en échelle log : le trafic bénin écrase les classes rares."""
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(distribution["label"], distribution["count"])
    ax.set_xscale("log")
    ax.invert_yaxis()
    ax.set_xlabel("Nombre de flux (échelle logarithmique)")
    ax.set_title("Distribution des classes (CIC-IDS2017 nettoyé)")
    ax.set_xlim(right=distribution["count"].max() * 50)
    for bar, count, percent in zip(
        bars, distribution["count"], distribution["percent"], strict=True
    ):
        ax.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f" {count} ({percent:.3f} %)",
            va="center",
        )
    return _save(fig, output)


def plot_correlation_heatmap(correlation: pd.DataFrame, output: Path) -> Path:
    fig, ax = plt.subplots(figsize=(9, 8))
    image = ax.imshow(correlation.values, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(correlation.columns)), labels=correlation.columns, rotation=90)
    ax.set_yticks(range(len(correlation.index)), labels=correlation.index)
    fig.colorbar(image, ax=ax, label="Corrélation de Pearson")
    ax.set_title("Corrélations entre les features clés")
    return _save(fig, output)


def plot_class_signatures(medians: pd.DataFrame, output: Path) -> Path:
    """Carte de chaleur des médianes par classe, en échelle log puis min-max par feature."""
    logged = np.log1p(medians.clip(lower=0))
    spans = (logged.max() - logged.min()).replace(0, 1)
    normalized = (logged - logged.min()) / spans

    fig, ax = plt.subplots(figsize=(11, 6))
    image = ax.imshow(normalized.values, cmap="viridis", aspect="auto")
    ax.set_xticks(
        range(len(normalized.columns)), labels=normalized.columns, rotation=75, ha="right"
    )
    ax.set_yticks(range(len(normalized.index)), labels=normalized.index)
    fig.colorbar(image, ax=ax, label="Médiane normalisée (0 = minimum, 1 = maximum par feature)")
    ax.set_title("Signature de chaque classe : médiane des features clés")
    return _save(fig, output)


def _save(fig: plt.Figure, output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)
    return output