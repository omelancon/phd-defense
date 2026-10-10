# ΛV Results: Type Checks {#plot-lv-typechecks}

:::columns
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_typechecks_micro_hyperfunction" title="Micro benchmarks" legend=true heuristics="[arithmetic]" legend_heuristics=false sbbv=true width=5.3 height=4.4}
```
:::/column
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_typechecks_macro_hyperfunction" title="Macro benchmarks" legend=false heuristics="[arithmetic]" legend_heuristics=false sbbv=true width=5.3 height=4.4}
```
:::/column
:::/columns

::: notes
Thesis Figures 18 (micro) and 19 (macro), hyperfunction operators panels, arithmetic merge
heuristic only. Lower is better. Type checks executed, relative to compilation without
versioning. SBBV (dashed) always inlines operators; it is drawn for reference (the thesis draws it
only in the inlined panels). Micro (left): ΛV leaves 26% of the type checks at limit 3, 3.7% at
limit 7 and 1.2% at limit 10, while SBBV goes from 48% at limit 3 to 47% at limit 10: the gap is
what interprocedural propagation removes. In most micro benchmarks ΛV
eliminates all redundant type checks with a limit of about 7: the function checks its argument
types once, then runs a hot loop without type checks, barring overflow. Optimal at: ack (5),
array1 (6), fact20 (3), fib (3), fibfp (3), quicksortfl (10), sum (7), sumfp (7), tak (10).
Macro (right): about half of all type checks are eliminated at a limit of 3 (48% left, against
57% for SBBV), little gain after. What remains: type checks on values read from lists and
vectors, which the contexts do not track. Benchmarks that benefit the most use numeric
arithmetic heavily (almabench, earley, maze, nucleic, slatex). The thesis also shows the random
and similarity heuristics, both worse (see the merge heuristics section). Hover a point for its
exact value.
:::
