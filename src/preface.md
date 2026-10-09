# Preface {#preface-title layout=title}
Some background

# Background {.small}

:::columns
:::column {#avg-src width=2fr}

```code-steps {#avg-code lang=scheme file="programs/average.scm"}
steps:
  - [sum-add, n-add, div, cdr] # every operator with extra work
```
:::/column
:::column {#avg-cfg width=0}

```bbv-cfg {#avg-graph program="programs/average.bbv" height=510}
```
:::/column
:::column {#dyn-notes width=3fr}
{.reveal}
- Object of study: dynamic programming languages
- *Dynamic*: behaviour decided at run time
- Example: `+` on integers, floats, mixed arithmetic (even strings in some languages)
- Run-time decisions: extra work in every operator
- Goal: remove these dynamic checks, for efficiency without losing safety
:::/column
:::column {#cfg-notes width=0}
{.reveal}
- Program analysis: programs as *control-flow graph*
- More flexible than 2D text
- Reason about paths taken through the program:
  {.reveal}
  - What values can a variable take?
  - What checks were already performed?
  - How will this variable be used down the line?
- Answering these allow more efficient code generation
:::/column
:::/columns

```arrow {#types to_anchor=right}
steps:
  - null
  - {to: n-add, to_anchor: 330, angle: 330, length: 260, label: "n counts elements: always a fixnum (small integer)"}
  - {to: elem, angle: 330, length: 150, label: "an element of the list: depends on the caller"}
  - {to: ints, angle: 345, length: 250, label: "here, integers (fixnums)"}
  - {to: flos, angle: 345, length: 190, label: "here, floats (flonums)"}
  - {to: sum-add, angle: 330, length: 150, label: "fixnum + fixnum, flonum + flonum, or even 0 + 36.6"}
  - null
```

```arrow {#cfg-parts}
steps:
  - null
  - {to: avg-graph.B, to_anchor: 200, length: 60, label: "basic block"}
  - {to: avg-graph.A->L, to_anchor: left, length: 60, label: "jump"}
  - {to: avg-graph.L, to_anchor: left, length: 40, label: "branch"}
  - null
```

```timeline
reveal 1                  # dynamic languages
reveal 2                  # dynamic behaviour
reveal 3                  # `+`: highlight the two additions
types 1..5                # what each `+` receives, one arrow per step
reveal 4, types end, avg-code 1   # all the operators that decide at run time
reveal 5                  # removing the checks
width avg-src=0 dyn-notes=0 avg-cfg=2fr cfg-notes=3fr, reveal 6   # the CFG replaces the code
cfg-parts 1..3            # basic block, jump, branch: one arrow per step
reveal 7, cfg-parts end   # the arrow goes away with the next bullet
reveal ..end
```

# Static Analysis of Dynamic Languages

{.reveal}
This Scheme program looks for the first element that satisfies a predicate in a vector.

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
- **will come back to this example**
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
reveal ..end-1, findv-morph ..end        # each sub-bullet with its highlight
reveal ..end
```

# Table of Content {.large}

{.reveal}
1. ## Background on Static Analysis
2. ## Static Basic Block Versioning (SBBV)
3. ## Lambda Versioning (ΛV)
4. ## Technique Improvements
5. ## Experimental Evaluation
6. ## Future Work