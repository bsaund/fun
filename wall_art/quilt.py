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


def generate_grid(n_colors: int, grid_cols: int, grid_rows: int,
                  probs: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Sample a (grid_rows, grid_cols) integer array of color indices."""
    grid = np.empty((grid_rows, grid_cols), dtype=int)
    for row in range(grid_rows):
        grid[row, :] = rng.choice(n_colors, size=grid_cols, p=probs[row])
    return grid


def _wood_grain_cell(base_rgb: tuple, cell_h: int, cell_w: int,
                     rng: np.random.Generator) -> np.ndarray:
    """
    Render a single wood-panel cell with procedural grain texture.

    Grain runs roughly horizontally with:
      - a slight random diagonal angle
      - two overlapping sine-wave frequencies (coarse bands + fine lines)
      - small random noise
    Color variation is warm-biased (more red shift than blue).
    """
    r, g, b = base_rgb

    y = np.arange(cell_h, dtype=float)[:, None]   # (H, 1)
    x = np.arange(cell_w, dtype=float)[None, :]   # (1, W)

    # Subtle diagonal so grain isn't perfectly horizontal
    angle = rng.uniform(-0.10, 0.10)
    gy = y + angle * x                             # effective grain coordinate

    # Coarse grain bands
    freq1  = rng.uniform(0.4, 1.2)
    phase1 = rng.uniform(0, 2 * np.pi)
    band1  = 0.055 * np.sin(gy * freq1 + phase1)

    # Fine grain lines
    freq2  = rng.uniform(2.5, 5.5)
    phase2 = rng.uniform(0, 2 * np.pi)
    band2  = 0.022 * np.sin(gy * freq2 + phase2)

    noise = rng.normal(0, 0.016, (cell_h, cell_w))

    v = band1 + band2 + noise   # total brightness variation

    # Warm shift: grain affects red channel most, blue least
    cell = np.stack([
        np.clip(r + v * 1.2, 0, 1),
        np.clip(g + v * 0.85, 0, 1),
        np.clip(b + v * 0.45, 0, 1),
    ], axis=-1)
    return cell


def grid_to_rgb(grid: np.ndarray, hex_colors: list[str],
                rng: np.random.Generator,
                cell_w: int = 20, cell_h: int = 20, gap: int = 1,
                texture: bool = True) -> np.ndarray:
    """
    Convert integer color-index grid to an RGB float image.

    Each grid tile becomes a (cell_h × cell_w) pixel block, with a 1-pixel
    dark gap between blocks to simulate panel seams.
    When texture=True each block gets procedural wood grain.
    """
    grid_rows, grid_cols = grid.shape
    stride_x = cell_w + gap
    stride_y = cell_h + gap
    img_h = grid_rows * stride_y - gap
    img_w = grid_cols * stride_x - gap

    # Dark gap / background colour
    gap_color = np.array([0.04, 0.02, 0.01])
    img = np.tile(gap_color, (img_h, img_w, 1))

    base_colors = [mcolors.to_rgb(h) for h in hex_colors]

    for row in range(grid_rows):
        for col in range(grid_cols):
            color_idx = grid[row, col]
            base = base_colors[color_idx]
            y0, x0 = row * stride_y, col * stride_x

            if texture:
                block = _wood_grain_cell(base, cell_h, cell_w, rng)
            else:
                block = np.full((cell_h, cell_w, 3), base)

            img[y0:y0 + cell_h, x0:x0 + cell_w] = block

    return img


def plot(img: np.ndarray, hex_colors: list[str], probs: np.ndarray,
         palette_name: str, grid_cols: int, grid_rows: int,
         printable: bool = False) -> None:
    if printable:
        fig, ax_quilt = plt.subplots(1, 1, figsize=(10, 10))
        fig.patch.set_color("white")
        ax_quilt.imshow(img, interpolation="bilinear", aspect="equal")
        ax_quilt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()
        return

    fig, axes = plt.subplots(
        1, 2, figsize=(14, 7),
        gridspec_kw={"width_ratios": [3, 1]},
    )
    fig.patch.set_facecolor("#1a1a2e")

    # ── Left: quilt grid ──────────────────────────────────────────────────
    ax_quilt = axes[0]
    ax_quilt.imshow(img, interpolation="bilinear", aspect="equal")
    ax_quilt.set_title(
        f"Gradient Quilt  •  {palette_name}  •  {grid_cols}×{grid_rows}",
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

    ax_prob.legend(
        loc="lower right", fontsize=9,
        facecolor="#1a1a2e", labelcolor="white",
        edgecolor="#555555",
    )

    plt.tight_layout(pad=2.0)
    plt.show()


def _parse_dims(value: str, name: str) -> tuple[int, int]:
    """Parse 'N' (square) or 'WxH' into (width, height)."""
    parts = value.lower().split("x")
    if len(parts) == 1:
        n = int(parts[0])
        return n, n
    if len(parts) == 2:
        return int(parts[0]), int(parts[1])
    raise argparse.ArgumentTypeError(f"--{name}: expected N or WxH, got '{value}'")


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
        "--grid", default="40", metavar="WxH",
        help="Grid dimensions as N (square) or WxH tiles, e.g. 40x30",
    )
    parser.add_argument(
        "--cell", default="20", metavar="WxH",
        help="Tile pixel size as N (square) or WxH pixels, e.g. 40x20",
    )
    parser.add_argument(
        "--sigma", type=float, default=0.35,
        help="Gradient steepness (smaller = sharper transition)",
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed for reproducibility",
    )
    parser.add_argument(
        "--no-texture", dest="texture", action="store_false",
        help="Disable wood grain texture (flat solid colors)",
    )
    parser.add_argument(
        "--printable", action="store_true",
        help="Show only the panel (no probability chart) for printing",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    n = max(2, min(7, args.colors))
    if n != args.colors:
        print(f"Clamping --colors to {n}")

    grid_cols, grid_rows = _parse_dims(args.grid, "grid")
    cell_w,    cell_h    = _parse_dims(args.cell, "cell")

    rng = np.random.default_rng(args.seed)
    hex_colors = PALETTES[args.palette][:n]

    probs = color_probabilities(n, grid_rows, sigma=args.sigma)
    grid  = generate_grid(n, grid_cols, grid_rows, probs, rng)
    img   = grid_to_rgb(grid, hex_colors, rng,
                        cell_w=cell_w, cell_h=cell_h, texture=args.texture)

    print(f"Palette: {args.palette}  |  {n} colors  |  "
          f"{grid_cols}×{grid_rows} tiles  |  {cell_w}×{cell_h}px per tile")
    for i, c in enumerate(hex_colors):
        tag = "darkest" if i == 0 else "lightest" if i == n - 1 else f"mid {i}"
        print(f"  [{i}] {c}  ({tag})")

    plot(img, hex_colors, probs, palette_name=args.palette,
         grid_cols=grid_cols, grid_rows=grid_rows, printable=args.printable)


if __name__ == "__main__":
    main()
