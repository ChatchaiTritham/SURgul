"""Generate manuscript-ready SURgul/SRGL figures.

The exports visualize the package's six-gate SRGL architecture and the
conservative merging rule implemented by `surgul.merging.ConservativeMerging`.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"


def add_box(ax, xy, width, height, label, facecolor="#f8fafc", edgecolor="#334155", size=9):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.03,rounding_size=0.025",
        linewidth=1.4,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(patch)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        label,
        ha="center",
        va="center",
        fontsize=size,
        wrap=True,
    )


def arrow(ax, start, end, color="#334155"):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={"arrowstyle": "->", "lw": 1.35, "color": color},
    )


def save_current(name: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        plt.savefig(FIGURES / f"{name}.{ext}", dpi=300, bbox_inches="tight")
    plt.close()


def generate_srgl_gate_architecture() -> None:
    fig, ax = plt.subplots(figsize=(12, 6.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.95, "SURgul / SRGL Six-Gate Safety Governance", ha="center", fontsize=16, fontweight="bold")

    add_box(ax, (0.04, 0.44), 0.14, 0.16, "Patient data\ncontext\nuncertainty", "#e0f2fe")

    gates = [
        ("G1\nCritical flags", 0.25, 0.73, "#fee2e2"),
        ("G2\nModerate risk", 0.43, 0.73, "#ffedd5"),
        ("G3\nData quality", 0.61, 0.73, "#fef9c3"),
        ("G4\nTiTrATE", 0.25, 0.43, "#dcfce7"),
        ("G5\nUncertainty", 0.43, 0.43, "#ede9fe"),
        ("G6\nTemporal", 0.61, 0.43, "#e0e7ff"),
    ]
    for label, x, y, color in gates:
        add_box(ax, (x, y), 0.13, 0.13, label, color)
        arrow(ax, (0.18, 0.52), (x, y + 0.065))

    add_box(ax, (0.80, 0.56), 0.15, 0.17, "Conservative\nmerging\nmax risk tier", "#f1f5f9")
    add_box(ax, (0.80, 0.27), 0.15, 0.17, "Triage decision\naction\nfull audit trail", "#dcfce7")

    for _, x, y, _ in gates:
        arrow(ax, (x + 0.13, y + 0.065), (0.80, 0.64))
    arrow(ax, (0.875, 0.56), (0.875, 0.44))

    ax.text(
        0.5,
        0.11,
        "The figure corresponds to SRGL.gates, ConservativeMerging.merge, and TriageDecision audit outputs.",
        ha="center",
        fontsize=9,
        color="#475569",
    )

    save_current("surgul_srgl_gate_architecture")


def generate_conservative_merging_lattice() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.94, "SURgul Conservative Merging and Abstention Priority", ha="center", fontsize=15, fontweight="bold")

    tiers = [
        ("SAFE", 0.12, "#dcfce7"),
        ("LOW", 0.26, "#bbf7d0"),
        ("MODERATE", 0.40, "#fef9c3"),
        ("HIGH", 0.54, "#fed7aa"),
        ("CRITICAL", 0.68, "#fecaca"),
        ("ABSTAIN", 0.84, "#e9d5ff"),
    ]
    for name, y, color in tiers:
        add_box(ax, (0.10, y), 0.20, 0.08, name, color, size=10)
        add_box(ax, (0.42, y), 0.20, 0.08, f"Gate output\n{name}", color, size=9)
        arrow(ax, (0.30, y + 0.04), (0.42, y + 0.04))

    add_box(ax, (0.72, 0.48), 0.18, 0.16, "Final tier\n=max risk\nunless abstain", "#f1f5f9", size=10)
    add_box(ax, (0.72, 0.22), 0.18, 0.14, "Final action\n+ enforcement\n+ explanation", "#e0f2fe", size=10)

    for _, y, _ in tiers:
        arrow(ax, (0.62, y + 0.04), (0.72, 0.56))
    arrow(ax, (0.81, 0.48), (0.81, 0.36))

    ax.text(
        0.5,
        0.06,
        "ConservativeMerging applies abstention priority, max-risk escalation, and union of enforcement actions.",
        ha="center",
        fontsize=9,
        color="#475569",
    )

    save_current("surgul_conservative_merging_lattice")


def main() -> None:
    generate_srgl_gate_architecture()
    generate_conservative_merging_lattice()
    print(f"Generated SURgul figures in {FIGURES}")


if __name__ == "__main__":
    main()
