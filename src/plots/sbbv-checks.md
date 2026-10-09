# SBBV Results: Dynamic Checks {#plot-sbbv-checks .small}

:::columns
:::column {width=3fr}
```plot {backend=vega source="thesis_plots.py:sbbv_checks" legend=true width=5.6 height=4.1}
```
:::/column
:::column {width=2fr}
- Gambit and Bigloo, R7RS benchmarks: checks executed, relative to no optimization
- No BBV: the compilers' own optimizations
- Limit 1, abstract interpretation: fewer checks
- Limit 2, duplication (macro): 54% of checks gone with Gambit, 62% with Bigloo
- Slow decrease past limit 10: the `similarity` heuristic needs many versions
:::/column
:::/columns

::: notes
Thesis Figure 9. Lower is better. Macro benchmarks are solid lines, micro benchmarks dashed. The y
axis is the ratio of run-time checks relative to compilation without any optimization, so the
"No BBV" point shows what Bigloo's and Gambit's existing optimizations already remove. At a limit
of one version, each version's context approximates all reachable contexts: abstract
interpretation without code duplication. The further decrease beyond it is what duplication buys.
The slow, never-ending decrease (micro benchmarks especially, which are small monomorphic programs
expected to stabilize early) is the weakness of the similarity heuristic, fixed in the ΛV chapter.
Hover a point for its exact value.
:::
