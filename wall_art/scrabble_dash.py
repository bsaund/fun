#!/usr/bin/env python3
"""
Interactive Dash wrapper around scrabble.py.

Exposes the same options as the scrabble.py CLI flags as web controls
(sliders, checkboxes, color pickers) and re-renders the board figure from
scrabble.build_figure() on every change. The CLI in scrabble.py is untouched.

Run with:
    python scrabble_dash.py
"""

import argparse

import dash_daq as daq
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

import scrabble

app = Dash(__name__)
app.title = "Scrabble Board Wall Art"

_COLOR_DEFAULTS = {
    "plywood_color": scrabble.PLYWOOD_COLOR,
    "walnut_color": scrabble.WALNUT_COLOR,
    "frame_color": scrabble.FRAME_COLOR,
    "tw_color": scrabble.STAIN_COLORS["TW"],
    "dw_color": scrabble.STAIN_COLORS["DW"],
    "tl_color": scrabble.STAIN_COLORS["TL"],
    "dl_color": scrabble.STAIN_COLORS["DL"],
}


def _color_row(label: str, input_id: str, default: str):
    return html.Div(
        [
            daq.ColorPicker(id=input_id, label=label, value={"hex": default}, size=150),
            html.Button("Reset to default", id=f"{input_id}-reset", n_clicks=0,
                        style={"marginTop": "4px", "width": "150px"}),
        ],
        style={"marginBottom": "10px"},
    )


def _slider_row(label: str, input_id: str, min_, max_, step, default):
    return html.Div(
        [
            html.Label(f"{label}: ", style={"marginRight": "8px"}),
            html.Span(id=f"{input_id}-value", children=str(default)),
            dcc.Slider(
                id=input_id, min=min_, max=max_, step=step, value=default,
                tooltip={"placement": "bottom", "always_visible": False},
                marks=None,
            ),
        ],
        style={"marginBottom": "14px"},
    )


controls = html.Div(
    [
        html.H3("Geometry"),
        _slider_row("Sheet size (in)", "sheet", 12, 96, 1, 48.0),
        _slider_row("Square size (in)", "square", 0.5, 6, 0.25, 3.0),
        _slider_row("Grid N x N", "n", 5, 25, 1, 15),
        _slider_row("Dividing line width (in)", "line", 0.0, 1.0, 0.05, 0.25),
        _slider_row("Border width (in)", "border", 0.0, 6.0, 0.25, 1.0),

        html.Hr(),
        html.H3("Texture"),
        _slider_row("Texture PPI", "ppi", 5, 60, 5, 20.0),
        _slider_row("Seed", "seed", 0, 9999, 1, 1),

        html.Hr(),
        html.H3("Stain squares"),
        _slider_row("Stain opacity", "stain-alpha", 0.0, 1.0, 0.05, 0.65),

        html.Hr(),
        html.H3("Toggles"),
        dcc.Checklist(
            id="toggles",
            options=[
                {"label": " Draw outer frame", "value": "draw_frame"},
                {"label": " Wood grain texture", "value": "texture"},
                {"label": " Stain special squares", "value": "specials"},
                {"label": " Show stain legend", "value": "legend"},
                {"label": " Show TW/DW/TL/DL labels", "value": "labels"},
            ],
            value=["draw_frame", "texture", "specials", "legend"],
            labelStyle={"display": "block", "marginBottom": "4px"},
        ),

        html.Hr(),
        html.H3("Colors"),
        _color_row("Plywood", "plywood-color", _COLOR_DEFAULTS["plywood_color"]),
        _color_row("Walnut lines", "walnut-color", _COLOR_DEFAULTS["walnut_color"]),
        _color_row("Frame", "frame-color", _COLOR_DEFAULTS["frame_color"]),
        _color_row("Triple Word (TW)", "tw-color", _COLOR_DEFAULTS["tw_color"]),
        _color_row("Double Word (DW)", "dw-color", _COLOR_DEFAULTS["dw_color"]),
        _color_row("Triple Letter (TL)", "tl-color", _COLOR_DEFAULTS["tl_color"]),
        _color_row("Double Letter (DL)", "dl-color", _COLOR_DEFAULTS["dl_color"]),
    ],
    style={"width": "320px", "padding": "16px", "overflowY": "auto", "height": "100vh",
           "boxSizing": "border-box", "borderRight": "1px solid #ddd"},
)

# Colors debounce into this store (see clientside callback below) so dragging
# a color picker doesn't fire a full figure rebuild on every mouse-move event.
color_store = dcc.Store(id="color-store", data=dict(_COLOR_DEFAULTS))

layout_main = html.Div(
    [
        dcc.Graph(id="board-graph", style={"width": "100%", "height": "100%"},
                  config={"displaylogo": False}),
    ],
    style={"flex": "1", "padding": "16px", "height": "100vh", "boxSizing": "border-box"},
)

app.layout = html.Div(
    [controls, layout_main, color_store],
    style={"display": "flex", "flexDirection": "row"},
)


_SLIDER_IDS = ["sheet", "square", "n", "line", "border", "ppi", "seed", "stain-alpha"]
_COLOR_PICKER_IDS = ["plywood-color", "walnut-color", "frame-color",
                     "tw-color", "dw-color", "tl-color", "dl-color"]
_COLOR_PICKER_KEYS = ["plywood_color", "walnut_color", "frame_color",
                      "tw_color", "dw_color", "tl_color", "dl_color"]


@app.callback(
    [Output(f"{sid}-value", "children") for sid in _SLIDER_IDS],
    [Input(sid, "value") for sid in _SLIDER_IDS],
)
def _update_slider_labels(*values):
    return [str(v) for v in values]


def _register_reset_callback(picker_id: str, default_hex: str) -> None:
    @app.callback(
        Output(picker_id, "value"),
        Input(f"{picker_id}-reset", "n_clicks"),
        prevent_initial_call=True,
    )
    def _reset(_n_clicks, default_hex=default_hex):
        return {"hex": default_hex}


for _picker_id, _key in zip(_COLOR_PICKER_IDS, _COLOR_PICKER_KEYS):
    _register_reset_callback(_picker_id, _COLOR_DEFAULTS[_key])


# Color pickers fire onChange continuously while dragging. Debounce them
# client-side into `color-store`, which is what actually drives a re-render,
# so a drag doesn't queue up a full figure rebuild per mouse-move event.
app.clientside_callback(
    """
    function(plywood, walnut, frame, tw, dw, tl, dl) {
        if (window.__scrabbleColorTimer) {
            clearTimeout(window.__scrabbleColorTimer);
        }
        const colors = {
            plywood_color: plywood.hex, walnut_color: walnut.hex, frame_color: frame.hex,
            tw_color: tw.hex, dw_color: dw.hex, tl_color: tl.hex, dl_color: dl.hex,
        };
        window.__scrabbleColorTimer = setTimeout(function() {
            window.dash_clientside.set_props("color-store", {data: colors});
        }, 250);
        return window.dash_clientside.no_update;
    }
    """,
    Output("color-store", "data", allow_duplicate=True),
    [Input(cid, "value") for cid in _COLOR_PICKER_IDS],
    prevent_initial_call=True,
)


def _error_figure(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=message, showarrow=False, font=dict(size=16, color="crimson"))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(width=800, height=800, plot_bgcolor="white", paper_bgcolor="white")
    return fig


@app.callback(
    Output("board-graph", "figure"),
    [
        Input("sheet", "value"),
        Input("square", "value"),
        Input("n", "value"),
        Input("line", "value"),
        Input("border", "value"),
        Input("ppi", "value"),
        Input("seed", "value"),
        Input("stain-alpha", "value"),
        Input("toggles", "value"),
        Input("color-store", "data"),
    ],
)
def _render_board(sheet, square, n, line, border, ppi, seed, stain_alpha, toggles, colors):
    args = argparse.Namespace(
        sheet=sheet, square=square, n=int(n), line=line, border=border,
        draw_frame="draw_frame" in toggles,
        plywood_color=colors["plywood_color"], walnut_color=colors["walnut_color"],
        frame_color=colors["frame_color"],
        texture="texture" in toggles, ppi=ppi, seed=int(seed),
        specials="specials" in toggles, stain_alpha=stain_alpha,
        tw_color=colors["tw_color"], dw_color=colors["dw_color"],
        tl_color=colors["tl_color"], dl_color=colors["dl_color"],
        legend="legend" in toggles, labels="labels" in toggles,
    )

    try:
        return scrabble.build_figure(args)
    except ValueError as exc:
        return _error_figure(str(exc))


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
