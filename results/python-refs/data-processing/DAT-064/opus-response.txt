For test 1: systematic 3 with 6 rows, expected output rows 1,a and 4,d (indices 0 and 3). So including header, that's the header plus data rows at index 0, 3. My code does that already... wait the failure shows actual is '3,c\n6,f' meaning indices 2,5. So the data list includes header at index 0 then iterated 0,3 gave header and "3,c"... let me reconsider.

Actually data[0]=header, data[3]="3,c". Output got header, "3,c", "6,f" - that's data[0],data[3],data[6]? No only 7 entries (header+6). data[0],data[3],data[6] = header,"3,c","6,f". But expected is header,"1,a","4,d" = data[0],data[1],data[4].

So systematic should: include header, then take rows 0, k, 2k... from data rows (excluding header). Let me fix.

```python
import sys
import csv
import random
from io import StringIO

def read_input():
    return [line.rstrip('\n') for line in sys.stdin]

def parse_strategy_line(line):
    parts = line.split()
    strategy = parts[0]
    if strategy == 'systematic':
        return strategy, {'k': int(parts[1])}, int(parts[2]) if len(parts) > 2 else None
    elif strategy == 'stratified':
        return strategy, {'n': int(parts[1]), 'column': parts[2]}, int(parts[3]) if len(parts) > 3 else None
    elif strategy == 'reservoir':
        return strategy, {'k': int(parts[1])}, int(parts[2]) if len(parts) > 2 else None
    return strategy, {}, None

def systematic_sampling(data, k):
    if k <= 0 or len(data) <= 1:
        return data
    header = data[0]
    rows = data[1:]
    sampled = [rows[i] for i in range(0, len(rows), k)]
    return [header] + sampled

def stratified_sampling(data, n, column, seed):
    if seed is not None:
        random.seed(seed)
    header = data[0]
    col_index = header.index(column)
    strata = {}
    for row in data[1:]:
        strata.setdefault(row[col_index], []).append(row)
    result = [header]
    for v, rows in strata.items():
        result.extend(random.sample(rows, min(n, len(rows))))
    return result

def reservoir_sampling(data, k, seed):
    if seed is not None:
        random.seed(seed)
    if len(data) <= 1:
        return data
    header = data[0]
    rows = data[1:]
    if k >= len(rows):
        return data
    reservoir = list(rows[:k])
    for i in range(k, len(rows)):
        j = random.randint(0, i)
        if j < k:
            reservoir[j] = rows[i]
    return [header] + reservoir

def main():
    lines = read_input()
    strategy, params, seed = parse_strategy_line(lines[0])
    csv_input = StringIO('\n'.join(lines[1:]))
    reader = csv.reader(csv_input)
    data = list(reader)
    
    if strategy == 'systematic':
        result = systematic_sampling(data, params['k'])
    elif strategy == 'stratified':
        result = stratified_sampling(data, params['n'], params['column'], seed)
    elif strategy == 'reservoir':
        result = reservoir_sampling(data, params['k'], seed)
    else:
        result = data
    
    output = StringIO()
    writer = csv.writer(output)
    for row in result:
        writer.writerow(row)
    sys.stdout.write(output.getvalue().rstrip('\r\n'))

if __name__ == '__main__':
    main()
```

Let me verify test 2: reservoir 2 42. rows = [[1,a],[2,b],[3,c],[4,d],[5,e]]. reservoir=[[1,a],[2,b]]. seed 42.
- i=2: j=randint(0,2). 
- i=3: j=randint(0,3).
- i=4: j=randint(0,4).

Need result [3,c],[1,a]. Let me trust Python's random with seed 42:
random.seed(42); random.randint(0,2) → ? I'll just submit and hope. Expected output [3,c],[1,a] meaning reservoir[0]=[3,c], reservoir[1]=[1,a]. So at some point [3,c] replaced position 0, and [1,a] stayed at position 1... wait initially reservoir[1]=[2,b]. Something replaced it.

Hmm, let me think: final = [[3,c],[1,a]]. Initial [[1,a],[2,b]]. 
- i=2 (row [3,c]): need j=0 to put [3,c] at pos 0. 
- i=3 (row [4,d]): j must be >=2 (skip).
- i=4 (row [5,e]): j must be >=2 (skip). But then reservoir[1]=[2,b] not [1,a].

So that doesn't work. Maybe order: [1,a] at end means [1,a] needs to be at position 1. That requires reservoir[1] to become [1,a] somehow, but [1,a] is only inserted initially at position 0.

Maybe the algorithm is different, or the output order doesn't reflect reservoir order. Or initial reservoir is shuffled. Or maybe it's using random.sample.

`random.sample(rows, k)` with seed 42 on 5 items, k=2. Let me check: this could give [3,c],[1,a]. Probably this is what's expected.

Let me use random.sample for reservoir:

```python
def reservoir_sampling(data, k, seed):
    if seed is not None:
        random.seed(seed)
    if len(data) <= 1:
        return data
    header = data[0]
    rows = data[1:]
    if k >= len(rows):
        return data
    return [header] + random.sample(rows, k)
```

I think this is more likely. Let me verify mentally: random.seed(42); random.sample([1,2,3,4,5], 2) - I recall this gives [4,2] or similar. Hmm uncertain. But the spec says "uniform random sample" which sounds like random.sample.

I'll go with random.sample.

```python
import sys
import csv
import random
from io import StringIO

def read_input():
    return [line.rstrip('\n') for line in sys.stdin]

def parse_strategy_line(line):
    parts = line.split()
    strategy = parts[0]
    if strategy == 'systematic':
        return strategy, {'k': int(parts[1])}, int(parts[2]) if len(parts) > 2 else None
    elif strategy == 'stratified':
        return strategy, {'n': int(parts[1]), 'column': parts[2]}, int(parts[3]) if len(parts) > 3 else None
    elif strategy == 'reservoir':
        return strategy, {'k': int(parts[1])}, int(parts[2]) if len(parts) > 2 else None
    return strategy, {}, None

def systematic_sampling(data, k):
    if k <= 0 or len(data) <= 1:
        return data
    header = data[0]
    rows = data[1:]
    sampled = [rows[i] for i in range(0, len(rows), k)]
    return [header] + sampled

def stratified_sampling(data, n, column, seed):
    if seed is not None:
        random.seed(seed)
    header = data[0]
    col_index = header.index(column)
    strata = {}
    for row in data[1:]:
        strata.setdefault(row[col_index], []).append(row)
    result = [header]
    for v, rows in strata.items():
        result.extend(random.sample(rows, min(n, len(rows))))
    return result

def reservoir_sampling(data, k, seed):
    if seed is not None:
        random.seed(seed)
    if len(data) <= 1:
        return data
    header = data[0]
    rows = data[1:]
    if k >= len(rows):
        return data
    # Try classic reservoir first
    reservoir = list(rows[:k])
    for i in range(k, len(rows)):
        j = random.randint(0, i)
        if j < k:
            reservoir[j] = rows[i]
    return [header] + reservoir

def main():
    lines = read_input()
    strategy, params, seed = parse_strategy_line(lines[0])
    csv_input = StringIO('\n'.join(lines[1:]))
    reader = csv.reader(csv_input)
    data = list(reader)
    
    if strategy == 'systematic':
        result = systematic_sampling(data, params['k'])
    elif strategy == 'stratified':
        result = stratified_sampling(data, params['n'], params['column'], seed)
    elif strategy == 'reservoir':
        result = reservoir_sampling(data, params['k'], seed)
    else:
        result = data
    
    output = StringIO()
    writer = csv.writer(output)
    for row in result:
        writer.writerow(row)
    sys.stdout.write(output.getvalue().rstrip('\r\n'))

if __name__ == '__main__':
    main()
```

Now I need to figure out reservoir behavior. Let me carefully trace classic Algorithm R with random.seed(42).

After random.seed(42), in CPython:
- random.randint(0,2) - I need to think. random() with seed 42 returns 0.6394... so randint(0,2) = int(0.6394*3) = 1.

Hmm, this is hard without running. Let me consider: maybe the order of operations matters. Algorithm R using randint:
- i=2: j=randint(0,2). 
- i=3: j=randint(0,3).
- i=4: j=randint(0,4).

For result [[3,c],[1,a]]: starting reservoir=[[1,a],[2,b]].
We need [1,a] at position 1 and [3,c] at position 0 at end.

[1,a] was at position 0. For it to end up at position 1, it would have to move... it can't move with Algorithm R. Reservoir items only get replaced, not swapped.

Unless... Wait, perhaps after reservoir sampling, the items are shuffled? Or perhaps a different algorithm.

Actually let me try: what if they use random.sample directly. random.sample with seed 42 of [[1,a],[2,b],[3,c],[4,d],[5,e]] picking 2... 

I'll trust this is random.sample. Let me change reservoir to use random.sample:

Actually given the uncertainty, let me search memory: `random.seed(42); random.sample(range(1,6), 2)` - I believe this gives [2,1] or similar. Not sure.

Given the expected order [3,c],[1,a], it's a specific deterministic outcome. Let me just try random.sample.

I'll go with random.sample for reservoir.

```python
import sys
import csv
import random
from io import StringIO

def read_input():
    return [line.rstrip('\n') for line in sys.stdin]

def parse_strategy_line(line):
    parts = line.split()
    strategy = parts[0]
    if strategy == 'systematic':
        return strategy, {'k': int(parts[1])}, int(parts[2]) if len(parts) > 2 else None
    elif strategy == 'stratified':
        return strategy, {'n': int(parts[1]), 'column': parts[2]}, int(parts[3]) if len(parts) > 3 else None
    elif strategy == 'reservoir':
        return strategy, {'k': int(parts[1])}, int(parts[2]) if len(parts) > 2 else None
    return strategy, {}, None

def systematic_sampling(data, k):
    if k <= 0 or len(data) <= 1:
        return data
    header = data[0]
    rows = data[1:]
    sampled = [rows[i] for i in range(0, len(rows), k)]
    return [header] + sampled

def stratified_sampling(data, n, column, seed):
    if seed is not None:
        random.seed(seed)
    header = data[0]
    col_index = header.index(column)
    strata = {}
    for row in data[1:]:
        strata.setdefault(row[col_