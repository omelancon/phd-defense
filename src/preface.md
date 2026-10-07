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
- Reason about paths taken through the program
:::/column
:::/columns

```timeline
reveal 1                  # dynamic languages
reveal 2                  # dynamic behaviour
reveal 3, fib-code 1      # `+`: highlight its expression
reveal 4, fib-code 2      # all the operators that decide at run time
reveal 5                  # removing the checks
width fib-src=0 dyn-notes=0 fib-cfg=2fr cfg-notes=3fr, reveal 6   # the CFG replaces the code
reveal 7
reveal 8
```
