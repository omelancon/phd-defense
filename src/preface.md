# Preface {#preface-title layout=title}
First, some background

# Example: My Favorite Polynomial

{.reveal}
Suppose you want to compute values of your favorite polynomial: $p(x) = x^2 + x$.

{.reveal}
:::group
Naturally, you write a program. You choose C because you heard it's fast!

```code-morph {#poly-morph lang=c room=max}
versions:
  - file: programs/c-polynomial.c
  - file: programs/c-polynomial-tests.c
  - file: programs/c-polynomial-tests.c
    highlight: answer3
  - file: programs/c-polynomial-tests.c
    highlight: int
  - file: programs/c-polynomial-fxfl-tests.c
  - file: programs/c-polynomial-fxfl-tests.c
    highlight: answer3
  - file: programs/c-polynomial-fxfl-overflow.c
    highlight: overflow
```
:::

{.reveal}
- Statically typed for `int`
- Workaround gymnastics for `float`
- It does not cover overflows!

```timeline
reveal ..2
poly-morph ..2
poly-morph +1, reveal +1
poly-morph +1, reveal +1
poly-morph +1
poly-morph +1, reveal +1
```

# Example: My Favorite Polynomial (Attempt 2)

{.reveal}
:::group
You turn to OCaml!

```code-morph {#poly-morph2 lang=ocaml room=max}
versions:
  - file: programs/ocaml-polynomial.ml
  - file: programs/ocaml-polynomial-tests.ml
  - file: programs/ocaml-polynomial-tests.ml
    highlight: error
  - file: programs/ocaml-polynomial-fxfl.ml
```
:::

{.reveal}
- Compile-time type error for `float` input
- There is a fix, but...
- Still a silent wrap-around for `int` overflow

```timeline
reveal +1
poly-morph2 ..1
poly-morph2 +1, reveal +1
poly-morph2 +1, reveal +1
reveal +1
```
# Example: My Favorite Polynomial (Attempt 3)

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