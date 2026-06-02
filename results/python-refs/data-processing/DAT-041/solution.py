import sys

def run_length_encode(data):
    if not data:
        return ""
    
    encoded = []
    current_char = data[0]
    count = 1
    
    for i in range(1, len(data)):
        if data[i] == current_char:
            count += 1
        else:
            encoded.append(str(count) + current_char)
            current_char = data[i]
            count = 1
    
    # Add the last group
    encoded.append(str(count) + current_char)
    
    return ''.join(encoded)

def calculate_compression_ratio(original, encoded):
    return len(encoded) / len(original)

# Read input
data = input().strip()

# Encode
encoded = run_length_encode(data)

# Calculate ratio
ratio = calculate_compression_ratio(data, encoded)

# Output
print(encoded)
print(f"Ratio: {ratio:.2f}")