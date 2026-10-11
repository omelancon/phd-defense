# performance-of-dynamic-languages

**Related work**: gradual typing is a trade-off between the two.

Siek & Taha, "Gradual Typing for Functional Languages", Scheme Workshop 2006. The programmer
chooses, with type annotations: "the cost of dynamism is "pay-as-you-go", so partially annotated
programs enjoy the benefits of static typing to the degree that they are annotated."
They list "the Bigloo [6, 36] dialect of Scheme" among the languages with such a mix.

Its run-time cost at the boundaries (Takikawa et al., "Is Sound Gradual Typing Dead?", POPL 2016,
Section 7): "In the context of current implementation technology, sound gradual typing is dead."
(Fair to add: their Section 7 is titled "Long Live Sound Gradual Typing".)

Contrast: this thesis asks for no annotation, keeps the flexibility, and only removes checks.

# intuition-on-static-analysis

**Related work**:  Here the checks are written and removed; the other way is to start from no type checks. When the type assignment algorithm fails, the soft type system inserts explicit run-time checks

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

**Related work**: Cousot & Cousot, "Abstract interpretation: a unified lattice model for static analysis of programs
by construction or approximation of fixpoints", POPL 1977, pp. 238-252.
- Same goal as this thesis, check elimination (Section 9.2, p. 247): "the compiler should ensure that
  arrays are subscripted only by indices within bounds"; when the analysis is imprecise, "runtime
  subscript tests may be inserted in the absence of certainty" (p. 248).
- Branches: "tests behave like filters" (p. 248), what the next slides call narrowing at branches.
- Careful with words: the paper's *narrowing* (Δ, Section 9) is a different operator, used on
  decreasing sequences. The widening (∇) of the next slide is defined in Section 9, which they
  credit to their earlier work (Section 2): "Section 9 introduces finite fixpoint approximation
  methods to be used when Kleene's sequences are infinite, Cousot[76]."

# overview-of-static-basic-block-versioning

**Related work**: Chevalier-Boisvert & Feeley, "Simple and Effective Type Check Removal
through Lazy Basic Block Versioning", ECOOP 2015.
- A JIT technique: generates contexts on the fly;
- At the **version limit** there is no merge: failing an existing compatible version, "a **fully generic version** of the block that assigns the unknown type to all live variables will be generated."
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

Optims Bigloo and Gambit already have:
  - constant folding
  - **inlining**
  - flat closures
  - lambda lifting

**Gains are on top of years of tuning.** 

Timing: perf stat, each run at least 5 s, 50 runs with the 5
highest and 5 lowest removed; relative standard deviation at most 0.24% (macro) and 2.20% (micro).

Intel Core i7-7700K, 48 GB, Debian 10.

# plot-sbbv-checks

At limit of 2: -54% (Gambit) and -62% (Bigloo) check on macro.

# plot-sbbv-size

At low limits check elimination outweighs code duplication. Gambit at limit 1, Bigloo up to limit 4.

Then size grows with the limit: 5× (Gambit) and 1.7× (Bigloo) at limit 20 on macro benchmarks.

# plot-sbbv-time

Time drops quickly at low limits, reaches its **minimum at limit 2
(89%), then rises and stabilizes (93% for Gambit)**. Bigloo stays at about 91% from limit 1.

# plot-sbbv-compile-time

Gambit (8.4× at limit 20 on macro benchmarks): Gambit
compiles each Scheme module as a single C function. At limit 1, Gambit programs are smaller and compile faster (0.8×).

Bigloo reaches 3.4× at limit 20 on macro benchmarks.

# core-idea-of-lambda-versioning

**Related work**

Bodík, Gupta & Soffa, "Interprocedural Conditional Branch Elimination", PLDI 1997.
- Closest idea: Entry/exit splitting. Exit splitting "**requires passing additional return addresses** to the procedure."
- Differences: C programs; a demand-driven per branch, code growth budget per branch. Not whole-program.

Saleil & Feeley, "Interprocedural Specialization of Higher-Order Dynamic Languages Without Static
Analysis", ECOOP 2017.
- When a call site is executed, a new version of the callee is generated".
- Returns are specialized too, on the type of the result only.
- LV, since AOT, converges to a finer-tuned call interface per function.

# lv-setup

No other compiler optimization interferes No interval analysis, so no overflow or bounds checks.

Intel Core i7-7700K with 48 GB, Debian 10

# plot-lv-typechecks

Optimal at: ack (5), array1 (6), fact20 (3), fib (3), fibfp (3), quicksortfl (10), sum (7), sumfp (7), tak (10).

Benchmarks that benefit the most use numeric arithmetic heavily (almabench, earley, maze, nucleic, slatex).

# plot-lv-compile-time

Growth is linear
- on micro benchmarks about +1.1 per version with hyperfunctions, against +1.5 with inlined operators and +0.35 for SBBV
- on macro benchmarks at limit 10: 14× SBBV at limit 1 with
hyperfunctions, against 17× with inlined operators.

# plot-lv-versions

Micro: about 4 versions per block at limit 10. 6 with inlined operators.

Macro: 1.2 (hyperfunctions) against 2.0 (inlined) at limit 1 and
about 4 against 7.4 at limit 10.

**Related work**: find duplicated code and factor it out as procedures. Observed here, and *future work for speeding compilation*.

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

**Related work**

Shivers & Fisher, "Multi-return function call", ICFP 2004 (journal version: JFP 2006).
- "the ability to specify multiple return points when calling a function".
- different kinds of tail calls

Saleil & Feeley, ECOOP 2017.
- the closure is "extended to store a pointer to a set of entry points
(entry point table) instead of a single entry point address.
- for returns, "the continuation entry point table address is pushed to the stack instead of a single return address
introducing no additional cost."
- First appeared, for entry points only, in Saleil & Feeley, Scheme Workshop 2015: "Our implementation does not currently propagate the type of
the return values."

FORTRAN 77 (ANSI X3.9-1978):
- a CALL can pass "An alternate return specifier"
- does not permit tail calls
