# Program Analysis

{.reveal}
- Consider this Scheme function that sums number up from $1$ to $n$:

{.reveal-with}
```code {lang=scheme file="programs/sum-to-n.scm"}
```

::::: columns
:::: column {width=1fr}
::detour-badge{ref=sum-to-n-assert}
{.reveal}
- It fails if `n` is not a number
- It returns a non-negative integer
::::
:::: column {width=1fr}
::detour-badge{ref=useful}
::::
:::::

::::: detour {#sum-to-n-assert label="What can we assert about this program?" key=q at=1 badge=step}
# What can we assert about this function?

:::: columns
::: column {width=2fr}
```code {lang=scheme file="programs/sum-to-n.scm"}
```
:::
::: column {width=3fr}
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
  - from: '#sum-to-n-facts > li:nth-child(5)'
    to: result
  - from: '#sum-to-n-facts > li:nth-child(6)'
    to: n-test
```

{#sum-to-n-facts .reveal}
- `i` starts at $0$
- `i` stays a non-negative integer
- `sum` starts at $0$
- `sum` stays non-negative
- `sum-to-n` returns a non-negative integer
- `sum-to-n` fails if `n` is not a number
:::
::::

```timeline
reveal 2              # the arrow (fragment 1) and the first fact appear together
reveal 3, facts-arrow 1
reveal 4, facts-arrow 2
reveal 5, facts-arrow 3
reveal 6, facts-arrow 4
reveal 7, facts-arrow 5
```

:::::

::: detour {#useful label="Why is that useful?" key=w at=3 badge=step}
# Why
...
:::
