# ΛV Experimental Results {#lv-experiments-title layout=title}

# ΛV: Experimental Setup {#lv-setup .small}

Implemented source to source: Scheme in, specialized Scheme out, run on **Gambit**

```dot
digraph setup {
  rankdir=LR; nodesep=0.3; ranksep=0.4;
  node [shape=box, style=rounded, fontsize=18, margin="0.2,0.1"];
  edge [arrowsize=0.7];

  src [label="Scheme\nbenchmarks", shape=note, style=solid];
  pre [label="CPS +\nlambda lifting"];
  lv [label="ΛV", fontsize=22, style="rounded,filled,bold", color="#648FFF", fillcolor="#648FFF40", penwidth=2];
  sbbv [label="SBBV\n(ΛV without\ninterprocedural parts)", style="rounded,dashed", penwidth=1.5];
  out [label="specialized Scheme\n(hyperfunctions)"];
  run [label="Gambit +\nhyperfunction macro"];
  prof [label="profiled run:\ncount type checks", shape=note, style=solid];

  src -> pre; pre -> lv; pre -> sbbv [style=dashed];
  lv -> out; sbbv -> out [style=dashed];
  out -> run -> prof;
}
```

::::: columns
::: column {width=1fr}
{.reveal}
:::: group
### 27 benchmarks

12 macro, over 400 lines

15 micro: `fib`, `tak`, `sum`...
::::
::: /column
::: column {width=1fr}
{.reveal}
:::: group
### 60 configurations

3 heuristics, 2 operator forms

Version limit 1 to 10
::::
::: /column
::: column {width=1fr}
{.reveal}
:::: group
### 3 measures

Type checks executed

Compile time, code duplication
::::
::: /column
:::::

::: detour {#lv-no-time label="Why no execution time?" key=e}
# Why No Execution Time? {#lv-no-time-slide .small}

::: columns
::: column {width=1fr}
{#hf-points .reveal}
- **Multi-return functions** through CPS: one continuation per return point
- **No native implementation** of hyperfunctions: a Scheme macro emulates them, slower than the source program
::: /column
::: column {width=1fr}
```code {#hf-code lang=racket file="programs/hyperfunction-square.scm" title="square, calling * as a hyperfunction"}
```
::: /column
::: /columns

```arrow {#hf-arrow}
steps:
  - null
  - {from: "hf-points[1]", from_anchor: bottom, to: hf-code, to_anchor: left}
  - null
```

```timeline
reveal 1, hf-arrow 1     # first bullet, arrow to the hyperfunction
reveal 2, hf-arrow 2     # second bullet, arrow gone
```

::: /detour

::include{file="plots/lv-typechecks.md"}
::include{file="plots/lv-compile-time.md"}
::include{file="plots/lv-versions.md"}
