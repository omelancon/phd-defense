# ΛV Results: Compile Time {#plot-lv-compile-time .small}

Compile time in seconds by version limit (benchmarks that reach 1 s at some limit)

```table-steps
compact: true
table: |
  | Benchmark | Lines | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
  |:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
  | `almabench` | 414 | 0.4 | 0.6 | 1.0 | **1.3** | 1.6 | 1.8 | 2.4 | 2.7 | 3.1 | 3.1 |
  | `compiler` | 11,707 | 5.2 | 11.1 | 15.8 | **23.7** | 30.7 | 41.4 | 50.1 | 62.8 | 72.9 | 85.9 |
  | `dynamic` | 1,599 | 0.4 | 0.5 | 0.6 | **0.8** | 0.9 | 1.0 | 1.0 | 1.2 | 1.2 | 1.4 |
  | `earley` | 505 | 0.5 | 0.7 | 0.9 | **1.1** | 1.6 | 2.0 | 2.1 | 2.7 | 3.2 | 3.7 |
  | `leval` | 433 | 0.2 | 0.3 | 0.5 | **0.6** | 0.9 | 1.0 | 1.1 | 1.2 | 1.4 | 1.5 |
  | `maze` | 424 | 0.3 | 0.5 | 0.6 | **0.8** | 1.0 | 1.2 | 1.6 | 1.9 | 2.1 | 2.5 |
  | `nucleic` | 3,286 | 0.4 | 0.6 | 0.7 | **1.0** | 1.3 | 1.5 | 1.8 | 2.1 | 2.4 | 2.7 |
  | `scheme` | 809 | 0.4 | 0.5 | 0.7 | **0.8** | 0.9 | 1.1 | 1.2 | 1.5 | 1.8 | 2.2 |
  | `slatex` | 2,280 | 0.5 | 0.6 | 0.9 | **0.9** | 0.9 | 0.9 | 0.9 | 0.9 | 1.0 | 1.0 |
```

::: corner-badge
::detour-badge{ref=lv-duplication}
::: /corner-badge

::: detour {#lv-duplication label="Code duplication" key=d}
::include{file="lv-versions.md"}
::: /detour
