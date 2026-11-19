"""Vega-Lite spec for the polynomial benchmark of the preface (slide "Attempt 3").

The data is plots/polynomial-bench.csv, measured by polynomial-bench/run.sh: each program reads
N and x from standard input, calls p(x) = x*x + x N times (N = 919227392, so that C takes about
0.5 s) and prints the sum of the results; the time is the median wall-clock time of 5 interleaved
runs. The Lustre program is compiled by lv6 to C and run by a small driver (see bench.lus).

Each bar has its own colour (column `color` of the CSV), from the IBM colour-blind safe palette
used across the deck, matched to the logos where it can be: Gambit amber, Python blue,
and the remaining purple for GCC; LV6 takes the red of the Verimag logo (#e13d25).
"""
from __future__ import annotations

import csv
from pathlib import Path

CSV = Path(__file__).resolve().parent / "polynomial-bench.csv"


def polynomial_bench():
    with open(CSV, newline="", encoding="utf-8") as f:
        values = [{**r, "seconds": float(r["seconds"])} for r in csv.DictReader(f)]
    order = [v["compiler"] for v in values]
    x = {"field": "compiler", "type": "nominal", "sort": order, "title": None,
         "axis": {"labelAngle": 0, "labelFontSize": 15, "grid": False}}
    y = {"field": "seconds", "type": "quantitative", "title": "time (s)",
         "axis": {"labelFontSize": 13, "titleFontSize": 15, "tickCount": 5}}
    return {
        "data": {"values": values},
        "encoding": {"x": x, "y": y},
        "layer": [
            {"mark": {"type": "bar", "width": {"band": 0.6}},
             "encoding": {"color": {"field": "color", "type": "nominal", "scale": None, "legend": None},
                          "tooltip": [{"field": "compiler"}, {"field": "seconds", "format": ".2f"}]}},
            {"mark": {"type": "text", "dy": -9, "fontSize": 15},
             "encoding": {"text": {"field": "seconds", "format": ".2f"}}},
        ],
    }
