import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    nums = [int(x) for x in data]
    if not nums:
        return
    max_val = max(nums)
    digit_names = ['ones','tens','hundreds','thousands','ten-thousands','hundred-thousands','millions','ten-millions','hundred-millions','billions']
    pass_num = 0
    exp = 1
    arr = nums[:]
    while exp <= max_val:
        buckets = [[] for _ in range(10)]
        for n in arr:
            d = (n // exp) % 10
            buckets[d].append(n)
        parts = []
        for i in range(10):
            if buckets[i]:
                parts.append('[' + str(i) + ':' + ','.join(str(x) for x in buckets[i]) + ']')
        name = digit_names[pass_num] if pass_num < len(digit_names) else 'digit'+str(pass_num)
        print('Pass ' + str(pass_num+1) + ' (' + name + '): ' + ' '.join(parts))
        arr = []
        for b in buckets:
            arr.extend(b)
        exp *= 10
        pass_num += 1
    print('Sorted: ' + ' '.join(str(x) for x in arr))

main()
