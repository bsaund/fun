#!/usr/bin/env python3
"""
Generate laser-cut files for the Scrabble wall-art tiles.

Each tile is a square of acrylic, sized slightly smaller than the 2.75"
grid spacing on the board (so it drops into a grid square with clearance),
with slightly rounded corners and the letter's Scrabble point value in the
bottom-right corner, built from three stacked layers:
  - bottom: solid black acrylic
  - middle: copper
  - top: black acrylic, with the letter marked by either cutting all the
    way through (so the copper shows through) or laser engraving into the
    surface (--technique engrave), depending on --technique.

--technique cut (default): the letter's shape is cut all the way through
the top layer. Letters with an interior counter (A, B, D, O, P, Q, R, ...)
will free a small loose island where the counter is cut out -- that's
expected, not a bug. Keep the islands and glue each one back into the
middle of its letter after assembly, so the counter reads as background
(black) instead of copper, matching normal typography.

--technique engrave: no material is removed all the way through, so
there's no loose-island problem, but nothing shows through from the
copper layer either -- the letter just reads as a frosted/marked area on
the top layer's surface.

File format is chosen per technique, since Ponoko needs different things
from each:
  - cut     -> DXF, blue stroke (RGB 0,0,255) -- Ponoko's convention for
              cut geometry, and DXF is their preferred format generally.
  - engrave -> SVG, gray fill (RGB 128,128,128) -- Ponoko's convention
              for area/raster engraving. Critically, a letter's counter
              (the hole in "O") is written as a genuine SVG compound path
              (one <path> with multiple subpaths + fill-rule="evenodd"),
              which is how Ponoko says shapes-with-holes must be built.
              DXF's LWPOLYLINE has no equivalent of a compound path, and
              Ponoko's area-engrave fills every closed path it's given
              independently (no hole/nesting detection at all) -- so a
              DXF version of this either has the counter filled in solid,
              or needs an ugly "keyhole" zero-width slit hack to fake a
              single simple path. SVG avoids that entirely.

Three modes:
  test    Generate a single letter, to check fit/size before committing
          to a bigger run.
  sample  Nest a 3x3 square of 9 varied tiles (widest/narrowest letters,
          letters with counters, the most common letter, a two-digit
          point value, and a blank) -- a small first order to dial in the
          real material/settings before committing to the full run.
  all     Nest every top-layer tile needed for a full 100-tile Scrabble
          set (standard English letter distribution, incl. 2 blanks) onto
          one sheet layout (or --num-sheets N to split it across N sheet
          files), plus a single blank-square part for the copper/black
          backer layers.

All output is 1:1 scale in inches, with only the flat geometry itself --
no extra text or annotation. The copper/black backer squares are always
plain, unmarked squares regardless of --technique, so they're always DXF
(there's nothing to engrave on them).
"""

import argparse
import csv
import math
import pathlib

import ezdxf
import numpy as np
from ezdxf.math import bulge_to_arc
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath

# Standard English Scrabble tile distribution (100 tiles, incl. 2 blanks).
# "" (empty string) stands for the blank tile.
LETTER_COUNTS = {
    "A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2,
    "I": 9, "J": 1, "K": 1, "L": 4, "M": 2, "N": 6, "O": 8, "P": 2,
    "Q": 1, "R": 6, "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1,
    "Y": 2, "Z": 1, "": 2,
}

# Standard English Scrabble point values. Blanks carry no printed value.
POINT_VALUES = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4,
    "I": 1, "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3,
    "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8,
    "Y": 4, "Z": 10,
}

DEFAULT_TILE_SIZE = 2.65        # inches. Grid spacing is 2.75".
DEFAULT_LETTER_HEIGHT = 1.55    # inches
DEFAULT_LETTER_OFFSET_Y = 0.12  # inches, shifts the letter up to make room for the point value
DEFAULT_POINT_VALUE_HEIGHT = 0.38  # inches
DEFAULT_POINT_MARGIN = 0.2      # inches, gap from tile edge to the point-value digits
DEFAULT_CORNER_RADIUS = 0.15    # inches
DEFAULT_FONT_FAMILY = "DejaVu Sans"
DEFAULT_FONT_WEIGHT = "bold"
DEFAULT_SPACING = 0.1           # inches, gap between nested parts on a sheet

# SendCutSend's largest acrylic part is ~30" x 44"; stay a bit inside that
# so nested sheets are never rejected as oversized.
DEFAULT_MAX_SHEET_WIDTH = 29.0
DEFAULT_MAX_SHEET_HEIGHT = 43.0

# A varied 9-tile sample for a small first test order, alphabetical and
# nested 3x3:
#   A (common, one counter)   B (two counters)         E (most common, x12)
#   I (narrowest letter)      O (one round counter)    Q (two-digit point value, 10)
#   S (curvy, common)         W (widest letter)        "" (blank)
SAMPLE_LETTERS = ["A", "B", "E", "I", "O", "Q", "S", "W", ""]

# Arc bulge for a 90-degree corner fillet (tan(90/4)).
_QUARTER_ARC_BULGE = math.tan(math.radians(22.5))


def rounded_square_points(half: float, radius: float) -> list[tuple[float, float, float]]:
    """
    (x, y, bulge) vertices for a `2*half`-side square centered on (0, 0)
    with corners filleted to `radius`, traversed counterclockwise starting
    at the bottom edge. Passed straight to `add_lwpolyline(..., format="xyb")`.
    """
    if radius <= 0:
        return [(-half, -half, 0.0), (half, -half, 0.0), (half, half, 0.0), (-half, half, 0.0)]
    r = radius
    return [
        (-half + r, -half, 0.0),
        (half - r, -half, _QUARTER_ARC_BULGE),
        (half, -half + r, 0.0),
        (half, half - r, _QUARTER_ARC_BULGE),
        (half - r, half, 0.0),
        (-half + r, half, _QUARTER_ARC_BULGE),
        (-half, half - r, 0.0),
        (-half, -half + r, _QUARTER_ARC_BULGE),
    ]


def text_glyph_rings(text: str, height: float, font_family: str,
                      font_weight: str) -> tuple[list[np.ndarray], float]:
    """
    Return `text`'s outline as a list of closed polygon rings, each an
    (N, 2) array of inch coordinates, centered on (0, 0) and scaled so it
    stands `height` tall -- plus the resulting overall width, for
    alignment. Works for a single letter or a multi-digit number; matplotlib
    lays out and kerns multiple glyphs on its own.

    Includes both outer strokes and inner counters (e.g. the hole in "O")
    as separate rings -- a laser just cuts every closed ring it's given, so
    no boolean subtraction against the tile square is needed here; the
    tile outline and the glyph rings are simply cut as independent paths.
    """
    if not text:
        return [], 0.0
    prop = FontProperties(family=font_family, weight=font_weight)
    path = TextPath((0, 0), text, size=100, prop=prop)  # 100 = arbitrary reference size
    rings = path.to_polygons()

    all_pts = np.concatenate(rings, axis=0)
    y_min, y_max = all_pts[:, 1].min(), all_pts[:, 1].max()
    x_min, x_max = all_pts[:, 0].min(), all_pts[:, 0].max()
    scale = height / (y_max - y_min)
    cx, cy = (x_min + x_max) / 2, (y_min + y_max) / 2

    centered = [(ring - [cx, cy]) * scale for ring in rings]
    return centered, (x_max - x_min) * scale


def tile_geometry(letter: str, tile_size: float, letter_height: float, letter_offset_y: float,
                   point_value_height: float, point_margin: float, corner_radius: float,
                   font_family: str, font_weight: str
                   ) -> tuple[list[tuple[float, float, float]], list[np.ndarray]]:
    """
    One tile's geometry, centered on (0, 0): (rounded-square points, cutout
    rings). Cutout rings cover the letter itself -- shifted up by
    `letter_offset_y` to leave room below it -- plus its Scrabble point
    value, right- and bottom-aligned into the corner that frees up. Blank
    tiles (`letter == ""`) get no cutouts at all.
    """
    half = tile_size / 2
    square = rounded_square_points(half, corner_radius)
    if not letter:
        return square, []

    letter_rings, _ = text_glyph_rings(letter, letter_height, font_family, font_weight)
    rings = [ring + [0.0, letter_offset_y] for ring in letter_rings]

    point_rings, point_width = text_glyph_rings(str(POINT_VALUES[letter]), point_value_height,
                                                 font_family, font_weight)
    px = (half - point_margin) - point_width / 2
    py = (-half + point_margin) + point_value_height / 2
    rings += [ring + [px, py] for ring in point_rings]

    return square, rings


def new_doc() -> ezdxf.document.Drawing:
    """DXF is only ever used for cut geometry; blue (RGB 0,0,255) is Ponoko's convention for it."""
    doc = ezdxf.new("R2010")
    doc.units = ezdxf.units.IN
    doc.layers.add("CUT", color=5, true_color=ezdxf.rgb2int((0, 0, 255)))
    return doc


def add_tile(msp, square: list[tuple[float, float, float]], cutout_rings: list[np.ndarray],
             offset: tuple[float, float] = (0.0, 0.0)) -> None:
    """Add one tile's cut geometry: the tile outline plus, if any, the letter/point-value outlines."""
    ox, oy = offset
    pts = [(x + ox, y + oy, b) for x, y, b in square]
    msp.add_lwpolyline(pts, format="xyb", close=True, dxfattribs={"layer": "CUT"})
    for ring in cutout_rings:
        pts = [(x + ox, y + oy) for x, y in ring]
        msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "CUT"})


def flatten_bulge_path(points_with_bulge: list[tuple[float, float, float]],
                        segments_per_arc: int = 8) -> list[tuple[float, float]]:
    """
    Expand a closed (x, y, bulge) polyline (see `rounded_square_points`)
    into plain (x, y) points, with arcs flattened to short line segments
    -- for output formats without native bulge/arc support (SVG).
    """
    pts = []
    n = len(points_with_bulge)
    for i in range(n):
        x0, y0, bulge = points_with_bulge[i]
        x1, y1, _ = points_with_bulge[(i + 1) % n]
        pts.append((x0, y0))
        if bulge:
            center, start_angle, end_angle, radius = bulge_to_arc((x0, y0), (x1, y1), bulge)
            if end_angle < start_angle:  # bulge_to_arc always returns a CCW arc, but the raw
                end_angle += 2 * math.pi  # angles wrap at +-180 deg, so this can read backwards
            for k in range(1, segments_per_arc):
                t = start_angle + (end_angle - start_angle) * k / segments_per_arc
                pts.append((center.x + radius * math.cos(t), center.y + radius * math.sin(t)))
    return pts


def _svg_path_d(rings: list) -> str:
    """SVG compound path 'd' attribute: one "M ... Z" subpath per ring, all in one <path>."""
    return " ".join("M " + " L ".join(f"{x:.4f},{y:.4f}" for x, y in ring) + " Z" for ring in rings)


def build_svg(tiles: list[tuple[list[tuple[float, float, float]], list[np.ndarray]]],
              cols: int, rows: int, tile_size: float, spacing: float) -> tuple[str, float, float]:
    """
    Build one SVG sheet: a blue-stroked compound path for every tile
    outline (cut), and a single gray-filled compound path with
    fill-rule="evenodd" for every tile's letter + point value (area
    engrave). Because it's a genuine compound path -- multiple subpaths in
    one <path>, not separate independent shapes -- a letter's counter
    (the hole in "O") comes out as a clean hole via the fill rule, with no
    bridge/seam hack needed, unlike DXF's LWPOLYLINE.
    """
    pitch = tile_size + spacing
    half = tile_size / 2
    sheet_w = cols * tile_size + (cols - 1) * spacing
    sheet_h = rows * tile_size + (rows - 1) * spacing
    cut_rings, engrave_rings = [], []
    for i, (square, cutout_rings) in enumerate(tiles):
        col, row = i % cols, i // cols
        # tile_geometry centers each tile on (0, 0); shift by +half so tile
        # (0, 0) lands in [0, tile_size] -- SVG's viewBox clips to
        # [0, sheet_w] x [0, sheet_h], unlike a DXF viewer, which just
        # auto-fits to whatever extents exist, negative coordinates included.
        ox, oy = col * pitch + half, row * pitch + half
        cut_rings.append([(x + ox, y + oy) for x, y in flatten_bulge_path(square)])
        engrave_rings += [ring + [ox, oy] for ring in cutout_rings]

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{sheet_w}in" height="{sheet_h}in" '
        f'viewBox="0 0 {sheet_w:.4f} {sheet_h:.4f}">',
        f'<g transform="translate(0,{sheet_h:.4f}) scale(1,-1)">',
    ]
    if engrave_rings:
        svg.append(f'<path d="{_svg_path_d(engrave_rings)}" fill="rgb(128,128,128)" '
                    f'fill-rule="evenodd" stroke="none"/>')
    svg.append(f'<path d="{_svg_path_d(cut_rings)}" fill="none" stroke="rgb(0,0,255)" stroke-width="0.01"/>')
    svg += ["</g>", "</svg>"]
    return "\n".join(svg), sheet_w, sheet_h


def sanitize_filename(letter: str, ext: str) -> str:
    return f"tile_{letter}.{ext}" if letter else f"tile_blank.{ext}"


def cmd_test(args: argparse.Namespace) -> None:
    out_dir = pathlib.Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    square, cutout_rings = tile_geometry(args.letter, args.tile_size, args.letter_height,
                                          args.letter_offset_y, args.point_value_height,
                                          args.point_margin, args.corner_radius,
                                          args.font_family, args.font_weight)
    if args.technique == "cut":
        doc = new_doc()
        add_tile(doc.modelspace(), square, cutout_rings)
        path = out_dir / sanitize_filename(args.letter, "dxf")
        doc.saveas(path)
    else:
        svg, _, _ = build_svg([(square, cutout_rings)], 1, 1, args.tile_size, args.spacing)
        path = out_dir / sanitize_filename(args.letter, "svg")
        path.write_text(svg)
    print(f"Wrote test tile for {args.letter!r} ({args.technique}) -> {path}")
    print(f"Tile size: {args.tile_size}\"  |  Letter height: {args.letter_height}\"  |  "
          f"Corner radius: {args.corner_radius}\"  |  Point value height: {args.point_value_height}\"")
    if args.technique == "cut":
        print("Cut this one first and check fit against a 2.75\" grid square before running --mode all.")
    else:
        print("Engrave this one first to check depth/legibility before running --mode all.")


def square_grid(n: int) -> tuple[int, int]:
    """Choose (cols, rows) for `n` tiles as close to a square as possible."""
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    return cols, rows


def max_sheet_grid(tile_size: float, spacing: float, max_width: float,
                    max_height: float) -> tuple[int, int]:
    """The most (cols, rows) of tiles that fit within a max_width x max_height sheet."""
    pitch = tile_size + spacing
    cols = max(1, int((max_width + spacing) // pitch))
    rows = max(1, int((max_height + spacing) // pitch))
    return cols, rows


def fit_grid(n: int, max_cols: int, max_rows: int) -> tuple[int, int]:
    """
    Choose (cols, rows) for `n` tiles (assumed <= max_cols * max_rows) that's
    as close to square as possible while staying within max_cols/max_rows --
    e.g. a small last/remainder sheet gets a compact layout instead of being
    stretched across the sheet's full width.
    """
    cols, rows = square_grid(n)
    if rows > max_rows:
        rows = max_rows
        cols = math.ceil(n / rows)
    if cols > max_cols:
        cols = max_cols
        rows = math.ceil(n / cols)
    return cols, rows


def nest_sheet(tiles: list[tuple[list[tuple[float, float, float]], list[np.ndarray]]],
               cols: int, rows: int, tile_size: float, spacing: float
               ) -> tuple[ezdxf.document.Drawing, float, float]:
    """Nest `tiles` (square, cutout_rings pairs) into a `cols`x`rows` grid of DXF cut geometry."""
    pitch = tile_size + spacing
    doc = new_doc()
    msp = doc.modelspace()
    for i, (square, cutout_rings) in enumerate(tiles):
        col, row = i % cols, i // cols
        add_tile(msp, square, cutout_rings, offset=(col * pitch, row * pitch))
    sheet_w = cols * tile_size + (cols - 1) * spacing
    sheet_h = rows * tile_size + (rows - 1) * spacing
    return doc, sheet_w, sheet_h


def write_sheet(tiles: list[tuple[list[tuple[float, float, float]], list[np.ndarray]]],
                 cols: int, rows: int, tile_size: float, spacing: float, technique: str,
                 out_dir: pathlib.Path, basename: str) -> tuple[pathlib.Path, float, float]:
    """Write `tiles` nested onto one sheet, as DXF (technique=cut) or SVG (technique=engrave)."""
    if technique == "cut":
        doc, sheet_w, sheet_h = nest_sheet(tiles, cols, rows, tile_size, spacing)
        path = out_dir / f"{basename}.dxf"
        doc.saveas(path)
    else:
        svg, sheet_w, sheet_h = build_svg(tiles, cols, rows, tile_size, spacing)
        path = out_dir / f"{basename}.svg"
        path.write_text(svg)
    return path, sheet_w, sheet_h


def cmd_sample(args: argparse.Namespace) -> None:
    out_dir = pathlib.Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    tiles = [tile_geometry(letter, args.tile_size, args.letter_height, args.letter_offset_y,
                            args.point_value_height, args.point_margin, args.corner_radius,
                            args.font_family, args.font_weight)
             for letter in SAMPLE_LETTERS]

    cols, rows = square_grid(len(tiles))
    path, sheet_w, sheet_h = write_sheet(tiles, cols, rows, args.tile_size, args.spacing,
                                          args.technique, out_dir, "sheet_sample")

    print(f"Wrote {len(tiles)} sample tiles ({', '.join(l or 'blank' for l in SAMPLE_LETTERS)}) "
          f"nested {cols}x{rows} ({sheet_w:.2f}\" x {sheet_h:.2f}\") -> {path}")
    print(f"Order this small batch first ({args.technique}) to check fit/legibility on real "
          "material before committing to --mode all.")


def build_tile_list(counts: dict[str, int], args: argparse.Namespace) -> list:
    """Expand a {letter: count} distribution into a flat list of (square, cutout_rings) tiles."""
    tiles = []
    for letter in sorted(l for l, n in counts.items() if l and n > 0):
        square, cutout_rings = tile_geometry(letter, args.tile_size, args.letter_height,
                                              args.letter_offset_y, args.point_value_height,
                                              args.point_margin, args.corner_radius,
                                              args.font_family, args.font_weight)
        tiles += [(square, cutout_rings)] * counts[letter]
    if counts.get("", 0) > 0:
        blank_square, _ = tile_geometry("", args.tile_size, args.letter_height, args.letter_offset_y,
                                         args.point_value_height, args.point_margin,
                                         args.corner_radius, args.font_family, args.font_weight)
        tiles += [(blank_square, [])] * counts[""]
    return tiles


def cmd_all(args: argparse.Namespace) -> None:
    out_dir = pathlib.Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    max_cols, max_rows = max_sheet_grid(args.tile_size, args.spacing,
                                         args.max_sheet_width, args.max_sheet_height)
    letter_desc = "letter cutouts, full thickness" if args.technique == "cut" else "letters engraved (area fill)"
    manifest_rows = []

    # --sample-sheet carves the same varied 9-tile selection used by
    # --mode sample out of the full distribution -- one of each of those
    # letters comes off the main count -- and writes it as its own sheet,
    # meant to be ordered (and checked) first, before committing to the
    # rest. It's still part of the same 100-tile set, not extra tiles.
    counts = dict(LETTER_COUNTS)
    if args.sample_sheet:
        sample_tiles = [tile_geometry(letter, args.tile_size, args.letter_height, args.letter_offset_y,
                                       args.point_value_height, args.point_margin, args.corner_radius,
                                       args.font_family, args.font_weight)
                         for letter in SAMPLE_LETTERS]
        for letter in SAMPLE_LETTERS:
            counts[letter] -= 1
        cols, rows = fit_grid(len(sample_tiles), max_cols, max_rows)
        path, sheet_w, sheet_h = write_sheet(sample_tiles, cols, rows, args.tile_size, args.spacing,
                                              args.technique, out_dir, "sheet_sample")
        print(f"Wrote {len(sample_tiles)} sample tiles nested {cols}x{rows} "
              f"({sheet_w:.2f}\" x {sheet_h:.2f}\") -> {path}  [order this one first]")
        manifest_rows.append({
            "file": path.name, "part": f"{len(sample_tiles)} nested sample tiles (order first)",
            "quantity": 1, "layer": f"top ({letter_desc})", "material": "black acrylic",
        })

    # Every remaining top-layer tile (letters + blanks), in the correct
    # quantity, split across sheets that fit within max_sheet_width x
    # max_sheet_height -- both dimensions, not just width. --num-sheets
    # forces more (smaller) sheets than the auto-computed minimum, e.g.
    # for easier handling, but never fewer than fit.
    tiles = build_tile_list(counts, args)
    capacity = max_cols * max_rows
    min_sheets = math.ceil(len(tiles) / capacity)
    n_sheets = max(min_sheets, args.num_sheets)
    if args.num_sheets < min_sheets:
        print(f"Note: --num-sheets {args.num_sheets} is too few to fit {len(tiles)} tiles at "
              f"{max_cols}x{max_rows}/sheet ({capacity} tiles); using {n_sheets} sheets instead.")
    chunk_size = math.ceil(len(tiles) / n_sheets)
    chunks = [tiles[i:i + chunk_size] for i in range(0, len(tiles), chunk_size)]

    for idx, chunk in enumerate(chunks, start=1):
        cols, rows = fit_grid(len(chunk), max_cols, max_rows)
        basename = "sheet_letters" if n_sheets == 1 else f"sheet_letters_{idx}"
        path, sheet_w, sheet_h = write_sheet(chunk, cols, rows, args.tile_size, args.spacing,
                                              args.technique, out_dir, basename)
        print(f"Wrote {len(chunk)} tiles nested {cols}x{rows} onto sheet {idx}/{n_sheets} "
              f"({sheet_w:.2f}\" x {sheet_h:.2f}\") -> {path}")
        manifest_rows.append({
            "file": path.name, "part": f"{len(chunk)} nested letter/blank tiles", "quantity": 1,
            "layer": f"top ({letter_desc})", "material": "black acrylic",
        })

    # Backer square (copper middle layer + solid black bottom layer): plain,
    # unmarked, and always DXF/cut regardless of --technique -- there's
    # nothing to engrave on a backer. One repeated shape, so a single
    # un-nested part is enough -- set quantity per material when ordering.
    blank_square, _ = tile_geometry("", args.tile_size, args.letter_height, args.letter_offset_y,
                                     args.point_value_height, args.point_margin,
                                     args.corner_radius, args.font_family, args.font_weight)
    blank_doc = new_doc()
    add_tile(blank_doc.modelspace(), blank_square, [])
    blank_path = out_dir / "tile_blank.dxf"
    blank_doc.saveas(blank_path)

    manifest_rows += [
        {"file": blank_path.name, "part": "backer square", "quantity": 100,
         "layer": "middle", "material": "copper"},
        {"file": blank_path.name, "part": "backer square", "quantity": 100,
         "layer": "bottom", "material": "black acrylic"},
    ]
    manifest_path = out_dir / "manifest.csv"
    with open(manifest_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "part", "quantity", "layer", "material"])
        writer.writeheader()
        writer.writerows(manifest_rows)

    print(f"Wrote tile_blank.dxf + manifest.csv -> {out_dir}/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate laser-cut/engrave files for the Scrabble wall-art tiles.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--mode", choices=["test", "sample", "all"], default="test",
                         help="'test' generates one letter; 'sample' nests a 3x3 varied test batch; "
                              "'all' nests the full tile set")
    parser.add_argument("--technique", choices=["cut", "engrave"], default="cut",
                         help="'cut' cuts the letter all the way through, as DXF; "
                              "'engrave' area-engraves it into the surface, as SVG")
    parser.add_argument("--letter", default="A",
                         help="Letter to generate in --mode test (use '' for a blank tile)")
    parser.add_argument("--output-dir", default="tile_cuts", help="Directory to write output files into")
    parser.add_argument("--tile-size", type=float, default=DEFAULT_TILE_SIZE,
                         help="Tile side length (inches). Grid spacing is 2.75\".")
    parser.add_argument("--letter-height", type=float, default=DEFAULT_LETTER_HEIGHT,
                         help="Target letter height (inches)")
    parser.add_argument("--letter-offset-y", type=float, default=DEFAULT_LETTER_OFFSET_Y,
                         help="How far up to shift the letter, to leave room for the point value (inches)")
    parser.add_argument("--point-value-height", type=float, default=DEFAULT_POINT_VALUE_HEIGHT,
                         help="Height of the point-value digits in the corner (inches)")
    parser.add_argument("--point-margin", type=float, default=DEFAULT_POINT_MARGIN,
                         help="Gap from the tile edge to the point-value digits (inches)")
    parser.add_argument("--corner-radius", type=float, default=DEFAULT_CORNER_RADIUS,
                         help="Tile corner fillet radius (inches); 0 for sharp corners")
    parser.add_argument("--font-family", default=DEFAULT_FONT_FAMILY,
                         help="Font family (matplotlib font lookup, e.g. 'DejaVu Sans')")
    parser.add_argument("--font-weight", default=DEFAULT_FONT_WEIGHT,
                         help="Font weight, e.g. 'bold' or 'normal'")
    parser.add_argument("--spacing", type=float, default=DEFAULT_SPACING,
                         help="Gap between nested parts on the sheet, --mode all/sample (inches)")
    parser.add_argument("--num-sheets", type=int, default=1,
                         help="Force at least N sheet files, --mode all (auto-computed minimum "
                              "to fit max-sheet-width/height is used if this is too small)")
    parser.add_argument("--sample-sheet", action="store_true",
                         help="--mode all: carve the varied 9-tile sample selection (see --mode "
                              "sample) out as its own first sheet -- order it alone to check the "
                              "look before committing to the rest")
    parser.add_argument("--max-sheet-width", type=float, default=DEFAULT_MAX_SHEET_WIDTH,
                         help="Max sheet width per sheet, --mode all (inches)")
    parser.add_argument("--max-sheet-height", type=float, default=DEFAULT_MAX_SHEET_HEIGHT,
                         help="Max sheet height per sheet, --mode all (inches)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.mode == "test":
        cmd_test(args)
    elif args.mode == "sample":
        cmd_sample(args)
    else:
        cmd_all(args)


if __name__ == "__main__":
    main()
