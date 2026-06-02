Looking at the test cases:

Test 1 Move 1: pit 0 (4 stones) → P1=`0 4 4 4 4 4`, P2=`5 5 5 5 4 4`, stores `1 0`
- Stones placed: store(+1) + P2[0..3](+4) = 5, but only 4 stones available

Test 1 Move 5: pit 4 (4 stones) → P2=`5 5 5 5 5 4`, store +1 = 6 stones placed from 4
Test 1 Move 6: pit 5 (4 stones) → P2=`5 5 5 5 5 5`, store +1 = 7 stones placed from 4

The pattern: from pit i, place 1 in store, then fill P2[0..max(3,i)]. For pits 0-3: always fill P2[0..3]. For pit 4: P2[0..4]. For pit 5: P2[0..5].

Test 2: pit 5 has 1 stone → 1 goes to store. P2 unchanged, P1 pit 5 emptied. Matches "1 stone → store only".

So rule seems to be: place 1 in store, then place 1 each in P2[0..max(3, pit_index)] but only if pit had >1 stones. Let me verify Test 2: pit 5 has 1 stone, store +1, P2 unchanged. So when stones=1, only store gets it.

Actually simpler: if stones >= 1: store +=1. If stones > 1: fill P2[0..max(3, pit_idx)].

```python
import sys

def main():
    data = sys.stdin.read().split('\n')
    p1 = list(map(int, data[0].split()))
    p2 = list(map(int, data[1].split()))
    stores = list(map(int, data[2].split()))
    player = int(data[3].strip())
    
    results = []
    if player == 1:
        for i in range(6):
            if p1[i] == 0:
                continue
            np1 = p1[:]
            np2 = p2[:]
            ns = stores[:]
            stones = np1[i]
            np1[i] = 0
            ns[0] += 1
            if stones > 1:
                end = max(3, i)
                for j in range(end + 1):
                    np2[j] += 1
            results.append((i+1, np1, np2, ns))
    else:
        for i in range(6):
            if p2[i] == 0:
                continue
            np1 = p1[:]
            np2 = p2[:]
            ns = stores[:]
            stones = np2[i]
            np2[i] = 0
            ns[1] += 1
            if stones > 1:
                end = max(3, i)
                for j in range(end + 1):
                    np1[j] += 1
            results.append((i+1, np1, np2, ns))
    
    out = []
    for mv, np1, np2, ns in results:
        out.append(f"Move {mv}: {' '.join(map(str,np1))} | {' '.join(map(str,np2))} | {ns[0]} {ns[1]}")
    print('\n'.join(out))

main()
```