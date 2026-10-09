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

{.reveal}
:::group
You decide to try dynamic languages.

::: columns
::: column
```code {lang=scheme file="programs/scheme-polynomial-tests.scm" title="Scheme"}
```
::: /column
::: column
```code {lang=python file="programs/python-polynomial-tests.py" title="Python"}
```
::: /column
::: /columns
:::

{.reveal}
It just works! But what is the catch?

{.reveal}
```plot {backend=vega source="plots/polynomial_bench.py:polynomial_bench" width=11 height=1.6}
```

# Performance of Dynamic Languages

{.reveal}
What makes dynamic languages slower?

::: columns
::: column {width=5fr}
{.reveal-with}
```code-morph {#perf-morph lang=scheme room=fit}
versions:
  - file: programs/scheme-polynomial.scm
    label: "polynomial.scm"
  - file: programs/scheme-polynomial-expanded.scm
    label: "expanded operators"
    highlight: changed
  - file: programs/scheme-polynomial-expanded.scm
    label: "expanded operators"
  - file: programs/scheme-polynomial-expanded.scm
    label: "expanded operators"
    highlight: [x-fix, x-flo, y-fix, y-flo]
  - file: programs/scheme-polynomial-expanded.scm
    label: "expanded operators"
    highlight: [x-ovf, y-ovf]
```
::: /column
::: column {width=6fr}
{.reveal}
- static languages (C, OCaml) test types at compile time
- dynamic languages (Scheme, JavaScript, Python) check them at run time
  {.reveal}
  - type checks
  - overflow checks
- More flexible...
- ... but degrades performance
::: /column
::: /columns

```timeline
reveal 1                      # the question and the program
reveal +1, perf-morph +1      # operators expanded; static languages
reveal +1, perf-morph +1      # dynamic languages, nothing highlighted
reveal +1, perf-morph +1      # type checks highlighted
reveal +1, perf-morph +1      # overflow checks highlighted
reveal +1, perf-morph -2      # more flexible...
reveal +1                     # ... but slower
```

# Object of this Thesis {.center}

```statement
How can an ahead-of-time compiler **eliminate run-time checks**, so that dynamic languages
**run as fast as static ones** without **losing their flexibility**?
```

# Table of Content {.large}

{.reveal}
1. ## Background on Static Analysis
2. ## Static Basic Block Versioning (SBBV)
3. ## Lambda Versioning (ΛV)
4. ## Technique Improvements
5. ## Experimental Evaluation
6. ## Future Work