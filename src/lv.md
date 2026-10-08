# Lambda Versioning {#lv-title layout=title}

*Whole-program* ahead-of-time basic block versioning

# Overview of Lambda Versioning {.small}

{.reveal}
**The missing puzzle piece of SBBV**

{.reveal}
- *Intraprocedural* technique: limited propagation across abstraction barriers (functions)

{.reveal}
**Why?**

{.reveal}
1. SBBV propagates information *forward only*.
    - Propagating from a function's exit site to the call site requires *backward propagation*.
2. Call sites have a single return point.
    - This acts as a join point for all exit sites, losing context precision.

{.reveal}
**Solution**

{.reveal}
1. Backward propagation from function's exit sites to call sites.
2. Duplicate functions' entry points and exit sites to preserve context precision.

```timeline
reveal +2
reveal +2
reveal +1
reveal +2
reveal ..end
```

# Framing the problem with an example {#lv-framing .small}

:::columns
:::column {#sq-src width=1fr}
```code-morph {#sq-morph lang=scheme room=fit}
versions:
  - file: programs/polynomial-square.scm
    label: "polynomial-square.scm"
  - file: programs/polynomial-square-expanded.scm
    label: "expanded operators"
    highlight: changed
  - file: programs/polynomial-square-expanded.scm
    label: "expanded operators"
  - file: programs/polynomial-square-expanded.scm
    label: "expanded operators"
    highlight: y-fix
  - file: programs/polynomial-square-expanded.scm
    label: "expanded operators"
```
:::/column
:::column {#sq-notes width=0}
{.reveal}
- This conditional type information is lost at the return point
- We want the analysis to define specialized call interfaces:
  {.reveal}
  - If the argument is a fixnum, provide one return point for fixnum and one for bignum
  - If the argument is a flonum, the result is always a flonum
  - If the argument is unknown, it could be a fixnum, flonum or another number, provide a return point for each
:::/column
:::column {#sq-col width=0}
```bbv-anim {#sq-sbbv program="programs/square.bbv" algorithm=sbbv heuristic=arithmetic limit=3 direction=TB height=480}
show: [label, context, code]
paths:
  - input: {x: fx}
  - input: {x: fl}
  - input: {x: any}
```
:::/column
:::/columns

```arrow {#sq-exits}
steps:
  - null
  - {to: sq-sbbv.R1, to_anchor: bottom, angle: 290, length: 45, label: "when x is a fixnum, square returns a fixnum..."}
  - {to: sq-sbbv.C1, to_anchor: bottom, angle: 290, length: 45, label: "... or a bignum"}
  - null
  - {to: sq-sbbv.E1, to_anchor: bottom, angle: 250, length: 45, label: "when x is a flonum, square returns a flonum"}
  - null
  - {to: sq-sbbv.R1, to_anchor: bottom, angle: 290, length: 45, label: "if argument type any, it was discovered at exit sites"}
  - {to: y-fix, to_anchor: right, angle: 60, length: 90, label: "can be used to remove checks at return point"}
  - null
```

```timeline
sq-morph 1                                            # expand the arithmetic operators
width sq-src=5fr sq-col=6fr, sq-morph +1              # the SBBV run slides in; highlight off
sq-sbbv 1..end-3                                      # the full run, one frame per step
sq-sbbv +1                                            # the path of a fixnum x
sq-exits 1                                            # fixnum exit site
sq-exits 2                                            # bignum exit site
sq-sbbv +1, sq-exits 3                                # the path of a flonum x
sq-exits 4                                            # its only exit site
sq-sbbv +1, sq-exits 5                                # the path of an unknown x: the whole CFG
sq-exits 6                                            # the type is discovered at the exit sites
sq-exits 7, sq-morph +1                               # the test in polynomial that can use it
width sq-src=0 sq-notes=5fr sq-col=6fr, sq-sbbv end-3, sq-exits end, sq-morph +1, reveal 1   # the code collapses; first bullet
reveal ..end
```

# Core idea of Lambda Versioning {.small}

{.reveal}
**Core idea**

{.reveal}
- Transform the source program into one with **multi-entry/multi-return functions**
- Context at call sites propagate information to generate specialized entry points
- Entry points track the exit sites they can reach
- When a specialized exit site is discovered/removed, its call sites are notified and updated

{.reveal}
**Algorithm sketch**

{.reveal}
- Extend SBBV with multi-source recahability algorithm that associates entry points and exit sites
- When a new exit site is found, generate a specialized return point for each of its call sites
- When a merge removes an exit site, remove the corresponding return points from its call sites
- Entry points and exit sites duplication is governed by the same version limit as SBBV

```timeline
reveal +2
reveal ..5
reveal +2
reveal ..end
```

# Example: polynomial and square {#lv-example .small}

:::columns
:::column {#ex-src width=1fr}
```code {#ex-code lang=scheme file="programs/polynomial-square-call.scm"}
```
:::/column
:::column {#ex-col width=0}
```bbv-anim {#ex-lv program="programs/polynomial-square.bbv" algorithm=lv heuristic=arithmetic limit=3 entry=main direction=TB height=500}
show: [label, context, code]
```
:::/column
:::/columns

```arrow {#ex-notes}
steps:
  - null
  - {to: ex-lv.M1, to_anchor: right, angle: 340, length: 120, label: "polynomial called with argument of type any"}
  - {to: ex-lv.A1, to_anchor: right, angle: 340, length: 120, label: "entry site created for x: any"}
  - null
  - {to: ex-lv.A1, to_anchor: right, angle: 340, length: 120, label: "square called with argument of type any"}
  - {to: ex-lv.S1, to_anchor: bottom, angle: 250, length: 110, label: "entry site created for x: any"}
  - null
  - {to: ex-lv.A1, to_anchor: bottom, angle: 290, length: 180, label: "no return point created yet because no exit site discovered in square"}
  - null
  - {to: ex-lv.U1, to_anchor: bottom, angle: 250, length: 110, label: "fixnum-specialized exit site created in square"}
  - {to: ex-lv.B1, to_anchor: bottom, angle: 290, length: 110, label: "fixnum-specialized return point created"}
  - null
  - {to: ex-lv.W1, to_anchor: bottom, angle: 290, length: 110, label: "overflow exit site created in square"}
  - {to: ex-lv.B2, to_anchor: bottom, angle: 290, length: 130, label: "bignum-specialized return point created"}
  - null
  - {to: ex-lv.B1, to_anchor: bottom, angle: 290, length: 110, label: "return points are merged as per SBBV"}
  - null
  - {to: ex-lv.J1, to_anchor: right, angle: 340, length: 120, label: "as exit sites are found in polynomial"}
  - {to: ex-lv.N1, to_anchor: bottom, angle: 250, length: 230, label: "specialized return points are created"}
  - null
  - {to: "ex-lv.A1->B1", angle: 100, length: 70, label: "indices define an ordering on which caller and callee agree"}
  - {to: "ex-lv.A1->B5", angle: 80, length: 70, label: "the same return point can be passed at multiple indices (due to merge)"}
```

```arrow {#ex-idx-u}
steps:
  - null
  - {to: ex-lv.U1, to_anchor: bottom, angle: 328, length: 181}
  - null
```

```arrow {#ex-idx-w follow=ex-idx-u}
steps:
  - null
  - {to: ex-lv.W1, to_anchor: bottom, angle: 308, length: 127}
  - null
```

```arrow {#ex-idx-x follow=ex-idx-u}
steps:
  - null
  - {to: ex-lv.X1, to_anchor: bottom, angle: 266, length: 98, label: "exit contexts are assigned indices"}
  - null
```

```arrow {#ex-idx-z follow=ex-idx-u}
steps:
  - null
  - {to: ex-lv.Z1, to_anchor: bottom, angle: 227, length: 137}
  - null
```

```timeline
width ex-src=0 ex-col=1fr       # the code collapses; the ΛV run takes the whole width
ex-lv 1..2                      # M1 queued, then dequeued
ex-lv 3, ex-notes 1             # M1 specialized: polynomial called with x: any
ex-notes 2                      # the entry point A1
ex-notes 3
ex-lv 4..5                      # A1 dequeued, S1 created
ex-lv 6, ex-notes 4             # A1 specialized: square called with x: any
ex-notes 5                      # the entry point S1
ex-notes 6
ex-lv 7..10                     # S1, T1 specialized
ex-lv 11, ex-notes 7            # no exit site of square yet, so no return point at A1
ex-notes 8
ex-lv 12..14                    # U1 is the first exit site
ex-lv 15, ex-notes 9            # B1 added for the fixnum exit U1
ex-notes 10                     # the return point B1
ex-notes 11
ex-lv 16..18                    # W1, the overflow exit site
ex-lv 19, ex-notes 12           # B2 added for the overflow exit W1
ex-notes 13                     # the return point B2
ex-notes 14
ex-lv 20..29                    # X1 and Z1 add B3 and B4
ex-lv 30, ex-notes 15           # B is over the limit: return points merge as in SBBV
ex-notes 16
ex-lv 31..52                    # the merge, then polynomial is specialized
ex-lv 53, ex-notes 17           # J1 is an exit site of polynomial
ex-notes 18                     # so main gets the return point N1
ex-notes 19
ex-lv ..end                     # the rest of the run
ex-idx-u 1                      # the four exit sites of square, with their followers
ex-idx-u end, ex-notes 20       # the return edge of index 0
ex-notes 21                     # B5 is passed at two indices
```
