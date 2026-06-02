def kadane_algorithm(arr):
    max_sum = float('-inf')
    current_sum = 0
    start = 0
    end = 0
    temp_start = 0
    
    for i in range(len(arr)):
        current_sum += arr[i]
        
        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i
        
        if current_sum < 0:
            current_sum = 0
            temp_start = i + 1
    
    return max_sum, start, end

# Read input
numbers = list(map(int, input().split()))

# Find maximum sum subarray
max_sum, start_idx, end_idx = kadane_algorithm(numbers)

# Get the subarray
subarray = numbers[start_idx:end_idx + 1]

# Output results
print(f"Max sum: {max_sum}")
print(f"Subarray: {' '.join(map(str, subarray))}")
print(f"Indices: {start_idx} {end_idx}")