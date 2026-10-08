"""Vega-Lite specs for the evaluation figures of the thesis (Figures 9 to 12 and 18 to 23).

Each public function is a `source` of a `plot {backend=vega}` block in this folder. The data is a
one-time copy in data/thesis-figures/ at the root of the defense project (see its README.md); the
encodings follow the thesis: same colours, solid and dashed lines, same baselines and y ranges.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "thesis-figures"


def _rows(path: Path) -> list[list[float]]:
    with open(path, newline="", encoding="utf-8") as f:
        return [[float(v) for v in row] for row in csv.reader(f) if row]


def _x_axis(limits: list[int], zero_label: str) -> dict:
    return {
        "field": "limit", "type": "quantitative", "title": "Version limit",
        "scale": {"domain": [min(limits), max(limits)], "nice": False, "zero": False},
        # labelOverlap: keep 1, 2, 3... beside the zero label, which sits left of its tick
        "axis": {"values": limits, "grid": False, "labelOverlap": False, "labelFontSize": 14,
                 "labelExpr": f"datum.value == 0 ? '{zero_label}' : datum.label",
                 "labelAlign": {"expr": "datum.value == 0 ? 'right' : 'center'"}},
    }


def _y_axis(title: str, domain: list[float], fmt: str) -> dict:
    return {
        "field": "value", "type": "quantitative", "title": title,
        "scale": {"domain": domain, "nice": False, "zero": domain[0] == 0},
        "axis": {"format": fmt, "tickCount": 6},
    }


def _legend(orient: str) -> dict:
    return {"title": None, "orient": orient, "offset": 6, "labelFontSize": 15, "symbolStrokeWidth": 2.5,
            "symbolSize": 260, "rowPadding": 2}


def _chart(values, x, y, color, dash, legend_orient, title=None) -> dict:
    """Lines with points, one series per (color, dash) pair, and a tooltip on every point."""
    tooltip = [
        {"field": "limit", "type": "quantitative", "title": "version limit"},
        {"field": color["field"], "type": "nominal"},
        {"field": dash["field"], "type": "nominal"},
        {"field": "value", "type": "quantitative", "format": ".3f"},
    ]
    legends = legend_orient is not None
    color = {**color, "type": "nominal", "legend": _legend(legend_orient) if legends else None}
    dash = {**dash, "type": "nominal", "legend": _legend(legend_orient) if legends else None}
    spec = {
        "data": {"values": values},
        "encoding": {"x": x, "y": y, "color": color},
        "layer": [
            {"mark": {"type": "line", "strokeWidth": 2.5}, "encoding": {"strokeDash": dash}},
            {"mark": {"type": "point", "filled": True, "size": 55},
             "encoding": {"shape": {**dash, "scale": {"domain": dash["scale"]["domain"],
                                                      "range": ["circle", "square"]},
                                    "legend": None},
                          "tooltip": tooltip}},
        ],
    }
    if title:
        spec["title"] = {"text": title, "fontSize": 18, "fontWeight": 500, "anchor": "middle"}
    return spec


# ---------------------------------------------------------------------------------- SBBV (Ch. 3)

# Columns of data/thesis-figures/sbbv/*.csv after the version limit (see sbbv-plot/scripts/plot.gp).
SBBV_SERIES = [("Gambit", "macro"), ("Gambit", "micro"), ("Bigloo", "macro"), ("Bigloo", "micro")]
SBBV_COLORS = {"domain": ["Gambit", "Bigloo"], "range": ["#0072B2", "#D55E00"]}
SUITE_DASH = {"domain": ["macro", "micro"], "range": [[1, 0], [7, 4]]}


def _sbbv(name: str, ytitle: str, domain: list[float] | None, fmt: str, legend_orient: str) -> dict:
    rows = _rows(DATA / "sbbv" / f"{name}.csv")
    values = [{"limit": int(r[0]), "compiler": c, "suite": s, "value": v}
              for r in rows for (c, s), v in zip(SBBV_SERIES, r[1:])]
    if domain is None:
        domain = [0, _ceiling(max(v["value"] for v in values))]
    limits = [int(r[0]) for r in rows]
    return _chart(values, _x_axis(limits, "No BBV"), _y_axis(ytitle, domain, fmt),
                  {"field": "compiler", "scale": SBBV_COLORS}, {"field": "suite", "scale": SUITE_DASH},
                  legend_orient)


def sbbv_checks():
    """Thesis Figure 9: run-time checks relative to compilation without any optimization."""
    return _sbbv("checks", "Relative dynamic checks", [0, 1], ".1f", "top-right")


def sbbv_size():
    """Thesis Figure 10: program size relative to compilation without SBBV."""
    return _sbbv("size", "Relative program size", None, "~g", "top-left")


def sbbv_time():
    """Thesis Figure 11: execution time relative to compilation without SBBV (y axis from 0.6)."""
    return _sbbv("time", "Relative execution time", [0.6, 1.0], ".2f", "bottom-right")


def sbbv_compile_time():
    """Thesis Figure 12: compile time relative to compilation without SBBV."""
    return _sbbv("compile-time", "Relative compile time", None, "~g", "top-left")


# ---------------------------------------------------------------------------- Lambda Versioning (Ch. 4)

HEURISTICS = ["random", "similarity", "arithmetic"]
HEURISTIC_COLORS = {"domain": HEURISTICS, "range": ["#FFB000", "#DC267F", "#648FFF"]}
ALGO_DASH = {"domain": ["ΛV", "SBBV"], "range": [[1, 0], [7, 4]]}
# Column of each metric in data/thesis-figures/lv/geomeans.*.csv (written by aggregate-benchmark.sh).
LV_COLUMNS = {"typechecks": 1, "compile-time": 2, "versions": 4}


def _lv_series(metric: str, kind: str, variant: str, algo: str, first: int) -> list[dict]:
    col = LV_COLUMNS[metric]
    out = []
    for h in HEURISTICS:
        suffix = f"{h}.{variant}." if variant else f"{h}."
        for r in _rows(DATA / "lv" / f"geomeans.{suffix}{kind}.csv"):
            if r[0] >= first and r[col] > 0:  # -1: no value (aggregate-benchmark.sh)
                out.append({"limit": int(r[0]), "heuristic": h, "algorithm": algo, "value": r[col]})
    return out


def _ceiling(m: float) -> float:
    if m <= 1:
        return 1
    step = 1 if m <= 10 else 5
    return step * math.ceil(m / step)


def _lv(metric: str, kind: str, panel: str, ytitle: str, sbbv_in_hyper: bool) -> dict:
    """One panel of a thesis figure; both panels of a figure share their y range."""
    first = 0 if metric == "typechecks" else 1
    inlined = _lv_series(metric, kind, "inline-rts", "ΛV", first)
    hyper = _lv_series(metric, kind, "", "ΛV", first)
    sbbv = _lv_series(metric, kind, "sbbv", "SBBV", first)
    if metric == "typechecks":
        domain, fmt = [0, 1], ".1f"
    else:
        domain, fmt = [0, _ceiling(max(v["value"] for v in inlined + hyper + sbbv))], "~g"
    if panel == "inlined":
        values, title, legend = sbbv + inlined, "Inlined operators", "top-right" if first == 0 else "top-left"
    else:
        values, title, legend = (sbbv if sbbv_in_hyper else []) + hyper, "Hyperfunction operators", None
    limits = list(range(first, 11))
    return _chart(values, _x_axis(limits, "No ΛV"), _y_axis(ytitle, domain, fmt),
                  {"field": "heuristic", "scale": HEURISTIC_COLORS}, {"field": "algorithm", "scale": ALGO_DASH},
                  legend, title)


# Thesis Figures 18 and 19: type checks relative to compilation without ΛV/SBBV. As in the thesis,
# the hyperfunction panel leaves SBBV out (SBBV always uses inlined operators).
def lv_typechecks_micro_inlined():
    return _lv("typechecks", "micro", "inlined", "Relative type checks", False)


def lv_typechecks_micro_hyperfunction():
    return _lv("typechecks", "micro", "hyperfunction", "Relative type checks", False)


def lv_typechecks_macro_inlined():
    return _lv("typechecks", "macro", "inlined", "Relative type checks", False)


def lv_typechecks_macro_hyperfunction():
    return _lv("typechecks", "macro", "hyperfunction", "Relative type checks", False)


# Thesis Figures 20 and 21: compile time relative to SBBV with a limit of one version.
def lv_compile_time_micro_inlined():
    return _lv("compile-time", "micro", "inlined", "Relative compile time", True)


def lv_compile_time_micro_hyperfunction():
    return _lv("compile-time", "micro", "hyperfunction", "Relative compile time", True)


def lv_compile_time_macro_inlined():
    return _lv("compile-time", "macro", "inlined", "Relative compile time", True)


def lv_compile_time_macro_hyperfunction():
    return _lv("compile-time", "macro", "hyperfunction", "Relative compile time", True)


# Thesis Figures 22 and 23: average number of versions per basic block of the source program.
def lv_versions_micro_inlined():
    return _lv("versions", "micro", "inlined", "Versions per basic block", True)


def lv_versions_micro_hyperfunction():
    return _lv("versions", "micro", "hyperfunction", "Versions per basic block", True)


def lv_versions_macro_inlined():
    return _lv("versions", "macro", "inlined", "Versions per basic block", True)


def lv_versions_macro_hyperfunction():
    return _lv("versions", "macro", "hyperfunction", "Versions per basic block", True)
