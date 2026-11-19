#include <stdio.h>
/* noipa: keep p a real call (no inlining, and no interprocedural analysis that would let gcc
   see that p is pure and hoist the call with its loop-invariant argument out of the loop) */
__attribute__((noipa)) int p(int x) { return x * x + x; }
int main(void) {
  long n; int x;
  if (scanf("%ld %d", &n, &x) != 2) return 1;
  long acc = 0;
  for (long i = 0; i < n; i++) acc += p(x);
  printf("%ld\n", acc);
  return 0;
}
