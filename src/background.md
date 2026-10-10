# Static Analysis {#abstract-interpretation-title layout=title}

What is it and why it falls short?

# Intuition on Static Analysis {.small}

{.reveal}
Even to the human eye, some tests beg to be removed.

::: columns
::: column {width=5fr}
{.reveal-with}
```code-morph {#findv-morph lang=scheme room=fit}
versions:
  - file: programs/background-findv.scm
    label: "findv.scm"
  - file: programs/background-findv-expanded.scm
    label: "expanded operators"
    highlight: changed
  - file: programs/background-findv-expanded.scm
    label: "expanded operators"
    highlight: [vec-check, fix-check, ovf-check, flo-check, ref-vec, ref-lo, ref-hi]
  - file: programs/background-findv-optimized.scm
    label: "redundant checks removed"
  - file: programs/background-findv-optimized.scm
    label: "redundant checks removed"
    highlight: lifted
  - file: programs/background-findv-optimized.scm
    label: "redundant checks removed"
    highlight: [fx-add, fx-gte]
  - file: programs/background-findv-optimized.scm
    label: "redundant checks removed"
    highlight: vref
  - file: programs/background-findv-optimized.scm
    label: "redundant checks removed"
    highlight: ref-fix
```
::: /column
::: column {width=4fr}
{.reveal}
- operators implicit run-time checks
- many of which are redundant
- eliminating them can make the program more efficient
  {.reveal}
  - lift `vector?` out of the loop
  - fixnum arithmetic
  - eliminated bound checks
  - can this test be removed?
- **will come back to this example**

{.reveal}
```related-work-note
title: "Inserting checks only where needed:"
items:
  - soft typing (Cartwright & Fagan 1991)
inline: true
```
::: /column
::: /columns

```arrow {#why}
steps:
  - null
  - {to: vec-check, angle: 315, length: 260, label: "checked at every iteration"}
  - {to: fix-check, angle: 315, label: "index arithmetic will always be on small integers"}
  - {to: ref-vec, angle: 45, length: 220, label: "already checked in findv"}
  - {to: ref-hi, angle: 45, label: "findv known to return valid index"}
  - null
```

```timeline
reveal 1                               # the program
reveal +1, findv-morph +1              # expanded operators, what they add highlighted
reveal +1, findv-morph +1              # the redundant checks
why ..+4                               # why four of them are redundant, one arrow each
reveal +1, findv-morph +1, why end     # redundant checks removed, nothing highlighted
reveal ..8, findv-morph ..end           # each sub-bullet with its highlight
reveal 9                                 # will come back to this example
reveal 10                                # related work: soft typing
```

::: notes
Related work, revealed after "will come back to this example". Here the checks are written out and
the redundant ones removed; the other way is to start from a typed view and insert checks only
where they are needed.

Cartwright & Fagan, "Soft Typing", PLDI 1991: "a type checker need not reject programs containing
"ill-typed" phrases. Instead, the type checker can insert explicit run-time checks". No
annotation: "The system should not require the programmer to declare the types of any program
phrases or operations."

For Scheme (Wright & Cartwright, "A Practical Soft Type System for Scheme", TOPLAS 1997): "the type
checker typically eliminates 90% of the run-time checks that are necessary for safe execution
without soft typing", and "most soft typed programs run 10 to 15% faster than their dynamically
typed counterparts".

Two limits that this thesis addresses:
- the fixnum? test on the result of findv needs a specialized copy of code; they ruled duplication
  out: "uninhibited cloning is impractical, as it can exponentially increase program size" (SBBV
  and ΛV bound it with a version limit);
- arithmetic: "too weak to effectively eliminate dispatches in generic arithmetic operators"
  (because + on small integers may overflow into a bignum).
:::

# Static Analysis Overview {.small}

:::columns
:::column {width=2fr}
{.reveal}
- Based on abstract interpretation
- Technique for sound approximation of program semantics
- Executes on abstract values (sets of concrete values)

```related-work-note {#rw-cousot}
title: "Related work:"
items:
  - Abstract interpretation (Cousot & Cousot 1977)
flash: true
```

{.reveal}
**Algorithm sketch:**

{.reveal}
- Propagate abstract values through the control-flow graph
- Start from an entry point with a generic context
- A block's context is *at least* the union of its predecessors'
- Branches narrow contexts flowing to their successors
- Repeat until a fixed point is reached

{.reveal}
**Dynamic languages**

{.reveal}
- Wide range of run-time behaviors: approximation is coarse.
:::/column
:::column {width=1fr}
```bbv-cfg {#overview-cfg program="programs/overview-diamond.bbv" height=430 follow=overview-run}
```
:::/column
:::column {width=0}
```bbv-anim {#overview-run program="programs/overview-diamond.bbv" algorithm=sbbv}
events: [done]
paths:
  - versions: [A1, B1, C1, D1]
  - versions: [A1]
  - versions: [B1]
  - versions: [C1]
  - versions: [D1]
```
:::/column
:::/columns

```arrow {#overview-cfg-parts}
steps:
  - null
  - {to: overview-cfg.A, to_anchor: top, length: 60, label: "control-flow graph"}
  - {to: overview-cfg.B, to_anchor: 200, length: 60, label: "basic block"}
  - {to: overview-cfg.B->D, to_anchor: left, length: 60, label: "jump"}
  - null
```

```arrow {#overview-parts}
steps:
  - null
  - {to: overview-cfg.A, to_anchor: top, angle: 120, length: 90, label: "entry point"}
  - {to: overview-cfg.D, to_anchor: left, angle: 200, length: 90, label: "join point"}
  - {to: overview-cfg.A, to_anchor: right, angle: 290, length: 80, label: "branch point"}
  - null
```

```timeline
reveal +1
reveal +1                          # sound approximation
reveal +1                          # abstract values
rw-cousot 1                        # related work: Cousot & Cousot 1977, over the room of the next blocks
reveal +2, rw-cousot end, overview-run 1, overview-cfg-parts 1   # note gone; "Algorithm sketch" with "Propagate": every block lit, the CFG named
overview-cfg-parts 2, overview-run 3               # basic block
overview-cfg-parts 3, overview-run 0               # jump
reveal +1, overview-cfg-parts end, overview-run 2, overview-parts 1   # lights and arrows go away: entry point
reveal +1, overview-parts 2, overview-run 5        # union at the join point
reveal +1, overview-parts 3, overview-run 2        # narrowing at the branch point
reveal +1, overview-parts end, overview-run 0      # fixed point
reveal +2                         # "Dynamic languages" with its point
```

::: notes
Related work, flashed after "Executes on abstract values" (one step, then gone).

Cousot & Cousot, "Abstract interpretation: a unified lattice model for static analysis of programs
by construction or approximation of fixpoints", POPL 1977, pp. 238-252.
- Same goal as this thesis, check elimination (Section 9.2, p. 247): "the compiler should ensure that
  arrays are subscripted only by indices within bounds"; when the analysis is imprecise, "runtime
  subscript tests may be inserted in the absence of certainty" (p. 248).
- Branches: "tests behave like filters" (p. 248), what the next slides call narrowing at branches.
- Careful with words: the paper's *narrowing* (Δ, Section 9) is a different operator, used on
  decreasing sequences. The widening (∇) of the next slide is defined in Section 9, which they
  credit to their earlier work (Section 2): "Section 9 introduces finite fixpoint approximation
  methods to be used when Kleene's sequences are infinite, Cousot[76]."
:::


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
  - nodes: {s0: operand, s1: null, i01: past, i12: operand}
    edges: {s1->i01: null}
    caption: "[0, 1] ∪ [1, 2]"
  - nodes: {i02: union}
    edges: {i01->i02: union, i12->i02: union}
    caption: "[0, 1] ∪ [1, 2] = [0, 2]"
  - nodes: {i02: past, mf1: result}
    edges: {i02->mf1: widen}
    caption: "2 is not a threshold: widened to [0, maxfix-1]"
  - nodes: {i01: past, i12: null, mf1: past, mf1b: operand}
    edges: {i12->i02: null}
    caption: "[0, maxfix-1] ∪ [1, maxfix]"
  - nodes: {mf: result}
    edges: {mf1->mf: union, mf1b->mf: union}
    caption: "[0, maxfix-1] ∪ [1, maxfix] = [0, maxfix]"
  - nodes: {mf1: past, mf1b: null, mf: past, mfpb: operand}
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
union-ai 1..6             # C receives {1} from B: union
union-lattice 1..2        # on the lattice: {0} ∪ {1}
union-ai 7..10            # C receives [1, 2] from B: union with widening
union-lattice 3..4        # on the lattice: [0, 1] ∪ [1, 2]
union-lattice 5, maxfix-note 1   # widening to [0, maxfix-1], and what maxfix is
maxfix-note end            
union-ai 11..14           # C receives [1, maxfix] from B: union
union-lattice 6           # on the lattice: [0, maxfix-1] ∪ [1, maxfix]
union-lattice 7
union-ai 15..18           # C receives [1, maxfix+1] from B: union with widening
union-lattice 8..10       # on the lattice: [0, maxfix] ∪ [1, maxfix+1], then widening
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
reveal 1..2                                  # the idea
narrow-cmp 1                              # A: x is a nonnegative integer
narrow-cmp 2                              # x <= 10 holds: x in [0, 10] in B
narrow-cmp 3                              # x <= 10 fails: x in [11, ∞) in C
narrow-cmp ..end                          # B and C, then the fixed point
width narrow-cmp-col=0 narrow-type-col=2fr, reveal 3   # the second example replaces the first
narrow-type 1                             # A: x can be anything
narrow-type 2                            # fixnum?(x) holds: x is a fixnum in B
narrow-type 3                             # fixnum?(x) fails: x is anything but a fixnum in C
narrow-type ..end                         # B and C, then the fixed point
```

::: notes
A test tells each branch something new. On the true branch of x <= 10, x is in [0, 10] (so also a fixnum); on the false branch it is in [11, ∞). On the true branch of fixnum?(x), x is a fixnum; on the false branch, anything but a fixnum.
:::

# Static Analysis of `findv` {#findv-absint}

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
