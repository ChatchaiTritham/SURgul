"""Generate manuscript-ready SURgul/SRGL figures.

The exports visualize the package's six-gate SRGL architecture and the
conservative merging rule implemented by `surgul.merging.ConservativeMerging`.

Both figures are conceptual schematics (no measured data); they render through
the shared pubviz style (serif fonts, palette edges, vector PDF + 300-dpi PNG).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from pubviz import apply_pub_style, save_fig, PALETTE, add_box, arrow

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"


def generate_srgl_gate_architecture() -> None:
    fig, ax = plt.subplots(figsize=(12, 6.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.95, "SURgul / SRGL Six-Gate Safety Governance", ha="center", fontsize=16, fontweight="bold")

    add_box(ax, (0.04, 0.44), 0.14, 0.16, "Patient data\ncontext\nuncertainty", facecolor="#e0f2fe")

    gates = [
        ("G1\nCritical flags", 0.25, 0.73, "#fee2e2"),
        ("G2\nModerate risk", 0.43, 0.73, "#ffedd5"),
        ("G3\nData quality", 0.61, 0.73, "#fef9c3"),
        ("G4\nTiTrATE", 0.25, 0.43, "#dcfce7"),
        ("G5\nUncertainty", 0.43, 0.43, "#ede9fe"),
        ("G6\nTemporal", 0.61, 0.43, "#e0e7ff"),
    ]
    for label, x, y, color in gates:
        add_box(ax, (x, y), 0.13, 0.13, label, facecolor=color)
        arrow(ax, (0.18, 0.52), (x, y + 0.065))

    add_box(ax, (0.80, 0.56), 0.15, 0.17, "Conservative\nmerging\nmax risk tier", facecolor="#f1f5f9")
    add_box(ax, (0.80, 0.27), 0.15, 0.17, "Triage decision\naction\nfull audit trail", facecolor="#dcfce7")

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

    save_fig(fig, "surgul_srgl_gate_architecture", FIGURES)
    plt.close(fig)


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
        add_box(ax, (0.10, y), 0.20, 0.08, name, facecolor=color, size=10)
        add_box(ax, (0.42, y), 0.20, 0.08, f"Gate output\n{name}", facecolor=color, size=9)
        arrow(ax, (0.30, y + 0.04), (0.42, y + 0.04))

    add_box(ax, (0.72, 0.48), 0.18, 0.16, "Final tier\n=max risk\nunless abstain", facecolor="#f1f5f9", size=10)
    add_box(ax, (0.72, 0.22), 0.18, 0.14, "Final action\n+ enforcement\n+ explanation", facecolor="#e0f2fe", size=10)

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

    save_fig(fig, "surgul_conservative_merging_lattice", FIGURES)
    plt.close(fig)


def main() -> None:
    apply_pub_style()
    generate_srgl_gate_architecture()
    generate_conservative_merging_lattice()
    print(f"Generated SURgul figures in {FIGURES}")


if __name__ == "__main__":
    main()
