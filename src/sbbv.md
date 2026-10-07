# Static Basic Block Versioning {layout=title}

# Overview of Static Basic Block Versioning

**Abstract interpretation and dynamic languages**
- Tug of war between union and narrowing operations
- Inputs exist that produce wide ranges of behaviors
- Union *wins* over narrowing

**Core idea**
- Delay the union operation
- Duplicate basic blocks for different contexts
- When a version limit is reached, perform a *merge*

# SBBV: A first example {#sbbv-first-example}

:::columns
:::column {#poly-src width=1fr}
```code-morph {#poly-morph lang=scheme room=fit}
versions:
  - file: programs/polynomial.scm
    label: "polynomial.scm"
  - file: programs/polynomial-expanded.scm
    label: "expanded operators"
    highlight: changed
  - file: programs/polynomial-expanded.scm
    label: "expanded operators"
    highlight: [x-fix, x-flo]
  - file: programs/polynomial-expanded.scm
    label: "expanded operators"
```
:::/column
:::column {#poly-cfg-col width=1fr}
{.reveal}
```bbv-cfg {#poly-cfg program="programs/polynomial.bbv" height=500}
```
:::/column
:::column {#poly-sbbv-col width=0}
```bbv-anim {#poly-sbbv program="programs/polynomial.bbv" algorithm=sbbv heuristic=arithmetic limit=3 direction=LR height=480}
show: [label, context, code]
```
:::/column
:::/columns

```arrow {#poly-join}
steps:
  - null
  - {to: poly-cfg.J, to_anchor: left, angle: 210, length: 160, label: "union at join points prevents propagating precise types"}
  - null
```

```arrow {#poly-versions}
steps:
  - null
  - {to: poly-sbbv.J1, to_anchor: right, angle: 330, length: 110, label: "first version"}
  - null
  - {to: poly-sbbv.J2, to_anchor: right, angle: 330, length: 110, label: "second version"}
  - null
  - {to: poly-sbbv.J4, to_anchor: right, angle: 330, length: 110, label: "merge"}
  - {to: poly-sbbv.J5, to_anchor: right, angle: 330, length: 110, label: "merge"}
  - null
```

```timeline
poly-morph 1                                        # expand the operators
reveal 1                                            # the CFG of the expanded program
poly-morph 2, poly-join 1                           # the tests of x in *, and the union at the join point J
width poly-src=0 poly-cfg-col=0 poly-sbbv-col=1fr, poly-join end, poly-morph 3   # SBBV replaces the CFG, highlight off
poly-sbbv 1..3                                      # A specialized, B dequeued
poly-sbbv 4, poly-versions 1                        # B queues the first version of J
poly-sbbv 5, poly-versions 2
poly-sbbv 6..9
poly-sbbv 10, poly-versions 3                       # C queues the second version of J
poly-sbbv 11, poly-versions 4
poly-sbbv 12..17                                    # E and F queue J3 and J4
poly-sbbv 18, poly-versions 5                       # over the limit: J4 will be merged
poly-sbbv 19, poly-versions 6                       # the generic and overflow versions merge into J5
poly-sbbv 20, poly-versions end
poly-sbbv ..end                                     # the rest of the specialization
```

::: notes
After expansion, * tests x once and dispatches to fx*? (with its overflow fallback), fl* or the generic ##*. The four results meet at J: their union is "any number", so the + after it must test y again. SBBV keeps one version of J per incoming context, up to the limit of 3; when F queues a fourth one, the arithmetic heuristic merges the two contexts that may hold a bignum (overflow and generic), and the fixnum and flonum versions keep precise types for +.
:::
