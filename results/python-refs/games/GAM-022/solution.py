import sys
from itertools import permutations

EPS = 1e-9

def solve(nums):
    # nums: list of (value, expr_str)
    if len(nums) == 1:
        if abs(nums[0][0] - 24) < EPS:
            return nums[0][1]
        return None
    n = len(nums)
    for i in range(n):
        for j in range(n):
            if i == j: continue
            rest = [nums[k] for k in range(n) if k != i and k != j]
            a_val, a_str = nums[i]
            b_val, b_str = nums[j]
            combos = []
            combos.append((a_val + b_val, '(' + a_str + ' + ' + b_str + ')'))
            combos.append((a_val - b_val, '(' + a_str + ' - ' + b_str + ')'))
            combos.append((a_val * b_val, '(' + a_str + ' * ' + b_str + ')'))
            if abs(b_val) > EPS:
                combos.append((a_val / b_val, '(' + a_str + ' / ' + b_str + ')'))
            for cv, cs in combos:
                result = solve(rest + [(cv, cs)])
                if result is not None:
                    return result
    return None

def main():
    data = sys.stdin.read().split()
    nums = [(float(x), x) for x in data]
    res = solve(nums)
    if res is None:
        print('Impossible')
    else:
        # strip outermost parens if present
        if res.startswith('(') and res.endswith(')'):
            # check balance
            depth = 0
            ok = True
            for idx, ch in enumerate(res):
                if ch == '(': depth += 1
                elif ch == ')': depth -= 1
                if depth == 0 and idx < len(res) - 1:
                    ok = False
                    break
            if ok:
                res = res[1:-1]
        print(res)

main()
