# Data of the ΛV paper figures

A copy of the data behind Figures 9 and 10 of the ΛV paper (`lv_paper/paper.pdf`, "Optimizing
Dynamic Languages using Multi-Return Function Calls"), which supersede the type check results of the
thesis. The slide `src/plots/lv-typechecks.md` reads these files through the `lv_paper_typechecks_*`
functions of `src/plots/thesis_plots.py`. The files are copies and are not meant to be regenerated
here.

## `lv/`

Copied verbatim from `lv_paper/assets/experiments/scripts/lambda-versioning/benchmarks/results/data/`
(lambda-versioning at commit `27ecbca58c50d358559e9a9839042d4c49adf999`, the one the paper's plots
were last generated for: `lv_paper/assets/experiments/scripts/.plot-stamp`), where
`make plot-paper` writes them and `plot-area.sh --bigloo` draws the figures from them.

| File | Paper figure | Content |
|---|---|---|
| `ALL.typechecks.arithmetic.no-hetero-ds.csv` | 9 | ΛV, benchmarks that do not use heterogeneous data structures (10) |
| `ALL.typechecks.arithmetic.hetero-ds.csv` | 10 | ΛV, benchmarks that use heterogeneous data structures (17) |
| `all-bigloo.csv` | 9, 10 | Bigloo, every benchmark |

The `ALL.typechecks.*` files have a header: `version` (version limit, 0 = without ΛV), `geomean`,
`min`, `max` (over the benchmarks of the group, of the run-time type checks relative to the limit 0
run) and `count` (benchmarks). ΛV with the arithmetic merge heuristic and operators as hyperfunctions.

`all-bigloo.csv` has a header: `benchmark`, `typechecks`, `relative-typechecks` (relative to the
limit 0 run of the same benchmark). The red line of a figure is the geometric mean of
`relative-typechecks` over the benchmarks of its group (0.356 and 0.550), computed by
`thesis_plots.py` as `aggregate-bigloo.sh --geomean` does. The benchmarks without heterogeneous data
structures are `NO_HETERO_DS_BENCHMARKS` of `lambda-versioning/benchmarks/makefile`: ack, array1,
fact20, fact100, fib, fibfp, quicksortfl, sum, sumfp, tak.

Table 1 of the paper (compile time) is written out in `src/plots/lv-compile-time.md`, from the
`\ResCompileTime` and `\ResLoC` values of `lv_paper/assets/experiments/values.tex`.
