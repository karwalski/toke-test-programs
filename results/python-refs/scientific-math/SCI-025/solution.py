Let me trace: [5,3,1,4,2]

i=1, key=3: j=0, cmp 5>3 yes, shift, j=-1. comparisons=1, shifts=1
i=2, key=1: j=1, cmp 5>1, shift, j=0. cmp 3>1, shift, j=-1. comparisons=3, shifts=3
i=3, key=4: j=2, cmp 5>4, shift, j=1. cmp 3>4 no, break. comparisons=5, shifts=4
i=4, key=2: j=3, cmp 5>2, shift, j=2. cmp 4>2, shift, j=1. cmp 3>2, shift, j=0. cmp 1>2 no, break. comparisons=9, shifts=7

Expected: 8 comparisons, 6 shifts. So we need to not count one comparison/shift somewhere. Hmm.

Maybe shifts count only when key moves to new position (not counting the key placement)? No, shifts are already 7 from moving.

Wait - maybe "shifts" excludes the final key placement when adjacent? Or maybe comparisons don't count the "break" comparison?

If we don't count comparison when arr[j]<=key (the breaking one): 
i=1: 1 cmp, 1 shift
i=2: 2 cmp, 2 shifts
i=3: 1 cmp (5>4) + then 3>4 not counted = 1 cmp, 1 shift  
i=4: 3 cmp + 1>2 not counted = 3 cmp, 3 shifts
Total: 7 cmp, 7 shifts. Not matching.

Expected 8 cmp, 6 shifts. Difference from current: -1 cmp, -1 shift.

Maybe when key equals position (j+1==i, no shift needed), don't count? i=3: 5>4 shift, then j=1, 3>4 false break. So one shift, one comparison wasted... 

What if i=4 last comparison 1>2 isn't counted (because j reached... no j=0 still valid).

Let me try: shifts counted as number of position changes for key item. Hmm.

Alternative: comparisons count only successful (arr[j]>key) ones = shifts count. That'd give 7=7. No.

Maybe shifts = 6 means one less. Perhaps the algorithm uses different approach: shift only when necessary, and i=3 case: 5>4 shift counted, but the key placement counts differently...

Let me try: don't shift if it would just put the value back. For i=3, after shifting 5 right, key 4 goes at position 2. That's a real shift. shifts=1.

What if shifts only count when j != i-1 initially moved more than... 

Let me try counting comparisons differently: when while loop exits via j<0, don't count an extra comparison (we don't make one). Current code already does this correctly.

Hmm wait: maybe shifts=6 because one of those shifts isn't needed. Looking at [5,3,1,4,2]: total inversions = (5,3),(5,1),(5,4),(5,2),(3,1),(3,2),(4,2),(1 with nothing)... = 7 inversions. Hmm 7.

Let me try: comparisons = shifts + (number of elements that found their place without going to start) = 6 + 2 = 8? Elements that didn't reach j=-1: i=3 (key=4) and... i=4? key=2 stops at j=0 (since 1<2). So i=1 reaches j=-1, i=2 reaches j=-1, i=3 stops, i=4 stops. That's 2 elements that stopped (got extra comparison). So comparisons = shifts + 2 = 6+2 = 8. ✓

So shifts should be 6. Inversions = 7 but expected 6. Let me recount inversions: 5>3,5>1,5>4,5>2,3>1,3>2,4>2 = 7. Hmm.

Maybe one shift is counted as placement? Like when key=4 enters position 2, we shift 5 right - that's a "shift" but maybe key placement isn't counted separately... it isn't in my count.

What if shifts only count when the element being shifted moves more than 1? No that's weird.

Let me try: don't count shift when j+1 == i originally... no.

What if shifts = comparisons - (successful comparisons that break)? = 8-2=6. So shifts = comparisons where arr[j]>key minus the break comparisons? That doesn't make sense as definition.

Actually maybe: count comparison even on break (so +2 to current shifts-then-break logic). Wait current code DOES count on break. Let me recount with current code:

i=1: while j=0: cmp++ (1), 5>3 shift++(1), j=-1. exit.
i=2: j=1: cmp++(2), 5>1 shift++(2), j=0. cmp++(3), 3>1 shift++(3), j=-1.
i=3: j=2: cmp++(4), 5>4 shift++(4), j=1. cmp++(5), 3>4 false break.
i=4: j=3: cmp++(6), 5>2 shift++(5), j=2. cmp++(7), 4>2 shift++(6), j=1. cmp++(8), 3>2 shift++(7), j=0. cmp++(9), 1>2 false break.

Comparisons=9, shifts=7. Expected 8, 6. Diff -1 each.

What if we skip last iteration's last shift? Or one of i=4's shifts... If 3>2 wasn't shifted... but it must be to sort correctly.

Wait expected output IS sorted correctly. So actual sort is fine. Just counts differ by 1.

Maybe the implementation does: compare arr[j+1] with arr[j] swapping style? Let's try swap-based insertion sort:

```
for i in 1..n:
  j = i
  while j > 0 and arr[j-1] > arr[j]:
    swap, j--
```
Each swap = shift? Each comparison the same.

i=1, j=1: cmp 5>3 swap [3,5,1,4,2], j=0. cmp(2): wait need j>0 first check (short-circuit). j=0 exit. comparisons=1, shifts=1.
i=2, j=2: cmp 5>1 swap[3,1,5,4,2], j=1. cmp 3>1 swap[1,3,5,4,2], j=0. exit. cmp=3, sh=3.
i=3, j=3: cmp 5>4 swap[1,3,4,5,2], j=2. cmp 3>4 false exit. cmp=5, sh=4.
i=4, j=4: cmp 5>2 swap, j=3. cmp 4>2 swap, j=2. cmp 3>2 swap, j=1. cmp 1>2 false. cmp=9, sh=7.

Same count.

Hmm. What if comparisons don't count for the first element check when j==0 boundary? Like when j reaches -1, the previous comparison still counted... 

Let me try: i=1 key=3, only 1 element before. We do 1 comparison and 1 shift. Fine. 
What if for i=1 specifically we count 0 comparisons? Like single comparison goes off-grid? No.

Let me try a different metric: shifts = inversions for adjacent swaps = 7. Doesn't match 6 either.

What if shifts means the number of times we move other elements only when key actually moves more than one position? i=1 key=3 moves 1 position. i=2 key=1 moves 2 positions. i=3 key=4 moves 1 position. i=4 key=2 moves 3 positions. Total moves = 1+2+1+3 = 7. Same.

Hmm what about comparisons = number of position changes total of key = 7? +... let me look at problem differently.

Maybe both counts decrease by 1 due to off-by-one. What if loop starts at i=2 (1-indexed)? Or i=0?

Or maybe: when j+1==i (no movement needed), we still made 1 comparison. That happened for... never in this case (all keys moved).

Hmm what if increments aren't done for the very last i? Test 1 has length 5, so last i=4. Without it: cmp=5, shifts=4. No.

Without first i=1: cmp=8, shifts=6! ✓

So loop should start from i=2? But that gives wrong sort for [2,1]. Unless... wait test only has these two cases. Let me check: [5,3,1,4,2] starting i=2: skip i=1, key=3 stays.
Pass i=2: key=1, [5,3,1,...] -> compare 3>1 shift, 5>1 shift, [1,5,3,4,2]. Wait no: array is [5,3,1,4,2], i=2, key=arr[2]=1, j=1. 3>1 shift -> [5,3,3,4,2], j=0, 5>1 shift -> [5,5,3,4,2], place key: [1,5,3,4,2]. comparisons=2, shifts=2.
i=3, key=4, j=2: 3>4 false. comparisons=3, shifts=2.
i=4, key=2, j=3: 5>2 shift, j=2, 3>2 shift, j=1, 5>2... wait array is [1,5,3,4,2] after i=2. Let me redo.

Actually array after i=2 should be [1,3,5,4,2] if we sort properly considering i=1 was skipped, hmm 3 would still be at index 1. Let me redo: original [5,3,1,4,2], skip i=1. i=2: key=arr[2]=1, j=1, arr[1]=3>1 shift arr[2]=3 -> [5,3,3,4,2], j=0, arr[0]=5>1 shift arr[1]=5 -> [5,5,3,4,2], j=-1, place: arr[0]=1 -> [1,5,3,4,2]. Hmm, but 3 is now at position 2 not sorted with 5.

So skipping i=1 doesn't sort correctly. But expected output IS sorted [1,2,3,4,5]. So can't skip.

Unless we use a different algorithm. What if we don't count operations when i=1 because list is already "sorted of size 1"? No that doesn't make sense.

Let me try: comparisons in i=4 (last) only counts until... hmm.

Another idea: counts exclude the final i iteration. With i=1..3 only: cmp=1+3+5=... wait current count after i=3 is cmp=5, shifts=4. After i=4 added: 9, 7. We want 8, 6 = i=4 contributes 3 cmp, 2 shifts instead of 4 and 3.

Or each iteration contributes (cmp_i, shifts_i):
i=1: (1,1)
i=2: (2,2) 
i=3: (2,1)
i=4: (4,3)... if we use the without-extra-comparison version (don't count break):
i=1: (1,1) [reached -1]
i=2: (2,2) [reached -1]
i=3: (1,1) [break, don't count]
i=4: (3,3) [break, don't count]
Total: 7,7. No.

Mixed: count break for some?
Want total 8 cmp, 6 shifts.

What if shifts only counts moves of distinct elements per pass? Like each element shifted at most once per pass? Then:
i=2: elements 5,3 shifted -> 2 shifts
i=4: elements 5,4,3 shifted -> 3 shifts
i=1: element 5 -> 1
i=3: element 5 -> 1
Total: 7. No.

What if a shift only counts when the shifted element ends up further than original index of key? Hmm.

OK let me try yet another model. What if comparison happens for arr[j] vs arr[j+1]? In some implementations:

```
for i = 1 to n-1:
  for j = i down to 1:
    if arr[j-1] > arr[j]:
      swap; shifts++
    cmp++
    if not swapped, break
```

This counts a comparison even when not swapping (the break). Same as before.

What if there's a sentinel? Insertion sort with sentinel arr[0] = -inf. Then we don't need j>=0 check, only arr[j]>key check. Comparisons = shifts + (n-1)