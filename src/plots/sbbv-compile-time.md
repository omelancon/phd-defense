# SBBV Results: Compile Time {#plot-sbbv-compile-time}

```plot {backend=vega source="thesis_plots.py:sbbv_compile_time" legend=true width=10 height=4.6}
```

::: notes
Thesis Figure 12. Lower is better. Macro benchmarks are solid lines, micro benchmarks dashed.
Compile time is the whole compilation, relative to compiling without SBBV. It grows roughly
linearly with the limit, more steeply in Gambit (8.4× at limit 20 on macro benchmarks): Gambit
compiles each Scheme module as a single C function, so code duplication puts additional strain on
the C compiler; Bigloo reaches 3.4× at limit 20 on macro benchmarks. At a limit of one version,
Gambit programs are smaller and compile faster (0.8×). Hover a point for its exact value.
:::
