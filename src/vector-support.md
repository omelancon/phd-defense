# Vector Bound Checks Elimination {#vector-bound-checks-elimination-title layout=title}

# Vector Support: New Rules {#vector-rules}

{.reveal}
**Intervals with symbolic bounds**

{.reveal}
- A bound is written `⟦v⟧-i`, with `i ≥ 0`: the length of vector `v` minus `i`

{.reveal}
**New rules**

{.reveal}
- `(##vector-length v)` returns the singleton `⟦v⟧`
  {.reveal}
  - `⟦v⟧`: exactly the length of `v`, some fixnum in `[0, maxfix]`
- `(fx< x len)` with `len = ⟦v⟧` narrows the upper bound of `x` to `⟦v⟧-1` when true
- `(fx< x len)` with `x` in `[0, ⟦v⟧-1]` and `len == ⟦v⟧` is always true

# Example: vector-ref {#vector-simple .small}

:::columns
:::column {#vs-src width=1fr}
```code-morph {#vs-morph lang=scheme room=fit}
versions:
  - file: programs/vector-simple.scm
    label: "vector-simple.scm"
  - file: programs/vector-simple-expanded.scm
    label: "expanded vector-length and vector-ref"
    highlight: changed
  - file: programs/vector-simple-expanded.scm
    label: "expanded vector-length and vector-ref"
  - file: programs/vector-simple-expanded.scm
    label: "expanded vector-length and vector-ref"
    highlight: [ref-hi]
```
:::/column
:::column {#vs-col width=0}
```bbv-anim {#vs-sbbv program="programs/vector-simple.bbv" algorithm=sbbv heuristic=arithmetic limit=2 intervals=true vector_bounds=true direction=TB rank_wrap=2 height=500}
show: [label, context, code]
```
:::/column
:::/columns

```arrow {#vs-removed}
steps:
  - null
  - {to: vs-sbbv.H1, to_anchor: 350, angle: 20, length: 55, label: "check removed"}
```

```timeline
vs-morph 1                                          # expand vector-length and vector-ref
width vs-src=4fr vs-col=5fr, vs-morph +1            # the SBBV run slides in; highlight off
vs-sbbv 1..end                                      # the run, one frame per step
vs-removed 1, vs-morph +1                           # the bound check of vector-ref is gone
```

# Example: findv with vector bounds {#vector-findv .small}

:::columns
:::column {#vf-src width=1fr}
```code-morph {#vf-morph lang=scheme room=fit}
versions:
  - file: programs/background-findv.scm
    label: "findv.scm"
  - file: programs/background-findv-expanded.scm
    label: "expanded operators"
    highlight: changed
  - file: programs/background-findv-expanded.scm
    label: "expanded operators"
    highlight: [ref-hi]
```
:::/column
:::column {#vf-col width=0}
```bbv-anim {#vf-lv program="programs/findv-call.bbv" algorithm=lv heuristic=arithmetic limit=2 entry=main direction=LR rank_wrap=auto call_edges=true height=500 intervals=true vector_bounds=true}
show: [label, context, code]
prims: {pred: {args: [any, any], result: bool}}
thresholds: [sign, maxfix-1, maxfix]
```
:::/column
:::/columns

```arrow {#vf-removed}
steps:
  - null
  - {to: vf-lv.F1, to_anchor: top, angle: 70, length: 80, label: "bound check removed"}
```

```timeline
vf-morph 1                      # expand the operators
vf-morph 2                      # the bound check to remove
width vf-src=0 vf-col=1fr       # the code collapses; the ΛV run takes the whole width
vf-lv 1..end                    # the run, one frame per step
vf-removed 1                    # the bound check on the result of findv is gone
```
