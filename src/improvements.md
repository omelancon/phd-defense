# Various Improvements {#lv-improvements .small}

Three refinements.

::::: columns
::: column {width=1fr}
:::: group
### Vector bound checks

*intervals with symbolic bounds*

- A bound is `⟦v⟧-i`: the length of vector `v` minus `i`
- `(fx< x len)` narrows the index `x` to `[0, ⟦v⟧-1]`
- The bound check of `vector-ref` is removed
::::

::detour-badge{ref=detour-vector}
::: /column
::: column {width=1fr}
:::: group
### Operators as functions

*specializations are reused*

- SBBV requires inlined operators
- ΛV supports `+` and `*` as functions
- Each specialization is computed once
::::

::detour-badge{ref=detour-operators}
::: /column
::: column {width=1fr}
:::: group
### Merge heuristics

*similarity vs arithmetic*

- `similarity` merges the closest contexts
- `arithmetic` preserves pure arithmetic
- `arithmetic` is better on all benchmarks
::::

::detour-badge{ref=detour-heuristics}
::: /column
:::::

::: detour {#detour-vector label="Vector bound checks" key=v}
::include{file="vector-support.md"}
::: /detour

::: detour {#detour-operators label="Operators as functions" key=f}
::include{file="operators-as-functions.md"}
::: /detour

::: detour {#detour-heuristics label="Merge heuristics" key=h}
::include{file="heuristics.md"}
::: /detour
