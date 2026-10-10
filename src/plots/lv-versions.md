# ΛV Results: Code Duplication {#plot-lv-versions}

:::columns
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_versions_micro_hyperfunction" title="Micro benchmarks" legend=true heuristics="[arithmetic]" legend_heuristics=false width=5.3 height=4.4}
```
:::/column
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_versions_macro_hyperfunction" title="Macro benchmarks" legend=false heuristics="[arithmetic]" legend_heuristics=false width=5.3 height=4.4}
```
:::/column
:::/columns

::: notes
Thesis Figures 22 (micro) and 23 (macro), hyperfunction operators panels, arithmetic merge
heuristic only. Lower is better. The y axis is the average number of versions of each basic block
of the source program; SBBV (dashed, inlined operators) is kept for reference. With inlined
operators there is a double duplication cost, one from inlining and one from ΛV; hyperfunctions
avoid it by sharing specializations. Micro: about 4 versions per block at limit 10, against 6
with inlined operators; the effect is small at low limits since some operators are used only
once. Macro: always fewer versions than with inlined operators, 1.2 against 2.0 at limit 1 and
about 4 against 7.4 at limit 10. This suggests outlining (Komondoor and Horwitz): extract similar
code segments as one hyperfunction, specialize it once, then inline it back after ΛV, which could
further reduce compile time; left as future work. Hover a point for its exact value.
:::
