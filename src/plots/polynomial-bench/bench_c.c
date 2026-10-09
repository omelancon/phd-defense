#include <stdio.h>
#include <stdlib.h>
__attribute__((noinline)) int p(int x) { return x * x + x; }
int main(int argc, char **argv) {
  long n = atol(argv[1]), acc = 0;
  for (long i = 0; i < n; i++) acc += p(i & 1023);
  printf("%ld\n", acc);
  return 0;
}
