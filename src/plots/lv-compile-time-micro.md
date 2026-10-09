# ΛV Results: Compile Time, Micro Benchmarks {#plot-lv-compile-time-micro .small}

:::columns
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_compile_time_micro_inlined" legend=true width=4.6 height=2.55}
```
:::/column
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_compile_time_micro_hyperfunction" legend=false width=4.6 height=2.55}
```
:::/column
:::/columns

- Time of the versioning algorithm only, relative to SBBV at limit 1
- Linear: +1.5 per version inlined, +1.1 with hyperfunctions, +0.35 for SBBV
- `random` grows faster: the heuristic matters for compile time too

::: notes
Thesis Figure 20. Lower is better. Compile time here is the execution of the ΛV (or SBBV)
algorithm only. Baseline: SBBV with a limit of one version. The extra cost of ΛV comes from
exploring more contexts and back-propagating exit contexts to call sites to create specialized
return points. Slopes are for the arithmetic and similarity heuristics; SBBV's ~0.35 per version
is consistent with Chapter 3. The right panel keeps SBBV (inlined operators) for reference.
Hover a point for its exact value.
:::
