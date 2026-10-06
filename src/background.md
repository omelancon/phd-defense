# Program Analysis of Dynamic Languages

{.reveal}
This Scheme program looks for the first odd number in a vector.

::: columns
::: column {width=5fr}
{.reveal-with}
```code-morph {#findv-morph lang=scheme room=fit}
versions:
  - file: programs/background-findv.scm
    label: "findv.scm"
  - file: programs/background-findv-expanded.scm
    label: "expanded operators"
    highlight: changed
  - file: programs/background-findv-expanded.scm
    label: "expanded operators"
    highlight: [vec-check, fix-check, ovf-check, flo-check, ref-vec, ref-lo, ref-hi]
  - file: programs/background-findv-optimized.scm
    label: "redundant checks removed"
  - file: programs/background-findv-optimized.scm
    label: "redundant checks removed"
    highlight: lifted
  - file: programs/background-findv-optimized.scm
    label: "redundant checks removed"
    highlight: [fx-add, fx-gte]
  - file: programs/background-findv-optimized.scm
    label: "redundant checks removed"
    highlight: vref
  - file: programs/background-findv-optimized.scm
    label: "redundant checks removed"
    highlight: ref-fix
```
::: /column
::: column {width=4fr}
{.reveal}
- operators implicit run-time checks
- many of which are redundant
- eliminating them can make the program more efficient
  {.reveal}
  - lift `vector?` out of the loop
  - fixnum arithmetic
  - eliminated bound checks
  - can this test be removed?
::: /column
::: /columns

```arrow {#why}
steps:
  - null
  - {to: vec-check, angle: 315, length: 260, label: "checked at every iteration"}
  - {to: fix-check, angle: 315, label: "index arithmetic will always be on small integers"}
  - {to: ref-vec, angle: 45, length: 220, label: "already checked in findv"}
  - {to: ref-hi, angle: 45, label: "findv known to return valid index"}
  - null
```

```timeline
reveal 1                               # the program
reveal +1, findv-morph +1              # expanded operators, what they add highlighted
reveal +1, findv-morph +1              # the redundant checks
why ..+4                               # why four of them are redundant, one arrow each
reveal +1, findv-morph +1, why end     # redundant checks removed, nothing highlighted
reveal ..end, findv-morph ..end        # each sub-bullet with its highlight
```

# Abstract interpretation of `findv` {#findv-absint}

:::columns
:::column {#findv-ai-src width=1fr}
```code-morph {#findv-ai-morph lang=scheme room=fit}
versions:
  - file: programs/background-findv-expanded.scm
    label: "expanded operators"
  - file: programs/background-findv-absint.scm
    label: "expanded operators"
    highlight: [vec-check, bound-check]
```
:::/column
:::column {#findv-ai-cfg width=0}
```abstract-interp-anim {#findv-ai program="programs/findv-absint.bbv" height=470}
direction: TB
show: [label, context, code]
panel: [worklist, history]
history: [L.i]
prims: {pred: {args: [any, any], result: bool}}
vector_bounds: false
thresholds: [sign, maxfix-1, maxfix]
```
:::/column
:::/columns

```timeline
width findv-ai-src=0 findv-ai-cfg=1fr       # the code makes room for the analysis
findv-ai ..end                              # the analysis, one frame per step
width findv-ai-src=1fr findv-ai-cfg=0
findv-ai-morph +1   # back to the code: the checks it proved redundant
```
