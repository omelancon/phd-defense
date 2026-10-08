# ΛV Results: Code Duplication, Micro Benchmarks {#plot-lv-versions-micro .small}

:::columns
:::column {#lv-versions-micro-inl width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_versions_micro_inlined" width=4.6 height=2.55}
```
:::/column
:::column {#lv-versions-micro-hyp width=0}
```plot {backend=vega source="thesis_plots.py:lv_versions_micro_hyperfunction" width=4.6 height=2.55}
```
:::/column
:::/columns

{.reveal}
- Versions per basic block of the source program, before inlining
- Inlined operators pay twice: inlining, then versioning of every copy
- Hyperfunctions share specializations: 4 versions per block at limit 10, not 6

```timeline
width lv-versions-micro-hyp=1fr     # the hyperfunction panel slides in beside the inlined one
reveal 1..end
```

::: notes
Thesis Figure 22. Lower is better. The y axis is the average number of versions of each basic
block of the source program. With inlined operators there is a double duplication cost, one from
inlining and one from ΛV; hyperfunctions avoid it. On micro benchmarks, where some operators are
used only once, the effect is small at low limits and grows with the limit. The right panel keeps
SBBV (inlined operators) for reference. Hover a point for its exact value.
:::
