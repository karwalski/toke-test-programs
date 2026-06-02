import sys

def radix_sort_lsd(numbers):
    if not numbers:
        return numbers, 0
    
    # Find the maximum number to determine number of digits
    max_num = max(numbers)
    max_digits = len(str(max_num))
    
    # Copy the input list
    arr = numbers[:]
    
    # Perform counting sort for each digit position
    for digit_pos in range(max_digits):
        # Create buckets for digits 0-9
        buckets = [[] for _ in range(10)]
        
        # Distribute numbers into buckets based on current digit
        for num in arr:
            digit = (num // (10 ** digit_pos)) % 10
            buckets[digit].append(num)
        
        # Collect numbers from buckets back into array
        arr = []
        for bucket in buckets:
            arr.extend(bucket)
    
    return arr, max_digits

# Read input
line = input().strip()
numbers = list(map(int, line.split()))

# Sort using LSD radix sort
sorted_numbers, passes = radix_sort_lsd(numbers)

# Output results
print("Sorted:", " ".join(map(str, sorted_numbers)))
print("Passes:", passes)