# SBBV Results: Compile Time {#plot-sbbv-compile-time .small}

:::columns
:::column {width=3fr}
```plot {backend=vega source="thesis_plots.py:sbbv_compile_time" width=5.6 height=4.1}
```
:::/column
:::column {width=2fr}
- Compile time relative to compilation without SBBV
- Grows roughly linearly with the limit
- Steeper in Gambit (8.4× at limit 20, macro): a module is one C function, duplication strains the C compiler
- Gambit at limit 1: smaller programs, faster compilation (0.8×)
:::/column
:::/columns

::: notes
Thesis Figure 12. Lower is better. Macro benchmarks are solid lines, micro benchmarks dashed.
Compile time is the whole compilation, relative to compiling without SBBV. Gambit compiles each
Scheme module as a single C function, so code duplication puts additional strain on the C
compiler; Bigloo reaches 3.4× at limit 20 on macro benchmarks. At a limit of one version, Gambit programs are smaller and
compile faster. Hover a point for its exact value.
:::
