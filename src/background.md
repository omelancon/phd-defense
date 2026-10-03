# Motivation: Program Analysis

{.reveal}
- Consider this Scheme function that sums number up from $1$ to $n$:

{.reveal-with}
```code {lang=scheme file="programs/sum-to-n.scm"}
```

::::: columns
:::: column {width=1fr}
::detour-badge{ref=sum-to-n-assert}
{.reveal}
- fails if `n` is not a number
- returns a non-negative integer
::::
:::: column {width=1fr}
::detour-badge{ref=sum-to-n-usage}
{.reveal}
- type check elimination
- bound check elimination
::::
:::::

:::::: detour {#sum-to-n-assert label="What can we assert about this function?" key=q at=1 badge=step}
# What can we assert about this function?

::::: columns
:::: column {width=2fr}
```code {lang=scheme file="programs/sum-to-n.scm"}
```
::::
:::: column {width=3fr}
{.reveal}
:::group
**To the human eye**

$\sum_{i=1}^{n} i \geqslant 0$
:::

{.reveal}
**A more methodical approach**

{.reveal}
```arrow {#facts-arrow color=detour curve=0.2 from_anchor=left}
steps:
  - from: '#sum-to-n-facts > li:nth-child(1)'
    to: i-init
  - from: '#sum-to-n-facts > li:nth-child(2)'
    to: i-step
  - from: '#sum-to-n-facts > li:nth-child(3)'
    to: sum-init
  - from: '#sum-to-n-facts > li:nth-child(4)'
    to: sum-step
  - from: '#sum-to-n-conclusion > li:nth-child(1)'
    to: result
  - from: '#sum-to-n-conclusion > li:nth-child(2)'
    to: n-test
```

{#sum-to-n-facts .reveal}
- `i` starts at $1$
- `i` stays a positive integer
- `sum` starts at $0$
- `sum` stays non-negative

{.reveal}
**Conclusion**

{#sum-to-n-conclusion .reveal}
- `sum-to-n` returns a non-negative integer
- `sum-to-n` fails if `n` is not a number
::::
:::::

```timeline
reveal 1                  # To the human eye
reveal 2                  # A more methodical approach
reveal 4                  # the arrow (fragment 3) with the first fact: i-init
reveal 5, facts-arrow 1   # i-step
reveal 6, facts-arrow 2   # sum-init
reveal 7, facts-arrow 3   # sum-step
reveal 8                  # Conclusion
reveal 9, facts-arrow 4   # result
reveal 10, facts-arrow 5  # n-test
```

::::::

::::: detour {#sum-to-n-usage label="Why is that useful?" key=w at=3 badge=step}
# Why is that useful?

:::: columns
::: column {width=2fr}
```code {lang=scheme file="programs/sum-to-n-usage.scm"}
```
:::
::: column {width=3fr}
123
:::
::::


:::::
