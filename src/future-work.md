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
::: callout
Related work explored some designs:

- Multi-barrelled CPS (Shivers 2004)
- Extended flat closure (Saleil 2017)
- Alternate returns (FORTRAN 77)
:::
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

