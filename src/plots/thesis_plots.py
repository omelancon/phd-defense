"""Vega-Lite specs for the evaluation figures of the thesis (Figures 9 to 12 and 18 to 23, and
one derived plot: the ΛV compile time of operators as functions against inlined operators).

Each public function is a `source` of a `plot {backend=vega}` block in this folder. The data is a
one-time copy in data/thesis-figures/ at the root of the defense project (see its README.md); the
encodings follow the thesis: same colours, solid and dashed lines, same baselines and y ranges.

Every function takes the block's `legend` (default true), which Lattice passes to a source with
that parameter: the slide decides whether the panel has a legend, the function only where it goes.
The ΛV functions also take a `heuristics` option, the merge heuristics to show (all of them by
default): `heuristics="[arithmetic]"` on the block, and `legend_heuristics` (default true): false
leaves the heuristics out of the legend, which then names only ΛV and SBBV. Lattice passes the
options it does not know to the source and refuses one the function does not take, so these two
options on an SBBV plot are errors. Every function also takes a `title` option: the plot's title
in place of its own (`title="micro benchmarks"`); without it, a plot keeps its title (the ΛV panels
"Inlined operators" or "Hyperfunction operators", none for the SBBV figures).
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

from lattice import ComponentError

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


def _chart(values, x, y, color, dash, legend_orient, title=None, color_legend=True) -> dict:
    """Lines with points, one series per (color, dash) pair, and a tooltip on every point. Without
    `color_legend`, the legend shows the dashes only."""
    tooltip = [
        {"field": "limit", "type": "quantitative", "title": "version limit"},
        {"field": color["field"], "type": "nominal"},
        {"field": dash["field"], "type": "nominal"},
        {"field": "value", "type": "quantitative", "format": ".3f"},
    ]
    legends = legend_orient is not None
    color = {**color, "type": "nominal",
             "legend": _legend(legend_orient) if legends and color_legend else None}
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


def _sbbv(name: str, ytitle: str, domain: list[float] | None, fmt: str, legend_orient: str,
          legend: bool, title=None) -> dict:
    """One SBBV figure; its legend, if `legend`, sits at `legend_orient`; no title unless
    `title`."""
    legend_orient = legend_orient if _flag("legend", legend) else None
    rows = _rows(DATA / "sbbv" / f"{name}.csv")
    values = [{"limit": int(r[0]), "compiler": c, "suite": s, "value": v}
              for r in rows for (c, s), v in zip(SBBV_SERIES, r[1:])]
    if domain is None:
        domain = [0, _ceiling(max(v["value"] for v in values))]
    limits = [int(r[0]) for r in rows]
    return _chart(values, _x_axis(limits, "No BBV"), _y_axis(ytitle, domain, fmt),
                  {"field": "compiler", "scale": SBBV_COLORS}, {"field": "suite", "scale": SUITE_DASH},
                  legend_orient, _title(title, None))


def sbbv_checks(legend=True, title=None):
    """Thesis Figure 9: run-time checks relative to compilation without any optimization."""
    return _sbbv("checks", "Relative dynamic checks", [0, 1], ".1f", "top-right", legend, title)


def sbbv_size(legend=True, title=None):
    """Thesis Figure 10: program size relative to compilation without SBBV."""
    return _sbbv("size", "Relative program size", None, "~g", "top-left", legend, title)


def sbbv_time(legend=True, title=None):
    """Thesis Figure 11: execution time relative to compilation without SBBV (y axis from 0.6)."""
    return _sbbv("time", "Relative execution time", [0.6, 1.0], ".2f", "bottom-right", legend,
                 title)


def sbbv_compile_time(legend=True, title=None):
    """Thesis Figure 12: compile time relative to compilation without SBBV."""
    return _sbbv("compile-time", "Relative compile time", None, "~g", "top-left", legend, title)


# ---------------------------------------------------------------------------- Lambda Versioning (Ch. 4)

HEURISTICS = ["random", "similarity", "arithmetic"]
HEURISTIC_COLORS = {"domain": HEURISTICS, "range": ["#FFB000", "#DC267F", "#648FFF"]}
ALGO_DASH = {"domain": ["ΛV", "SBBV"], "range": [[1, 0], [7, 4]]}
# Column of each metric in data/thesis-figures/lv/geomeans.*.csv (written by aggregate-benchmark.sh).
LV_COLUMNS = {"typechecks": 1, "compile-time": 2, "versions": 4}


def _heuristics(heuristics) -> list[str]:
    """The heuristics a plot shows, in the order of HEURISTICS: all of them when not given."""
    if heuristics is None:
        return HEURISTICS
    if isinstance(heuristics, str):
        heuristics = [heuristics]
    if not isinstance(heuristics, list) or not heuristics:
        raise ComponentError(f"heuristics must be a non-empty list of {', '.join(HEURISTICS)}")
    unknown = [h for h in heuristics if h not in HEURISTICS]
    if unknown:
        raise ComponentError(f"unknown heuristic {', '.join(map(repr, unknown))}: "
                             f"expected {', '.join(HEURISTICS)}")
    return [h for h in HEURISTICS if h in heuristics]


def _lv_series(metric: str, kind: str, variant: str, algo: str, first: int,
               heuristics: list[str]) -> list[dict]:
    col = LV_COLUMNS[metric]
    out = []
    for h in heuristics:
        suffix = f"{h}.{variant}." if variant else f"{h}."
        for r in _rows(DATA / "lv" / f"geomeans.{suffix}{kind}.csv"):
            if r[0] >= first and r[col] > 0:  # -1: no value (aggregate-benchmark.sh)
                out.append({"limit": int(r[0]), "heuristic": h, "algorithm": algo, "value": r[col]})
    return out


def _flag(name: str, value) -> bool:
    if not isinstance(value, bool):
        raise ComponentError(f"{name} must be true or false, not {value!r}")
    return value


def _title(title, default: str | None) -> str | None:
    """The plot's title: `title` when given, else `default` (None: no title)."""
    if title is None:
        return default
    if not isinstance(title, str):
        raise ComponentError(f"title must be a string, not {title!r}")
    return title


def _ceiling(m: float) -> float:
    if m <= 1:
        return 1
    step = 1 if m <= 10 else 5
    return step * math.ceil(m / step)


def _lv(metric: str, kind: str, panel: str, ytitle: str, sbbv_in_hyper: bool, heuristics=None,
        legend_heuristics=True, legend=True, title=None) -> dict:
    """One panel of a thesis figure; both panels of a figure share their y range. `heuristics` keeps
    some of the merge heuristics, each with its colour of the full figure; `legend_heuristics=False`
    leaves them out of the legend. The legend, if `legend`, sits where the curves leave room: top
    right where they fall (type checks), top left where they rise. `title` replaces the panel's
    title ("Inlined operators" or "Hyperfunction operators")."""
    shown = _heuristics(heuristics)
    legend_heuristics = _flag("legend_heuristics", legend_heuristics)
    first = 0 if metric == "typechecks" else 1
    inlined = _lv_series(metric, kind, "inline-rts", "ΛV", first, shown)
    hyper = _lv_series(metric, kind, "", "ΛV", first, shown)
    sbbv = _lv_series(metric, kind, "sbbv", "SBBV", first, shown)
    if metric == "typechecks":
        domain, fmt = [0, 1], ".1f"
    else:
        domain, fmt = [0, _ceiling(max(v["value"] for v in inlined + hyper + sbbv))], "~g"
    legend = ("top-right" if first == 0 else "top-left") if _flag("legend", legend) else None
    if panel == "inlined":
        values, default_title = sbbv + inlined, "Inlined operators"
    else:
        values, default_title = (sbbv if sbbv_in_hyper else []) + hyper, "Hyperfunction operators"
    limits = list(range(first, 11))
    # the dash legend names only the algorithms drawn (the type check panel of hyperfunction
    # operators has no SBBV)
    drawn = [a for a in ALGO_DASH["domain"] if any(v["algorithm"] == a for v in values)]
    dash = {"domain": drawn, "range": [r for a, r in zip(ALGO_DASH["domain"], ALGO_DASH["range"]) if a in drawn]}
    return _chart(values, _x_axis(limits, "No ΛV"), _y_axis(ytitle, domain, fmt),
                  {"field": "heuristic", "scale": _heuristic_colors(shown)},
                  {"field": "algorithm", "scale": dash},
                  legend, _title(title, default_title), legend_heuristics)


def _heuristic_colors(shown: list[str]) -> dict:
    colors = dict(zip(HEURISTIC_COLORS["domain"], HEURISTIC_COLORS["range"]))
    return {"domain": shown, "range": [colors[h] for h in shown]}


# Thesis Figures 18 and 19: type checks relative to compilation without ΛV/SBBV. As in the thesis,
# the hyperfunction panel leaves SBBV out (SBBV always uses inlined operators), unless the block
# passes `sbbv=true` to draw it for reference, as the compile time and versions panels do.
def lv_typechecks_micro_inlined(heuristics=None, legend_heuristics=True, legend=True,
                                title=None):
    return _lv("typechecks", "micro", "inlined", "Relative type checks", False,
               heuristics, legend_heuristics, legend, title)


def lv_typechecks_micro_hyperfunction(heuristics=None, legend_heuristics=True, legend=True,
                                      title=None, sbbv=False):
    return _lv("typechecks", "micro", "hyperfunction", "Relative type checks", _flag("sbbv", sbbv),
               heuristics, legend_heuristics, legend, title)


def lv_typechecks_macro_inlined(heuristics=None, legend_heuristics=True, legend=True,
                                title=None):
    return _lv("typechecks", "macro", "inlined", "Relative type checks", False,
               heuristics, legend_heuristics, legend, title)


def lv_typechecks_macro_hyperfunction(heuristics=None, legend_heuristics=True, legend=True,
                                      title=None, sbbv=False):
    return _lv("typechecks", "macro", "hyperfunction", "Relative type checks", _flag("sbbv", sbbv),
               heuristics, legend_heuristics, legend, title)


# Thesis Figures 20 and 21: compile time relative to SBBV with a limit of one version.
def lv_compile_time_micro_inlined(heuristics=None, legend_heuristics=True, legend=True,
                                  title=None):
    return _lv("compile-time", "micro", "inlined", "Relative compile time", True,
               heuristics, legend_heuristics, legend, title)


def lv_compile_time_micro_hyperfunction(heuristics=None, legend_heuristics=True, legend=True,
                                        title=None):
    return _lv("compile-time", "micro", "hyperfunction", "Relative compile time", True,
               heuristics, legend_heuristics, legend, title)


def lv_compile_time_macro_inlined(heuristics=None, legend_heuristics=True, legend=True,
                                  title=None):
    return _lv("compile-time", "macro", "inlined", "Relative compile time", True,
               heuristics, legend_heuristics, legend, title)


def lv_compile_time_macro_hyperfunction(heuristics=None, legend_heuristics=True, legend=True,
                                        title=None):
    return _lv("compile-time", "macro", "hyperfunction", "Relative compile time", True,
               heuristics, legend_heuristics, legend, title)


# Thesis Figures 22 and 23: average number of versions per basic block of the source program.
def lv_versions_micro_inlined(heuristics=None, legend_heuristics=True, legend=True,
                              title=None):
    return _lv("versions", "micro", "inlined", "Versions per basic block", True,
               heuristics, legend_heuristics, legend, title)


def lv_versions_micro_hyperfunction(heuristics=None, legend_heuristics=True, legend=True,
                                    title=None):
    return _lv("versions", "micro", "hyperfunction", "Versions per basic block", True,
               heuristics, legend_heuristics, legend, title)


def lv_versions_macro_inlined(heuristics=None, legend_heuristics=True, legend=True,
                              title=None):
    return _lv("versions", "macro", "inlined", "Versions per basic block", True,
               heuristics, legend_heuristics, legend, title)


def lv_versions_macro_hyperfunction(heuristics=None, legend_heuristics=True, legend=True,
                                    title=None):
    return _lv("versions", "macro", "hyperfunction", "Versions per basic block", True,
               heuristics, legend_heuristics, legend, title)


# Not a thesis figure: the compile time panels of Figures 20 and 21 redrawn to compare the two
# representations of the operators, both with ΛV and the arithmetic heuristic. The colour is the
# heuristic's, as in the figures; the dashes tell the representation: solid for operators as
# functions (the hyperfunction data), dashed for inlined operators. SBBV is left out. The `_all`
# function combines the micro and macro geometric means (15 and 12 benchmarks).
OPERATORS_DASH = {"domain": ["As function", "Inlined"], "range": [[1, 0], [7, 4]]}


# Number of benchmarks of each suite in the geometric means (thesis, Chapter 4 evaluation).
SUITE_SIZES = {"micro": 15, "macro": 12}


def _combined(metric: str, variant: str, algo: str, first: int) -> list[dict]:
    """The geometric mean over both suites at each limit, from the geometric means of the suites:
    exp(sum(n_k ln g_k) / sum(n_k)), n_k the number of benchmarks of suite k. It is exact when each
    value is the geometric mean of per-benchmark ratios, as in the thesis files."""
    suites = {k: {int(v["limit"]): v["value"]
                  for v in _lv_series(metric, k, variant, algo, first, ["arithmetic"])}
              for k in SUITE_SIZES}
    total = sum(SUITE_SIZES.values())
    limits = sorted(set.intersection(*(set(v) for v in suites.values())))
    return [{"limit": n, "heuristic": "arithmetic", "algorithm": algo,
             "value": math.exp(sum(SUITE_SIZES[k] * math.log(suites[k][n]) for k in SUITE_SIZES)
                               / total)}
            for n in limits]


def _lv_operators(metric: str, kind: str | None, ytitle: str, legend=True, title=None) -> dict:
    """ΛV with operators as functions (solid) against ΛV with inlined operators (dashed), arithmetic
    heuristic, for one kind of benchmarks, or for both together when `kind` is None (the geometric
    mean over the benchmarks of both suites, see `_combined`). The legend, if `legend`, names the
    two representations and sits top left where the curves rise."""
    first = 1
    if kind is None:
        function = _combined(metric, "", "As function", first)
        inlined = _combined(metric, "inline-rts", "Inlined", first)
    else:
        function = _lv_series(metric, kind, "", "As function", first, ["arithmetic"])
        inlined = _lv_series(metric, kind, "inline-rts", "Inlined", first, ["arithmetic"])
    domain = [0, _ceiling(max(v["value"] for v in function + inlined))]
    legend = "top-left" if _flag("legend", legend) else None
    return _chart(function + inlined, _x_axis(list(range(first, 11)), "No ΛV"),
                  _y_axis(ytitle, domain, "~g"),
                  {"field": "heuristic", "scale": _heuristic_colors(["arithmetic"])},
                  {"field": "algorithm", "scale": OPERATORS_DASH},
                  legend, _title(title, None), False)


def lv_operators_compile_time_micro(legend=True, title=None):
    return _lv_operators("compile-time", "micro", "Relative compile time", legend, title)


def lv_operators_compile_time_macro(legend=True, title=None):
    return _lv_operators("compile-time", "macro", "Relative compile time", legend, title)


def lv_operators_compile_time_all(legend=True, title=None):
    """Both suites together: the geometric mean over the 15 micro and 12 macro benchmarks."""
    return _lv_operators("compile-time", None, "Relative compile time", legend, title)
