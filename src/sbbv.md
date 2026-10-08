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
:::column {#poly-follow-col width=0}
```bbv-cfg {#poly-follow program="programs/polynomial.bbv" follow=poly-sbbv height=480}
show: [label]
```
:::/column
:::column {#poly-sbbv-col width=0}
```bbv-anim {#poly-sbbv program="programs/polynomial.bbv" algorithm=sbbv heuristic=arithmetic limit=3 direction=LR height=480}
show: [label, context, code]
paths:
  - input: {x: fl}
  - input: {x: fx}
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

```arrow {#poly-spec-paths}
steps:
  - null
  - {to: poly-sbbv.D1, to_anchor: bottom, angle: 290, length: 90, label: "flonum-specialized path"}
  - {to: poly-sbbv.B1, to_anchor: top, angle: 70, length: 90, label: "fixnum-specialized path"}
```

```timeline
poly-morph 1                                        # expand the operators
reveal 1                                            # the CFG of the expanded program
poly-morph 2, poly-join 1                           # the tests of x in *, and the union at the join point J
width poly-src=0 poly-cfg-col=0 poly-follow-col=1fr poly-sbbv-col=5fr, poly-join end, poly-morph 3   # SBBV, with the source CFG following, replaces the code and the CFG; highlight off
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
poly-sbbv ..end-2                                   # the rest of the specialization
poly-sbbv +1, poly-spec-paths +1                    # the path of a flonum x: one flonum? test
poly-sbbv +1, poly-spec-paths +1
```

# SBBV: Behavior with loops {#sbbv-with-loops}
:::columns
:::column {#vp-src width=5fr}
```code-morph {#vp-morph lang=scheme room=fit}
versions:
  - file: programs/vector-print.scm
    label: "vector-print.scm"
  - file: programs/vector-print-expanded.scm
    label: "expanded vector-length, vector-ref and +"
    highlight: changed
  - file: programs/vector-print-expanded.scm
    label: "expanded vector-length, vector-ref and +"
    highlight: [ref-check]
  - file: programs/vector-print-expanded.scm
    label: "expanded vector-length, vector-ref and +"
    highlight: [len-check]
  - file: programs/vector-print-expanded.scm
    label: "expanded vector-length, vector-ref and +"
```
:::/column
:::column {#vp-cfg-col width=4fr}
{.reveal}
```bbv-cfg {#vp-cfg program="programs/vector-print.bbv" height=500}
```
:::/column
:::column {#vp-follow-col width=0}
```bbv-cfg {#vp-follow program="programs/vector-print.bbv" follow=vp-sbbv height=480}
show: [label]
```
:::/column
:::column {#vp-sbbv-col width=0}
```bbv-anim {#vp-sbbv program="programs/vector-print.bbv" algorithm=sbbv heuristic=arithmetic limit=2 intervals=true vector_bounds=false direction=LR height=480}
show: [label, context, code]
thresholds: [0, 1, maxfix-1, maxfix]
paths:
  - versions: [L1, B1, C1, I1, J1, N1, D1, G1, M1]
  - versions: [L6, B4, C3, I3, J3, N3, D3, G3, M3]
```
:::/column
:::/columns

```arrow {#vp-absint}
steps:
  - null
  - {to: vp-cfg.C, to_anchor: right, angle: 75, length: 240, label: "abstract interpretation can remove this test"}
  - {to: vp-cfg.L, to_anchor: left, angle: 200, length: 160, label: "but not this one"}
  - null
```

```arrow {#vp-heads}
steps:
  - null
  - {to: vp-sbbv.L1, to_anchor: bottom, angle: 290, length: 110, label: "vector? check on the first iteration"}
  - null
  - {to: vp-sbbv.L2, to_anchor: bottom, angle: 290, length: 110, label: "unrolling the loop, no more check"}
  - null
```

```arrow {#vp-merges}
steps:
  - null
  - {to: vp-sbbv.L3, to_anchor: bottom, angle: 290, length: 110, label: "merge"}
  - {to: vp-sbbv.B2, to_anchor: bottom, angle: 290, length: 110, label: "merge will make this path unreachable"}
  - null
  - {to: vp-sbbv.L5, to_anchor: bottom, angle: 290, length: 110, label: "merge"}
  - {to: vp-sbbv.B3, to_anchor: bottom, angle: 290, length: 110, label: "will become unreachable"}
  - null
  - {to: vp-sbbv.C3, to_anchor: bottom, angle: 290, length: 110, label: "this path has already been explored"}
  - null
```

```arrow {#vp-paths}
steps:
  - null
  - {to: vp-sbbv.J1, to_anchor: top, angle: 70, length: 110, label: "unrolled first iteration"}
  - {to: vp-sbbv.J3, to_anchor: bottom, angle: 290, length: 110, label: "hot loop"}
  - {to: vp-sbbv.L6, to_anchor: bottom, angle: 290, length: 110, label: "eliminated vector? check"}
  - null
```

```timeline
vp-morph 1                                          # expand vector-length, vector-ref and +
reveal 1                                            # the CFG of the expanded program
vp-morph 2, vp-absint 1                             # the vector? test of vector-ref: abstract interpretation removes it
vp-morph 3, vp-absint 2                             # the vector? test of vector-length, at the loop head: it stays
width vp-src=0 vp-cfg-col=0 vp-follow-col=1fr vp-sbbv-col=10fr, vp-absint end, vp-morph 4   # SBBV, with the source CFG following, replaces the code and the CFG; highlight off
vp-sbbv 1..2                                        # A specialized, L1 queued
vp-heads 1                                          # the first version of the loop head
vp-sbbv 3..4                                        # L1 specialized: its vector? test stays
vp-sbbv 5, vp-heads 2
vp-sbbv 6..26                                       # first iteration; M1 queues L2 (i: fx {1})
vp-heads 3                                          # the second version of the loop head
vp-sbbv 27..28                                      # L2 specialized: its vector? test is removed
vp-sbbv 29, vp-heads end
vp-sbbv 30..46                                      # second iteration; L3 queued, L is over the limit
vp-merges 1                                         # L3 will be merged
vp-merges 2                                         # the path from L2 will become unreachable
vp-sbbv 47, vp-merges 3                             # L2 and L3 merge into L4 (widened)
vp-sbbv 48..67                                      # L4 specialized, its path queues L5; over the limit again
vp-merges 4                                         # L5 will be merged
vp-merges 5                                         # the path from L4 will become unreachable
vp-sbbv 68, vp-merges 6                             # L4 and L5 merge into L6
vp-sbbv 69..71                                      # L6 specialized; before B4 jumps to C3
vp-sbbv 72, vp-merges 7                             # C3 is reused
vp-sbbv 73                                          # done
vp-merges +1
vp-sbbv 74, vp-paths 1                              # path: the unrolled first iteration
vp-sbbv 75, vp-paths 2                              # path: the hot loop, after the merges
vp-paths 3                                          # its loop head has no vector? check
vp-sbbv 73, vp-paths end                            # back to the final graph, no highlight
```
