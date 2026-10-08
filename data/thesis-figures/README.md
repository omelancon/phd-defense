# Data of the thesis evaluation figures

A one-time copy of the data behind the evaluation figures of the thesis (`phd-these/these.pdf`).
The slides in `src/plots/` read these files through `src/plots/thesis_plots.py`. The files are
copies and are not meant to be regenerated.

## `sbbv/`: Static Basic Block Versioning (thesis Figures 9 to 12)

Copied verbatim from `phd-these/figures/sbbv-plot/scripts/`, where `plot.sh` draws them.

| File | Thesis figure | Metric |
|---|---|---|
| `checks.csv` | 9 | run-time checks (type, overflow, bounds) relative to compilation without any optimization |
| `size.csv` | 10 | program size relative to compilation without SBBV |
| `time.csv` | 11 | execution time relative to compilation without SBBV |
| `compile-time.csv` | 12 | compile time relative to compilation without SBBV |

No header. Columns: version limit (0 = without SBBV), Gambit macro, Gambit micro, Bigloo macro,
Bigloo micro. Every value is a geometric mean over the benchmarks of the suite.

## `lv/`: Lambda Versioning (thesis Figures 18 to 23)

Generated once from the raw per-benchmark results in
`lambda-versioning/benchmarks/results/data/results.lv*.csv` with the aggregation step of
`lambda-versioning/benchmarks/plot-geomeans.sh`, that is, for each suffix and kind:

    ./aggregate-benchmark.sh --geomean SUFFIX.KIND results/data geomeans.SUFFIX.KIND.csv ""

(`SKIP_COMPILER` unset, as for the thesis). The thesis imports the PDFs drawn from these files
(`phd-these/figures/import_plot.sh`); the values were checked against those PDFs.

File names: `geomeans.HEURISTIC[.VARIANT].KIND.csv` where

- `HEURISTIC` is the merge heuristic: `arithmetic`, `similarity` or `random`;
- `VARIANT` is absent for ΛV with operators as hyperfunctions, `inline-rts` for ΛV with inlined
  operators, `sbbv` for SBBV (inlined operators);
- `KIND` is `micro` or `macro`.

No header. Columns, in the order written by `aggregate-benchmark.sh`:

1. version limit (0 = without ΛV/SBBV, 1 to 10)
2. `typechecks`: run-time type checks relative to the limit 0 run (Figures 18, 19)
3. `compile-time`: compile time relative to SBBV with a limit of 1 (Figures 20, 21)
4. `entry-points-time`: time spent on entry points, same baseline
5. `versions`: average versions per basic block of the source program (Figures 22, 23)
6. `source-versions`
7. `generated-versions`
8. `unused-versions`
9. `merge`: merges relative to SBBV with a limit of 1

`-1` marks a value that could not be computed (every metric but the type checks at limit 0).
