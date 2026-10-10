# ΛV Results: Compile Time {#plot-lv-compile-time}

:::columns
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_compile_time_micro_hyperfunction" title="Micro benchmarks" legend=true heuristics="[arithmetic]" legend_heuristics=false width=5.3 height=4.4}
```
:::/column
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_compile_time_macro_hyperfunction" title="Macro benchmarks" legend=false heuristics="[arithmetic]" legend_heuristics=false width=5.3 height=4.4}
```
:::/column
:::/columns

::: notes
Thesis Figures 20 (micro) and 21 (macro), hyperfunction operators panels, arithmetic merge
heuristic only. Lower is better. Compile time is the execution of the ΛV (or SBBV) algorithm
only, relative to SBBV with a limit of one version; SBBV (dashed, inlined operators) is kept for
reference. The two panels have their own y scales. Growth is linear: on micro benchmarks about
+1.1 per version with hyperfunctions, against +1.5 with inlined operators and +0.35 for SBBV,
consistent with Chapter 2. On macro benchmarks at limit 10: 14× SBBV at limit 1 with
hyperfunctions, against 17× with inlined operators. The extra cost of ΛV comes from exploring
more contexts and back-propagating exit contexts to call sites to create specialized return
points. Hyperfunction operators let a specialization be reused by every call site with the same
calling context, while inlined operators are respecialized at each call site. The random
heuristic is the most expensive (thesis). Hover a point for its exact value.
:::
