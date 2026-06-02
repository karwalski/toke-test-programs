import math

n, r = map(int, input().split())

nCr = math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
nPr = math.factorial(n) // math.factorial(n - r)

print(nCr)
print(nPr)