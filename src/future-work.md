# Future Work {#future-work-title layout=title}

# Native Multi-Return Functions {#future-native .small}

::::: columns
:::: column {width=1fr}
::: columns
::: column
{#native-points .reveal}
- Efficient native implementation
- Here is a work-in-progress
::: /column
::: /columns

{.reveal}
```related-work-note
title: "Related work explored some designs:"
items:
  - Multi-barrelled CPS (Shivers 2004)
  - Extended flat closure (Saleil 2017)
  - Alternate returns (FORTRAN 77)
```
:::: /column
:::: column {#native-code-col width=0}
```code {#native-code lang=tasm file="programs/hvm-hyperfunction.hvm" title="HVM: a VM for hyperfunctions"}
```
:::: /column
:::: column {#native-room width=1fr}
:::: /column
::::: /columns

```arrow {#native-arrow}
steps:
  - null
  - {from: "native-points[2]", from_anchor: right, to: native-code, to_anchor: left}
```

```timeline
reveal 1                                                           # first bullet
reveal 2, native-arrow 1, width native-code-col=1fr native-room=0  # second bullet; the code opens in place of the empty column
reveal 3, native-arrow 0                                           # related work, at the bottom left
```


# Heterogeneous Datastructures {#future-heterogeneous .small}

::::: columns
:::: column {width=1fr}
{#het-points .reveal}
- **Most remaining checks** in benchmarks are on values read from **heterogeneous structures** (vector, pair, box, etc.)
- Include **mutability/escapability** information in contexts to track the type of values within structures
:::: /column
:::: column {#het-col width=0}
```code {#het-code lang=scheme file="programs/heterogeneous.scm"}
```

```bbv-anim {#het-sbbv program="programs/heterogeneous.bbv" algorithm=sbbv limit=1 direction=TB height=375}
show: [label, context, code]
```
:::: /column
:::: column {#het-room width=1fr}
:::: /column
::::: /columns

```arrow {#het-lost}
steps:
  - null
  - {to: het-sbbv.C1, to_anchor: right, angle: 0, length: 110, label: "type of 42 lost"}
  - null
```

```timeline
reveal 1, width het-col=1fr het-room=0      # first bullet; the example opens in place of the empty column
het-sbbv 1..end                             # the SBBV run, one frame per step
het-lost 1                                  # the value read back has type any
reveal 2, het-lost 2                        # second bullet; the arrow goes away
```
