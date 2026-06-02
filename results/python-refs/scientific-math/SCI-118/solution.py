def max_subarray_sum(arr):
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

def max_sum_rectangle(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    max_sum = float('-inf')
    final_left = 0
    final_right = 0
    final_top = 0
    final_bottom = 0
    
    for left in range(cols):
        temp = [0] * rows
        
        for right in range(left, cols):
            for i in range(rows):
                temp[i] += matrix[i][right]
            
            current_sum, top, bottom = max_subarray_sum(temp)
            
            if current_sum > max_sum:
                max_sum = current_sum
                final_left = left
                final_right = right
                final_top = top
                final_bottom = bottom
    
    return max_sum, final_top, final_left, final_bottom, final_right

# Read input
rows, cols = map(int, input().split())
matrix = []
for _ in range(rows):
    row = list(map(int, input().split()))
    matrix.append(row)

# Find maximum sum rectangle
max_sum, top, left, bottom, right = max_sum_rectangle(matrix)

# Output result
print(f"Max sum: {max_sum}")
print(f"Rectangle: top_left=({top},{left}) bottom_right=({bottom},{right})")