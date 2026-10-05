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
    highlight: [vec-check, fix-check, flo-check, ref-vec, ref-lo, ref-hi]
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
  - vector access known to be safe
  - can this be removed?
::: /column
::: /columns

```timeline
reveal 1                               # the program
reveal +1, findv-morph +1              # expanded operators, what they add highlighted
reveal +1, findv-morph +1              # the redundant checks
reveal +1, findv-morph +1              # redundant checks removed, nothing highlighted
reveal ..end, findv-morph ..end        # each sub-bullet with its highlight
```
