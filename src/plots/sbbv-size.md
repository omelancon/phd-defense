# SBBV Results: Program Size {#plot-sbbv-size .small}

:::columns
:::column {width=3fr}
```plot {backend=vega source="thesis_plots.py:sbbv_size" width=5.6 height=4.1}
```
:::/column
:::column {width=2fr}
- Executable size relative to compilation without SBBV
- Low limits shrink programs: Gambit at limit 1, Bigloo up to limit 4
- Then size grows with the limit: 5× (Gambit) and 1.7× (Bigloo) at limit 20 on macro benchmarks
- The trade-off that keeps the version limit low
:::/column
:::/columns

::: notes
Thesis Figure 10. Lower is better. Macro benchmarks are solid lines, micro benchmarks dashed.
Program size is measured in bytes, relative to executables compiled without SBBV. At low limits
check elimination outweighs code duplication, as in the polynomial example, so executables get
smaller. Size is the main reason the limit cannot be raised indefinitely to remove every check.
With the similarity heuristic this trade-off is suboptimal: ideally a merge heuristic keeps the
useful versions and removes most checks within a low limit. Hover a point for its exact value.
:::
