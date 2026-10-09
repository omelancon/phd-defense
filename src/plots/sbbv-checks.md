# SBBV Results: Dynamic Checks {#plot-sbbv-checks .small}

:::columns
:::column {width=3fr}
```plot {backend=vega source="thesis_plots.py:sbbv_checks" legend=true width=5.6 height=4.1}
```
:::/column
:::column {width=2fr}
- Gambit and Bigloo, R7RS benchmarks: checks executed, relative to no optimization
- No BBV: the compilers' own optimizations
- Limit 1, equivalent to static analysis: fewer checks
- Limit 2, duplication (macro): 54% of checks gone with Gambit, 62% with Bigloo
- Slow decrease past limit 10: the `similarity` heuristic needs many versions
:::/column
:::/columns

