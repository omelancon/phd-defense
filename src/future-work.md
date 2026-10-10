# Future Work {#future-work-title layout=title}

# Native Multi-Return Functions {#future-native .small}

::::: columns
:::: column {width=1fr}
::: columns
::: column
{#native-points .reveal}
- Efficient native implementation
- Here is a work-in-progress
::: /column
::: /columns

{.reveal}
```related-work-note
title: "Related work explored some designs:"
items:
  - Multi-barrelled CPS (Shivers 2004)
  - Extended flat closure (Saleil 2017)
  - Alternate returns (FORTRAN 77)
```
:::: /column
:::: column {#native-code-col width=0}
```code {#native-code lang=tasm file="programs/hvm-hyperfunction.hvm" title="HVM: a VM for hyperfunctions"}
```
:::: /column
:::: column {#native-room width=1fr}
:::: /column
::::: /columns

```arrow {#native-arrow}
steps:
  - null
  - {from: "native-points[2]", from_anchor: right, to: native-code, to_anchor: left}
```

```timeline
reveal 1                                                           # first bullet
reveal 2, native-arrow 1, width native-code-col=1fr native-room=0  # second bullet; the code opens in place of the empty column
reveal 3, native-arrow 0                                           # related work, at the bottom left
```


# Heterogeneous Datastructures {#future-heterogeneous .small}

::::: columns
:::: column {width=1fr}
{#het-points .reveal}
- **Most remaining checks** in benchmarks are on values read from **heterogeneous structures** (vector, pair, box, etc.)
- Include **mutability/escapability** information in contexts to track the type of values within structures
:::: /column
:::: column {#het-col width=0}
```code {#het-code lang=scheme file="programs/heterogeneous.scm"}
```

```bbv-anim {#het-sbbv program="programs/heterogeneous.bbv" algorithm=sbbv limit=1 direction=TB height=375}
show: [label, context, code]
```
:::: /column
:::: column {#het-room width=1fr}
:::: /column
::::: /columns

```arrow {#het-lost}
steps:
  - null
  - {to: het-sbbv.C1, to_anchor: right, angle: 0, length: 110, label: "type of 42 lost"}
  - null
```

```timeline
reveal 1, width het-col=1fr het-room=0      # first bullet; the example opens in place of the empty column
het-sbbv 1..end                             # the SBBV run, one frame per step
het-lost 1                                  # the value read back has type any
reveal 2, het-lost 2                        # second bullet; the arrow goes away
```

# Built-in Constant Folding {#future-constant-folding .small}

:::columns
:::column {#cf-src width=1fr}
```code {#cf-code lang=scheme file="programs/incr.scm"}
```
:::/column
:::column {#cf-col width=0}
```bbv-anim {#cf-lv program="programs/incr.bbv" algorithm=lv heuristic=arithmetic limit=3 entry=main direction=TB intervals=true call_edges=true fold=true generic_entry=false}
show: [label, context, code]
```
:::/column
:::/columns

```arrow {#cf-note}
steps:
  - null
  - {to: cf-lv.N1, to_anchor: bottom, angle: 270, length: 90, label: "receives exactly 1"}
  - {to: cf-lv.R1, to_anchor: left, angle: 180, length: 110, label: "no side-effects"}
  - {to: cf-lv.N1, to_anchor: bottom, angle: 270, length: 140, label: "replace the call with the constant 1"}
  - {to: cf-lv.A1, to_anchor: right, angle: 0, length: 90, label: "these versions can be freed"}
  - null
```

```timeline
width cf-src=0 cf-col=1fr       # the code collapses; the ΛV run takes the whole width
cf-lv 1..10                     # the run, up to the return point N1 for the exit R1
cf-note 1                       # N1 receives exactly the singleton 1
cf-lv 11                        # R1 specialized: every version incr/A1 reaches is known
cf-lv 12, cf-note 2             # incr called with x: 0 has no side effects
cf-lv 13, cf-note 3             # the call site and its return point
cf-lv 14, cf-note 4             # the fold: the call becomes #res = 1, A1, B1 and R1 can be freed
cf-lv 15, cf-note 5             # they are gone
cf-lv ..end                     # the rest of the run
```
