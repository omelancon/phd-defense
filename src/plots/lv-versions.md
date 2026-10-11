# ΛV Results: Code Duplication {#plot-lv-versions}

:::columns
:::column {#dup-micro width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_versions_micro_hyperfunction" title="Micro benchmarks" legend=false heuristics="[arithmetic]" legend_heuristics=false width=5.3 height=4.4}
```
:::/column
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_versions_macro_hyperfunction" title="Macro benchmarks" legend=true heuristics="[arithmetic]" legend_heuristics=false width=5.3 height=4.4}
```
:::/column
:::column {#dup-note width=0}
```related-work-note
title: "Related work"
items:
  - Using Slicing to Identify Duplication in Source Code (Komondoor & Horwitz 2001)
```
:::/column
:::/columns

```timeline
width dup-micro=0 dup-note=1fr   # the micro benchmarks make room for the related work
```
