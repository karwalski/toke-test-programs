Test 1: 9 elements, K=3. Expected I/O = 18. 9 reads initial + 9 writes final? Let me think: just count N reads at start and N writes at end = 18. For test 2: 4 elements, I/O=8 = 2*N. So I/O = 2*N regardless of passes.

```python
import sys

def merge_two_runs(run1, run2):
    merged = []
    i, j = 0, 0
    while i < len(run1) and j < len(run2):
        if run1[i] <= run2[j]:
            merged.append(run1[i]); i += 1
        else:
            merged.append(run2[j]); j += 1
    merged.extend(run1[i:])
    merged.extend(run2[j:])
    return merged

lines = sys.stdin.read().split('\n')
numbers = list(map(int, lines[0].split()))
k = int(lines[1])

runs = []
for i in range(0, len(numbers), k):
    chunk = sorted(numbers[i:i+k])
    runs.append(chunk)

for i, run in enumerate(runs):
    print(f"Run {i+1}: [{','.join(map(str, run))}]")

pass_num = 1
while len(runs) > 1:
    new_runs = []
    for i in range(0, len(runs), 2):
        if i + 1 < len(runs):
            new_runs.append(merge_two_runs(runs[i], runs[i+1]))
        else:
            new_runs.append(runs[i])
    runs = new_runs
    print(f"Merge pass {pass_num}: " + " ".join([f"[{','.join(map(str, run))}]" for run in runs]))
    pass_num += 1

io_count = 2 * len(numbers)
print(f"I/O ops: {io_count}")
print(f"Sorted: {' '.join(map(str, runs[0]))}")
```