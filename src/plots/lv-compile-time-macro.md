# ΛV Results: Compile Time, Macro Benchmarks {#plot-lv-compile-time-macro .small}

:::columns
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_compile_time_macro_inlined" width=4.6 height=2.55}
```
:::/column
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_compile_time_macro_hyperfunction" width=4.6 height=2.55}
```
:::/column
:::/columns

- Same pattern as micro benchmarks: linear, steeper with inlined operators
- At limit 10 (`arithmetic`): 14× SBBV at limit 1 with hyperfunctions, 17× inlined
- `random` is again the most expensive

::: notes
Thesis Figure 21. Lower is better. Baseline: SBBV with a limit of one version, on macro
benchmarks. Hyperfunction operators let a specialization of an operator be reused by every call
site with the same calling context, while inlined operators are respecialized at each call site,
often for the same contexts: hence the gap between the panels. The right panel keeps SBBV
(inlined operators) for reference. Hover a point for its exact value.
:::
