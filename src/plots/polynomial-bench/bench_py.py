import sys
def p(x):
    return x * x + x
def run(n):
    acc = 0
    for i in range(n):
        acc += p(i & 1023)
    return acc
print(run(int(sys.argv[1])))
