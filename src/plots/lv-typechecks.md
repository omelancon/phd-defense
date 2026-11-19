# ΛV Results: Type Checks {#plot-lv-typechecks .small}

:::columns
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_paper_typechecks_no_hetero" title="Without heterogeneous data structures" legend=true width=5.3 height=3.75}
```
:::/column
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_paper_typechecks_hetero" title="With heterogeneous data structures" legend=false width=5.3 height=3.75}
```
:::/column
:::/columns

Type checks executed, relative to the source program without any optimization (lower is better).\
**Lines**: geometric means, ΛV in blue and Bigloo in red.

::: corner-badge
::detour-badge{ref=lv-setup-detour}
::: /corner-badge

::: detour {#lv-setup-detour label="Experimental Setup" key=s}
::include{file="../lv-setup.md"}
::: /detour
