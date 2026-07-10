#!/usr/bin/env python3
"""
Visualize the scrabble-board wall art: a 15x15 grid of squares on light
plywood, divided by dark walnut lines, built on a square sheet with a dark
wood frame around the perimeter.

Geometry (inches), all to scale:
  - 15x15 grid of 3" squares (standard scrabble board).
  - 0.25" walnut dividing lines, centered on each of the 16 grid boundaries.
  - The grid doesn't run edge-to-edge on the sheet. Outside the grid there's
    a light plywood border, and the dividing lines continue straight into
    that border rather than stopping at the last square.
  - A dark wood frame sits at the outer edge of the sheet.

Sheet size, grid size, and border width are all given; the frame width is
whatever is left over: frame = (sheet - grid - 2*border) / 2.
"""

import argparse
import base64
import functools
import io

import numpy as np
import plotly.graph_objects as go
from PIL import Image

PLYWOOD_COLOR = "#e8d3a0"
WALNUT_COLOR = "#5c3a1e"
FRAME_COLOR = "#2a160c"

# Standard 15x15 Scrabble board layout, row 0 = top edge of the board as it's
# normally drawn. "." is a plain square; the center square (7, 7) is the
# double-word start square. https://en.wikipedia.org/wiki/Scrabble#Board
_SCRABBLE_ROWS = [
    "TW . . DL . . . TW . . . DL . . TW",
    ". DW . . . TL . . . TL . . . DW .",
    ". . DW . . . DL . DL . . . DW . .",
    "DL . . DW . . . DL . . . DW . . DL",
    ". . . . DW . . . . . DW . . . .",
    ". TL . . . TL . . . TL . . . TL .",
    ". . DL . . . DL . DL . . . DL . .",
    "TW . . DL . . . DW . . . DL . . TW",
    ". . DL . . . DL . DL . . . DL . .",
    ". TL . . . TL . . . TL . . . TL .",
    ". . . . DW . . . . . DW . . . .",
    "DL . . DW . . . DL . . . DW . . DL",
    ". . DW . . . DL . DL . . . DW . .",
    ". DW . . . TL . . . TL . . . DW .",
    "TW . . DL . . . TW . . . DL . . TW",
]
SCRABBLE_LAYOUT = [row.split() for row in _SCRABBLE_ROWS]

SPECIAL_LABELS = {
    "TW": "Triple Word",
    "DW": "Double Word",
    "TL": "Triple Letter",
    "DL": "Double Letter",
}

# Final stain allocation. Hex values are best-effort estimates of how each
# looks on plywood -- eyeball against a real test swatch and adjust with
# --tw-color/--dw-color/--tl-color/--dl-color.
STAIN_COLORS = {
    "TW": "#3b2415",   # Minwax Dark Walnut - darkest, anchors the 8 TW squares
    "DW": "#8f2f22",   # General Finishes Cherry - vivid red
    "TL": "#a35a34",   # Varathane Red Oak - medium brown
    "DL": "#c79a5f",   # General Finishes Honey Maple - light honey/amber
}


def _hex_to_rgb01(hex_color: str) -> tuple[float, float, float]:
    """Parse '#rrggbb' (or 'rrggbb') into (r, g, b) floats in [0, 1]."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def _hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    """Parse '#rrggbb' into a Plotly-friendly 'rgba(r, g, b, a)' string."""
    r, g, b = (round(c * 255) for c in _hex_to_rgb01(hex_color))
    return f"rgba({r}, {g}, {b}, {alpha})"


@functools.lru_cache(maxsize=64)
def _wood_grain_image(base_hex: str, height_in: float, width_in: float,
                       ppi: float, seed: int) -> np.ndarray:
    """
    Procedurally render a wood-grain texture, sized in physical inches.

    Built from three layers, all in cycles/inch so the look stays the same
    regardless of `ppi`:
      - Primary grain: coarse + fine bands running mostly horizontally
        (the dominant "length of the board" direction), with a slight
        random diagonal drift.
      - Cross-grain: several weaker layers at random angles from
        horizontal to vertical, so the texture isn't just uniform stripes.
      - A couple of knots (radial swirl + decay) for character.

    Cached on its (hashable) arguments: this is the expensive part of
    rendering the board, and callers -- like the Dash app -- often re-render
    with the same texture but a different stain/frame color.
    """
    rng = np.random.default_rng(seed)
    r, g, b = _hex_to_rgb01(base_hex)

    h_px, w_px = int(round(height_in * ppi)), int(round(width_in * ppi))
    y = np.arange(h_px, dtype=float)[:, None] / ppi   # inches
    x = np.arange(w_px, dtype=float)[None, :] / ppi   # inches
    Y, X = np.broadcast_arrays(y, x)

    v = np.zeros((h_px, w_px))

    # Primary grain: mostly horizontal, coarse bands + fine lines.
    base_angle = rng.uniform(-0.12, 0.12)   # radians of drift from horizontal
    proj = Y + base_angle * X
    for freq_lo, freq_hi, amp in ((0.12, 0.28, 0.05), (0.8, 1.6, 0.024), (3.0, 6.0, 0.012)):
        freq = rng.uniform(freq_lo, freq_hi)
        phase = rng.uniform(0, 2 * np.pi)
        v += amp * np.sin(proj * 2 * np.pi * freq + phase)

    # Cross-grain: weaker layers at random angles (0 = horizontal bands,
    # pi/2 = vertical bands) so grain direction varies across the sheet
    # instead of reading as uniform stripes.
    for _ in range(4):
        angle = rng.uniform(0, np.pi / 2)
        freq = rng.uniform(0.3, 2.5)
        phase = rng.uniform(0, 2 * np.pi)
        amp = rng.uniform(0.008, 0.02)
        cross_proj = X * np.sin(angle) + Y * np.cos(angle)
        v += amp * np.sin(cross_proj * 2 * np.pi * freq + phase)

    # Knots: a couple of localized elliptical swirls.
    for _ in range(rng.integers(2, 5)):
        cx = rng.uniform(0, width_in)
        cy = rng.uniform(0, height_in)
        stretch = rng.uniform(1.5, 3.0)
        dist = np.hypot(X - cx, (Y - cy) * stretch)
        ring_freq = rng.uniform(2.5, 4.5)
        decay = np.exp(-dist / rng.uniform(1.2, 2.5))
        v += 0.06 * np.sin(dist * ring_freq) * decay

    noise = rng.normal(0, 0.015, (h_px, w_px))
    v += noise

    img = np.stack([
        np.clip(r + v * 1.2, 0, 1),
        np.clip(g + v * 0.85, 0, 1),
        np.clip(b + v * 0.45, 0, 1),
    ], axis=-1)
    return img


@functools.lru_cache(maxsize=64)
def _wood_grain_data_uri(base_hex: str, height_in: float, width_in: float,
                         ppi: float, seed: int) -> str:
    """PNG data URI of `_wood_grain_image`, ready to embed as a layout image.

    Flipped vertically because raster images are stored top-row-first, while
    our array's row 0 is y=0 (the bottom of the plot).
    """
    img = _wood_grain_image(base_hex, height_in, width_in, ppi, seed)
    rgb888 = np.flipud((img * 255).round().astype(np.uint8))
    buf = io.BytesIO()
    Image.fromarray(rgb888, mode="RGB").save(buf, format="png")
    encoded = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def draw_board(fig: go.Figure, sheet: float, square: float, n: int, line: float,
                border: float, plywood_color: str, walnut_color: str,
                frame_color: str, draw_frame: bool = True,
                texture: bool = True, ppi: float = 30.0,
                seed: int | None = None) -> float:
    """
    Draw the board onto `fig`. Returns the computed frame width.

    Layout along one axis:
      [ frame ][ border ][            grid (n squares)            ][ border ][ frame ]
                          ^ lines drawn at each of the n+1 boundaries,
                            extended to span the full border+grid zone.

    The frame itself is just the plot's background color showing through the
    ring outside the plywood field -- nothing else is drawn out there -- so
    there's no need to stack a frame shape underneath the texture image.
    """
    if seed is None:
        seed = np.random.SeedSequence().entropy

    grid_span = n * square
    frame = (sheet - grid_span - 2 * border) / 2
    if frame < 0:
        raise ValueError(
            f"Sheet too small: grid ({grid_span}\") + 2*border ({2 * border}\") "
            f"exceeds sheet ({sheet}\")."
        )

    light_lo, light_hi = frame, sheet - frame
    light_size = light_hi - light_lo
    grid_lo = frame + border

    fig.update_layout(plot_bgcolor=frame_color if draw_frame else "white")

    # Light plywood field: border + grid, inset from the frame.
    if texture:
        uri = _wood_grain_data_uri(plywood_color, light_size, light_size, ppi, seed)
        fig.add_layout_image(
            source=uri, x=light_lo, y=light_lo, sizex=light_size, sizey=light_size,
            xref="x", yref="y", xanchor="left", yanchor="bottom",
            sizing="stretch", layer="below",
        )
    else:
        fig.add_shape(
            type="rect", x0=light_lo, y0=light_lo, x1=light_hi, y1=light_hi,
            fillcolor=plywood_color, line_width=0, layer="below",
        )

    # Dividing lines at each of the n+1 grid boundaries, spanning the full
    # light zone (border-to-border) so they run past the last square.
    for i in range(n + 1):
        pos = grid_lo + i * square - line / 2
        # Vertical line
        fig.add_shape(
            type="rect", x0=pos, y0=light_lo, x1=pos + line, y1=light_hi,
            fillcolor=walnut_color, line_width=0,
        )
        # Horizontal line
        fig.add_shape(
            type="rect", x0=light_lo, y0=pos, x1=light_hi, y1=pos + line,
            fillcolor=walnut_color, line_width=0,
        )

    return frame


def draw_special_squares(fig: go.Figure, layout: list[list[str]], square: float, n: int,
                          line: float, grid_lo: float,
                          stain_colors: dict[str, str], alpha: float = 0.65) -> None:
    """
    Stain each special square (TW/DW/TL/DL) from `layout` inside its cell,
    inset by half a line-width on each side so the walnut dividers stay
    visible around it.

    `layout[row][col]` uses row 0 = top of the board (as it's normally
    drawn); the plot's y-axis increases upward, so row r is placed at
    grid position (n - 1 - r).
    """
    inset = line / 2
    cell = square - line
    for row in range(n):
        for col in range(n):
            code = layout[row][col]
            if code not in stain_colors:
                continue
            x0 = grid_lo + col * square + inset
            y0 = grid_lo + (n - 1 - row) * square + inset
            fig.add_shape(
                type="rect", x0=x0, y0=y0, x1=x0 + cell, y1=y0 + cell,
                fillcolor=_hex_to_rgba(stain_colors[code], alpha), line_width=0,
            )


def _readable_text_color(hex_color: str) -> str:
    """Pick black or white text, whichever contrasts against `hex_color`."""
    r, g, b = _hex_to_rgb01(hex_color)
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return "white" if luminance < 0.5 else "black"


def draw_special_labels(fig: go.Figure, layout: list[list[str]], square: float, n: int,
                         grid_lo: float, stain_colors: dict[str, str],
                         fontsize: float = 14.0) -> None:
    """
    Overlay the TW/DW/TL/DL code at the center of each special square, in a
    color that contrasts with that square's stain -- handy as a staining
    reference sheet.
    """
    for row in range(n):
        for col in range(n):
            code = layout[row][col]
            if code not in stain_colors:
                continue
            cx = grid_lo + (col + 0.5) * square
            cy = grid_lo + (n - 1 - row + 0.5) * square
            fig.add_annotation(
                x=cx, y=cy, text=code, showarrow=False,
                font=dict(size=fontsize, color=_readable_text_color(stain_colors[code]), weight="bold"),
            )


def draw_legend(fig: go.Figure, stain_colors: dict[str, str], alpha: float = 0.65) -> None:
    """
    Add clickable legend entries for the stain colors, via zero-data dummy
    traces (shapes and images can't add themselves to a Plotly legend).
    """
    for code in ("TW", "DW", "TL", "DL"):
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="markers",
            marker=dict(size=12, symbol="square", color=stain_colors[code], opacity=alpha),
            name=f"{code} – {SPECIAL_LABELS[code]}", showlegend=True,
        ))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Visualize the scrabble-board wall art layout.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--sheet", type=float, default=48.0, help="Plywood sheet size (inches, square)")
    parser.add_argument("--square", type=float, default=3.0, help="Size of one scrabble square (inches)")
    parser.add_argument("--n", type=int, default=15, help="Grid dimension (NxN squares)")
    parser.add_argument("--line", type=float, default=0.25, help="Walnut dividing line width (inches)")
    parser.add_argument("--border", type=float, default=1.0, help="Light plywood border around the grid, before the frame (inches)")
    parser.add_argument("--no-frame", dest="draw_frame", action="store_false", help="Don't draw the dark outer frame")
    parser.add_argument("--plywood-color", default=PLYWOOD_COLOR, help="Background plywood color")
    parser.add_argument("--walnut-color", default=WALNUT_COLOR, help="Dividing line color")
    parser.add_argument("--frame-color", default=FRAME_COLOR, help="Outer frame color")
    parser.add_argument("--no-texture", dest="texture", action="store_false", help="Disable wood grain texture (flat plywood color)")
    parser.add_argument("--ppi", type=float, default=30.0, help="Texture resolution, pixels per inch")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for the wood grain texture")
    parser.add_argument("--no-specials", dest="specials", action="store_false", help="Don't stain the TW/DW/TL/DL squares")
    parser.add_argument("--stain-alpha", type=float, default=0.65, help="Opacity of the special-square stain (0-1)")
    parser.add_argument("--tw-color", default=STAIN_COLORS["TW"], help="Triple Word stain color")
    parser.add_argument("--dw-color", default=STAIN_COLORS["DW"], help="Double Word stain color")
    parser.add_argument("--tl-color", default=STAIN_COLORS["TL"], help="Triple Letter stain color")
    parser.add_argument("--dl-color", default=STAIN_COLORS["DL"], help="Double Letter stain color")
    parser.add_argument("--no-legend", dest="legend", action="store_false", help="Don't draw the stain-color legend")
    parser.add_argument("--labels", action="store_true", help="Overlay TW/DW/TL/DL text on each special square (staining reference)")
    return parser.parse_args()


def build_figure(args: argparse.Namespace) -> go.Figure:
    """Build the full board figure from a parsed/parsed-like args namespace.

    Shared by the CLI (`main`) and the Dash app, so both stay driven by the
    same set of options.
    """
    fig = go.Figure()
    frame = draw_board(
        fig, sheet=args.sheet, square=args.square, n=args.n, line=args.line,
        border=args.border, plywood_color=args.plywood_color,
        walnut_color=args.walnut_color, frame_color=args.frame_color,
        draw_frame=args.draw_frame, texture=args.texture, ppi=args.ppi, seed=args.seed,
    )

    if args.specials:
        stain_colors = {
            "TW": args.tw_color, "DW": args.dw_color,
            "TL": args.tl_color, "DL": args.dl_color,
        }
        grid_lo = frame + args.border
        draw_special_squares(
            fig, SCRABBLE_LAYOUT, square=args.square, n=args.n, line=args.line,
            grid_lo=grid_lo, stain_colors=stain_colors, alpha=args.stain_alpha,
        )
        if args.labels:
            draw_special_labels(
                fig, SCRABBLE_LAYOUT, square=args.square, n=args.n,
                grid_lo=grid_lo, stain_colors=stain_colors,
            )
        if args.legend:
            draw_legend(fig, stain_colors, alpha=args.stain_alpha)

    fig.update_xaxes(range=[0, args.sheet], visible=False, constrain="domain")
    fig.update_yaxes(range=[0, args.sheet], visible=False, scaleanchor="x", scaleratio=1)
    fig.update_layout(
        title=dict(
            text=(f"Scrabble board  •  {args.n}x{args.n} @ {args.square}\"  •  "
                  f"{args.sheet}\" sheet  •  border {args.border}\"  •  frame {frame:.2f}\""),
            font=dict(size=14),
        ),
        legend=dict(orientation="h", yanchor="top", y=-0.02, xanchor="center", x=0.5),
        margin=dict(l=10, r=10, t=50, b=10),
        width=800, height=800,
    )
    return fig


def main() -> None:
    args = parse_args()

    fig = build_figure(args)

    print(f"Grid span: {args.n * args.square}\"  |  Border: {args.border}\"  |  "
          f"Computed frame width: "
          f"{(args.sheet - args.n * args.square - 2 * args.border) / 2:.3f}\"  |  "
          f"Sheet: {args.sheet}\"")

    fig.show()


if __name__ == "__main__":
    main()
