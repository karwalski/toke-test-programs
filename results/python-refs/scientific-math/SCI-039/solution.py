def heaps_algorithm(arr):
    permutations = []
    
    def generate(k):
        if k == 1:
            permutations.append(arr[:])
            return
        
        for i in range(k):
            generate(k - 1)
            
            if k % 2 == 0:
                # k is even: swap i-th and last element
                arr[i], arr[k - 1] = arr[k - 1], arr[i]
            else:
                # k is odd: swap first and last element
                arr[0], arr[k - 1] = arr[k - 1], arr[0]
    
    generate(len(arr))
    return permutations

# Read input
elements = input().split()

# Generate permutations using Heap's algorithm
permutations = heaps_algorithm(elements)

# Output permutations
for perm in permutations:
    print(' '.join(perm))

# Output total count
print(f"Total: {len(permutations)}")