import hashlib

def extend_simon_sequence(sequence, n):
    colors = ['R', 'G', 'B', 'Y']
    extended = sequence
    
    for i in range(n):
        # Create a hash based on the current sequence and position
        hash_input = extended + str(len(extended))
        hash_obj = hashlib.md5(hash_input.encode())
        hash_value = int(hash_obj.hexdigest(), 16)
        
        # Use hash to select next color
        next_color_index = hash_value % 4
        next_color = colors[next_color_index]
        extended += next_color
    
    return extended

# Read input
line = input().strip()
parts = line.split()
sequence = parts[0]
n = int(parts[1])

# Generate and print result
result = extend_simon_sequence(sequence, n)
print(result)