#!/usr/bin/env python3
"""
Generate a pseudorandom gradient quilt pattern.

NOTE: This is not the original quilt code (written ~2020, now lost). It was
recreated by Cursor in 2026 as a design tool for wood wall art — the idea
being to use the gradient color grid as a template for arranging stained or
painted wood panels.

Colors are drawn from a palette ranging dark-to-light. Each color has a
probability distribution that peaks at a different row, creating a smooth
gradient from dark (top) to light (bottom).
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

# Palettes ordered dark → light, each with at least 7 swatches
PALETTES = {
    # Ebony → dark rosewood → walnut → cherry → oak → light pine
    "wood":       ["#1a0f0a", "#3b1a12", "#6b3a2a", "#8b5a3a", "#b8864e", "#d4a96a"],
    "ocean":      ["#0a1628", "#0d2d4f", "#1a5276", "#2471a3", "#2e86c1", "#5dade2", "#aed6f1"],
    "sunset":     ["#1a0500", "#7b1a00", "#c0392b", "#e74c3c", "#e67e22", "#f39c12", "#f9e79f"],
    "forest":     ["#0a150a", "#1b4d1b", "#1e8449", "#27ae60", "#52be80", "#a9dfbf", "#d5f5e3"],
    "earth":      ["#1a0e00", "#4a2500", "#7e5109", "#a0522d", "#c8975e", "#d5b99a", "#f0e0cb"],
    "monochrome": ["#080808", "#252525", "#454545", "#686868", "#959595", "#c0c0c0", "#ebebeb"],
    "lavender":   ["#12001f", "#3b0764", "#6b21a8", "#9333ea", "#c084fc", "#d8b4fe", "#f3e8ff"],
    "rose":       ["#1a0008", "#7b0028", "#be185d", "#e91e8c", "#f472b6", "#fbb6ce", "#fce7f3"],
}


def color_probabilities(n_colors: int, grid_height: int, sigma: float = 0.35) -> np.ndarray:
    """
    Return an (grid_height, n_colors) array of per-row probabilities.

    Each color i has a Gaussian centred at row fraction i/(n_colors-1).
    sigma=0.35 puts ~50% probability on the darkest color at the very top
    and ~0% at the very bottom, with smooth transitions in between.
    """
    peaks = np.linspace(0.0, 1.0, n_colors)           # 0 = top, 1 = bottom
    rows  = np.linspace(0.0, 1.0, grid_height)

    # Shape: (grid_height, n_colors)
    dist = np.exp(-0.5 * ((rows[:, None] - peaks[None, :]) / sigma) ** 2)

    # Normalise each row so probabilities sum to 1
    return dist / dist.sum(axis=1, keepdims=True)


def generate_grid(n_colors: int, grid_size: int, probs: np.ndarray,
                  rng: np.random.Generator) -> np.ndarray:
    """Sample a (grid_size, grid_size) integer array of color indices."""
    grid = np.empty((grid_size, grid_size), dtype=int)
    for row in range(grid_size):
        grid[row, :] = rng.choice(n_colors, size=grid_size, p=probs[row])
    return grid


def grid_to_rgb(grid: np.ndarray, hex_colors: list[str]) -> np.ndarray:
    """Convert integer color-index grid to an RGB float image."""
    h, w = grid.shape
    img = np.zeros((h, w, 3))
    for i, hex_color in enumerate(hex_colors):
        img[grid == i] = mcolors.to_rgb(hex_color)
    return img


def plot(img: np.ndarray, hex_colors: list[str], probs: np.ndarray,
         palette_name: str, grid_size: int) -> None:
    fig, axes = plt.subplots(
        1, 2, figsize=(14, 7),
        gridspec_kw={"width_ratios": [3, 1]},
    )
    fig.patch.set_facecolor("#1a1a2e")

    # ── Left: quilt grid ──────────────────────────────────────────────────
    ax_quilt = axes[0]
    ax_quilt.imshow(img, interpolation="nearest", aspect="equal")
    ax_quilt.set_title(
        f"Gradient Quilt  •  {palette_name}  •  {grid_size}×{grid_size}",
        color="white", fontsize=13, pad=10,
    )
    ax_quilt.axis("off")

    # ── Right: probability curves ─────────────────────────────────────────
    ax_prob = axes[1]
    ax_prob.set_facecolor("#0f0f1a")

    rows = np.arange(probs.shape[0])
    n = len(hex_colors)
    labels = (
        ["darkest"] +
        [f"mid {i}" for i in range(1, n - 1)] +
        ["lightest"]
    ) if n > 2 else ["dark", "light"][:n]

    for i, (hex_color, label) in enumerate(zip(hex_colors, labels)):
        ax_prob.plot(
            probs[:, i] * 100, rows,
            color=hex_color, linewidth=2.5, label=label,
        )

    ax_prob.set_xlabel("Probability (%)", color="white")
    ax_prob.set_ylabel("Row  (0 = top)", color="white")
    ax_prob.set_title("Color bias by row", color="white", fontsize=11)
    ax_prob.tick_params(colors="white")
    ax_prob.spines[:].set_color("#555555")
    ax_prob.invert_yaxis()
    ax_prob.grid(True, alpha=0.2, color="white")

    legend = ax_prob.legend(
        loc="lower right", fontsize=9,
        facecolor="#1a1a2e", labelcolor="white",
        edgecolor="#555555",
    )

    plt.tight_layout(pad=2.0)
    plt.show()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a pseudorandom gradient quilt pattern.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--colors", type=int, default=5, metavar="N",
        help="Number of color swatches (2–7)",
    )
    parser.add_argument(
        "--palette", default="wood", choices=sorted(PALETTES),
        help="Color palette (dark → light)",
    )
    parser.add_argument(
        "--size", type=int, default=40, metavar="N",
        help="Grid size (N×N squares)",
    )
    parser.add_argument(
        "--sigma", type=float, default=0.35,
        help="Gradient steepness (smaller = sharper transition)",
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed for reproducibility",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    n = max(2, min(7, args.colors))
    if n != args.colors:
        print(f"Clamping --colors to {n}")

    rng = np.random.default_rng(args.seed)
    hex_colors = PALETTES[args.palette][:n]

    probs = color_probabilities(n, args.size, sigma=args.sigma)
    grid  = generate_grid(n, args.size, probs, rng)
    img   = grid_to_rgb(grid, hex_colors)

    print(f"Palette: {args.palette}  |  {n} colors  |  {args.size}×{args.size} grid")
    for i, c in enumerate(hex_colors):
        tag = "darkest" if i == 0 else "lightest" if i == n - 1 else f"mid {i}"
        print(f"  [{i}] {c}  ({tag})")

    plot(img, hex_colors, probs, palette_name=args.palette, grid_size=args.size)


if __name__ == "__main__":
    main()
