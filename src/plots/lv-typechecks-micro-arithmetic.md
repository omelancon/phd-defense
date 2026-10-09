# ΛV Results: Type Checks, Micro Benchmarks (arithmetic) {#plot-lv-typechecks-micro-arithmetic .small}

:::columns
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_typechecks_micro_inlined" legend=true heuristics="[arithmetic]" legend_heuristics=false width=4.6 height=2.55}
```
:::/column
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_typechecks_micro_hyperfunction" legend=false heuristics="[arithmetic]" legend_heuristics=false width=4.6 height=2.55}
```
:::/column
:::/columns

- The `arithmetic` heuristic alone: ΛV (solid) against SBBV (dashed)
- Limit 3: 24% of the type checks left with ΛV, 48% with SBBV
- Limit 7: 2 to 4% left with ΛV; SBBV stays near 47%

::: notes
Thesis Figure 18 restricted to the arithmetic heuristic. Lower is better. Solid lines: Lambda
Versioning; dashed: SBBV, which shares the heuristic, so the gap is what interprocedural
propagation removes. Left panel: operators inlined (24% left at limit 3, 2.3% at limit 7, 1.0% at
limit 10); right panel: operators as hyperfunctions, ΛV only (26%, 3.7% and 1.2%). SBBV goes from
48% at limit 3 to 47% at limit 10. Hover a point for its exact value.
:::
