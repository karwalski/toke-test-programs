n = int(input())

# Initialize the first two Catalan numbers
catalan = [0] * (n + 1)
if n >= 0:
    catalan[0] = 1
if n >= 1:
    catalan[1] = 1

# Compute Catalan numbers using recurrence formula
# C(n) = sum(C(i) * C(n-1-i)) for i from 0 to n-1
for i in range(2, n + 1):
    catalan[i] = 0
    for j in range(i):
        catalan[i] += catalan[j] * catalan[i-1-j]

# Output the results
for i in range(n):
    print(f"C({i})={catalan[i]}")