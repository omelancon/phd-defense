import sys
def p(x):
    return x * x + x
def run(n, x):
    acc = 0
    for _ in range(n):
        acc += p(x)
    return acc
n, x = map(int, sys.stdin.read().split())
print(run(n, x))
