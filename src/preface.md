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
- Oops! Undefined behavior!

```timeline
reveal ..2
poly-morph ..2
poly-morph +1, reveal +1
poly-morph +1, reveal +1
poly-morph +1
poly-morph +1, reveal +1
```

# Example: My Favorite Polynomial (Attempt 2) {#lustre-polynomial}

{.reveal}
:::group
You turn to Lustre!

```code-morph {#poly-lustre lang=ada room=max}
versions:
  - file: programs/lustre-polynomial.lus
  - file: programs/lustre-polynomial.lus
    highlight: [real, error]
  - file: programs/lustre-polynomial.lus
    highlight: overflow
  - file: programs/lustre-polynomial-fxfl.lus
    highlight: [real-x, real-y]
```
:::

{.reveal}
- Statically typed
- Wrap-around on 32-bit overflow (with default C backend)
- `int` and `real` do not mix

```timeline
reveal +1                        # the int node, with its flows of inputs and outputs
poly-lustre +1, reveal +1        # a real input is a type error
poly-lustre +1, reveal +1        # the overflow
poly-lustre +1, reveal +1        # a second node for real, with its flows
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
Finally, the expected result! But what is the catch?

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
- dynamic languages (Scheme, JavaScript, Python) check types at run time
  {.reveal}
  - type checks
  - overflow checks
- More flexible, but degrades performance
::: /column
::: /columns

```timeline
reveal 1                      # the question and the program
reveal +1, perf-morph +1      # dynamic languages; operators expanded
reveal +1, perf-morph +2      # type checks highlighted
reveal +1, perf-morph +1      # overflow checks highlighted
reveal +1, perf-morph -2      # more flexible...
```

# Object of this Talk {.center}

```statement {note="* In this talk, mostly type checks. In general, any branching test."}
How to deduce **information ahead of time** about a program to **remove run-time checks***?
```

# Table of Contents {.toc}

{.reveal}
1. ## Background on Static Analysis
2. ## Static Basic Block Versioning (SBBV)
3. ## Lambda Versioning (ΛV)
4. ## Experimental Evaluation
5. ## Future Work