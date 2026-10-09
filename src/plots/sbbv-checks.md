# SBBV Results: Dynamic Checks {#plot-sbbv-checks}

```plot {backend=vega source="thesis_plots.py:sbbv_checks" legend=true width=10 height=4.6}
```

::: notes
Thesis Figure 9. Lower is better. Macro benchmarks are solid lines, micro benchmarks dashed.
Checks executed on the R7RS benchmarks, relative to compilation without any optimization. The
"No BBV" point is the compilers' own optimizations. A limit of 1 is equivalent to a static
analysis and already removes checks. A limit of 2 adds duplication: on macro benchmarks, 54% of
checks are gone with Gambit and 62% with Bigloo. Past a limit of about 10 the decrease is slow:
the similarity heuristic needs many versions. Hover a point for its exact value.
:::
