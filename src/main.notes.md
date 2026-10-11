# performance-of-dynamic-languages

Related work, revealed after "... but degrades performance": gradual typing is a trade-off between
the two.

Siek & Taha, "Gradual Typing for Functional Languages", Scheme Workshop 2006. The programmer
chooses, with type annotations: "the cost of dynamism is "pay-as-you-go", so partially annotated
programs enjoy the benefits of static typing to the degree that they are annotated."
They list "the Bigloo [6, 36] dialect of Scheme" among the languages with such a mix.

Its run-time cost at the boundaries (Takikawa et al., "Is Sound Gradual Typing Dead?", POPL 2016,
Section 7): "In the context of current implementation technology, sound gradual typing is dead."
(Fair to add: their Section 7 is titled "Long Live Sound Gradual Typing".)

Contrast: this thesis asks for no annotation, keeps the flexibility, and only removes checks.

# intuition-on-static-analysis

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

# static-analysis-overview

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

# union-of-incoming-contexts

The context at the entry of C is the union of what A and B send it. Thresholds 0, 1, maxfix-1, maxfix: a bound that is not a threshold moves up to the next one, so the chain of C.i is finite: {0}, [0, 1], [0, maxfix-1], [0, maxfix], [0, ∞).

# narrowing-of-outgoing-contexts

A test tells each branch something new. On the true branch of x <= 10, x is in [0, 10] (so also a fixnum); on the false branch it is in [11, ∞). On the true branch of fixnum?(x), x is a fixnum; on the false branch, anything but a fixnum.

# overview-of-static-basic-block-versioning

Related work, revealed last: Chevalier-Boisvert & Feeley, "Simple and Effective Type Check Removal
through Lazy Basic Block Versioning", ECOOP 2015.
- A JIT technique: it "lazily generates type-specialized versions of basic blocks on-the-fly";
  "Versions for a particular context are only generated when that context is encountered during
  execution." Laziness is what bounds the versions; ahead of time, SBBV has no execution to guide it.
- At the version limit there is no merge: failing an existing compatible version, "a fully generic
  version of the block that assigns the unknown type to all live variables will be generated."
  SBBV merges contexts instead, so what they have in common is kept.
- Results: "A limit of 5 versions per block eliminates 71% of total type tests, compared to 16% for
  the analysis".
- Intraprocedural, as SBBV: it "only tracks type information intraprocedurally" (what ΛV adds later).

# sbbv-context-table

Thesis Appendix D, Figure 14 (Section 4.5, "Putting the Results in Context"). Node.js 21.7.1,
Bigloo 4.6a, Gambit 4.9.4-377, Chez Scheme 9.5.1, Racket 7.2. The programs have Scheme and
JavaScript versions from previous work, a subset of the benchmark suite. Without SBBV, Gambit and
Bigloo beat Node.js on every program except almabench (V8 has special optimizations for floats
and arrays), up to 24× faster on bague, and are in the same ballpark as Chez Scheme. So the gains
of SBBV are measured against compilers that are already competitive. The slide opens without the
SBBV columns; the step adds them, and the highlight moves to the fastest times with SBBV.

# sbbv-setup

SBBV was added as a pass in the CFG pipeline of two independently developed, mature optimizing
ahead-of-time Scheme to C compilers, which are also back ends of compilers for JavaScript and
Python. They already implement constant folding, inlining, flat closures, lambda lifting: any
gain is on top of years of tuning. Merge heuristic: similarity (merge the most similar versions).
To count checks, every primitive is redefined by a macro with explicit inline checks (type,
overflow, array bounds), so both compilers perform the same checks in the same order; counting
runs are separate from timing runs. Timing: perf stat, each run at least 5 s, 50 runs with the 5
highest and 5 lowest removed; relative standard deviation at most 0.24% (macro) and 2.20% (micro).
Intel Core i7-7700K, 48 GB, Debian 10. Micro benchmarks only shed light on specific behaviors.
The detour (key f) shows that the baseline compilers are already competitive with Node.js and
Chez Scheme.

# plot-sbbv-checks

Thesis Figure 9. Lower is better. Macro benchmarks are solid lines, micro benchmarks dashed.
Checks executed on the R7RS benchmarks, relative to compilation without any optimization. The
"No BBV" point is the compilers' own optimizations. A limit of 1 is equivalent to a static
analysis and already removes checks. A limit of 2 adds duplication: on macro benchmarks, 54% of
checks are gone with Gambit and 62% with Bigloo. Past a limit of about 10 the decrease is slow:
the similarity heuristic needs many versions. Hover a point for its exact value.

# plot-sbbv-size

Thesis Figure 10. Lower is better. Macro benchmarks are solid lines, micro benchmarks dashed.
Program size is measured in bytes, relative to executables compiled without SBBV. At low limits
check elimination outweighs code duplication, as in the polynomial example, so executables get
smaller: Gambit at limit 1, Bigloo up to limit 4. Then size grows with the limit: 5× (Gambit) and
1.7× (Bigloo) at limit 20 on macro benchmarks. Size is the main reason the limit cannot be raised
indefinitely to remove every check. With the similarity heuristic this trade-off is suboptimal:
ideally a merge heuristic keeps the useful versions and removes most checks within a low limit.
Hover a point for its exact value.

# plot-sbbv-time

Thesis Figure 11. Lower is better. Macro benchmarks are solid lines, micro benchmarks dashed.
The y axis does not start at 0 (it starts at 0.6, the thesis draws a broken axis). The size
trade-off shows in Gambit: time drops quickly at low limits, reaches its minimum at limit 2
(89%), then slowly rises and stabilizes (93% for Gambit). Bigloo stays at about 91% from limit 1.
Micro benchmarks under Gambit keep improving, down to 71% at limit 10. The best limit varies per
benchmark (Appendix D), so a single static limit is suboptimal: per-function limits under the
programmer's control may be preferable. Checks are cheap in these compilers (pointer tagging):
there is more to gain where a type check reads memory (Python, Ruby). Hover a point for its exact
value.

# plot-sbbv-compile-time

Thesis Figure 12. Lower is better. Macro benchmarks are solid lines, micro benchmarks dashed.
Compile time is the whole compilation, relative to compiling without SBBV. It grows roughly
linearly with the limit, more steeply in Gambit (8.4× at limit 20 on macro benchmarks): Gambit
compiles each Scheme module as a single C function, so code duplication puts additional strain on
the C compiler; Bigloo reaches 3.4× at limit 20 on macro benchmarks. At a limit of one version,
Gambit programs are smaller and compile faster (0.8×). Hover a point for its exact value.

# core-idea-of-lambda-versioning

Related work, flashed after the core idea (one step, then gone).

Bodík, Gupta & Soffa, "Interprocedural Conditional Branch Elimination", PLDI 1997.
- The closest idea: "The entry splitting transformation creates multiple entries to a procedure,
  and the exit splitting transformation allows a procedure to return control to one of several
  return points in the caller." Exit splitting "requires passing additional return addresses to
  the procedure."
- Same motivation as square: "the value returned is often selected by an if-statement. This value
  may again be checked by the caller."
- Differences: C programs; a demand-driven question per branch, of the form "(v relop c)" (a
  variable compared with a constant), with a code growth budget per branch. ΛV propagates whole
  type and interval contexts, under the version limit and merges of SBBV.

Saleil & Feeley, "Interprocedural Specialization of Higher-Order Dynamic Languages Without Static
Analysis", ECOOP 2017.
- Lazy BBV in a Scheme JIT, made interprocedural: "When a call site is executed, a new version of
  the callee is generated".
- Returns are specialized too, on the type of the result only: "Our implementation limits Pcall to
  the type of the returned value". With both, the compiler can "remove 46% more checks than
  intraprocedural BBV".
- Difference: ΛV specializes return points ahead of time, on whole contexts discovered at the exit
  sites, with no run-time dispatch on the returned value.

# lv-no-time-slide

Thesis Sections 3.2.2, 3.5.1 and 3.7. ΛV turns every function into a hyperfunction: after CPS
conversion and lambda lifting, each block is a lambda that receives its live variables and its
return points as continuations (K[0], K[1], K[2]), so a call passes one continuation per return
point. The example is square from the thesis (Section 3.2.2), specialized with three entry points
(any, fx, fl), each dispatching to a specialized entry point of the * operator, itself a
hyperfunction; the call to * is a tail call, so square passes its own return points through.
The slide elides the bodies of A2 and A3 (thesis listing: A2 calls *.fx×arg[0] with K[0] and
K[2], A3 calls *.fl×arg[0] with K[1]).
There is no native implementation of hyperfunctions yet: the experiments use the Scheme macro of
Appendix B, which only shows that a working interface takes little effort, and programs in this
representation always run slower than their source. Execution time would measure the macro, not
ΛV, so type checks are the metric. Native designs exist (Section 3.6): extended flat closures and
pre-allocated return point tables cost a single indirection per call and return. Implementing
hyperfunctions natively is future work.

# lv-setup

Thesis Section 3.5.1 and Appendix C. ΛV works on source code: preprocessing (desugaring, alpha
conversion, assignment conversion, then CPS and lambda lifting) turns every lambda into an
unspecialized hyperfunction, and ΛV outputs valid Scheme, run here on Gambit with the
hyperfunction macro. SBBV is reimplemented by disabling the interprocedural parts of ΛV, so the
gap between the two is exactly what interprocedural propagation removes. Unlike Chapter 2, no
other compiler optimization interferes (no inlining or constant folding noise), and only type
checks are tracked: no interval analysis, so no overflow or bounds checks. Benchmarks: the R7RS
subset used for SBBV plus fact20 and fact100; micro under 400 lines, macro over. Each one is
profiled without specialization, then with ΛV and SBBV at version limits 1 to 10, for the three
merge heuristics and both operator representations. compiler (about 12,000 lines, 1,500
functions) is left out of the geometric means: it timed out (2.5 hours) at high limits. Compile
time is the versioning algorithm only, on an Intel Core i7-7700K with 48 GB, Debian 10. The
detour (key e) explains why execution time is not measured.

# plot-lv-typechecks

Thesis Figures 18 (micro) and 19 (macro), hyperfunction operators panels, arithmetic merge
heuristic only. Lower is better. Type checks executed, relative to compilation without
versioning. SBBV (dashed) always inlines operators; it is drawn for reference (the thesis draws it
only in the inlined panels). Micro (left): ΛV leaves 26% of the type checks at limit 3, 3.7% at
limit 7 and 1.2% at limit 10, while SBBV goes from 48% at limit 3 to 47% at limit 10: the gap is
what interprocedural propagation removes. In most micro benchmarks ΛV
eliminates all redundant type checks with a limit of about 7: the function checks its argument
types once, then runs a hot loop without type checks, barring overflow. Optimal at: ack (5),
array1 (6), fact20 (3), fib (3), fibfp (3), quicksortfl (10), sum (7), sumfp (7), tak (10).
Macro (right): about half of all type checks are eliminated at a limit of 3 (48% left, against
57% for SBBV), little gain after. What remains: type checks on values read from lists and
vectors, which the contexts do not track. Benchmarks that benefit the most use numeric
arithmetic heavily (almabench, earley, maze, nucleic, slatex). The thesis also shows the random
and similarity heuristics, both worse (see the merge heuristics section). Hover a point for its
exact value.

# plot-lv-compile-time

Thesis Figures 20 (micro) and 21 (macro), hyperfunction operators panels, arithmetic merge
heuristic only. Lower is better. Compile time is the execution of the ΛV (or SBBV) algorithm
only, relative to SBBV with a limit of one version; SBBV (dashed, inlined operators) is kept for
reference. The two panels have their own y scales. Growth is linear: on micro benchmarks about
+1.1 per version with hyperfunctions, against +1.5 with inlined operators and +0.35 for SBBV,
consistent with Chapter 2. On macro benchmarks at limit 10: 14× SBBV at limit 1 with
hyperfunctions, against 17× with inlined operators. The extra cost of ΛV comes from exploring
more contexts and back-propagating exit contexts to call sites to create specialized return
points. Hyperfunction operators let a specialization be reused by every call site with the same
calling context, while inlined operators are respecialized at each call site. The random
heuristic is the most expensive (thesis). Hover a point for its exact value.

# plot-lv-versions

Thesis Figures 22 (micro) and 23 (macro), hyperfunction operators panels, arithmetic merge
heuristic only. Lower is better. The y axis is the average number of versions of each basic block
of the source program; SBBV (dashed, inlined operators) is kept for reference. With inlined
operators there is a double duplication cost, one from inlining and one from ΛV; hyperfunctions
avoid it by sharing specializations. Micro: about 4 versions per block at limit 10, against 6
with inlined operators; the effect is small at low limits since some operators are used only
once. Macro: always fewer versions than with inlined operators, 1.2 against 2.0 at limit 1 and
about 4 against 7.4 at limit 10. This suggests outlining (Komondoor and Horwitz): extract similar
code segments as one hyperfunction, specialize it once, then inline it back after ΛV, which could
further reduce compile time; left as future work. Hover a point for its exact value.

# operators-compile-time

Thesis Figures 20 (micro) and 21 (macro), ΛV only, arithmetic merge heuristic, the two suites
combined: geometric mean over the 15 micro and 12 macro benchmarks, computed from the geometric
means of the suites weighted by their sizes. Lower is better.
Compile time is the execution of the ΛV algorithm, relative to SBBV with a limit of one version.
Solid: operators as functions (hyperfunctions). Dashed: inlined operators. A specialization of an
operator is computed once and reused by every call site with the same calling context, while
inlined operators are respecialized at each call site. At limit 10: about 12.3 against 16.1 over
all benchmarks (micro 11.3 against 15.8, macro 13.7 against 16.6). Hover a point for its exact
value.

# future-native

Related work on implementing multi-return functions natively.

Shivers & Fisher, "Multi-return function call", ICFP 2004 (journal version: JFP 2006).
- "the ability to specify multiple return points when calling a function".
- Implementation: "we pass each return point as a frame-pointer/return-pc pair of values, either in
  registers or stack slots, just as with parameters". "Multi-return function call is a
  pay-as-you-go feature."
- They never call it "multi-barrelled": that term comes from Thielecke's double-barrelled CPS
  (two continuations).

Saleil & Feeley, ECOOP 2017: the closure is "extended to store a pointer to a set of entry points
(entry point table) instead of a single entry point address in the closure"; for returns, "the
continuation entry point table address is pushed to the stack instead of a single return address
introducing no additional cost." (Extended flat closures first appeared, for entry points only, in
Saleil & Feeley, Scheme Workshop 2015: "Our implementation does not currently propagate the type of
the return values.")

FORTRAN 77 (ANSI X3.9-1978): a CALL can pass "An alternate return specifier, of the form *s"
(Section 15.6.2.3), and RETURN e returns to the e-th of them (Section 15.8.3). Shivers & Fisher
credit it themselves: "the idea of passing multiple return points to a function goes back at least
as far as FORTRAN 77", but "these subroutines are not reentrant".
