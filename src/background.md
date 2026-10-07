# Abstract Interpretation {layout=title}

# Abstract Interpretation Overview {.small}

- Technique for sound approximation of program semantics.
- Executes the program on abstract values instead of concrete values.
  - Abstract values represent sets of concrete values.

**Algorithm sketch:**
- Start from an entry point with a generic context.
- Propagate abstract values through the control-flow graph.
  - A block's context is *at least* the union of its predecessors'.
  - Branches narrow contexts flowing to their successors.
- Repeat until a fixed point is reached.

**Dynamic languages**
- Wide range of possible run-time behaviors. Hence the approximation is often coarse.


# Union of Incoming Contexts {#union-of-incoming-contexts}

:::columns
:::column {width=3fr}
```abstract-interp-anim {#union-ai program="programs/union.bbv" height=390}
show: [label, context, code]
panel: [history]
panel_at: below
history: [C.i]
thresholds: [0, 1, maxfix-1, maxfix]
```
:::/column
:::column {width=2fr}
```hasse-anim {#union-lattice file="figures/interval-lattice.dot" height=495}
steps:
  - null
  - nodes: {s0: operand, s1: operand}
    caption: "{0} ∪ {1}"
  - nodes: {i01: result}
    edges: {s0->i01: union, s1->i01: union}
    caption: "{0} ∪ {1} = [0, 1]"
  - nodes: {s0: past, s1: null, i01: operand, i12: operand}
    edges: {s1->i01: null}
    caption: "[0, 1] ∪ [1, 2]"
  - nodes: {i02: union}
    edges: {i01->i02: union, i12->i02: union}
    caption: "[0, 1] ∪ [1, 2] = [0, 2]"
  - nodes: {i02: past, mf1: result}
    edges: {i02->mf1: widen}
    caption: "2 is not a threshold: widened to [0, maxfix-1]"
  - nodes: {i01: past, i12: null, mf1: operand, mf1b: operand}
    edges: {i12->i02: null}
    caption: "[0, maxfix-1] ∪ [1, maxfix]"
  - nodes: {mf: result}
    edges: {mf1->mf: union, mf1b->mf: union}
    caption: "[0, maxfix-1] ∪ [1, maxfix] = [0, maxfix]"
  - nodes: {mf1: past, mf1b: null, mf: operand, mfpb: operand}
    edges: {mf1b->mf: null}
    caption: "[0, maxfix] ∪ [1, maxfix+1]"
  - nodes: {mfp: union}
    edges: {mf->mfp: union, mfpb->mfp: union}
    caption: "[0, maxfix] ∪ [1, maxfix+1] = [0, maxfix+1]"
  - nodes: {mfp: past, pos: result}
    edges: {mfp->pos: widen}
    caption: "maxfix+1 is not a threshold: widened to [0, ∞)"
```
:::/column
:::/columns

```arrow {#maxfix-note}
steps:
  - null
  - to: union-lattice.mf1
    to_anchor: left
    angle: 107
    length: 115
    label: "maxfix: largest single-word int"
  - null
```

```timeline
union-ai 1..5             # A sends {0} to C, C sends it to B, B computes i + 1
union-lattice 1..2        # on the lattice: {0} ∪ {1}
union-ai 6                # C receives {1} from B: union
union-ai 7..9             # C sends [0, 1] to B, B computes [1, 2]
union-lattice 3..4        # on the lattice: [0, 1] ∪ [1, 2]
union-lattice 5, maxfix-note 1   # widening to [0, maxfix-1], and what maxfix is
maxfix-note end
union-ai 10               # C receives [1, 2] from B: union with widening
union-ai 11..13           # C sends [0, maxfix-1] to B, B computes [1, maxfix]
union-lattice 6           # on the lattice: [0, maxfix-1] ∪ [1, maxfix]
union-lattice 7
union-ai 14               # C receives [1, maxfix] from B: union
union-ai 15..17           # C sends [0, maxfix] to B, B computes [1, maxfix+1]
union-lattice 8..10       # on the lattice: [0, maxfix] ∪ [1, maxfix+1], then widening
union-ai 18               # C receives [1, maxfix+1] from B: union with widening
union-ai ..end            # one more round changes nothing: the fixed point, [0, ∞)
```

::: notes
The context at the entry of C is the union of what A and B send it. Thresholds 0, 1, maxfix-1, maxfix: a bound that is not a threshold moves up to the next one, so the chain of C.i is finite: {0}, [0, 1], [0, maxfix-1], [0, maxfix], [0, ∞).
:::

# Narrowing of Outgoing Contexts {#narrowing-of-outgoing-contexts}

:::columns
:::column {#narrow-cmp-col width=2fr}
```abstract-interp-anim {#narrow-cmp program="programs/narrow-cmp.bbv" height=420}
show: [label, context, code]
```
:::/column
:::column {#narrow-type-col width=0}
```abstract-interp-anim {#narrow-type program="programs/narrow-type.bbv" height=420}
show: [label, context, code]
```
:::/column
:::column {width=3fr}
{.reveal}
- gain information at conditional branches
  {.reveal}
  - arithmetic comparisons
  - type checks
:::/column
:::/columns

```timeline
reveal 1                                  # the idea
narrow-cmp 1                              # A: x is a nonnegative integer
narrow-cmp 2, reveal 2                    # x <= 10 holds: x in [0, 10] in B
narrow-cmp 3                              # x <= 10 fails: x in [11, ∞) in C
narrow-cmp ..end                          # B and C, then the fixed point
width narrow-cmp-col=0 narrow-type-col=2fr   # the second example replaces the first
narrow-type 1                             # A: x can be anything
narrow-type 2, reveal 3                   # fixnum?(x) holds: x is a fixnum in B
narrow-type 3                             # fixnum?(x) fails: x is anything but a fixnum in C
narrow-type ..end                         # B and C, then the fixed point
```

::: notes
A test tells each branch something new. On the true branch of x <= 10, x is in [0, 10] (so also a fixnum); on the false branch it is in [11, ∞). On the true branch of fixnum?(x), x is a fixnum; on the false branch, anything but a fixnum.
:::

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
