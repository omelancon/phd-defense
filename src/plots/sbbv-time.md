# SBBV Results: Execution Time {#plot-sbbv-time .small}

:::columns
:::column {width=3fr}
```plot {backend=vega source="thesis_plots.py:sbbv_time" legend=true width=5.6 height=4.1}
```
:::/column
:::column {width=2fr}
- Execution time relative to compilation without SBBV (y axis starts at 0.6)
- Gambit, macro: fastest at limit 2 (89%), then about 93%
- Bigloo, macro: about 91% from limit 1
- Gambit, micro: down to 71% at limit 10
- Cheap checks here (pointer tagging): more to gain where a type check reads memory (Python, Ruby)
:::/column
:::/columns

::: notes
Thesis Figure 11. Lower is better. Macro benchmarks are solid lines, micro benchmarks dashed.
The y axis does not start at 0 (it starts at 0.6, the thesis draws a broken axis). The size
trade-off shows in Gambit: time drops quickly at low limits, reaches its minimum at limit 2
(89%), then slowly rises and stabilizes (93% for Gambit, 91% for Bigloo). Micro benchmarks under
Gambit keep improving up to about limit 3 and slightly beyond. The best limit varies per
benchmark (Appendix D), so a single static limit is suboptimal: per-function limits under the
programmer's control may be preferable. Hover a point for its exact value.
:::
