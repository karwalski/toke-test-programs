For test 1: source="abc", target="yabd". After INS(0,y), we need SUB at position 3 (which is the position in the evolving string after insertion). The position seems to be `i` (1-indexed end) or based on target position. Position 3 = j-1 where j=4, or i in 1-indexed... Let me think: after INS(0,y), string is "yabc". Substituting c→d at position 3 (0-indexed) of "yabc". So SUB position is the position in the current/target string, which is j-1=3.

For INS(0,y): inserting y at position 0 in "abc" → "yabc". Position 0 in target.

So positions seem to be target-based (j-1 for SUB, and for INS it's where in target it's inserted = j-1=0). For DEL it'd be source-based likely.

Let me use j-1 for INS and SUB positions.

```python
def edit_distance_with_operations(source, target):
    m, n = len(source), len(target)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if source[i-1] == target[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    operations = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and source[i-1] == target[j-1]:
            i -= 1; j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + 1:
            operations.append(f"SUB({j-1},{source[i-1]},{target[j-1]})")
            i -= 1; j -= 1
        elif j > 0 and dp[i][j] == dp[i][j-1] + 1:
            operations.append(f"INS({j-1},{target[j-1]})")
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            operations.append(f"DEL({i-1},{source[i-1]})")
            i -= 1
    operations.reverse()
    return dp[m][n], operations

source = input()
target = input()
distance, operations = edit_distance_with_operations(source, target)
if not operations:
    print(f"Distance: {distance}")
    print("Operations: (none)")
else:
    print(f"Distance: {distance}")
    print("Operations:")
    print("\n".join(operations))
```