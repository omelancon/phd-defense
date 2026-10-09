# ΛV Results: Type Checks, Macro Benchmarks {#plot-lv-typechecks-macro .small}

:::columns
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_typechecks_macro_inlined" legend=true width=4.6 height=2.55}
```
:::/column
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_typechecks_macro_hyperfunction" legend=false width=4.6 height=2.55}
```
:::/column
:::/columns

- `arithmetic`: about half of the type checks gone at limit 3, little gain after
- What remains: values read from lists and vectors, not tracked by the contexts
- `arithmetic` beats `similarity`, which beats `random`; same with hyperfunctions

::: notes
Thesis Figure 19. Lower is better. Solid lines: ΛV; dashed: SBBV (left panel only). Macro
benchmarks are more representative of real programs. With arithmetic, about half of all type
checks are eliminated at a limit of 3 (47% left with inlined operators, 48% with hyperfunctions),
against 57% left with SBBV. Benchmarks that benefit the most use numeric arithmetic heavily
(almabench, earley, maze, nucleic, slatex), the computations arithmetic was designed for. random is
the worst case; similarity beats it by a small margin. Hover a point for its exact value.
:::
