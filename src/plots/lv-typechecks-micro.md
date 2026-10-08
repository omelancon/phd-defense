# ΛV Results: Type Checks, Micro Benchmarks {#plot-lv-typechecks-micro .small}

:::columns
:::column {#lv-typechecks-micro-inl width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_typechecks_micro_inlined" width=4.6 height=2.55}
```
:::/column
:::column {#lv-typechecks-micro-hyp width=0}
```plot {backend=vega source="thesis_plots.py:lv_typechecks_micro_hyperfunction" width=4.6 height=2.55}
```
:::/column
:::/columns

{.reveal}
- ΛV (solid) against SBBV (dashed): type checks executed, relative to no versioning
- `arithmetic`: 2 to 4% of checks left at limit 7, optimal code for `fib`, `fact20`, `ack`...
- SBBV plateaus near 47%; hyperfunctions remove as many checks as inlining

```timeline
width lv-typechecks-micro-hyp=1fr     # the hyperfunction panel slides in beside the inlined one
reveal 1..end
```

::: notes
Thesis Figure 18. Lower is better. Solid lines: Lambda Versioning; dashed: SBBV, reimplemented
by disabling the interprocedural parts of ΛV, so the difference is exactly what interprocedural
propagation removes. Left panel: operators inlined; right panel: operators as hyperfunctions (ΛV
only, SBBV always inlines). Micro benchmarks are short, typically recursive functions. With the
arithmetic heuristic ΛV eliminates all redundant type checks in most cases with a limit of about 7:
the function checks its argument types once, then runs a hot loop without type checks, barring
overflow. Optimal at: ack (5), array1 (6), fact20 (3), fib (3), fibfp (3), quicksortfl (10),
sum (7), sumfp (7), tak (10). Hover a point for its exact value.
:::
