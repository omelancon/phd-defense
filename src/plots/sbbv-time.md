# SBBV Results: Execution Time {#plot-sbbv-time}

```plot {backend=vega source="thesis_plots.py:sbbv_time" legend=true width=10 height=4.6}
```

::: notes
Thesis Figure 11. Lower is better. Macro benchmarks are solid lines, micro benchmarks dashed.
The y axis does not start at 0 (it starts at 0.6, the thesis draws a broken axis). The size
trade-off shows in Gambit: time drops quickly at low limits, reaches its minimum at limit 2
(89%), then slowly rises and stabilizes (93% for Gambit). Bigloo stays at about 91% from limit 1.
Micro benchmarks under Gambit keep improving, down to 71% at limit 10. The best limit varies per
benchmark (Appendix D), so a single static limit is suboptimal: per-function limits under the
programmer's control may be preferable. Checks are cheap in these compilers (pointer tagging):
there is more to gain where a type check reads memory (Python, Ruby). Hover a point for its exact
value.
:::
