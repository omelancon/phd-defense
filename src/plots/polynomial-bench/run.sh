#!/bin/sh
# Polynomial benchmark of the preface slide "Attempt 3": each program calls p(x) = x*x + x
# N times in a loop (p is kept out of line; the sum of the results is printed so the loop
# cannot be removed as dead code). Prints the median wall-clock time of each program.
# Results of 2026-10-09 (N = 360000000, gcc 13.3, OCaml 4.14.1, Gambit v4.9.8, CPython 3.13.16)
# are in ../polynomial-bench.csv.
set -e
cd "$(dirname "$0")"
N=${1:-360000000}
gcc -O2 -o c.exe bench_c.c
ocamlopt -o ml.exe bench_ml.ml
gsc -exe -o scm.exe bench_scm.scm
python3 - "$N" <<'PY'
import statistics, subprocess, sys, time
n = sys.argv[1]
for name, cmd, k in [("C", ["./c.exe"], 5), ("OCaml", ["./ml.exe"], 5),
                     ("Gambit", ["./scm.exe"], 5), ("Python", ["python3", "bench_py.py"], 3)]:
    ts = []
    for _ in range(k):
        t = time.perf_counter()
        out = subprocess.run(cmd + [n], capture_output=True, text=True, check=True).stdout.strip()
        ts.append(time.perf_counter() - t)
    print(f"{name:7} {statistics.median(ts):7.2f} s   (sum {out})")
PY
rm -f c.exe ml.exe scm.exe bench_ml.cm* bench_ml.o
