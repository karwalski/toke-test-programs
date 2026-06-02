import sys

comparisons = 0

def sift_down(a, start, end):
    global comparisons
    root = start
    while 2*root + 1 <= end:
        child = 2*root + 1
        swap = root
        comparisons += 1
        if a[swap] < a[child]:
            swap = child
        if child + 1 <= end:
            comparisons += 1
            if a[swap] < a[child+1]:
                swap = child + 1
        if swap == root:
            return
        a[root], a[swap] = a[swap], a[root]
        root = swap

def heapsort(a):
    n = len(a)
    for start in range((n-2)//2, -1, -1):
        sift_down(a, start, n-1)
    heap_state = a[:]
    for end in range(n-1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end-1)
    return heap_state, a

data = sys.stdin.read().split()
nums = [int(x) for x in data]
if not nums:
    print('Heap after build: ')
    print('Sorted: ')
    print('Comparisons: 0')
else:
    heap_state, sorted_arr = heapsort(nums[:])
    print('Heap after build: ' + ' '.join(str(x) for x in heap_state))
    print('Sorted: ' + ' '.join(str(x) for x in sorted_arr))
    print('Comparisons: ' + str(comparisons))
