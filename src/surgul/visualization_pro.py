"""Publication-oriented visualization helpers for SURgul."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Sequence, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

from surgul.constants import DEFAULT_DPI
from surgul.visualization import (
    VisualizationConfig,
    plot_abstention_tradeoff,
    plot_calibration_curve,
    plot_decision_time_distribution,
)

PUBLICATION_COLORS = {
    "primary": "#0072B2",
    "secondary": "#E69F00",
    "safe": "#009E73",
    "warning": "#D55E00",
    "muted": "#999999",
}


@dataclass
class PublicationFigureConfig:
    """Configuration for manuscript-preparation SURgul figures."""

    output_dir: Path = field(default_factory=lambda: Path("figures"))
    dpi: int = DEFAULT_DPI
    raster_formats: Tuple[str, ...] = ("png",)
    vector_formats: Tuple[str, ...] = ("pdf", "svg")
    figure_size: Tuple[float, float] = (7.0, 5.0)


def setup_publication_style(config: Optional[PublicationFigureConfig] = None) -> None:
    """Apply a compact, publication-friendly matplotlib style."""

    active_config = config or PublicationFigureConfig()
    plt.style.use("seaborn-v0_8-paper")
    plt.rcParams.update(
        {
            "figure.dpi": active_config.dpi,
            "savefig.dpi": active_config.dpi,
            "font.family": "DejaVu Sans",
            "font.size": 8,
            "axes.labelsize": 9,
            "axes.titlesize": 10,
            "legend.fontsize": 7,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "grid.alpha": 0.2,
        }
    )


class PublicationFigureGenerator:
    """Create and save publication-oriented SURgul figures."""

    def __init__(self, config: Optional[PublicationFigureConfig] = None):
        self.config = config or PublicationFigureConfig()
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        setup_publication_style(self.config)

    def save_figure(self, figure: plt.Figure, filename_stem: str) -> Tuple[Path, ...]:
        """Save a figure in configured raster and vector formats."""

        saved_paths = []
        for file_format in self.config.raster_formats + self.config.vector_formats:
            output_path = self.config.output_dir / f"{filename_stem}.{file_format}"
            figure.savefig(output_path, bbox_inches="tight", dpi=self.config.dpi)
            saved_paths.append(output_path)
        return tuple(saved_paths)

    def create_architecture_figure(self) -> plt.Figure:
        """Create a compact SURgul architecture schematic."""

        fig, ax = plt.subplots(figsize=self.config.figure_size)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.axis("off")

        ax.text(5, 7.5, "SURgul Safety-First Architecture", ha="center", va="center", fontsize=11, fontweight="bold")

        input_box = FancyBboxPatch((3.8, 6.5), 2.4, 0.6, boxstyle="round,pad=0.08", facecolor="#D6EEF8", edgecolor="black")
        ax.add_patch(input_box)
        ax.text(5.0, 6.8, "Patient Data", ha="center", va="center", fontsize=9, fontweight="bold")

        gate_labels = [
            "G1 Critical",
            "G2 Moderate",
            "G3 Data Quality",
            "G4 TiTrATE",
            "G5 Uncertainty",
            "G6 Temporal",
        ]
        gate_positions = [(1.6, 5.0), (4.0, 5.0), (6.4, 5.0), (1.6, 3.7), (4.0, 3.7), (6.4, 3.7)]
        gate_colors = [
            PUBLICATION_COLORS["warning"],
            PUBLICATION_COLORS["secondary"],
            PUBLICATION_COLORS["primary"],
            "#F0E442",
            "#CC79A7",
            PUBLICATION_COLORS["safe"],
        ]

        for (x_position, y_position), gate_label, gate_color in zip(gate_positions, gate_labels, gate_colors):
            gate_box = FancyBboxPatch(
                (x_position, y_position),
                1.6,
                0.65,
                boxstyle="round,pad=0.05",
                facecolor=gate_color,
                edgecolor="black",
                alpha=0.85,
            )
            ax.add_patch(gate_box)
            ax.text(x_position + 0.8, y_position + 0.325, gate_label, ha="center", va="center", fontsize=8, color="white", fontweight="bold")
            ax.add_patch(FancyArrowPatch((5.0, 6.5), (x_position + 0.8, y_position + 0.65), arrowstyle="->", lw=1.0, color=PUBLICATION_COLORS["muted"], mutation_scale=10))

        merge_box = FancyBboxPatch((3.2, 2.2), 3.6, 0.75, boxstyle="round,pad=0.08", facecolor="#FDE6C5", edgecolor="black")
        ax.add_patch(merge_box)
        ax.text(5.0, 2.6, "Conservative Merging", ha="center", va="center", fontsize=9, fontweight="bold")
        ax.text(5.0, 2.33, "Abstention priority + max risk tier", ha="center", va="center", fontsize=7)

        for x_position, y_position in gate_positions:
            ax.add_patch(FancyArrowPatch((x_position + 0.8, y_position), (5.0, 2.95), arrowstyle="->", lw=1.0, color="black", mutation_scale=10))

        output_box = FancyBboxPatch((3.7, 0.7), 2.6, 0.7, boxstyle="round,pad=0.08", facecolor="#D9F2E3", edgecolor="black")
        ax.add_patch(output_box)
        ax.text(5.0, 1.05, "Risk Tier + Action + Explanation", ha="center", va="center", fontsize=8.5, fontweight="bold")
        ax.add_patch(FancyArrowPatch((5.0, 2.2), (5.0, 1.4), arrowstyle="->", lw=1.2, color="black", mutation_scale=10))

        fig.tight_layout()
        return fig

    def create_decision_time_figure(self, decision_times_ms: Sequence[float]) -> plt.Figure:
        """Create a publication-styled decision time figure."""

        return plot_decision_time_distribution(
            decision_times_ms,
            system_name="SURgul",
            config=VisualizationConfig(figure_size=self.config.figure_size, dpi=self.config.dpi),
        )

    def create_calibration_figure(
        self,
        y_true: Sequence[int],
        y_prob: Sequence[float],
        n_bins: int = 10,
    ) -> plt.Figure:
        """Create a publication-styled calibration figure."""

        return plot_calibration_curve(
            y_true,
            y_prob,
            n_bins=n_bins,
            config=VisualizationConfig(figure_size=self.config.figure_size, dpi=self.config.dpi),
        )

    def create_tradeoff_figure(
        self,
        abstention_rates: Sequence[float],
        unsafe_rates: Sequence[float],
        labels: Sequence[str],
    ) -> plt.Figure:
        """Create a publication-styled safety-coverage tradeoff figure."""

        return plot_abstention_tradeoff(
            {
                "label": labels,
                "abstention_rate": np.asarray(abstention_rates, dtype=float),
                "unsafe_rate": np.asarray(unsafe_rates, dtype=float),
            },
            config=VisualizationConfig(figure_size=self.config.figure_size, dpi=self.config.dpi),
        )


def generate_all_professional_figures(output_dir: str = "figures") -> Tuple[Path, ...]:
    """Generate the core manuscript-preparation SURgul figures with demo data."""

    generator = PublicationFigureGenerator(
        PublicationFigureConfig(output_dir=Path(output_dir), raster_formats=("png",), vector_formats=("pdf",))
    )
    saved_paths = []

    architecture_figure = generator.create_architecture_figure()
    saved_paths.extend(generator.save_figure(architecture_figure, "surgul_architecture"))
    plt.close(architecture_figure)

    demo_times_ms = np.array([4.8, 5.1, 5.4, 5.9, 6.0, 6.2, 6.5, 7.1, 7.4, 8.0])
    decision_time_figure = generator.create_decision_time_figure(demo_times_ms)
    saved_paths.extend(generator.save_figure(decision_time_figure, "surgul_decision_time"))
    plt.close(decision_time_figure)

    return tuple(saved_paths)


__all__ = [
    "PublicationFigureConfig",
    "PublicationFigureGenerator",
    "generate_all_professional_figures",
    "setup_publication_style",
]
