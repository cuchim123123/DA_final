"""Shared Matplotlib/Seaborn style configuration and reusable plot helpers."""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from src.load_validate import OUTPUTS_DIR

FIGURES_DIR = OUTPUTS_DIR / "figures"

PALETTE_MAIN = {
    "navy": "#1B365D",
    "blue": "#0072B2",
    "teal": "#009E73",
    "orange": "#D55E00",
    "amber": "#E69F00",
    "purple": "#CC79A7",
    "red": "#C0392B",
    "gray": "#5D6D7E",
    "lightgray": "#BDC3C7",
}

SEASON_COLORS = {1: "#0072B2", 2: "#009E73", 3: "#D55E00", 4: "#CC79A7"}
SEASON_CALENDAR_RANGES = {
    1: "Dec 21–Mar 20", 2: "Mar 21–Jun 20", 3: "Jun 21–Sep 22", 4: "Sep 23–Dec 20"
}


def configure_style() -> None:
    """Apply clean, high-contrast academic Matplotlib/Seaborn styling."""
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Segoe UI"],
        "font.size": 10, "axes.titlesize": 11.5, "axes.titleweight": "bold",
        "axes.labelsize": 10, "axes.labelweight": "bold",
        "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 8.5,
        "figure.titlesize": 13, "figure.titleweight": "bold",
        "savefig.dpi": 300, "savefig.bbox": "tight",
        "axes.edgecolor": "#333333", "axes.linewidth": 0.8,
    })


def save_fig(fig: plt.Figure, filename: str) -> str:
    """Save figure to `outputs/figures/` at 300 DPI and close figure handle."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = FIGURES_DIR / filename
    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return str(out_path.relative_to(OUTPUTS_DIR.parent)).replace("\\", "/")


def add_stat_box(
    ax: plt.Axes, text: str, x: float = 0.04, y: float = 0.95, ec: str = "#888888", fontsize: float = 8.2
) -> None:
    """Render a consistent rounded white annotation box on `ax` in axes coordinates."""
    ax.text(
        x, y, text, transform=ax.transAxes, va="top", ha="left", fontsize=fontsize,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=ec, alpha=0.92),
    )


def plot_qq_panel(
    ax: plt.Axes, values: np.ndarray, color: str, title: str, ylabel: str, box_text: str
) -> None:
    """Render a standardized Normal Q-Q plot panel with reference line and diagnostic box."""
    (osm, osr), (slope, intercept, _) = stats.probplot(values, dist="norm")
    ax.scatter(osm, osr, color=color, alpha=0.55, s=20, label=f"Observed Quantiles (n={len(values)})")
    ax.plot(osm, intercept + slope * osm, color=PALETTE_MAIN["red"], lw=2.0, label="Normal Reference Line")
    add_stat_box(ax, box_text)
    ax.set_title(title)
    ax.set_xlabel("Theoretical Standard Normal Quantiles")
    ax.set_ylabel(ylabel)
    ax.legend(loc="lower right", frameon=True)
