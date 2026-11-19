/* Driver for the C code that lv6 generates from bench.lus (lv6 -2c -2csf): N / 1024 reactions
   of the node bench, with the hidden input x at every reaction; each reaction calls p 1024
   times. unity.inc (written by run.sh) includes the generated files of everything but the node p,
   so that gcc compiles the reactions as one unit; the node p (bench_p.c) is compiled
   separately, so that it stays an out-of-line call, as p is in the other programs. */
#include <stdio.h>
#include "unity.inc"
#define PER_REACTION 1024
int main(void) {
  long n; int x;
  if (scanf("%ld %d", &n, &x) != 2 || n % PER_REACTION) return 1;
  bench_bench_ctx_type *ctx = bench_bench_ctx_new_ctx();
  _integer acc = 0;
  for (long i = 0; i < n / PER_REACTION; i++) bench_bench_step(x, &acc, ctx);
  printf("%d\n", acc);  /* Lustre int is 32 bits: the sum wraps around */
  return 0;
}
