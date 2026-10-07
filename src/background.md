# Abstract Interpretation {layout=title}

# Union of Incoming Contexts {#union-of-incoming-contexts}

# Narrowing of Outgoing Contexts {#narrowing-of-outgoing-contexts}

# Abstract Interpretation of `findv` {#findv-absint}

:::columns
:::column {#findv-ai-src width=1fr}
```code-morph {#findv-ai-morph lang=scheme room=fit}
versions:
  - file: programs/background-findv-expanded.scm
    label: "expanded operators"
  - file: programs/background-findv-expanded.scm
    label: "expanded operators"
    highlight: [vec-check, fix-check, ovf-check, flo-check, ref-vec, ref-lo, ref-hi, ref-fix]
  - file: programs/background-findv-absint.scm
    label: "expanded operators"
    highlight: [vec-check, bound-check, ref-fix]
```
:::/column
:::column {#findv-ai-cfg width=0}
```abstract-interp-anim {#findv-ai program="programs/findv-absint.bbv"}
direction: LR
show: [label, context, code]
panel: [worklist, history]
panel_at: below
history: [S.i]
prims: {pred: {args: [any, any], result: bool}}
vector_bounds: false
thresholds: [sign, maxfix-1, maxfix]
```
:::/column
:::/columns

```timeline
findv-ai-morph +1
width findv-ai-src=0 findv-ai-cfg=1fr       # the code makes room for the analysis
findv-ai ..end                              # the analysis, one frame per step
width findv-ai-src=1fr findv-ai-cfg=0
findv-ai-morph +1   # back to the code: the checks it proved redundant
findv-ai-arrows 1   # the check removable by Static Basic Block Versioning
findv-ai-arrows 2   # the check removable by Lambda Versioning
findv-ai-arrows 3   # the check removable by vector-extended contexts
```

```arrow {#findv-ai-arrows curve=0}
steps:
  - null
  - to: vec-check
    to_anchor: top
    angle: 15
    length: 340
    label: "removable by Static Basic Block Versioning"
  - to: ref-fix
    to_anchor: right
    angle: 0
    length: 300
    label: "removable by Lambda Versioning"
  - to: bound-check
    to_anchor: right
    angle: 0
    length: 260
    label: "removable by vector-extended contexts"
```
