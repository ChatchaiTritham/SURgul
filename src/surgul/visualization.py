"""Visualization utilities for SURgul results and safety analyses."""

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Optional, Sequence, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np

from surgul.constants import DEFAULT_DPI, DEFAULT_FIGURE_SIZE
from surgul.gates import GateOutput, RiskTier

PLOT_COLORS = {
    "safe": "#56B4E9",
    "low": "#009E73",
    "moderate": "#F0E442",
    "high": "#E69F00",
    "critical": "#D55E00",
    "abstain": "#999999",
    "primary": "#0072B2",
}

RISK_TIER_LABELS = ["SAFE", "LOW", "MODERATE", "HIGH", "CRITICAL", "ABSTAIN"]
RISK_TIER_VALUES = [0, 1, 2, 3, 4, -1]


@dataclass
class VisualizationConfig:
    """Shared plotting configuration for SURgul figures."""

    figure_size: Tuple[float, float] = DEFAULT_FIGURE_SIZE
    dpi: int = DEFAULT_DPI
    style: str = "seaborn-v0_8-whitegrid"


def set_visualization_defaults(config: Optional[VisualizationConfig] = None) -> None:
    """Apply consistent plotting defaults for SURgul visualizations."""

    config = config or VisualizationConfig()
    plt.style.use(config.style)
    plt.rcParams.update(
        {
            "figure.dpi": config.dpi,
            "savefig.dpi": config.dpi,
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.25,
        }
    )


def save_figure(
    figure: plt.Figure,
    output_path: Union[str, Path],
    dpi: int = DEFAULT_DPI,
) -> Path:
    """Save a matplotlib figure and return the resolved output path."""

    resolved_path = Path(output_path)
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(resolved_path, bbox_inches="tight", dpi=dpi)
    return resolved_path


def plot_gate_tier_distribution(
    gate_outputs: Sequence[GateOutput],
    config: Optional[VisualizationConfig] = None,
) -> plt.Figure:
    """Plot the risk tiers assigned by each SURgul gate."""

    set_visualization_defaults(config)
    figure_size = (config.figure_size if config else DEFAULT_FIGURE_SIZE)
    fig, ax = plt.subplots(figsize=figure_size)

    gate_names = [output.gate_name for output in gate_outputs]
    tier_values = [output.tier.value for output in gate_outputs]
    colors = [_tier_to_color(output.tier) for output in gate_outputs]

    ax.bar(gate_names, tier_values, color=colors, edgecolor="black", linewidth=0.8)
    ax.axhline(RiskTier.MODERATE.value, linestyle="--", color=PLOT_COLORS["primary"], linewidth=1.2)
    ax.set_ylabel("Risk Tier")
    ax.set_title("Gate-Level Risk Tier Outputs")
    ax.set_yticks(RISK_TIER_VALUES)
    ax.set_yticklabels(RISK_TIER_LABELS)
    ax.tick_params(axis="x", rotation=30)

    for index, output in enumerate(gate_outputs):
        ax.text(
            index,
            output.tier.value + 0.1,
            f"{output.confidence:.2f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.tight_layout()
    return fig


def plot_decision_time_distribution(
    decision_times_ms: Sequence[float],
    system_name: str = "SURgul",
    config: Optional[VisualizationConfig] = None,
) -> plt.Figure:
    """Plot histogram and summary markers for decision times."""

    set_visualization_defaults(config)
    figure_size = (config.figure_size if config else DEFAULT_FIGURE_SIZE)
    fig, ax = plt.subplots(figsize=figure_size)

    values = np.asarray(decision_times_ms, dtype=float)
    ax.hist(values, bins=min(30, max(10, values.size // 5)), color=PLOT_COLORS["primary"], alpha=0.8)
    mean_value = float(np.mean(values))
    percentile_95 = float(np.percentile(values, 95))
    ax.axvline(mean_value, color=PLOT_COLORS["critical"], linestyle="--", label=f"Mean {mean_value:.2f} ms")
    ax.axvline(percentile_95, color=PLOT_COLORS["high"], linestyle=":", label=f"P95 {percentile_95:.2f} ms")
    ax.set_xlabel("Decision Time (ms)")
    ax.set_ylabel("Count")
    ax.set_title(f"{system_name} Decision Time Distribution")
    ax.legend()
    fig.tight_layout()
    return fig


def plot_calibration_curve(
    y_true: Sequence[int],
    y_prob: Sequence[float],
    n_bins: int = 10,
    config: Optional[VisualizationConfig] = None,
) -> plt.Figure:
    """Plot a simple reliability diagram with bin counts."""

    set_visualization_defaults(config)
    figure_size = (config.figure_size if config else DEFAULT_FIGURE_SIZE)
    fig, ax = plt.subplots(figsize=figure_size)

    y_true_array = np.asarray(y_true, dtype=float)
    y_prob_array = np.asarray(y_prob, dtype=float)
    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)

    predicted_probabilities = []
    observed_frequencies = []
    counts = []

    for index in range(n_bins):
        if index == 0:
            in_bin = (y_prob_array >= bin_edges[index]) & (y_prob_array <= bin_edges[index + 1])
        else:
            in_bin = (y_prob_array > bin_edges[index]) & (y_prob_array <= bin_edges[index + 1])

        if np.any(in_bin):
            predicted_probabilities.append(float(np.mean(y_prob_array[in_bin])))
            observed_frequencies.append(float(np.mean(y_true_array[in_bin])))
            counts.append(int(np.sum(in_bin)))

    ax.plot([0, 1], [0, 1], linestyle="--", color="black", label="Perfect calibration")
    ax.plot(
        predicted_probabilities,
        observed_frequencies,
        marker="o",
        color=PLOT_COLORS["primary"],
        linewidth=2,
        label=f"ECE {expected_calibration_error(y_true_array, y_prob_array, n_bins):.3f}",
    )

    for x_value, y_value, count in zip(predicted_probabilities, observed_frequencies, counts):
        ax.text(x_value, y_value + 0.03, f"n={count}", ha="center", fontsize=8)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Predicted Probability")
    ax.set_ylabel("Observed Frequency")
    ax.set_title("Calibration Curve")
    ax.legend()
    fig.tight_layout()
    return fig


def plot_abstention_tradeoff(
    results: Union[Sequence[Mapping[str, float]], Mapping[str, Sequence[float]]],
    config: Optional[VisualizationConfig] = None,
) -> plt.Figure:
    """Plot abstention rate against unsafe or false-negative rate."""

    set_visualization_defaults(config)
    figure_size = (config.figure_size if config else DEFAULT_FIGURE_SIZE)
    fig, ax = plt.subplots(figsize=figure_size)

    labels, abstention_rates, unsafe_rates = _normalize_tradeoff_inputs(results)

    ax.scatter(abstention_rates, unsafe_rates, s=120, color=PLOT_COLORS["primary"], edgecolors="black")
    for label, abstention_rate, unsafe_rate in zip(labels, abstention_rates, unsafe_rates):
        ax.annotate(label, (abstention_rate, unsafe_rate), textcoords="offset points", xytext=(5, 5))

    ax.axhspan(0.0, 1.0, color=PLOT_COLORS["low"], alpha=0.12)
    ax.set_xlabel("Abstention Rate (%)")
    ax.set_ylabel("Unsafe Rate (%)")
    ax.set_title("Safety-Coverage Trade-off")
    fig.tight_layout()
    return fig


def expected_calibration_error(
    y_true: Sequence[float],
    y_prob: Sequence[float],
    n_bins: int = 10,
) -> float:
    """Compute expected calibration error for binary probabilities."""

    y_true_array = np.asarray(y_true, dtype=float)
    y_prob_array = np.asarray(y_prob, dtype=float)
    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    calibration_error = 0.0

    for index in range(n_bins):
        if index == 0:
            in_bin = (y_prob_array >= bin_edges[index]) & (y_prob_array <= bin_edges[index + 1])
        else:
            in_bin = (y_prob_array > bin_edges[index]) & (y_prob_array <= bin_edges[index + 1])

        if np.any(in_bin):
            accuracy = float(np.mean(y_true_array[in_bin]))
            confidence = float(np.mean(y_prob_array[in_bin]))
            weight = float(np.mean(in_bin))
            calibration_error += abs(accuracy - confidence) * weight

    return calibration_error


def _normalize_tradeoff_inputs(
    results: Union[Sequence[Mapping[str, float]], Mapping[str, Sequence[float]]]
) -> Tuple[Sequence[str], np.ndarray, np.ndarray]:
    """Normalize tradeoff inputs from record or column-oriented mappings."""

    if isinstance(results, Mapping):
        labels = [str(value) for value in results["label"]]
        abstention_rates = np.asarray(results["abstention_rate"], dtype=float)
        unsafe_rates = np.asarray(results["unsafe_rate"], dtype=float)
        return labels, abstention_rates, unsafe_rates

    labels = [str(record["label"]) for record in results]
    abstention_rates = np.asarray([record["abstention_rate"] for record in results], dtype=float)
    unsafe_rates = np.asarray([record["unsafe_rate"] for record in results], dtype=float)
    return labels, abstention_rates, unsafe_rates


def _tier_to_color(risk_tier: RiskTier) -> str:
    """Map a risk tier to a consistent plot color."""

    if risk_tier == RiskTier.SAFE:
        return PLOT_COLORS["safe"]
    if risk_tier == RiskTier.LOW:
        return PLOT_COLORS["low"]
    if risk_tier == RiskTier.MODERATE:
        return PLOT_COLORS["moderate"]
    if risk_tier == RiskTier.HIGH:
        return PLOT_COLORS["high"]
    if risk_tier == RiskTier.CRITICAL:
        return PLOT_COLORS["critical"]
    return PLOT_COLORS["abstain"]


__all__ = [
    "VisualizationConfig",
    "expected_calibration_error",
    "plot_abstention_tradeoff",
    "plot_calibration_curve",
    "plot_decision_time_distribution",
    "plot_gate_tier_distribution",
    "save_figure",
    "set_visualization_defaults",
]
