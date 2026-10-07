# Preface {#preface .small}

:::columns
:::column {#fib-src width=2fr}

```code-steps {#fib-code lang=scheme file="programs/fib.scm"}
steps:
  - plus                      # `+` alone
  - [le, plus, sub1, sub2]    # every arithmetic and comparison operator
```
:::/column
:::column {#fib-cfg width=0}

```bbv-cfg {#fib-graph program="programs/fib.bbv" height=510}
```
:::/column
:::column {#dyn-notes width=3fr}
{.reveal}
- Object of study: dynamic programming languages
- *Dynamic*: behaviour decided at run time
- Example: `+` on integers, floats, mixed arithmetic (even strings in some languages)
- Run-time decisions: extra work in every operator
- Goal: remove these dynamic checks, for efficiency without losing expressiveness
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

```timeline
reveal 1                  # dynamic languages
reveal 2                  # dynamic behaviour
reveal 3, fib-code 1      # `+`: highlight its expression
reveal 4, fib-code 2      # all the operators that decide at run time
reveal 5                  # removing the checks
width fib-src=0 dyn-notes=0 fib-cfg=2fr cfg-notes=3fr, reveal 6   # the CFG replaces the code
reveal ..end
```

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