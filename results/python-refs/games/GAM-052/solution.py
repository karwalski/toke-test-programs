Test 1: 10 → expected '2'. Zeckendorf of 10 = 8+2, smallest is 2. ✓
Test 2: 1 → expected '1'. 1 is a Fibonacci number... but expected is '1', not 'Losing position'.
Test 3: 3 → expected 'Losing position'. 3 is Fibonacci. ✓

So 1 is special case. Let me handle it.

```python
def fibonacci_up_to(n):
    fibs = []
    a, b = 1, 2
    while a <= n:
        fibs.append(a)
        a, b = b, a + b
    return fibs

def zeckendorf(n, fibs):
    result = []
    i = len(fibs) - 1
    while n > 0 and i >= 0:
        if fibs[i] <= n:
            result.append(fibs[i])
            n -= fibs[i]
            i -= 2
        else:
            i -= 1
    return result

def solve(stones):
    if stones == 0:
        return "Losing position"
    if stones == 1:
        return "1"
    fibs = fibonacci_up_to(stones)
    if stones in fibs:
        return "Losing position"
    z = zeckendorf(stones, fibs)
    return str(z[-1])

stones = int(input().strip())
print(solve(stones))
```