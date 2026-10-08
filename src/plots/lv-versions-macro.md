# ΛV Results: Code Duplication, Macro Benchmarks {#plot-lv-versions-macro .small}

:::columns
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_versions_macro_inlined" width=4.6 height=2.55}
```
:::/column
:::column {width=1fr}
```plot {backend=vega source="thesis_plots.py:lv_versions_macro_hyperfunction" width=4.6 height=2.55}
```
:::/column
:::/columns

- Hyperfunction operators always give fewer versions: 1.2 against 2.0 at limit 1
- At limit 10: about 4 versions per block with hyperfunctions, 7.4 inlined
- Next: outline similar code into hyperfunctions, specialize once, inline after ΛV

::: notes
Thesis Figure 23. Lower is better. On macro benchmarks the number of versions with
hyperfunction operators is always lower than with inlined operators, even at low limits. This
reuse of operator specializations suggests outlining (Komondoor and Horwitz): extract similar code
segments as one hyperfunction, specialize it once, then inline it back after ΛV, which could
further reduce compile time; left as future work. Hover a point for its exact value.
:::
