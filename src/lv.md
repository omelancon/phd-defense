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