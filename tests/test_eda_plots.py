import pandas as pd

from netsentinel.eda.plots import (
    plot_class_distribution,
    plot_class_signatures,
    plot_correlation_heatmap,
)


def test_plot_class_distribution_writes_a_file(tmp_path) -> None:
    distribution = pd.DataFrame(
        {"label": ["BENIGN", "DoS"], "count": [90, 10], "percent": [90.0, 10.0]}
    )

    output = plot_class_distribution(distribution, tmp_path / "figures" / "distribution.png")

    assert output.exists()


def test_plot_correlation_heatmap_writes_a_file(tmp_path) -> None:
    correlation = pd.DataFrame(
        [[1.0, 0.5], [0.5, 1.0]], index=["a", "b"], columns=["a", "b"]
    )

    assert plot_correlation_heatmap(correlation, tmp_path / "corr.png").exists()


def test_plot_class_signatures_handles_constant_columns(tmp_path) -> None:
    medians = pd.DataFrame(
        {"x": [1.0, 1.0], "y": [0.0, 5.0]}, index=pd.Index(["BENIGN", "DoS"], name="label")
    )

    assert plot_class_signatures(medians, tmp_path / "signatures.png").exists()