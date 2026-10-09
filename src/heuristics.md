# Merge Heuristics {#heuristics-title layout=title}

# Arithmetic vs Similarity {#heuristics-choice}

:::: columns
::: column {width=1fr}
### similarity

*merge closest*

```bbv-merge {#sim limit=3 heuristic=similarity height=300 fit_aspect="4:3" panel_at=below distance_magnitude=true}
contexts:
  - {x: fx, y: fx}
  - {x: fx, y: fl}
  - {x: fl, y: fl}
  - {x: fl, y: fx}
```
::: /column
::: column {width=1fr}
### arithmetic

*prefer pure arithmetic*

```bbv-merge {#ari limit=3 heuristic=arithmetic height=300 fit_aspect="4:3" panel_at=below distance_magnitude=true}
contexts:
  - {x: fx, y: fx}
  - {x: fx, y: fl}
  - {x: fl, y: fl}
  - {x: fl, y: fx}
```
::: /column
::::

```arrow {#pure}
steps:
  - null
  - {to: ari.C1, to_anchor: left, angle: 170, length: 115, label: "preserved pure arithmetic"}
```

```arrow {#pure-fl follow=pure}
steps:
  - null
  - {to: ari.C4, to_anchor: top, angle: 124, length: 160}
```

```timeline
sim 1..end, ari 1..end      # both merges play in sync
pure 1                      # the pure fixnum and flonum contexts survive
```

# Empirical Comparison {#heuristics-results .small}

:::: columns
::: column {width=1fr}
```plot {backend=vega source="plots/thesis_plots.py:lv_typechecks_micro_inlined" legend=true width=4.6 height=2.55}
```
::: /column
::: column {width=1fr}
```plot {backend=vega source="plots/thesis_plots.py:lv_typechecks_macro_inlined" legend=false width=4.6 height=2.55}
```
::: /column
::::

{.reveal}
- `arithmetic` fares better on all benchmarks
- generates optimal program for recursive functions such as `fib`
- heuristic has a larger impact on ΛV than SBBV.
