#!/bin/sh
# Polynomial benchmark of the preface slide "Attempt 3": each program calls p(x) = x*x + x
# N times in a loop and prints the sum of the results (so the loop cannot be removed). N and x
# are read from standard input, so no compiler can specialize the loop on them; p is kept out of
# line in every language (noipa in C, since with noinline gcc sees that p is pure and hoists the
# call out of the loop). Lustre has no loop: see bench.lus and lus_driver.c.
# Runs are interleaved (one run of each program per round); prints the median wall-clock time.
#   usage: ./run.sh [N] [ROUNDS]     N must be a multiple of 1024 (one Lustre reaction = 1024 calls)
# Results of 2026-11-19 (N = 919227392, chosen so that C takes about 0.5 s; x = 5; 5 rounds;
# gcc 13.3.0, lv6 v6.113.1, Gambit v4.9.8, CPython 3.13.18) are in ../polynomial-bench.csv.
set -e
cd "$(dirname "$0")"
N=${1:-919227392}
ROUNDS=${2:-5}
X=5
gcc -O2 -o c.exe bench_c.c
gsc -exe -o scm.exe bench_scm.scm
rm -rf lus && mkdir lus && cp bench.lus lus/
( cd lus && lv6 bench.lus -n bench -2c -2csf >/dev/null 2>&1 &&
  ls *.c | grep -v -e '^bench_p\.c$' -e '_loop' | sed 's/.*/#include "&"/' > unity.inc &&
  gcc -O2 -I. -o ../lus.exe ../lus_driver.c bench_p.c )
python3 - "$N" "$X" "$ROUNDS" <<'PY'
import statistics, subprocess, sys, time
n, x, rounds = sys.argv[1], sys.argv[2], int(sys.argv[3])
progs = [("C", ["./c.exe"]), ("LV6", ["./lus.exe"]),
         ("Gambit", ["./scm.exe"]), ("Python", ["python3", "bench_py.py"])]
times = {name: [] for name, _ in progs}
outs = {}
for r in range(rounds):
    for name, cmd in progs:
        t = time.perf_counter()
        out = subprocess.run(cmd, input=f"{n} {x}\n", capture_output=True, text=True, check=True).stdout.strip()
        times[name].append(time.perf_counter() - t)
        outs[name] = out
    print(f"round {r + 1}: " + "  ".join(f"{k} {v[-1]:.3f}" for k, v in times.items()), flush=True)
expected = int(n) * (int(x) * int(x) + int(x))
for name, _ in progs:
    got = int(outs[name])
    ok = got == expected or (name == "LV6" and got % 2**32 == expected % 2**32)
    print(f"{name:7} {statistics.median(times[name]):8.3f} s   (sum {outs[name]}{'' if ok else '  WRONG'})")
PY
rm -rf c.exe scm.exe lus.exe lus
