import sys

comparisons = 0

def merge_sort(a, depth=0):
    global comparisons
    if len(a) <= 1:
        return a, depth
    mid = len(a) // 2
    left, ld = merge_sort(a[:mid], depth+1)
    right, rd = merge_sort(a[mid:], depth+1)
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, max(ld, rd)

def main():
    global comparisons
    data = sys.stdin.read().split()
    nums = [int(x) for x in data]
    comparisons = 0
    if len(nums) <= 1:
        sorted_nums = nums
        depth = 0
    else:
        sorted_nums, max_depth = merge_sort(nums, 0)
        depth = max_depth
    print('Sorted: ' + ' '.join(str(x) for x in sorted_nums))
    print('Merge depth: ' + str(depth))
    print('Comparisons: ' + str(comparisons))

main()
